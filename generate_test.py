import scangraph
import base64
import json


with open('./tests/fixtures/scandetails_one.json', 'r') as f_handle:
    # This one has no reference_identifiers set
    structure_one = json.load(f_handle)

with open('./tests/fixtures/scandetails_two.json', 'r') as f_handle:
    # This one has both CIS and CCI reference_identifiers.
    structure_two = json.load(f_handle)

with open('./tests/fixtures/scandetails_three.json', 'r') as f_handle:
    # This one just has CIS reference_identifiers.
    structure_three = json.load(f_handle)


runner_one = structure_one
runner_two = structure_two
runner_three = structure_three
runner_four = [structure_one, structure_two]
runner_five = [structure_one, structure_two, structure_three]

runlist = [runner_one, runner_two, runner_three, runner_four, runner_five]
i = 1
for runner in runlist:
    graph = scangraph.ScanGraph(runner)
    prefix = "outfile_%s" % str(i)
    with open(prefix + '.png', 'w') as out_file:
        out_file.write(base64.b64decode(graph.render_png()))

    with open(prefix + '.gml', 'w') as out_file:
        out_file.write(base64.b64decode(graph.render_gml()))

    with open(prefix + '.dot', 'w') as out_file:
        out_file.write(base64.b64decode(graph.render_dot()))

    i += 1
