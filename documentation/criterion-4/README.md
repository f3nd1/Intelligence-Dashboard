# Criterion 4 — Student Protection and Support Services

## Purpose

This folder documents the live Criterion 4 implementation so future developers,
analysts and auditors can understand:

- which policies and subcriteria are represented;
- which DocTypes and fields are used;
- how source and metric readiness is calculated;
- how questions, exceptions and drill-downs are produced;
- which diagrams are available;
- which mappings are confirmed, inferred or still unresolved.

## Current status

Criterion 4 is a **live permission-aware dashboard**.

```text
API method: ucc_analytics_criterion_4
Allow Guest: disabled
```

The Server Script resolves approved candidate DocTypes and fields against live
Frappe metadata. It does not treat a translated label as a technical DocType
name.

## Supported actions

- `summary`
- `source_status`
- `policy_registry`
- `drilldown`

## Documentation in this folder

- `POLICY_AND_API_CONTRACT.md`
- `DOCTYPE_INVENTORY.md`
- `FIELD_REFERENCE.md`
- `ANALYTICS_MAPPING.md`
- `VISUAL_INVENTORY.md`
- `SECURITY_AND_PRIVACY.md`
- `OPEN_ITEMS.md`
- `RUNTIME_CONFIG_REFERENCE.md`
- `REVISION.json`

## Evidence labels

- **Confirmed** — directly present in the active Server Script, source registry
  or repository-reviewed mapping.
- **Runtime confirmed** — resolved from the target site or recorded as a
  live-confirmed site customisation.
- **Candidate** — approved alternate source or field name resolved at runtime.
- **Unknown** — insufficient evidence; do not implement by guessing.
