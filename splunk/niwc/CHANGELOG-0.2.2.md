# SCAP & STIG Compliance Splunk App 0.2.2 — 2026-11-18

## Narrow maintenance corrections from 0.2.1

- **Executive > Hosts Evaluated for Benchmark:** Rename the displayed `rules_informational` column from `CAT IV Fails` to `Informational`.
- **Executive > Hosts Evaluated for Operating System:** Preserve the sum of `rules_informational`, but alias it `informational` and label its output `Informational`, not `CAT IV Fails`.
- **Executive > Hosts Evaluated for Operating System:** Correct the final alias from `cat3_fails` to the existing aggregate `cat3`, making the output label `CAT III Fails`.
- **Regression tests:** Assert both informational labels, the CAT III alias, existing aggregation/OS filtering, and that no mislabeled CAT IV failure field remains in either affected query.
- Update application version to **0.2.2**. No changes to scanner output, event ingestion, dashboard navigation, app ID, search index macro, or rule filters.

## Explicit non-changes and known limitations

- `SysAdmin Studio Beta` is absent from the GitHub 0.2.1 source and installed `.spl`; if visible, investigate Splunk-local or user-owned dashboard definitions rather than removing source files.
- Future rule-level filtering changes remain deferred pending runtime testing.
- The base-search `rules_informational=coalesce(rules_informational, rules_info, cat4_fails, 0)` legacy fallback is unchanged in this label-only release. When no informational fields exist, it may use the CAT IV failure field as a fallback; producer-specific semantic validation remains important.
- CAT IV failures are **not** added as a separate displayed column in the two affected drilldowns. The source base search still retains `cat4_fails` for future, separately qualified use.
- Runtime Splunk checks, AppInspect/btool, and other historical issues are outside this static release qualification. All 0.2.1 limitations remain documented in `CHANGELOG-0.2.1.md`.
