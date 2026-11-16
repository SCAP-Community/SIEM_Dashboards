# Splunk app v0.2.0 — installation and index selection

## Install

Install `build/scap_stig_compliance-0.2.0.spl` on the Splunk search head (or an appropriate search head cluster deployment path). App name: `scap_stig_compliance`.

1. Create the index that SCC data will actually be ingested into. The default is `scap-scc`.
2. Configure SCC HEC sending to target that index, if using HEC. For file/forwarder ingestion, configure the destination index on the Splunk input/forwarding path; changing SCC's GUI string alone does not route uploaded JSONL files.
3. Ensure the incoming events use sourcetype `scap:json`, and verify the indexed `_time`, source, and native `host`.
4. If using an alternate index, **create** `etc/apps/scap_stig_compliance/local/macros.conf` on the search head with:

   ```ini
   [scap_index]
   definition = index="security_compliance"
   iseval = 0
   ```

   Replace `security_compliance` with the actual index name. Do **not** edit `default/macros.conf`: `local/` overrides defaults and is retained across app updates. Apply a supported Splunk configuration reload/restart procedure and confirm macro resolution and search permissions.
5. Ensure Splunk roles running the dashboards can search that index; verify with `` `scap_index` sourcetype="scap:json" | stats count by event_type `` in Search.

## Field extraction / forwarders

`default/props.conf` sets `KV_MODE=json` for search-time field extraction; it does not depend on `INDEXED_EXTRACTIONS=json` on every workstation forwarder. **However:** search-head `props.conf` does not configure forwarder/indexer event breaking, timestamp extraction or destination index. Configure parsing and timestamp rules at the *actual* ingestion tier if JSONL data is sent through file/forwarder inputs. For HEC, configure index/sourcetype and event timestamp as needed.

The app computes `target_host` at search time using the payload's `target_host`, `assessed_host` or legacy `host` key, not Splunk's native `host` field. New SCC exporters should emit `target_host` and stop emitting payload `host`. `host_id` should be used as the stable endpoint identity, and `scan_id` to select individual scans.

## Additional cautions

- Do not enable `INDEXED_EXTRACTIONS=json` in a separate deployed add-on for this sourcetype unless the overall extraction strategy is reviewed to avoid duplicate JSON extractions.
- The previously distributed, unused accelerated data model was removed. Dashboard searches do not use it.
- Existing dashboard trend/latest-scan/CCI logic still requires multi-scan runtime qualification; this release does not claim those defects have been resolved.
- `default/macros.conf` is shipped with the `scap-scc` default; user-specific settings belong in `local/macros.conf` and must not be bundled into the distributed app.
