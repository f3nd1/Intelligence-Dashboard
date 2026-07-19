# Frappe Server Scripts - UCC Intelligence Platform v1.9.5

Deploy the scripts as API Server Scripts with Allow Guest disabled.

## Confirmed mapping updates

- Criterion 1: Staff Goal analytics use `Goal`.
- Criterion 2: training needs use `Training Needs Analysis`; material approval uses `Material Vetting Form`.
- Criteria 3 and 6: `Provider Rating` is primary; `Supplier Rating` is an approved fallback.
- Shared Diagnostics: criterion reports no longer include unrelated shared-source duplicates.

Obsolete Criterion 2 source aliases are not probed.
