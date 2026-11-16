# SCAP & STIG Compliance — Splunk dashboard app v0.2.0

This repository contains the source and packaged Splunk dashboards for SCC SCAP results. It is an example integration, not a qualified or fully supported Splunk product.

## Distribution

- Source: `src/scap_stig_compliance/`
- Installable Splunk app: `build/scap_stig_compliance-0.2.0.spl` (gzip-compressed TAR archive)
- Change manifest: `CHANGELOG-0.2.0.md`
- Installation and configuration: `INSTALL.md`

## Compatibility and remaining limitations

The app expects sourcetype `scap:json` and events such as `scan_summary` and `rule_result`. Dashboards use the `scap_index` macro, which defaults to `scap-scc` and can be overridden through `local/macros.conf`.

Search-time JSON extraction uses `KV_MODE=json`. Ingestion-tier event breaking, timestamps, and index routing must be configured separately. Legacy SCC events with a payload `host` field are supported via a calculated `target_host` field, but the producer should emit `target_host` directly to avoid collisions with Splunk native `host` metadata. The SCC GUI does not automatically update the installed dashboard macro.

**Not yet qualified in live Splunk:** runtime rendering, ingest scenarios, AppInspect/btool, and existing dashboard search correctness for zero-score history, latest-scan CCI aggregation, and regression analysis. Do not construe this packaged release as qualification of those issues.
