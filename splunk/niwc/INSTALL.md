# SCAP & STIG Compliance Splunk App v0.2.2 — installation

## Install and select an index

Install `build/scap_stig_compliance-0.2.2.spl` on a Splunk search head or deploy it through the appropriate search-head cluster process. The installed app directory is `scap_stig_compliance`.

The distributed `default/macros.conf` contains:

```ini
[scap_index]
definition = index="scap-scc"
iseval = 0
```

To select a different index **without modifying dashboard XML or shipped defaults**, create `$SPLUNK_HOME/etc/apps/scap_stig_compliance/local/macros.conf` containing:

```ini
[scap_index]
definition = index="security_compliance"
iseval = 0
```

Replace the example with the actual destination index. The index must exist, be readable by the search user's role, and match the **ingestion index**, which is independently configured in the monitor `inputs.conf` or HEC destination/token. Changing the SCC GUI index name does not update this macro or an existing Splunk file monitor. Search-head clusters should distribute this override using their supported deployer process; do not independently edit each member. Reload/restart configuration as required by Splunk administrators.

Confirm with Splunk Search: 

```spl
`scap_index` sourcetype="scap:json"
| stats count by event_type
```

## Producer-neutral event contract

New producer events should use `host_name` for the **assessed** endpoint. Splunk native indexed `host` is separate and must not be overwritten. Keep `host_id` as the stable machine identifier and `scan_id` as the assessment-run identifier. All producers should emit:

- `scanner_name` — scanner product name, e.g. `SCC`, `OpenSCAP`.
- `scanner_version` — scanner software version, separate from `schema_version` and `benchmark_version`.

Emit both fields on **all** `scan_summary` and `rule_result` events when changing producer outputs. The sysadmin host summary displays them as `Scanner` and `Scanner Version`.

The Splunk app uses `KV_MODE=json` and calculated fields in `default/props.conf`:

```ini
EVAL-host_name = coalesce(json_extract(_raw, "host_name"), json_extract(_raw, "target_host"), json_extract(_raw, "assessed_host"), json_extract(_raw, "host"))
EVAL-scanner_name = coalesce(json_extract(_raw, "scanner_name"), if(isnotnull(json_extract(_raw, "scc_version")), "SCC", null()))
EVAL-scanner_version = coalesce(json_extract(_raw, "scanner_version"), json_extract(_raw, "scc_version"))
```

This permits previously indexed SCC events to remain visible when they are still in the configured index and time range. Only older scan summaries contain `scc_version`; historical rule results cannot gain version values that were not ingested. The compatibility layer **does not** delete, modify, or deduplicate indexed events; loading the same scan twice can still double-count it.

## Ingestion responsibilities

Configure `sourcetype=scap:json`, event boundaries, `_time` mapping from UNIX-seconds `epoch_time`, destination index, and access permissions at the appropriate ingestion tier. Search-head `props.conf` cannot configure event breaking and timestamp parsing on an upstream forwarder/indexer. For HEC, use a valid JSON event envelope and authorized index selection. Do not combine this app's search-time `KV_MODE=json` with additional `INDEXED_EXTRACTIONS=json` for the same data without deliberate verification.

## Limitations

Structural checks and sample-data validation are not live Splunk qualification. The existing zero-score trend, latest-scan CCI selection, and multi-scan regression issues have not been corrected by these field-name changes. Full installation and AppInspect/btool/runtime verification are still required.

See the producer-neutral dashboard guide in `docs/` and `CHANGELOG-0.2.1.md` for the file change register. SCC-specific configuration guides are distributed with SCC.
