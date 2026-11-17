# SCAP & STIG Compliance Splunk App 0.2.1 — 2026-11-17

## Maintenance changes from 0.2.0

- **Executive Dashboard:** Unique CAT I Findings and Top Failing Control Correlation Identifiers now correlate `rule_result` events with their `scan_summary` metadata using `scan_id`, so OS and Impact Profile (MAC) selectors work alongside STIG Benchmark and timeframe.
- **System Administrator Dashboard:** Unique CAT I Findings and its drilldown likewise use associated scan summary metadata for OS filtering; they also apply STIG Benchmark, Host FQDN, Test Engine Type, and timeframe selectors.
- **CCI query:** Uses `eventstats max(_time)` instead of the prior order-dependent `streamstats` expression to select the latest rule-result timestamp for each host/benchmark within the selected timeframe.
- **Release metadata:** `app.conf` is version 0.2.1; the package retains the `scap_stig_compliance` application identifier.
- **Release qualification:** Static XML, field contract, selector checks, full archive/source parity and file hashes. Live Splunk/AppInspect/btool validation has not been performed here.

## Unchanged behavior and limitations

- This is a maintenance release. Index macro, search-time field compatibility, navigation, static assets, and source event schema are unchanged.
- The 0.2.0 package and documentation are retained as historical artifacts.
- CAT I unique findings are the count of distinct `rule_id` values among qualifying events in the selected period. The System Administrator detail table groups by `(benchmark_id, rule_id)`, so row count can exceed the KPI if the same rule ID occurs in multiple benchmarks.
- The dashboard CCI query selects the most recent timestamp among rule-result events per host/benchmark, not the latest complete scan when a scan contains no rule-result events. Multi-scan historical semantics require separate qualification.
- `rule_result` events lack `target_os` and `profile_id`; both are inherited by matching `scan_id`. Missing or mismatched `scan_id` metadata prevents filtering for specific OS/profile selections.
- The known SCC/Linux scan timestamp/clock synchronization issue may exclude recently ingested assessments from short event-time searches. This release does not change the producer or ingestion timestamps.
- Existing 0.2.0 limitations remain; see `CHANGELOG-0.2.0.md`.
