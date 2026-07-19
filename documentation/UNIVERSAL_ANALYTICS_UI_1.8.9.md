# Universal Analytics UI — v1.8.9

## Scope

This release applies one interaction contract to Criteria 1–7 without replacing
their approved calculation engines.

## Criterion switching

When the dashboard selector changes:

1. the selected dashboard is made visible;
2. the dashboard hero is scrolled into view;
3. the dashboard-change event starts its live loader;
4. the loading card and readiness state are therefore visible at the top.

The runtime uses `scrollIntoView` and also handles a scrollable Frappe ancestor.

## Navigation contract

All of these menus are single-row, horizontally scrollable controls:

- criterion main tabs;
- Criterion 4 tabs;
- Criterion 5 parent tabs;
- Criterion 5 child tabs;
- Criterion 5 local section tabs;
- generated live-foundation tabs.

Criterion 5 child navigation is persistent:

```text
5.1 Overview | 5.1.1 Course Design & Development | 5.1.2 Course Review
5.2 Overview | 5.2.1 Course Planning | 5.2.2 Course Delivery
5.3 Overview | 5.3.1 Partnerships
```

## Management Questions contract

All tables use:

```text
Criterion | Question | Answer | Source / Calculation | Status
```

### Answer action

A readable live metric provides:

```text
View N matching records
```

This performs the API `drilldown` action where available. Criterion 5 uses its
validated in-memory record set or opens the resolved source list when no
in-memory record array exists.

### Source action

A resolved source provides:

```text
Open <DocType display name> list
```

The link uses the technical DocType returned by the API. Display aliases are
limited to known UCC terminology.

## Extended questions

For Criteria 1, 2, 3, 4, 6 and 7, any readable metric not already linked to a
curated management question receives a generated question:

```text
What is the current <metric label>?
```

The answer and source are derived from the live API result. No value is
invented.

Criterion 5 retains its existing extensive curated question catalogue.

## Visual inventories

| Criterion | Active visual target |
|---|---:|
| 1 | 18 |
| 2 | 30 |
| 3 | 20 |
| 4 | 24 |
| 5 | 94 |
| 6 | 36 |
| 7 | 12 |

New live-foundation visuals use only returned metric, readiness and exception
values. Supported forms include:

- bar;
- donut;
- funnel;
- lifecycle;
- matrix;
- radar;
- gauge;
- risk matrix;
- trend profile.

Each generated visual provides Diagram/Table switching and record drill-down.

## Provider Rating resolution

Criteria 3 and 6 use:

```python
"provider_rating": ["Provider Rating", "Supplier Rating"]
```

This supports sites where the UCC display/business term is Provider Rating but
the installed ERPNext technical DocType is Supplier Rating. The API response
contains the source actually resolved.
