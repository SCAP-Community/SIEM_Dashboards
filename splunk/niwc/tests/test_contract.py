"""Static contract tests; these do not execute Splunk SPL or prove runtime behavior."""
from pathlib import Path
import json, tarfile, xml.etree.ElementTree as ET, unittest
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'src/scap_stig_compliance'
class ContractChecks(unittest.TestCase):
    def test_dashboard_xml_and_queries(self):
        for name in ('stig_enterprise_compliance_dashboard.xml','sysadmin_stig_dashboard.xml'):
            data=(SRC/'default/data/ui/views'/name).read_text()
            ET.fromstring(data)
            self.assertIn('host_name',data)
            self.assertNotIn('target_host',data)
            self.assertNotIn('scc_version',data)
        s=(SRC/'default/data/ui/views/sysadmin_stig_dashboard.xml').read_text()
        self.assertIn('scanner_name as "Scanner"',s)
        self.assertIn('scanner_version as "Scanner Version"',s)
    def test_calculated_fallbacks(self):
        s=(SRC/'default/props.conf').read_text()
        self.assertIn('KV_MODE = json',s)
        self.assertNotIn('INDEXED_EXTRACTIONS = json',s)
        for k in ('host_name','target_host','assessed_host','host','scanner_name','scanner_version','scc_version'):
            self.assertIn('"'+k+'"',s)
        self.assertIn('EVAL-host_name',s)
        self.assertIn('EVAL-scanner_name',s)
        self.assertIn('EVAL-scanner_version',s)
        self.assertNotIn('DEST_KEY = MetaData:Host',s)
    def test_index_macro_unchanged(self):
        self.assertIn('definition = index="scap-scc"',(SRC/'default/macros.conf').read_text())
    def test_fixtures(self):
        data=[json.loads(s) for s in (ROOT/'tests/fixtures/new_and_legacy_events.jsonl').read_text().splitlines()]
        self.assertEqual(4,len(data))
        for row in data:
            self.assertIn(row['event_type'],('scan_summary','rule_result'))
            self.assertIn('host_id',row)
            self.assertIn('scan_id',row)
        self.assertEqual('ExampleScanner',data[0]['scanner_name'])
        self.assertEqual('5.16',data[2]['scc_version'])
if __name__=='__main__': unittest.main()
