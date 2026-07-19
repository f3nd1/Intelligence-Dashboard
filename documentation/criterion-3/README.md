# Criterion 3 — Recruitment Agent Source Inventory

## Purpose

This folder preserves the UCC DocType information supplied for EduTrust
Criterion 3 so it can be reused for:

- live analytics;
- Ask UCC Recruitment Agent;
- source-readiness checks;
- record drill-downs;
- impact analysis;
- future reports and dashboards;
- onboarding of developers and analysts.

## Current status

The source inventory is **confirmed from supplied DocType definitions**.

Criterion 3 uses the permission-aware live API foundation
`ucc_analytics_criterion_3`. The dashboard is connected to this API and displays
unavailable or unsupported states instead of dummy values.

## Confirmed primary DocTypes

1. Agent
2. External Onboarding
3. External Offboarding
4. Provider Rating
5. Supplier Rating Assessment Childtable
6. Agent Claim Form
7. Agent Annual Performance Review
8. Agent Contract
9. Non Disclosure Agreement
10. Student Applicant — reuse the existing Criterion 4 source mapping

## Documentation in this folder

- `DOCTYPE_INVENTORY.md` — role of every supplied DocType
- `FIELD_REFERENCE.md` — confirmed fields needed for implementation
- `ANALYTICS_MAPPING.md` — Criterion 3.1 and 3.2 source-to-metric mapping
- `SECURITY_AND_PRIVACY.md` — fields that must not be exposed
- `OPEN_ITEMS.md` — referenced child tables and workflows still needing metadata
- `RAW_AGENT_DOCTYPE.md` — exact supplied Agent DocType reference

## Evidence labels

- **Confirmed** — directly supplied in the DocType definitions
- **Inferred** — business meaning inferred from labels or field relationships
- **Unknown** — insufficient metadata; do not implement by guessing
## Provider Rating technical resolution

The live API resolves the provider-evaluation source using `Provider Rating`
first and `Supplier Rating` as the approved ERPNext technical fallback. The
response returns the actual resolved DocType used for list links and metrics.

