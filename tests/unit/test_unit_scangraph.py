import imp
import json
import os
import sys

module_name = 'scangraph'
here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
fixture_path = os.path.join(here_dir, '../fixtures/')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
scangraph = imp.load_module(module_name, fp, pathname, description)


class TestUnitScanGraph:
    def scangraph_instantiate(self):
        scan_data = self.get_scangraph_json()
        return scangraph.ScanGraph(scan_data)

    def get_scangraph_json(self):
        scan_file = os.path.join(fixture_path, "scandetails_three.json")
        with open(scan_file, 'r') as s_file:
            scan_data = json.load(s_file)
        return scan_data

    def test_scangraph_instantiate(self):
        assert self.scangraph_instantiate()

    def test_scangraph_reduce_edges(self):
        edges = [("ABC", "123", "red"),
                 ("ABC", "123", "black"),
                 ("XYZ", "987", "black"),
                 ("XYZ", "987", "red"),
                 ("LMNOP", "000", "red"),
                 ("LMNOP", "000", "red"),
                 ("LMNOP", "000", "red"),
                 ("LMNOP", "000", "black")]
        reduced = scangraph.ScanGraph.reduce_edges(edges)
        assert len(reduced) == 3

    def test_scangraph_edge_from_refid(self):
        refid = {"ABC": "123"}
        color = "pinkish-blue"
        desired = ("ABC", "123", "pinkish-blue")
        result = scangraph.ScanGraph.edge_from_refid(refid, color)
        assert desired == result

    def test_scangraph_edges_from_json(self):
        json_str = self.get_scangraph_json()
        final, red_leaves = scangraph.ScanGraph.edges_from_json(json_str)
        assert len(final) == 599
        assert len(red_leaves) == 85

    def test_json_to_dot(self):
        json_str = self.get_scangraph_json()
        dot = scangraph.ScanGraph.json_to_dot(json_str, "servername")
        assert isinstance(dot, unicode)

    def test_detonate_edge_1(self):
        edge = ("CIS", "1.1.2.3.4", "red")
        detonated = scangraph.ScanGraph.detonate_edge(edge)
        assert len(detonated) == 5

    def test_detonate_edge_2(self):
        edge = ("CCI", "000169", "red")
        detonated = scangraph.ScanGraph.detonate_edge(edge)
        assert len(detonated) == 1
