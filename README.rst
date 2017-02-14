----------
scan-graph
----------

Create a PNG file from a list of Halo scan results
==================================================


What it is
==========


This is a Python library that accepts CloudPassage Halo scan results and
returns .png files that show a graph of reference_identifier information.


Requirements
============


* Python 2.7
* Graphviz and associated development libraries (See the Dockerfile in this repo for details...)
* Other dependencies installed via setup routine:
    * cloudpassage >= 1.0
    * networkx >= 1.11
    * pygraphviz >= 1.3.1


How it works
============


::


    import scangraph

    structure = []  # This will be a list of scan results
    graph = scangraph.ScanGraph(structure)  # Instantiate the graph object
    b64_png = graph.render_png()  # Returns a .png file in a base64-encoded string.
    b64_gml = graph.render_gml()
    b64_dot = graph.render_dot()



Testing
=======


The easiest way to test is to try to build the Dockerfile:


::


    docker build .


If you want to test it natively, the testing dependencies (in addition to the other dependencies, above) are:

* pytest
* pytest-flake8
* pytest-cov (for coverage metrics)
