# Criterion 4 Security and Privacy

## Permission model

- `Allow Guest` must remain disabled.
- Every source requires current-user read permission.
- Child-table records are read only after parent permission is confirmed.
- Permission errors remain distinct from empty result sets.

## Sensitive data

Criterion 4 may contain:

- NRIC, FIN or passport numbers;
- student names;
- email and phone numbers;
- contracts and signatures;
- invoices and payment data;
- counselling, wellness and conduct information;
- attendance and leave information.

## Dashboard rules

- Prefer aggregate counts and status distributions.
- Drill-downs must expose only approved fields.
- Do not return signatures, identity documents or attachment payloads.
- Avoid including free-text counselling or wellness notes in exports.
- Do not log full API rows in browser diagnostics.
- Preserve Frappe row-level and DocType-level permissions.

## Zero-value rule

A valid zero is not missing data. For example:

```text
Open refunds = 0
Metric status = available
```
