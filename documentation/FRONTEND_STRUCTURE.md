# v1.8.7 Current-State Notice

Criteria 1–7 now use live data paths. Criteria 1, 2, 3, 6 and 7 use
permission-aware live foundations; Criterion 4 is mature live; Criterion 5 keeps
its validated live frontend. Any older preview discussion below is retained only
as historical design context and is not the active runtime.

# Frontend Structure — v1.8.4

## Deployed files

```text
custom-html-block/
├── HTML.html
├── CSS.css
└── JAVASCRIPT.js
```

## Logical structure

```text
#uccIntelligencePlatform
├── shared top navigation
│   ├── Analytics
│   ├── Explore
│   ├── Ask UCC
│   ├── criterion selector
│   └── manual minimise/expand arrow
├── Analytics workspace
│   └── seven criterion panels
├── Explore workspace
│   └── live and preview visual catalogue
└── Ask UCC workspace
    └── #ajaApp
```

## Shared criterion classes

- `.ucc-shared-hero`
- `.ucc-shared-action-card`
- `.ucc-shared-controls`
- `.ucc-shared-tabs`
- `.ucc-shared-panel`
- `.ucc-shared-kpis`

New criterion pages must use these contracts.

## View tools

Each action card contains:

```text
[data-ucc-tools-trigger]
[data-ucc-tools-menu]
[data-ucc-tool-action]
```

One shared JavaScript controller handles opening, positioning, closing and tool
actions. Native `<details>` elements are not used.

## JavaScript modules

```text
00-shared-runtime.js       shared utility functions
10-platform-runtime.js     shell, live C4/C5 and shared View tools
30-live-foundation-runtime.js  live foundation dashboards and renderers
20-explore-runtime.js      visual catalogue and navigation
```

## CSS safety

All component styling remains scoped beneath `.ucc-platform`, `.ucc-c5-v41`
or `.aja-app`. Do not add unscoped rules that can affect Frappe.
