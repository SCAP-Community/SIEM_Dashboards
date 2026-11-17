"""Static dashboard selector contracts. Does not execute SPL on Splunk."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
BASE=Path(__file__).resolve().parents[1]/'src/scap_stig_compliance/default/data/ui/views'

class FilterRegressionChecks(unittest.TestCase):
    def get_search(self,name,title):
        root=ET.parse(BASE/name).getroot()
        for parent in root.iter():
            if parent.findtext('title')==title:
                s=parent.find('search')
                if s is not None:
                    return s.findtext('query') or '',s
        self.fail('Missing panel: '+title)
    def assert_base_selectors(self,query,search,expect):
        self.assertIn('eventstats values(target_os) as scan_os',query)
        self.assertIn('by scan_id',query)
        self.assertIn('event_type="rule_result"',query)
        for selector in expect:
            self.assertIn('$'+selector+'$',query)
        self.assertEqual('$time_tok.earliest$',search.findtext('earliest'))
        self.assertEqual('$time_tok.latest$',search.findtext('latest'))
    def test_executive_unique(self):
        q,s=self.get_search('stig_enterprise_compliance_dashboard.xml','Unique CAT I Findings')
        self.assert_base_selectors(q,s,['os_tok','mac_tok','bench_tok'])
        self.assertIn('dc(rule_id) as unique_cat1_rules',q)
    def test_executive_cci(self):
        q,s=self.get_search('stig_enterprise_compliance_dashboard.xml','Top Failing Control Correlation Identifiers (CCI)')
        self.assert_base_selectors(q,s,['os_tok','mac_tok','bench_tok'])
        self.assertIn('eventstats max(_time) as latest_scan_time',q)
        self.assertNotIn('streamstats max(_time)',q)
    def test_sysadmin_unique(self):
        q,s=self.get_search('sysadmin_stig_dashboard.xml','Unique CAT I Findings')
        self.assert_base_selectors(q,s,['os_tok','bench_tok','host_search_tok','test_tok'])
        self.assertIn('dc(rule_id) as unique_cat1_rules',q)
    def test_sysadmin_drilldown(self):
        q,s=self.get_search('sysadmin_stig_dashboard.xml','Unique CAT I Findings Across Fleet (Sorted by STIG & Rule ID)')
        self.assert_base_selectors(q,s,['os_tok','bench_tok','host_search_tok','test_tok'])
        self.assertIn('by benchmark_id, rule_id',q)
if __name__=='__main__': unittest.main()
