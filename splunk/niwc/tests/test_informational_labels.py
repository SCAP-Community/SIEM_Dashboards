"""0.2.2 narrow presentation regression checks. No live Splunk execution."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
EX=ROOT/'src/scap_stig_compliance/default/data/ui/views/stig_enterprise_compliance_dashboard.xml'

class InformationalLabels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root=ET.parse(EX).getroot()
    def query_for(self,title):
        for panel in self.root.iter('table'):
            if (panel.findtext('title') or '').startswith(title):
                s=panel.find('search')
                if s is not None:return s.findtext('query') or ''
        self.fail('Missing table: '+title)
    def test_benchmark_informational_not_cativ(self):
        q=self.query_for('Hosts Evaluated for Benchmark:')
        self.assertIn('rules_informational as "Informational"',q)
        self.assertNotIn('rules_informational as "CAT IV Fails"',q)
        self.assertIn('cat3_fails as "CAT III Fails"',q)
    def test_os_informational_and_catiii(self):
        q=self.query_for('Hosts Evaluated for Operating System:')
        self.assertIn('sum(rules_informational) as informational',q)
        self.assertIn('informational as "Informational"',q)
        self.assertIn('sum(cat3_fails) as cat3',q)
        self.assertIn('cat3 as "CAT III Fails"',q)
        self.assertNotIn('cat3_fails as "CAT III Fails"',q)
        self.assertNotIn('cat4 as "CAT IV Fails"',q)
        self.assertIn('target_os==target_os_filter',q)
    def test_package_version(self):
        conf=(ROOT/'src/scap_stig_compliance/default/app.conf').read_text()
        self.assertIn('version = 0.2.2',conf)
        self.assertIn('id = scap_stig_compliance',conf)
if __name__=='__main__':unittest.main()
