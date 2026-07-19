# Criterion 6 — Quality Assurance, Innovation and Continual Improvement

## Purpose

This folder preserves the supplied Criterion 6 DocType information for future:

- live analytics;
- source and metric readiness;
- internal-audit and corrective-action reporting;
- management-review reporting;
- innovation and continual-improvement reporting;
- provider evaluation;
- risk and mitigation reporting;
- impact analysis and developer onboarding.

## Current status

Criterion 6 is connected to a **permission-aware live API foundation**.

The package includes and actively uses `ucc_analytics_criterion_6`.

The supplied metadata is sufficient to begin source modelling for:

- Quality Action;
- Quality Action Resolution;
- Management Review;
- Operational Outcomes Cost Time Saving.

Confirmed sources are live. Metrics requiring missing child tables or business rules remain explicitly unsupported.

## Confirmed supplied sources

1. Quality Action Resolution
2. Management Review
3. Operational Outcomes Cost Time Saving
4. Quality Action custom-field export

The Quality Action target is strongly indicated by the CSV field names and
linked child table `Quality Action Resolution`; the raw export does not include
a top-level DocType-name header, so this relationship is recorded explicitly.

## Existing cross-criterion source

`Provider Rating`, documented under Criterion 3, can also support Criterion
6.4 provider evaluation. Reuse that source inventory rather than creating a
duplicate definition.

## Documentation

- `DOCTYPE_INVENTORY.md`
- `QUALITY_ACTION_FIELD_REFERENCE.md`
- `QUALITY_ACTION_RESOLUTION_FIELD_REFERENCE.md`
- `MANAGEMENT_REVIEW_FIELD_REFERENCE.md`
- `OPERATIONAL_OUTCOMES_FIELD_REFERENCE.md`
- `ANALYTICS_MAPPING.md`
- `CURRENT_LIVE_MAPPING.md`
- `SECURITY_AND_PRIVACY.md`
- `OPEN_ITEMS.md`
- `SUPPLIED_DOCTYPE_DEFINITIONS.md`
- `source-material/`
- `REVISION.json`

## Evidence labels

- **Confirmed** — directly supplied in the DocType definition or CSV.
- **Cross-criterion confirmed** — previously supplied and documented elsewhere.
- **Inferred** — a relationship inferred from linked fields or labels.
- **Unknown** — insufficient metadata; do not implement by guessing.
## Provider Rating technical resolution

The live API resolves the provider-evaluation source using `Provider Rating`
first and `Supplier Rating` as the approved ERPNext technical fallback. The
response returns the actual resolved DocType used for list links and metrics.

