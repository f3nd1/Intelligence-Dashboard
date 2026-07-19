# v1.1.0 implementation notes

## Scope

This release expands the existing Criterion 5 subcriteria and adds a shared interaction layer to the single Custom HTML Block.

## Important behaviour

- Real calculations use currently loaded ERPNext fields.
- Missing or unsupported fields are shown explicitly.
- No placeholder number is presented as a real result.
- Room and Teacher clash detection compares sessions on the same date with overlapping start/end times.
- Planned versus delivered uses attendance linked to Course Schedule as delivery evidence.
- Changelog uses an in-page overlay because native `<dialog>` behaviour is inconsistent inside some Frappe Custom HTML Block contexts.

## Live verification still required

The ZIP passes static syntax and package checks. The following require testing on the UCC site:

- user permissions;
- exact custom field names;
- large dataset performance;
- real Frappe route behaviour;
- exported CSV content;
- copied filtered links after page refresh.
