import base64
import os
import shutil
import tempfile
import time
from pygraphviz import *
import networkx as nx


class ScanGraph(object):
    def __init__(self, scan_json, layout='circo'):
        """Layouts: neato, dot, twopi, circo, fdp, nop"""
        self.scan_json = scan_json
        self.layout = layout
        self.server_name = ScanGraph.server_name_from_scan_json(scan_json)

    def render_png(self):
        return ScanGraph.dot_to_png(ScanGraph.if_list_wrap(self.scan_json,
                                                           self.server_name),
                                    self.layout)

    def render_gml(self):
        return ScanGraph.dot_to_gml(ScanGraph.if_list_wrap(self.scan_json,
                                                           self.server_name))

    def render_dot(self):
        dotstring = ScanGraph.if_list_wrap(self.scan_json, self.server_name)
        return base64.b64encode(dotstring)

    @classmethod
    def server_name_from_scan_json(cls, scan_json):
        if isinstance(scan_json, list):
            target_scan = scan_json[0]
        else:
            target_scan = scan_json
        server_name = target_scan["server_hostname"]
        return server_name

    @classmethod
    def dot_to_gml(cls, dotstring):
        """Turn the contents of a dotfile into a base-64 encoded gml.
        Calling this class method with the contents of a dot-formatted file
        will get you a representation of the graph in gml format,
        base64-encoded.

        """
        temp_path = tempfile.mkdtemp()
        print temp_path
        in_dot = os.path.join(temp_path, "infile.dot")
        out_gml = os.path.join(temp_path, "outfile.gml")
        A = AGraph(dotstring)
        A.write(in_dot)
        G = nx.drawing.nx_agraph.read_dot(in_dot)
        # Write GML to outfile path
        nx.readwrite.gml.write_gml(G, out_gml)
        # Read from file handle into string
        with open(out_gml, 'r') as final_file:
            retval = final_file.read()
        shutil.rmtree(temp_path)
        return base64.b64encode(retval)

    @classmethod
    def dot_to_png(cls, dotstring, layout):
        """Turn the contents of a dotfile into a base-64 encoded png.
        Calling this class method with the contents of a dot-formatted file
        will get you a representation of the graph in png format,
        base64-encoded.

        """
        temp_path = tempfile.mkdtemp()
        outfile = os.path.join(temp_path, "outfile.png")
        g = AGraph(dotstring)
        g.draw(path=outfile, prog=layout)
        with open(outfile, 'r') as pngfile:
            retval = pngfile.read()
        shutil.rmtree(temp_path)
        return base64.b64encode(retval)

    @classmethod
    def if_list_wrap(cls, scan_json, server_name):
        """If we get a list of scans, process as such"""
        dots = []
        if isinstance(scan_json, list):
            for scan in scan_json:
                dots.append(ScanGraph.json_to_dot(scan, server_name))
        else:
            dots.append(ScanGraph.json_to_dot(scan_json, server_name))
        return "\n".join(dots)

    @classmethod
    def json_to_dot(cls, scan_json, server_name):
        edges, red_leaves = ScanGraph.reduce_edges(ScanGraph.edges_from_json(scan_json))
        g = AGraph(directed=True, root=server_name)
        g.add_node(server_name)
        for leaf in red_leaves:
            g.add_node(leaf, color="red")
        for edge in edges:
            if len(edge) == 3:
                g.add_edge(edge[0], edge[1], color=edge[2])
            else:
                g.add_edge(edge[0], edge[1])
        return g.string()

    @classmethod
    def edges_from_json(cls, scan_json):
        final = []
        edges = []
        standards = []
        red_leaves = []
        hostname = unicode(scan_json["server_hostname"])
        module = unicode(scan_json["module"])
        for finding in scan_json["findings"]:
            if finding["status"] == "bad":
                edge_color = "red"
            else:
                edge_color = "black"
            if "reference_identifiers" in finding:
                for ref_id in finding["reference_identifiers"]:
                    packed_edge = ScanGraph.edge_from_refid(ref_id, edge_color)
                    if packed_edge[0] not in standards:
                        standards.append(packed_edge[0])
                    if (edge_color == "red" and
                            ref_id.items()[0][1] not in red_leaves):
                        red_leaves.append(".".join([ref_id.items()[0][0], ref_id.items()[0][1]]))
                    edges.extend(ScanGraph.detonate_edge(packed_edge))
        for standard in standards:
            # Tie scan modules to covered standard
            final.append((module, standard, "black"))
        # Tie hostname to scan module
        final.append((hostname, module, "black"))
        # final.extend(standards)
        final.extend(edges)
        return final, red_leaves

    @classmethod
    def edge_from_refid(cls, ref_id, edge_color):
        # ("CIS", "1.2.3.4", "red")
        k, v = ref_id.items()[0]
        edge = (k, v, edge_color)
        return edge

    @classmethod
    def tuple_in_list(cls, tpl, lst):
        for item in lst:
            if tpl == item:
                return True
        return False

    @classmethod
    def reduce_edges(cls, edges):
        """Remove duplicate edges, ensure that reds persist"""
        final = []
        for edge in edges:
            cold_edge = (edge[0], edge[1], "black")
            hot_edge = (edge[0], edge[1], "red")
            if ScanGraph.tuple_in_list(edge, final):
                # if it's already there, move on.
                continue
            elif ScanGraph.tuple_in_list(hot_edge, final):
                # if the edge is already in the list, and it's red, leave it!
                continue
            elif len(edge) == 2:
                # It's not a hot/cold mapping if it isn't 3 long
                continue
            elif edge[2] == "red" and ScanGraph.tuple_in_list(cold_edge, final):
                # replace black with red
                final.remove(cold_edge)
            final.append(edge)
        return final

    @classmethod
    def detonate_edge(cls, edge):
        """If the node is dot-separated, attempt to extrapolate into leaves"""
        result = []
        parent = edge[0]
        color = edge[2]
        if "." in edge[1]:
            for level in edge[1].split("."):
                present = ".".join([parent, level])
                vein = (parent, present, color)
                result.append(vein)
                parent = present
        return result
