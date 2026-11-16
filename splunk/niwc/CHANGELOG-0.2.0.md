# SCAP & STIG Compliance v0.2.0 — source/file change register

**Baseline:** uploaded `SIEM_Dashboards-main.zip` version 0.1.0. **Scope:** Splunk NIWC app; Elastic placeholder and repository overview preserved.

## Modified existing files (relative to repository root)

- `splunk/niwc/src/scap_stig_compliance/default/app.conf` — `[launcher] version = 0.2.0`.
- `splunk/niwc/src/scap_stig_compliance/default/props.conf` — remove `INDEXED_EXTRACTIONS=json`, `KV_MODE=none` and `AUTO_KV_JSON=true`; set `KV_MODE=json`; add search-time `EVAL-target_host` with fallback to JSON payload `host` and `assessed_host`.
- `splunk/niwc/src/scap_stig_compliance/default/data/ui/views/stig_enterprise_compliance_dashboard.xml` — replace payload-host field references with `target_host`.
- `splunk/niwc/src/scap_stig_compliance/default/data/ui/views/sysadmin_stig_dashboard.xml` — replace payload-host field references with `target_host`.
- `splunk/niwc/src/scap_stig_compliance/metadata/default.meta` — remove unused data-model permission stanzas.
- `splunk/niwc/readme.md` — update version and setup/qualification pointers.

## Deleted existing files

- `splunk/niwc/src/scap_stig_compliance/default/datamodels.conf` — data-model acceleration was unused.
- `splunk/niwc/src/scap_stig_compliance/default/data/models/SCAP_Compliance_Executive_Summary.json` — unused and hard-coded the `scap-scc` index.
- `splunk/niwc/build/scap_stig_compliance-0.1.0.spl` — superseded compiled package.

## Added files

- `splunk/niwc/build/scap_stig_compliance-0.2.0.spl` — new installable TAR.GZ package regenerated from the source directory.
- `splunk/niwc/INSTALL.md` — index override, ingestion, metadata/host semantics, and validation instructions.
- `splunk/niwc/CHANGELOG-0.2.0.md` — this change register.

## Unchanged

- `splunk/niwc/src/scap_stig_compliance/default/macros.conf` — intentionally retains the overridable default `[scap_index]` macro (`index="scap-scc"`).
- Remaining JavaScript, CSS, assets, navigation, source license, guide PDF and Elastic placeholder unchanged.

## Outstanding

The SCC producer must be updated separately to output `target_host` instead of payload `host`. This release includes a backward-compatible dashboard fallback but cannot remove the metadata collision from legacy records. Zero-score history, latest-scan CCI and regression search behavior were **not** fixed or verified in live Splunk. SCC GUI index configuration does not propagate into a separately deployed Splunk app.
