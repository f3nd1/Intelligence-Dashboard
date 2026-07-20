# Changelog

## v1.9.6-cardsort (2026-07-20)

- Sorted the chart-card grid alphabetically by visual name, matching the visual navigation menu's existing order. The menu list was already alphabetical (`entries.sort()` in `20-explore-runtime.js`'s `buildRegistry()`), but the actual rendered cards on each subcriterion tab were a separate code path that built cards straight from the raw config order, so scanning down the page didn't match scanning the menu. Fixed for Criteria 1, 2, 3, 6 and 7 (`ensureLiveSectionCards` in `30-live-foundation-runtime.js`), Criterion 4 (`ensureC4ExpandedVisuals` in `10-platform-runtime.js`, preserving each visual's original data-window index so its live metrics are unchanged), and Criterion 5 (a one-time DOM reorder of its static chart cards, scoped within each existing card group so the nested 5.1.1-style sub-tab structure isn't disturbed).

## v1.9.6-urlparam (2026-07-20)

- Fixed direct-URL deep-linking to the wrong dashboard on first load. Navigating straight to a URL with `?dashboard=criterion_3` never worked; the page always showed whatever dashboard was last saved in `localStorage`, only appearing to "fix itself" after a reload because a manual `<select>` change had since overwritten that saved value. No code anywhere read the `dashboard` query parameter — it was write-only, produced only by the "copy link" actions. Now the parameter is read on load and passed through the same `setDashboard()` function the dashboard `<select>` already uses, taking priority over `localStorage` when present.

## v1.9.6-tabfix (2026-07-19)

- Fixed sub-criterion tab navigation doing nothing for Criteria 1, 2, 3, 5, 6 and 7 (Criterion 4 was unaffected). The shared tab bar was being covered by the loading overlay while a section loaded, so clicks landed on the overlay instead of the tab. Raised the tab bar above the overlay (`.ucc-shared-tabs { position:relative; z-index:1000 }`) so clicks always reach the tab buttons, even mid-load.

## v1.9.6-lazyload (2026-07-19)

- Fixed page-load lag in the Custom HTML Block. Chart-card DOM for every subcriterion section of Criteria 1, 2, 3, 6 and 7 was being built eagerly on every page load (449 chart cards total), regardless of which dashboard or tab was actually visible. Now only the active dashboard's active section builds on load; the rest build lazily the first time a user switches into that tab.
- Deferred Criterion 4's 7 Server Script API calls until the user actually switches to Criterion 4, instead of firing them unconditionally on every page load regardless of visibility.

## v1.9.5

- Fixed Source Mapping Report and hover-menu CSS by mounting overlays inside the scoped Custom HTML Block.
- Made the Source Mapping Report action open a proper modal rather than unstyled content below the dashboard.
- Restored exact visual catalogue counts and exact subcriterion ownership.
- Split grouped live panels by active subcriterion, preventing inactive diagrams from appearing blank.
- Increased blank-render detection from 4.5 seconds to 20 seconds and ignored active loading overlays.
- Mapped Staff Goal analytics to `Goal`, training needs to `Training Needs Analysis`, communication material vetting to `Material Vetting Form`, and provider evaluation to `Provider Rating`.
- Removed retired source probes and metrics for End of Module Survey (Student), Naming Series Register, Naming Series, TNA, Training Needs Assessment and Material Vetting.

## v1.9.4

- Standardised every Diagram/Table switch to the Criterion 5 compact control.
- Restored hover, focus and click visual menus across all seven criteria.
- Preserved exact visual catalogue counts of 84, 99, 90, 84, 94, 96 and 80.
- Made the hero View tools action functional and added visual navigation and
  source mapping actions.
- Added an approved-only Source Mapping Report for missing DocTypes, fallback
  resolution, permission failures and available fields.
- Changed source resolution to continue through approved fallbacks after a
  missing DocType or metadata failure, while still stopping on permission denial.
- Corrected Criterion 6 Provider Rating resolution using Provider Rating first
  and Supplier Rating as its approved fallback.
- Prevented non-finite chart values from producing invalid SVG paths and replaced
  blank or invalid visuals with a diagnostic state.
- Updated the package validator for v1.9.4 and exact visual count verification.

## v1.8.9

- Scroll the selected criterion back to its hero before loading.
- Keep all main and secondary criterion menus on one horizontal row.
- Restore persistent Criterion 5 child navigation for 5.1.1, 5.1.2, 5.2.1,
  5.2.2 and 5.3.1.
- Standardise Management Questions tables and record/source actions across all
  seven criteria.
- Add frontend-generated extended questions for readable live metrics.
- Add Provider Rating → Supplier Rating approved fallback resolution for
  Criteria 3 and 6.
- Expand live diagram inventories and preserve Diagram/Table/drill-down
  controls.
- Preserve the existing Criterion 4 and Criterion 5 calculation engines.


## v1.8.8

- Removed tuple/list assignment unpacking from Criterion 1, 2, 3, 5, 6 and 7
  Server Scripts.
- Fixed `NameError: _unpack_sequence_ is not defined` under Frappe 15.83
  RestrictedPython safe-exec.
- Preserved all API method names, payloads and response contracts.
- No dashboard calculation or layout logic changed.


## v1.8.7

- Moved the navigation arrow into the single-row desktop header.
- Added `UCC Analytics - Criterion 1.py`.
- Added `UCC Analytics - Criterion 2.py`.
- Added `UCC Analytics - Criterion 7.py`.
- Connected Criteria 1, 2, 3, 6 and 7 dashboards to permission-aware APIs.
- Preserved Criterion 4 and Criterion 5 live implementations.
- Added live source, metric, question, exception and drill-down rendering.
- Added official Criterion 1, 2 and 7 policy registries.
- Removed the unsupported active Criterion 7.2 preview tab.
- Added policy source files and reusable documentation for Criteria 1, 2 and 7.
- Replaced active dummy values with explicit unavailable or unsupported states.

## v1.8.5

- Added partial live Server Script foundations for Criteria 3 and 6.
- Added source inventories for Criteria 3–6.

Earlier release history is preserved in `documentation/RELEASE_NOTES.md`.
