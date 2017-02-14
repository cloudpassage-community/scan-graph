import scangraph
import base64
import json


with open('./tests/fixtures/scandetailsoutput.json', 'r') as f_handle:
    structure = json.load(f_handle)
    graph = scangraph.ScanGraph(structure)

with open('outfile.png', 'w') as out_file:
    out_file.write(base64.b64decode(graph.render_png()))

with open('outfile.gml', 'w') as out_file:
    out_file.write(base64.b64decode(graph.render_gml()))

with open('outfile.dot', 'w') as out_file:
    out_file.write(base64.b64decode(graph.render_dot()))
