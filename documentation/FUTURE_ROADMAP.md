## Placeholder implementation sequence

For each placeholder criterion, confirm the business owner, source DocTypes, fields, calculations, evidence, exceptions and drill-down rules before converting the placeholder to a live dashboard.

# Future Roadmap

## Phase 1 — Consolidation baseline

Completed in v1.0.0:

- one UCC frontend;
- Analytics Hub;
- Ask UCC;
- official UCC design;
- three active Ask modules;
- Criterion 5 preserved;
- standard package and documentation.

## Phase 2 — Criterion 5 API parity

Migrate in this order:

1. bootstrap and common filters;
2. 5.1.1 summary;
3. proposals;
4. module design;
5. course review;
6. evidence gaps;
7. 5.1.2;
8. 5.2.1;
9. 5.2.2;
10. 5.3.1;
11. 5.4 and 5.5;
12. overview, data quality and sources.

For each step:

```text
implement API
→ compare live output
→ switch one frontend section
→ remove only duplicated logic
```

## Phase 3 — Shared context

Allow a selected Analytics record or filter context to open the matching Ask UCC module without sending entire datasets to AI.

## Phase 4 — New Criteria

Add Criteria 1–4 and 6–7 only after collecting:

- management questions;
- exact DocTypes and fields;
- formulas;
- status thresholds;
- record drill-down rules;
- permissions;
- test cases.

Use one API per criterion.

## Phase 5 — Future Ask UCC modules

Potential modules, excluding LMS and Helpdesk:

- Admissions
- Fees and Payments
- Academic Operations
- HR
- Finance
- Enquiries
- Orders
- Quality and Compliance

Do not create empty modules. Add one when its user journey and data mapping are confirmed.

## Phase 6 — Reassess platform boundary

Request custom-app access if Server Script limitations begin to block testing, reuse, scheduled processing or performance.
