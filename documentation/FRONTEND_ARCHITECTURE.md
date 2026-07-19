# v1.8.7 Current-State Notice

Criteria 1–7 now use live data paths. Criteria 1, 2, 3, 6 and 7 use
permission-aware live foundations; Criterion 4 is mature live; Criterion 5 keeps
its validated live frontend. Any older preview discussion below is retained only
as historical design context and is not the active runtime.

## v1.8.4 update

- One Criterion 5-derived shared visual framework is applied to all criterion dashboards.
- View tools is a shared explicit popover, not a native `<details>` element.
- Criterion 4 renders 24 live diagrams from its existing metric registry.
- Criterion 3 and Criterion 6 use policy-aligned dummy previews.
- Policy and diagram mappings are recorded in `reference/policy-runtime-registry.json`.

# Frontend Architecture — v1.7.0

## Actual deployed refactor

Unlike v1.6.0, this release changes the deployable files.

Shared runtime functionality now exists once:

- CSV cell formatting
- table-to-CSV conversion
- browser download handling
- canonical DocType route creation
- DocType list opening
- HTML escaping
- local-storage reads and writes

Criterion-specific code keeps its existing names where required, but delegates
to `window.UCCShared`.

The deployment files are built from:

- `src/html/platform.html`
- `src/css/platform.css`
- `src/js/00-shared-runtime.js`
- `src/js/10-platform-runtime.js`

Run:

```bash
python tools/build_custom_block.py
```

## Size change

| File | Before | After | Reduction |
|---|---:|---:|---:|
| HTML | 155,901 | 139,957 | 15,944 |
| CSS | 134,191 | 116,897 | 17,294 |
| JavaScript | 314,045 | 315,535 | -1,490 |

## Future rule

New Criteria 1–7 must use `UCCShared` and the shared criterion CSS. New
criterion-specific copies of exports, downloads, source routing, dialogs,
Diagram/Table controllers or D3 loaders are not permitted.
