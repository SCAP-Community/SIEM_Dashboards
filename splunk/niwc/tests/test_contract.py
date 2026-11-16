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
        self.assertIn('scanner_name as "Scanner Name"',s)
        self.assertIn('scanner_version as "Scanner Version"',s)
    def test_approved_visible_branding(self):
        ex = ET.parse(SRC/'default/data/ui/views/stig_enterprise_compliance_dashboard.xml').getroot()
        sy = ET.parse(SRC/'default/data/ui/views/sysadmin_stig_dashboard.xml').getroot()
        self.assertEqual(ex.findtext('label'), 'Enterprise SCAP & STIG Compliance')
        self.assertEqual(ex.findtext('description'), 'Enterprise-wide SCAP and STIG compliance monitoring across assessed systems and benchmarks.')
        self.assertEqual(sy.findtext('label'), 'System STIG Compliance Dashboard')
        self.assertEqual(sy.findtext('description'), 'Host-level compliance analysis, assessment findings, historical trends, and regression tracking.')
        for obj in (ex, sy):
            rendered = ET.tostring(obj, encoding='unicode')
            for unsupported in ('SCC Version', 'Powered by', 'SCAP Compliance Checker'):
                self.assertNotIn(unsupported, rendered)
        src = (SRC/'default/data/ui/views/sysadmin_stig_dashboard.xml').read_text()
        self.assertIn('scanner_name as "Scanner Name"', src)
        self.assertIn('scanner_version as "Scanner Version"', src)
        conf = (SRC/'default/app.conf').read_text()
        self.assertIn('version = 0.2.0', conf)
        self.assertIn('author = NIWC Atlantic', conf)
        self.assertIn('description = Dashboards for monitoring SCAP and STIG compliance results from compatible assessment scanners.', conf)
    def test_no_old_scc_column_name(self):
        from pathlib import Path
        views = SRC/'default/data/ui/views'
        for name in ('stig_enterprise_compliance_dashboard.xml', 'sysadmin_stig_dashboard.xml'):
            content = (views/name).read_text()
            self.assertNotIn('SCC Version', content)
            self.assertNotIn('Powered by', content)
        table=(views/'sysadmin_stig_dashboard.xml').read_text()
        self.assertEqual(table.count('scanner_name as "Scanner Name"'), 1)
        self.assertEqual(table.count('scanner_version as "Scanner Version"'), 1)
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
