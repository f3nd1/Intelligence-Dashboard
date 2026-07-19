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

## Criterion catalogue placeholder

`UCC Analytics - Criterion Catalogue.py` is a self-contained API Server Script for the approved Criterion 1–7 catalogue. It does not query operational DocTypes.

# Server Script Structure

## Installed scripts

```text
server-scripts/
├── UCC Analytics - Bootstrap.py
├── UCC Analytics - Criterion 5.py
├── UCC Analytics - Drilldown.py
├── UCC Shared - Record Search.py
├── UCC Shared - Diagnostics.py
├── UCC Ask - Student Journey.py
├── UCC Ask - Recruitment Agent.py
└── UCC Ask - Quality Action.py
```

## Naming standard

Visible name:

```text
UCC Analytics - <Dashboard or Function>
UCC Ask - <Domain>
UCC Shared - <Function>
```

API method:

```text
ucc_analytics_<name>
ucc_ask_<domain>
ucc_shared_<function>
```

Examples:

```text
UCC Ask - Student Journey
→ ucc_ask_student_journey

UCC Analytics - Criterion 5
→ ucc_analytics_criterion_5
```

## Script independence

Each Server Script is self-contained because Server Scripts are not a normal Python package.

Do not assume this works:

```python
from ucc_shared import helper
```

Common patterns may need to be copied from an approved template.

## Required header

Each script should state:

- visible Server Script name;
- script type;
- API method;
- purpose;
- deployment rule;
- implementation status.

## Current statuses

- Ask UCC scripts: full current implementations.
- Bootstrap: usable.
- Drilldown: usable for approved datasets.
- Shared Record Search: usable but not yet required by the current assistant UI.
- Shared Diagnostics: usable.
- Criterion 5: migration foundation, not complete parity.
