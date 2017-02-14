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


class TestIntegrationScanGraph:
    def scangraph_instantiate(self):
        scan_data = self.get_scangraph_json()
        return scangraph.ScanGraph(scan_data)

    def scangraph_instantiate_multi(self):
        scan_data = [self.get_scangraph_json(), self.get_scangraph_json()]
        return scangraph.ScanGraph(scan_data)

    def get_scangraph_json(self):
        scan_file = os.path.join(fixture_path, "scandetailsoutput.json")
        with open(scan_file, 'r') as s_file:
            scan_data = json.load(s_file)
        return scan_data

    def test_scangraph_single_scan(self):
        sg_obj = self.scangraph_instantiate()
        b64_png = sg_obj.render_png()
        assert isinstance(b64_png, str)

    def test_scangraph_multiple_scan(self):
        sg_obj = self.scangraph_instantiate_multi()
        b64_png = sg_obj.render_png()
        assert isinstance(b64_png, str)
