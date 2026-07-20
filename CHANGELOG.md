# Changelog

## v1.9.8-remove-changelog (2026-07-20)

- **Removed the in-app Criterion 5 changelog feature entirely** (the `CHANGELOG` array, both dialog implementations, the version-pill trigger, and all styling). Root cause of the user's repeated failed removal attempts: the feature existed in **two independent implementations** in the source (`openChangelogDialog` + `<dialog data-changelog-dialog>` and `openChangelog` + `[data-changelog-overlay]` sheet, each with its own click handler on the same `[data-action="show-changelog"]` button), and edits made directly to the built/deployed `JAVASCRIPT.js` were silently reverted by the next `tools/build_custom_block.py` run, which regenerates it from `src/`. This removal is in the source files, so it survives rebuilds. Verified: zero `changelog` references remain in any of the three built files.
- Adopted the changelog-removal scope from the user's manually-edited reference file; the Criterion 4 visual-card feature that file accidentally deleted (`C4_VISUAL_EXPANSION`, `ensureC4ExpandedVisuals`, `renderC4Visual`, `drawC4Visual`, all D3 shape renderers) is untouched on main and verified intact — all 30 C4 expanded cards render.

## v1.9.8-hero-tools-stacking (2026-07-20)

- Fixed the hero "View tools" menu rendering behind the filter row, tab bar and loading overlay. Root cause: `header.hero` creates a stacking context at `z-index:20` while the sibling tab bar creates one at `z-index:1000`, so **no** z-index inside the hero (the menu's 240, or even the old portal's 2147483646) could ever lift the menu above the tabs — which is why earlier menu-z-index fixes never held. The fix raises the **hero itself** to `z-index:1200` only while a tools menu is open (`.ucc-platform .hero:has(.ucc-hero-tools[open])`). Verified via elementFromPoint sampling: all menu points now hit the menu in Criteria 1, 4 and 5.

## v1.9.8-dead-code (2026-07-20)

- Removed verified-dead code: `coverageStatus`/`evidenceDetails` (10-platform-runtime), the dead chain `numeric`/`adjusted`/`adjustmentFor`/`selectedFilters`/`renderChartCard`/`sectionCode` (30-live-foundation-runtime; `renderChartCard` even called the never-defined `makeChartRows`, proving it can never have run), the orphaned `.ucc-tools-portal` CSS block (no JS ever assigns that class), and `.evidence-detail`/`.detail-list` CSS orphaned by the `evidenceDetails` removal. Each candidate confirmed to have zero references across all source JS/HTML before deletion.


## v1.9.7-c5-drop-hydration (2026-07-20)

- Followed up the earlier parallel-hydration change (which batched the per-record `doc()` loops) by auditing whether Criterion 5's 10 `full:true` DocTypes need the full document at all. For each, traced exactly which fields the active (post-reduction) visuals read and compared against the fields `list()` already returns.
- Result: **2 of the 10 don't need hydration.** `Student Intake No` reads only `name`/`program`/`course_start_date`/`course_end_date` (all in `list()`), and `Supplier Rating` reads only `evaluation_stage` (in `list()`). Dropped `full:true` for both — replaced with `cap:500` so the loader still takes the same first-500 records (by `modified desc`) it did before, guaranteeing every visual's displayed counts/groups are byte-identical, but with **zero per-record `doc()` calls**. Verified in the instrumented harness: section 5.2.1 dropped from 18 to 12 hydration calls and 5.3.1 from 18 to 12 (the eliminated DocType's calls gone; in production this removes up to 500 sequential `doc()` round-trips per DocType per heavy section).
- The other 8 stay `full:true` (already batched) because they genuinely need the full document: child tables (`Course Review.actionplan_progress`, `Module Class Details.schedules`, `Partnerships Agreement Management.monitoring_childtable`/`table_luoo`, `Survey Response.response`) which `frappe.client.get_list` cannot return, and dynamic field-name probing (Module Review evidence ratings, Student Admission UCC / Partnership Agreement signature-and-status candidates, Classroom Observation likert/text) that would trip `safeList`'s field-mismatch fallback if the speculative names were requested by `list()`.
- No visual's data or values change; only how those two DocTypes are fetched. All prior fixes (lazy-load, tab-nav, click-to-render, consistent C5 chart rendering, friendly readiness, merged Sources/Data Quality tab, visual reduction) verified intact — both sections render with no console errors.

## v1.9.7-blank-guard-defer (2026-07-20)

- Fixed visuals showing **"Visual could not be rendered — The diagram area remained blank after the section finished loading."** Investigation found this was **not** a data/DocType/permission problem and **not** related to the archived visuals. The background visual guard (`scanVisuals()` in `40-visual-navigation-runtime.js`) replaces any on-screen chart container that stays empty for 20s with that diagnostic — but since the click-to-render deferral work, chart containers are **intentionally empty until the user opens the Diagram view**. The guard had no awareness of deferral, so every un-clicked deferred chart that had been on-screen for 20s got false-flagged and destructively overwritten. Reproduced in-harness: 11 of 25 on-screen demo charts were wrongly replaced after 22s with zero user interaction.
- Added a `deferredUnrendered(node)` check that skips charts still awaiting their first render, using each architecture's own render flag: demo `[data-demo-card][data-live-card-rendered]`, Criterion 4 `[data-c4-expanded-card][data-c4-card-rendered]`, and a new `data-c5-deferred` marker set on Criterion 5 chart nodes when deferred and cleared when the user opens them. The guard still fires on **genuinely** blank charts once they have rendered (verified: a rendered-then-emptied chart is still caught), so real render failures are still surfaced — only the false positives on not-yet-opened cards are suppressed.

## v1.9.7-inline-labels (2026-07-20)

- Fixed the visual card/menu label layout. Titles, descriptions and the chart-type label used to stack awkwardly (title on one line, "Gauges how many courses..." on the next, then "chart"), leaving orphaned whitespace. Now each visual reads **"Title — Description"** inline on the heading line, with the chart-type label (`chart`/`donut`/etc.) right-aligned on the same row. Applied consistently across the menu list and all three card architectures (demo `liveChartCardMarkup`, Criterion 4 `c4ExpandedChartMarkup`, Criterion 5 `ensureCardDescription`).
- The description moved from a separate `<p class="ucc-card-description">` into an inline `<span class="ucc-card-desc-inline">` appended to the `<h2>`; menu entries carry the description inline in `.ucc-visual-menu-desc` next to the title. Panel-head alignment switched to `flex-start` so the type/toggle stays on the heading's baseline.
- Correctness fix: `renderLiveChartCard` rebuilt the demo card heading with `heading.textContent = chart.title` on every render, which wiped the inline description span. It now sets `heading.innerHTML` to the title plus the inline description span, so the description survives click-to-render. Verified in-harness: the inline span persists after diagram render with the toggle on the same row and no console errors.

## v1.9.7-strip-archived (2026-07-20)

- Physically removed the 415 archived (disabled) visual definitions from the live build so `custom-html-block/JAVASCRIPT.js` is actually smaller: **520,744 -> 453,614 bytes (-67 KB, ~13%)**. Step #4 had only flagged them `enabled:false`, so their full definitions still shipped.
- Removed 299 entries from `LIVE_VISUAL_EXPANSION`, 54 from `C4_VISUAL_EXPANSION`, and 62 disabled entries from `C5_VISUAL_DESCRIPTIONS`. The full definitions are preserved in a new **`custom-html-block/archive/JAVASCRIPT_archived_v1.9.7.js`** (not loaded by the block) with per-criterion structure and restore instructions, cross-referencing `documentation/archived-visuals.md`.
- Critical correctness detail: the demo (`metricRows`) and Criterion 4 (`c4ExpandedRows`) renderers window into the API metrics by each visual's **array index**, so deleting entries would have shifted the kept visuals' indices and changed their displayed data. To prevent that, each kept entry now carries its original index as an `i` field, and the two render call sites use `chart.i` instead of the array position. Verified against the pre-change build: **0 of 180 kept visuals had an index mismatch** — every active visual's metric window is byte-identical.
- Criterion 5's archived visuals are static HTML cards (still in `HTML.html`, hidden via `C5_DISABLED_VISUALS`); only their now-unused JS descriptions were removed. Active counts unchanged (30/30/30/30/32/30/30); click-to-render, drill-downs, alphabetical sort, menu descriptions and all prior fixes re-verified, no console errors.

## v1.9.7-parallel-hydration (2026-07-20)

- Sped up Criterion 5's section loading (the "~186 steps" slow load). Investigation found the step explosion was **not** related to the archived visuals: Criteria 1/2/3/6/7 and Criterion 4 make one Server Script call per section that serves every visual (so archiving cards removed zero calls), and Criterion 5 loads data per section-source, not per-visual. The real cost was Criterion 5's per-record document hydration: 10 of its 20 DocTypes are `full:true`, and `load()`/`loadC511Source()`/`hydrateDocuments()` fetched each record with a **sequential** `await doc()` in a loop (up to 500/300 records), so a data-rich section became ~186 one-at-a-time round-trips.
- Added a bounded-concurrency `mapLimit(items, limit, fn)` helper and converted all three hydration loops to run in **batches of 8 in parallel**, preserving order and the same per-record error fallback. Exactly the same records/fields are loaded (no data or mapping change) - they now load 8-concurrent instead of one-at-a-time. Verified: identical call structure, max in-flight requests rose from 1 to 8, and the per-record progress steps (the visible "186") collapse to one update per source.
- No active visual behaviour changed; reduction counts (30/30/30/30/32/30/30) and the Criterion 5 chart-consistency work remain intact.

## v1.9.7-merge-sources-quality (2026-07-20)

- Consolidated each dashboard's separate "Data Quality" and "Sources" tabs into a single "Sources & Data Quality" tab, so source and data-quality information lives together in one place instead of being scattered across two tabs. A shared `window.__uccMergeSourcesQuality(dash, tabAttr, panelAttr)` helper moves the Data Quality panel's content into the Sources panel and removes the Data Quality tab button; it is applied uniformly across all three dashboard architectures (Criteria 1/2/3/6/7 `data-demo-tab`, Criterion 4 `data-c4-tab`, Criterion 5 `data-tab`).
- Criterion 5's standalone "Source Availability" widget (the live source-status panel that used to sit in the Overview) is now moved into the consolidated Sources & Data Quality tab, alongside the Source Registry and Data Quality Checks tables.
- Suppressed the visual-count badge on tabs with zero catalogue visuals (previously the Sources/Data Quality tabs showed a stray "0" chip), so the merged tab reads cleanly as "Sources & Data Quality".
- No data, drill-downs, or prior fixes changed; tab navigation, the reduction, chart consistency, and the readiness banners were all re-verified intact. The demo criteria's Overview "Live Source Availability" catalogue chart was left in place (it is part of the curated ~30-visual set); the Sources & Data Quality tab is the consolidated home for the source registry and data-quality detail.

## v1.9.7-friendly-readiness (2026-07-20)

- Fixed Criterion 5's readiness banner, which never appeared: the `status()` helper called `set("[data-status]", message)`, and because the readiness notice carries a `data-status` attribute (used for styling), that selector matched the notice and overwrote its inner title/copy/"View readiness" markup with a plain "section loaded" string on every status update. `setC5Notice()` already fully owns the notice, so the `set("[data-status]", ...)` call was both redundant and destructive; removed it. Criterion 5 now shows the same sources-available / metrics-available readiness indicator as the other criteria.
- Reworded every criterion's readiness banner to friendly, code-free text and removed the raw policy-code strings. Previously Criteria 1-4/6/7 showed e.g. "PPD-OEE-HR-2.1.1 v2.2 · 11/11 sources available · 15/16 metrics available" and Criterion 5 showed "... Policy code not configured ...". All now read "Live data connected · X of Y sources available · A of B metrics available" (with "· N item(s) need review" appended when there are gaps, and "with limitations" in the title). Also removed the policy code/version from the demo readiness modal, the Criterion 4 policy badge, and the Criterion 5 readiness dialog. Since the policy codes will change over time, they are no longer surfaced in any banner or readiness view.
- Note: the seven policy-reference chips shown in Criteria 3 and 6 section headings (e.g. a small "PPD-SES-SL-3.1.1 v1.2" pill next to a subcriterion title) are a separate, deliberate policy-reference UI in the static HTML and were left unchanged; only the readiness banners/indicators were reworded.

## v1.9.7-consistent-charts (2026-07-20)

- Made Criterion 5's charts render with the same visual components as Criteria 1-4/6/7. Criterion 5 was the only dashboard drawing charts as D3 SVG (vertical bars with rotated axis ticks, SVG donut/funnel), while every other criterion uses lightweight CSS `ucc-demo-*` components (horizontal bars, conic-gradient donut, CSS funnel). Converted Criterion 5's `bar`, `line`, `donutChart`, `funnelChart`, `radarChart` and `heatmapChart` to emit the same `ucc-demo-bars` / `ucc-demo-donut-layout` / `ucc-demo-funnel` / `ucc-demo-trend` / `ucc-demo-radar` / `ucc-demo-matrix` markup (styled by the shared rules already in `platform.css`), so all seven criteria now look identical. The multi-column evidence heatmap is now shown as the shared matrix component (per-record completion `done/total` with intensity), matching how the other criteria render "matrix" visuals. No underlying data, drill-downs, tables, or the click-to-render/deferral behaviour changed - only the diagram appearance. The exotic types only used by now-archived visuals (`bubbleChart`, `networkChart`, `radialBars`, `timelineChart`, `labelledBar`) were left as-is since no active visual uses them. Criterion 5 no longer depends on D3 for its active charts.

## v1.9.7-reduce (2026-07-20)

- Audit-focused visual reduction: trimmed each criterion to ~30 active visuals, keeping the highest-value visuals for EduTrust audit purposes (coverage / status / completion / readiness / evidence-completeness of each compliance area, mapped to live DocType data) and dropping redundant trend/profile/portfolio variations, near-duplicates, and low-signal or unconfirmed-source visuals. Active per-criterion counts: 30 / 30 / 30 / 30 / 32 / 30 / 30 (Criteria 1-7). Total: 627 -> 212 active, 415 archived.
- **Nothing was deleted.** Cut visuals in Criteria 1, 2, 3, 6, 7 (`LIVE_VISUAL_EXPANSION`) and Criterion 4 (`C4_VISUAL_EXPANSION`) carry `"enabled": false`; the render loop (`ensureLiveSectionCards`, `ensureC4ExpandedVisuals`) and the Explore/menu registry now skip them. Criterion 5's cut visuals (static HTML) are listed in a new `C5_DISABLED_VISUALS` set and hidden at init via the `ucc-visual-archived` class; `createEntry` skips them in Explore/menu. Every cut visual (name, type, subcriterion, reason) is recorded in the new `documentation/archived-visuals.md`, with restoration instructions.
- Updated the hard-locked counts to the new active totals: `tools/validate_package.py` `EXPECTED_VISUALS` (now counts only enabled visuals) and `VERSION.json` `diagram_counts` + `visual_targets`.
- No data mappings, chart types, or prior fixes changed (lazy-load, click-to-render, descriptions, alphabetical sort, tab-nav, stuck-menu all verified intact). Kept cards still render exactly as before; only the disabled ones no longer appear.

## v1.9.6-cardrefactor-c5 (2026-07-20)

- Extended the visual card refactor to Criterion 5 (batch 7 of 7, final batch), completing all 627 visuals across all 7 criteria. Criterion 5 is architecturally the most different of the three: its ~94 visuals are static HTML (no JSON definitions existed for it at all — built one from scratch, `C5_VISUAL_DESCRIPTIONS`), and each chart is drawn by its own individually hand-written call to one of 12 chart-type functions (`bar`, `line`, `radarChart`, `heatmapChart`, `networkChart`, `donutChart`, `bubbleChart`, `funnelChart`, `radialBars`, `timelineChart`, `labelledBar`, `chartAndTable`) scattered through ~2,400 lines, rather than one shared render pipeline.
- Investigated first (per the standing rule) before writing any deferral code: found that 77 of Criterion 5's 94 cards already have a Diagram/Table toggle statically pre-built in `platform.html` (from earlier UI standardisation work), while the remaining 17 get theirs built reactively by `ensureChartCompanion` the first time their chart function runs. Click-to-render needed to work identically for both.
- Added a generic `deferredChartCall(realFn, name, args)` wrapper and reassigned each of the 12 chart-type functions to route through it (`bar = function(n,rows){ deferredChartCall(__c5Bar, n, [rows]); }`, etc.) — this intercepts every one of the ~94 call sites for free, with no changes needed at the call sites themselves. On first call for a chart, it builds that card's toggle (if not already static) and description via `ensureCardDescription`, without drawing the chart; the real draw is deferred until the user clicks Diagram or Table, then cached, then rebuilt with fresh data if the card is re-prepared later (e.g. a filter change) so it never goes stale after being viewed once.
- Rewrote `ensureChartCompanion` to support being called a second time (previously it silently no-opped on repeat calls, meaning a chart whose data refreshed after being built once would show a stale table forever — fixed as part of enabling the deferred re-render, described in code comments as a general correctness improvement, not scope creep).
- `empty("learning-support", ...)` (a permanent "no source available" placeholder, not a real chart) was left out of the deferral — nothing to defer — but still gets its description added directly.
- Exposed the new description table as `window.UCCC5VisualDescriptions` and wired it into the Explore registry's `createEntry` for `kind: "c5"`, so the visual navigation menu and Explore workspace list show Criterion 5's descriptions too, matching the other six criteria.

Verified exhaustively in the harness (this was the highest-risk batch): all 94 chart nodes stay empty until clicked (confirmed for both statically pre-built and dynamically built cards); clicking Diagram or Table renders correctly — proven via the populated table content, since the mocked D3 proxy used for testing doesn't produce real SVG output, but the same deferred call also populates the table with real computed data, which does; repeat clicks don't re-render (cache verified via identical content across a Table→Diagram→Table cycle); the drill-through table (`chartAndTable`'s separate `tbody()` population) works correctly after a deferred render; the menu and Explore workspace list show all descriptions, still sorted alphabetically; Criteria 1 and 4 (different code paths) are unaffected. Along the way, fixed a pre-existing gap in the local test harness mock (it didn't handle the `frappe.client.get_list` calling convention Criterion 5 uses, unlike the Server-Script-style calls the other criteria use) — a test-infrastructure fix only, not part of the shipped code.

## v1.9.6-cardrefactor-c4 (2026-07-20)

- Extended the visual card refactor to Criterion 4 (batch 6 of 7), its own separate card-building path (`C4_VISUAL_EXPANSION`, `ensureC4ExpandedVisuals`, `c4ExpandedChartMarkup` in `10-platform-runtime.js`, distinct from the CONFIG-driven demo-kind criteria's code). Added real one-sentence descriptions for all 84 of Criterion 4's visuals.
- `c4ExpandedChartMarkup`: new layout matching the demo-kind cards — title and Diagram/Table toggle share one row (`.ucc-c4-dashboard .panel-head` was already flex/space-between, so no new CSS was needed), the description replaces the old "Live Criterion 4 API metrics..." sentence below that row.
- Click-to-render: `ensureC4ExpandedVisuals` now only stashes each card's pending data (chart, its original array index, and the API result) and binds the Diagram/Table toggle; the actual chart draw and table population moved to a new `renderC4ExpandedCardNow`, invoked on first click and cached via `data-c4-card-rendered`. Crucially, each visual's original index into `C4_VISUAL_EXPANSION[tab]` — not its sorted display position — is preserved for `c4ExpandedRows(result, index)`, so the specific metrics window each visual has always shown is unchanged; only when it draws changed.
- Added `description` to Criterion 4's entries in the Explore registry (`20-explore-runtime.js`), so the visual navigation menu and Explore workspace list show its descriptions too.

Verified in the harness across all 7 Criterion 4 sections (c411, c421, c422, c431, c441, c451, c461): every card shows its real description in the new layout, charts stay empty until clicked then render correctly and don't re-render on repeat clicks, card order stays alphabetical, the "View underlying records" drill button still opens the records dialog after a card renders, and the menu shows all 12 descriptions for the sampled section. Confirmed Criterion 1 (a different code path) is unaffected.

## v1.9.6-cardrefactor-c7 (2026-07-20)

- Added real one-sentence descriptions for Criterion 7's 80 visuals (batch 5 of 7) to `LIVE_VISUAL_EXPANSION`, replacing the generic fallback sentence. No code changes this batch — Criterion 7 shares the same shared card-building function, click-to-render, layout, and menu/Explore description display already shipped for Criteria 1, 2, 3 and 6. This completes all five CONFIG-driven demo-kind criteria (1, 2, 3, 6, 7); Criterion 4 and Criterion 5 remain, each on their own separate card-building code path.

## v1.9.6-cardrefactor-c6 (2026-07-20)

- Added real one-sentence descriptions for Criterion 6's 96 visuals (batch 4 of 7) to `LIVE_VISUAL_EXPANSION`, replacing the generic fallback sentence. No code changes this batch — Criterion 6 shares the same shared card-building function, click-to-render, layout, and menu/Explore description display already shipped for Criteria 1, 2 and 3.

## v1.9.6-cardrefactor-c3 (2026-07-20)

- Added real one-sentence descriptions for Criterion 3's 90 visuals (batch 3 of 7) to `LIVE_VISUAL_EXPANSION`, replacing the generic fallback sentence. No code changes this batch — Criterion 3 shares the same shared card-building function, click-to-render, layout, and menu/Explore description display already shipped for Criteria 1 and 2.

## v1.9.6-cardrefactor-c2 (2026-07-20)

- Added real one-sentence descriptions for Criterion 2's 99 visuals (batch 2 of 7) to `LIVE_VISUAL_EXPANSION`, replacing the generic fallback sentence introduced in v1.9.6-cardrefactor-c1's shared card-building refactor. No code changes this batch — the shared function, click-to-render, layout and menu/Explore description display already cover Criterion 2 automatically since it shares the same code path as Criterion 1.

## v1.9.6-cardrefactor-c1 (2026-07-20)

- Refactored visual cards onto a shared card-building function and a per-visual `description` field (batch 1 of 7 — Criterion 1 complete; Criteria 2, 3, 4, 5, 6 and 7 follow in later batches). Each visual definition in `LIVE_VISUAL_EXPANSION` (`30-live-foundation-runtime.js`) now carries a short one-sentence description alongside its existing name and chart type.
- New card layout: title and the Diagram/Table toggle now share one row (`liveChartCardMarkup`'s `.panel-head` holds both directly, matching its existing flex/space-between rule instead of the old stacked layout); the old generic "Permission-aware live metrics..." sentence is replaced by the visual's own description below that row (falls back to the old sentence for visuals not yet described).
- Click-to-render: chart cards no longer draw their chart/table immediately when a section loads. `renderLiveChartCard` now only stashes the pending data and updates the card heading; the actual draw happens in the new `renderLiveChartCardNow`, triggered the first time a card's Diagram or Table button is clicked, then cached (`data-live-card-rendered`) so repeat clicks don't redraw. This is a separate, finer-grained layer on top of the existing per-section lazy build (`ensureLiveSectionCards`) — that still controls which section's cards exist in the DOM at all; this controls whether an existing card's chart has been drawn yet.
- The visual navigation menu and the Explore workspace list now show each visual's description alongside its name and chart type, using the same description data.
- Verified: chart/table stays empty until first click, then renders and doesn't re-render on repeat clicks of the same card; menu-driven "open this visual" navigation still finds and renders the correct card; alphabetical sort order (shipped in v1.9.6-cardsort) is unaffected; Criteria without descriptions yet still render correctly with the fallback sentence.

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
