# v1.8.7 Current-State Notice

Criteria 1–7 now use live data paths. Criteria 1, 2, 3, 6 and 7 use
permission-aware live foundations; Criterion 4 is mature live; Criterion 5 keeps
its validated live frontend. Any older preview discussion below is retained only
as historical design context and is not the active runtime.

# Architecture — v1.8.4

## Deployment model

```text
ONE ZIP PACKAGE
│
├── Custom HTML Block
│   ├── HTML.html
│   ├── CSS.css
│   └── JAVASCRIPT.js
│
├── Independent Frappe API Server Scripts
│   ├── analytics
│   ├── Ask UCC
│   └── shared utilities
│
└── documentation and registries
```

## Runtime workspaces

```text
UCC Intelligence Platform
├── Analytics
│   ├── Criterion 1 — dummy preview
│   ├── Criterion 2 — dummy preview
│   ├── Criterion 3 — policy-grounded dummy preview
│   ├── Criterion 4 — live
│   ├── Criterion 5 — live
│   ├── Criterion 6 — policy-grounded dummy preview
│   └── Criterion 7 — dummy preview
├── Explore
│   └── opens the original live or preview visual card
└── Ask UCC
    ├── Student Journey
    ├── Recruitment Agent
    └── Quality Action
```

## Shared visual framework

Criterion 5 is the reference implementation. Criteria 1–7 reuse shared classes
and contracts for the hero, action card, filters, tabs, readiness, KPIs, panels
and View tools.

The View tools menu is an explicit JavaScript popover. The menu may be moved
to the document body while open to avoid clipping, but the dashboard shell
itself remains inside the Custom HTML Block.

## Data boundaries

- Criteria 4 and 5 are live and permission-aware.
- Criteria 1–3 and 6–7 are clearly labelled dummy previews.
- Criterion 4 diagrams share one metric registry.
- Criterion 5 remains in a hybrid migration state: existing frontend queries plus
  a section-by-section Python migration contract.
- Ask UCC uses separate deterministic Server Scripts.

## Build

`tools/build_custom_block.py` combines:

```text
src/html/platform.html
src/css/platform.css
src/js/00-shared-runtime.js
src/js/10-platform-runtime.js
src/js/30-live-foundation-runtime.js
src/js/20-explore-runtime.js
```

into the three files in both `custom-html-block/` and `dist/`.
