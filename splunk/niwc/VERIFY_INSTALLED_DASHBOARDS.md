# Verify the installed SCAP & STIG Compliance app v0.2.0

The updated Sysadmin dashboard contains an **Enterprise Host Compliance Summary** table with columns **Scanner Name** and **Scanner Version**. There is no **SCC Version** column in either dashboard shipped by this repository.

## Confirm installation and app namespace

1. Install `build/scap_stig_compliance-0.2.0.spl` using Splunk Web **Apps > Manage Apps > Install app from file**, selecting upgrade of the existing `scap_stig_compliance` application when prompted.
2. Open the **System STIG Compliance Dashboard** from the **SCAP & STIG Compliance** app, not a cloned or user-saved dashboard with a similar title.
3. Check for dashboard overrides in the corresponding `local` or user configuration directories. A saved dashboard can take precedence over the app's `default/data/ui/views/*.xml` source.
4. In a search-head cluster, use the established deployer/bundle procedure. Refresh the app/dashboard browser view after deployment; restart/reload services as required by the environment.

## Check the installed source on the search head

The app-relative path should be `$SPLUNK_HOME/etc/apps/scap_stig_compliance/default/data/ui/views/sysadmin_stig_dashboard.xml`.

Check for the exact SPL display aliases:

```spl
| rename scanner_name as "Scanner Name", scanner_version as "Scanner Version"
```

On a Linux search head, for example:

```sh
grep -nE 'SCC Version|scanner_name as|scanner_version as' \
  "$SPLUNK_HOME/etc/apps/scap_stig_compliance/default/data/ui/views/sysadmin_stig_dashboard.xml"
```

If the file contains the new labels but the UI still displays **SCC Version**, inspect overrides under:

- `$SPLUNK_HOME/etc/apps/scap_stig_compliance/local/data/ui/views/`
- `$SPLUNK_HOME/etc/users/<user>/scap_stig_compliance/local/data/ui/views/`

Do **not** delete a locally customized dashboard without first backing it up and evaluating the customizations. Compare its effective XML with the new default view, then update or remove the override through an approved deployment process.

The existing SCC JSONL `scc_version` summary field remains supported through the `EVAL-scanner_version` compatibility expression in `default/props.conf`. A field value of `Unknown` indicates missing or unextracted source metadata; it does not justify restoring the `SCC Version` column.

## Index override

The existing `scap_index` macro remains unchanged. To select a custom index, use `$SPLUNK_HOME/etc/apps/scap_stig_compliance/local/macros.conf`:

```ini
[scap_index]
definition = index="security_compliance"
iseval = 0
```

The index selected here must match the ingestion destination and be searchable by the user's Splunk role.

## Verification scope

The source and built `.spl` are compared byte-for-byte for their application files. These static checks do not prove live Splunk dashboard rendering or fix existing historical-query correctness issues.
