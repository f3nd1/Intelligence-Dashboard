# UCC Intelligence Platform v1.9.5

## v1.9.5 correction release

This release fixes the v1.9.4 visual-navigation and diagnostic regressions.

- Source Mapping Report and visual hover menus are mounted inside the Custom HTML Block, so Frappe-scoped CSS applies.
- The visual catalogue is built from the approved definitions only: Criterion 1 = 84, Criterion 2 = 99, Criterion 3 = 90, Criterion 4 = 84, Criterion 5 = 94, Criterion 6 = 96, Criterion 7 = 80.
- Grouped live panels now display only the active subcriterion's diagrams.
- Slow API responses are no longer marked as blank after 4.5 seconds. The guard waits 20 seconds and ignores active loading overlays.
- Confirmed mappings: Goal for Staff Goal analytics, Training Needs Analysis, Material Vetting Form and Provider Rating.
- Obsolete Criterion 2 source probes were removed and are no longer queried.

Deploy the three Custom HTML Block outputs together and replace the updated Server Scripts listed in `custom-html-block/DEPLOYMENT_NOTES.md`.
