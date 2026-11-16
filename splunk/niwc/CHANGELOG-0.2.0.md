# SCAP & STIG Compliance — v0.2.0 revised field-contract release

**Base:** earlier `SIEM_Dashboards-0.2.0.zip` from 2026-11-16. The app version remains **0.2.0** as requested; this bundle supersedes the earlier package of that same version. For production release management, a unique patch version/build identifier is advisable.

## Modified source files versus earlier v0.2.0

- `src/scap_stig_compliance/default/props.conf` — new `EVAL-host_name`, `EVAL-scanner_name`, `EVAL-scanner_version`; retains `KV_MODE=json`; normalized host fallback order: host_name → target_host → assessed_host → legacy raw host; scanner version falls back to legacy `scc_version` and scanner name to SCC **only** when `scc_version` is present. No modification of Splunk's native host metadata.
- `src/scap_stig_compliance/default/data/ui/views/stig_enterprise_compliance_dashboard.xml` — replace query references to `target_host` with `host_name`, maintaining displayed Host labeling and existing search logic.
- `src/scap_stig_compliance/default/data/ui/views/sysadmin_stig_dashboard.xml` — replace `target_host` with `host_name`, replace `scc_version` with `scanner_version` and add `scanner_name` in the host summary's extraction/aggregation/display; table columns now `Scanner` and `Scanner Version` rather than `SCC Version`. Update dashboard description to producer neutral.
- `src/scap_stig_compliance/default/app.conf` — producer-neutral description (version remains 0.2.0).
- `INSTALL.md`, `readme.md`, repository `README.md` — field contract, migration and index override documentation.
- `build/scap_stig_compliance-0.2.0.spl` — rebuilt tar.gz from the modified 16-file source application; no `candidate` suffix.

## Documentation changed / removed / added

- Removed outdated `docs/SCC_Splunk_Guide.pdf`, which referenced the old 0.1.x app behavior.
- Added updated `docs/SCAP_STIG_Splunk_Dashboard_Guide_v0.2.0.docx` and `.pdf` (producer-neutral).
- Added updated `docs/SCC_5.16_Splunk_Integration_Companion_v0.2.0.docx` and `.pdf` (SCC-specific).
- Added `tests/test_contract.py` and `tests/fixtures/new_and_legacy_events.jsonl` for static migration checks.

## Preserved / not changed

- `src/scap_stig_compliance/default/macros.conf` still defines `scap_index` as `index="scap-scc"`. Customers override it in **`$SPLUNK_HOME/etc/apps/scap_stig_compliance/local/macros.conf`**, not by editing `default/` or dashboard XML. SCC/HEC/monitor input destination configuration is separate.
- Remaining JS, CSS, icons, nav and meta settings, and Elastic placeholder are unchanged.
- Deleted data-model acceleration and model file from earlier v0.2.0 remain deleted.

## Limitations

- These are **field-contract updates**, not fixes for pre-existing history/CCI/latest-scan/zero-score/regression defects.
- Source/package and JSON structure were validated statically. No live Splunk, AppInspect, or runtime/dashboard rendering test was performed.
- SCC must independently implement producer-side output of `host_name`, `scanner_name`, `scanner_version` on every event. The supplied manually edited SCC sample only showed `target_host`; it did not establish exporter support.
- Repeated imports of the same `scan_id` are not automatically deduplicated.
- New producer-side field names constitute a reporting contract change; a separately ratified schema version is recommended. Illustrative 2.0.0 events in the guides are *examples*, not proof SCC 5.16 emits that schema.
