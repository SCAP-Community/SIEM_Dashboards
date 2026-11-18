# SCAP & STIG Compliance — Splunk Dashboard v0.2.2

This directory contains source, installable `.spl`, documentation, and validation fixtures for example SCAP/STIG compliance dashboards. The event format is producer-neutral; an upstream source must translate assessment results to the documented `scap:json` contract.

- `src/scap_stig_compliance/` — installable app source
- `build/scap_stig_compliance-0.2.2.spl` — compiled Splunk application (tar.gz)
- `docs/` — producer-neutral dashboard guide, DOCX/PDF; SCC-specific release docs are distributed separately
- `INSTALL.md` — macro override and ingestion instructions
- `CHANGELOG-0.2.2.md` — change log and remaining limitations
- `tests/` — static contract regression tests and synthetic example data

Dashboards use `host_name`, `scanner_name`, and `scanner_version`, with legacy SCC `target_host`, `assessed_host`, payload `host`, and `scc_version` handled by search-time calculated fields. Splunk native metadata `host` is not changed. The app's `scap_index` macro still defaults to `scap-scc` and can be overridden using search-head `local/macros.conf`.

Historical 0.2.0 application and dashboard guide files remain available for reference.

Not yet qualified: live Splunk rendering, AppInspect/btool, multi-scan latest-scan/CCI accuracy, trend zero-value handling and regression correctness. This demo app is not a certified compliance reporting product.
