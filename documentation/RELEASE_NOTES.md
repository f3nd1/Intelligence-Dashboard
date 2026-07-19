# UCC Intelligence Platform Release Notes

## v1.9.5

- Kept the Source Mapping Report and visual hover menu inside the Custom HTML
  Block so Frappe-scoped CSS applies to the complete overlay.
- Changed diagnostic-button handling to platform-level event delegation so
  dynamically rendered Source Mapping Report buttons remain clickable.
- Rebuilt the live visual registry from the approved definitions rather than
  legacy hidden chart containers. Exact counts are 84, 99, 90, 84, 94, 96
  and 80 for Criteria 1 to 7.
- Added exact subcriterion visual containers inside grouped panels, so tabs such
  as 2.3.1 and 2.3.2 expose only their own visual definitions.
- Increased the blank-visual guard to 20 seconds and made it aware of active
  dashboard loading overlays, preventing slow API responses from being marked
  blank prematurely.
- Mapped staff goals to `Goal`, training needs to `Training Needs Analysis`,
  communication material approvals to `Material Vetting Form`, and provider
  evaluations to `Provider Rating` with `Supplier Rating` as fallback.
- Removed obsolete Criterion 2 source probes for old survey, naming-series and
  abbreviated training-needs DocTypes.
- Filtered Source Mapping Report results to the active criterion, preventing
  unrelated shared source rows from producing duplicate or misleading errors.

## v1.9.4

- Restored compact visual menus on hover, keyboard focus and click for all
  criterion section tabs.
- Standardised Diagram/Table controls across Criteria 1 to 7 using the Criterion
  5 design.
- Exposed all live visual definitions without a permanent global navigator:
  Criterion 1 84, Criterion 2 99, Criterion 3 90, Criterion 4 84,
  Criterion 5 94, Criterion 6 96 and Criterion 7 80.
- Repaired View tools and added Open visual navigator and Source mapping report.
- Added approved-only DocType diagnostics, including resolved candidates,
  fallback use, permissions, missing fields and field inventories.
- Corrected Provider Rating resolution in Criterion 6 so a missing or invalid
  primary candidate does not prevent the approved Supplier Rating fallback.
- Added finite-number guards and explicit blank-visual diagnostics to prevent
  invalid SVG path output such as MNaN,NaN.
- Preserved all existing API method names, permission-aware retrieval and record
  drill-down boundaries.

## v1.9.3

- Removed the complete global Visual Navigator.
- Removed the visual search, jump selector, criterion row and sticky navigator.
- Added hierarchical child menus under Criterion 5 parent tabs.
- `5.1` exposes `5.1 Overview`, `5.1.1`, and `5.1.2`.
- `5.2` exposes `5.2 Overview`, `5.2.1`, and `5.2.2`.
- `5.3` exposes `5.3 Overview` and `5.3.1`.
- Child menus work with mouse hover, keyboard focus, arrow keys and click.
- Existing live charts, APIs, tables, question answers and drill-downs are preserved.


## v1.9.2

- Fixed the v1.9.1 visual navigator runtime being outside the platform scope.
- Removed references to undefined `root` and `state`.
- Corrected section discovery for Criterion 5 (`data-panel`), Criterion 4 (`data-c4-panel`) and live foundation dashboards (`data-demo-panel`).
- Corrected criterion switching through the existing dashboard selector.
- Preserved all v1.9.0 visual definitions and v1.9.1 navigator UI.


## v1.9.1

- Added a persistent visual navigator above the dashboards.
- Added visible Criterion 1–7 tabs.
- Added visible subcriterion tabs with live visual counts.
- Restored discoverability for Criterion 5 sections such as 5.1.1, 5.1.2, 5.2.1, 5.2.2 and 5.3.1.
- Added visual title/topic search.
- Added a jump-to-visual selector.
- Remembered the last-opened subcriterion per criterion.
- Removed reliance on hover-only or hidden child navigation.
- Added sticky desktop navigation and responsive mobile behavior.


## v1.9.0

- Expanded Criterion 1 to 84 live visual definitions.
- Expanded Criterion 2 to 99 live visual definitions.
- Expanded Criterion 3 to 90 live visual definitions.
- Expanded Criterion 4 to 84 live visual definitions using the existing mature API.
- Preserved all 94 Criterion 5 live charts.
- Expanded Criterion 6 to 96 live visual definitions.
- Expanded Criterion 7 to 80 live visual definitions.
- Added bar, donut, funnel, lifecycle, radar, matrix, gauge and trend presentations.
- Preserved Diagram/Table, matching-record drill-down and source-list actions.
- Used only live metrics, readiness summaries and exception values.
- Added browser rendering containment for the larger visual catalogue.


## v1.8.9

### Navigation and loading

- Criterion changes now scroll to the active dashboard hero before the live API
  load starts.
- Main tabs, Criterion 5 child tabs and local section tabs remain on one
  horizontal row and use horizontal scrolling when necessary.
- Criterion 5 child navigation is persistent rather than hover-only.

### Universal management questions

Every criterion now uses:

```text
Criterion | Question | Answer | Source / Calculation | Status
```

- Answer cells provide a matching-record action when a live metric is readable.
- Source / Calculation cells provide a resolved DocType-list action.
- Criteria 1, 2, 3, 4, 6 and 7 add extended questions for live metrics not
  already represented by a curated management question.
- Criterion 5 preserves its extensive curated question catalogue.

### Sources and diagrams

- Criteria 3 and 6 resolve Provider Rating through `Provider Rating`, then
  `Supplier Rating` when the site uses the ERPNext technical DocType.
- Criteria 1, 2 and 7 have expanded, non-bar-only live visual inventories.
- Every generated live visual includes Diagram/Table switching and record
  drill-down.
- Existing Criterion 4 and Criterion 5 visual inventories remain intact.


## v1.8.8

### Safe-exec hotfix

- Fixed the Criterion 7 traceback:
  `NameError: name '_unpack_sequence_' is not defined`.
- Removed all tuple/list assignment unpacking from Criterion 1, 2, 3, 5, 6 and
  7 API Server Scripts.
- Kept API methods, policy registries, metrics, filters and response contracts
  unchanged.
- No Custom HTML Block functionality changed.


## v1.8.7

### Navigation

- Moved the minimise/expand arrow into the desktop header's single grid row.
- The full header now uses: Brand | Workspaces | Dashboard | Arrow.
- The collapsed header uses: UCC control | Expand arrow.
- The shell remains inside `#uccIntelligencePlatform`.

### Analytics

- Added `ucc_analytics_criterion_1`.
- Added `ucc_analytics_criterion_2`.
- Added `ucc_analytics_criterion_7`.
- Connected Criteria 1, 2, 3, 6 and 7 to permission-aware API foundations.
- Preserved Criterion 4's mature live API.
- Preserved Criterion 5's validated live frontend and migration API.
- Removed active dummy KPI and chart values from Criteria 1, 2, 3, 6 and 7.
- Retained the diagram-rich layouts; their values are now derived from API metrics.
- Removed the unsupported active Criterion 7.2 tab.

### Policies and documentation

- Added approved policy registries and original policy files for Criteria 1, 2 and 7.
- Added criterion-specific source, metric, API and open-item documentation.
- Updated Bootstrap, Criterion Catalogue and deployment instructions.
- Unsupported sources and fields remain explicit instead of being guessed.

### Release boundary

A **live foundation** queries actual readable DocTypes and confirmed candidate
fields. It does not imply that every policy measure is fully implemented. Missing
metadata is returned as `unavailable`, `unsupported` or `unsupported_field`.

## v1.8.5

- Added `UCC Analytics - Criterion 3.py`.
- Added API method `ucc_analytics_criterion_3`.
- Added `UCC Analytics - Criterion 6.py`.
- Added API method `ucc_analytics_criterion_6`.
- Added permission-aware source and metric readiness.
- Added safe metric drill-downs.
- Added explicit unsupported states instead of guessed calculations.
- Updated Bootstrap and Criterion Catalogue with partial-live API metadata.
- Kept the Criterion 3 and Criterion 6 dashboard views as dummy previews.
- Added exact Frappe deployment instructions.


## v1.8.4 documentation revision — Criterion 6 partial inventory

- Added the confirmed Quality Action custom-field export.
- Added Quality Action Resolution.
- Added the complete supplied Management Review definition.
- Added Operational Outcomes Cost Time Saving.
- Added Criterion 6 source-to-policy and source-to-metric mapping.
- Recorded cross-criterion ownership for provider evaluation and cost-saving outcomes.
- Preserved the original CSV and text source files in the package.
- Recorded missing child tables, parent DocTypes, workflows and business rules.
- No Custom HTML Block runtime or Server Script logic changed.


## v1.8.4 documentation revision — Criteria 4 and 5 inventories

- Added a permanent Criterion 4 source, field, policy, metric and visual inventory.
- Documented the live `ucc_analytics_criterion_4` API contract.
- Added a permanent Criterion 5 source, field, section and visual inventory.
- Documented the exact Criterion 5 Server Script migration boundary.
- Recorded 24 Criterion 4 visuals and 94 Criterion 5 charts.
- Added security, privacy and unresolved-item references for both criteria.
- No Custom HTML Block runtime or Server Script logic changed.


## v1.8.4 documentation revision — Criterion 3 source inventory

- Added the confirmed Criterion 3 DocType inventory.
- Added normalized fields and source-to-metric mappings.
- Added sensitive-field and PII exclusions.
- Recorded that Student Applicant reuses the Criterion 4 mapping.
- Recorded remaining child-table, workflow and business-rule unknowns.
- No Custom HTML Block runtime or live Server Script logic changed.


## v1.8.4

- Unified every criterion hero banner, action card, filters, tabs, panels and KPI typography with the Criterion 5 framework.
- Replaced the broken `<details>` View tools implementation with one shared explicit popover component.
- View tools now works for live Criterion 4, live Criterion 5 and every dummy criterion.
- Expanded Criterion 4 from 7 to 24 live diagrams using its existing permission-aware metric registry.
- Retained the existing diagram-rich Criterion 5 analytics.
- Rebuilt Criterion 3 from PPD-SES-SL-3.1.1 v1.2 and PPD-SES-SL-3.2.1 v1.2.
- Rebuilt Criterion 6 from PPD-SGL-SQ-6.1.1 v1.2, PPD-SGL-SQ-6.2.1 v1.3, PPD-SGL-SQ-6.3.1 v1.2, PPD-OE-FN-6.4.1 v1.2 and PPD-SGL-SQ-6.5.3 v1.2.
- Added bar, donut, funnel, lifecycle, matrix, radar, trend, gauge and 5×5 risk-matrix preview renderers.
- Added `reference/policy-runtime-registry.json`.
- Updated `server-scripts/README.md` with all 11 scripts, API methods, deployment order and live/preview rules.


## v1.8.3

- Replaced automatic scroll minimising with a manual arrow control.
- Added a live Criterion 5 readiness strip with source and metric counts.
- Added Criterion 5 readiness details without inventing a policy code.
- Rebuilt Criteria 1–3 and 6–7 using the Criterion 5 framework.
- Added dummy filters, tabs, KPIs, diagrams, tables, questions, records,
  sources, data-quality pages, exports, diagnostics and readiness dialogs.
- Added dummy preview diagrams to Explore.
- Added `UCC Analytics - Placeholder Preview.py`.
- Preserved the existing live Criterion 4 and Criterion 5 integrations.


## v1.8.2

### Custom HTML Block stability

- The top navigation is never moved into `document.body`.
- The navigation remains inside `#uccIntelligencePlatform`, preserving scoped
  CSS and preventing unformatted duplicate-looking HTML below the block.
- After scrolling, the bar becomes a single UCC button.
- Clicking the UCC button expands the full navigation.
- Scrolling back to the top restores the normal full navigation.

### Interface consistency

- Removed points from visible criterion labels.
- Applied one shared typography scale to Criteria 4 and 5.
- Added a clear placeholder message in Explore for Criteria 1–3 and 6–7.
- Explore search and Clear remain isolated from Frappe global search.

### Housekeeping

- Active CSS is now maintained in one source file: `src/css/platform.css`.
- Version patch JavaScript was merged into `src/js/10-platform-runtime.js`.
- Inactive source files were moved to `archive/legacy-source/`.
- Release notes and validation now use one rolling file each.

## Previous release history

## Live deployment change

The approved navigation is now integrated into the real ERPNext Custom HTML
Block. There is no separate prototype application.

The deployment remains exactly:

```text
custom-html-block/
├── HTML.html
├── CSS.css
└── JAVASCRIPT.js
```

## Added

- third top-level workspace: **Explore**
- searchable catalogue generated from the real Criterion 4 and Criterion 5
  visual elements
- section and visual-type filters
- one-click navigation to the original live diagram card
- automatic activation of the correct criterion, section and diagram view
- highlighted destination and **Back to Explore** control
- automatic discovery of future diagrams without a second chart engine

## Preserved

- all Criterion 4 pages, calculations, D3 diagrams, tables and drill-downs
- all Criterion 5 pages, calculations, D3 diagrams, tables and drill-downs
- the existing role-first Ask UCC flow:
  - Student Journey
  - Recruitment Agent
  - Quality Action
  - HR placeholder
- record-first search, course filtering, pagination and recent records
- guided questions, optional free-form AI, exports, print and diagnostics
- source links, current-user permissions, empty states and notices
- Server Scripts and backend files

## Verification limitation

Static package checks passed. Live ERPNext/Frappe browser regression testing is
still required because this environment cannot execute the Custom HTML Block
inside the target UCC site.
## User-reported fixes

1. Restored `DEPLOYMENT_NOTES.md` inside `custom-html-block/`.
2. Updated relevant logs, version metadata and documentation.
3. The long navigation bar now minimises to the UCC icon at the top-left after scrolling.
4. Explore hero heading and descriptive text use readable white contrast.
5. Criterion 4 and Criterion 5 **View tools** menus use explicit open/close logic.
6. Criterion 4 and Criterion 5 dashboard typography and hero sizing are aligned.
7. Explore search stops propagation so it does not activate Frappe global search.
8. Explore Clear resets search, section and visual-type filters.
9. Criteria 1–7 titles, weights and subcriteria are now present.

## Placeholder policy

Criteria 1–3 and 6–7 display approved names and subcriteria only. They do not
show fabricated KPIs or pretend to have live source integrations.

A new optional Server Script, `UCC Analytics - Criterion Catalogue.py`, returns
the same catalogue and identifies live versus placeholder criteria.

## Live areas preserved

- Criterion 4
- Criterion 5
- Student Journey
- Recruitment Agent
- Quality Action
- Explore catalogue and original live diagram navigation
- exports, diagnostics, source links and record drill-downs

## Required UAT

Static checks pass, but the package must still be tested in the target Frappe
site for browser focus behavior, sticky navigation, permissions, live API
responses, exports and responsive rendering.
