# Criterion 4 Policy and API Contract

## Policy registry

| Subcriterion | Title | Policy code | Version |
| --- | --- | --- | --- |
| 4.1.1 | Pre-Course Counselling, Selection and Admissions | PPD-SSO-AD-4.1.1 | 2.2 |
| 4.2.1 | Student Contract | PPD-SSO-AD-4.2.1 | 2.2 |
| 4.2.2 | Fee Collection and Fee Protection Scheme | PPD-SSO-AD-4.2.2 | 2.3 |
| 4.3.1 | Course Transfer, Deferment and Withdrawal | PPD-SSO-SS-4.3.1 | 2.2 |
| 4.4.1 | Refund | PPD-SSO-SS-4.4.1 | 2.2 |
| 4.5.1 | Student Support Services | PPD-SSO-SS-4.5.1 | 2.3 |
| 4.6.1 | Student Conduct and Attendance | PPD-SSO-SS-4.6.1 | 2.2 |

## Request

```json
{
  "payload": {
    "action": "summary",
    "subcriterion": "4.6.1",
    "filters": {},
    "metric_id": null,
    "page": 1,
    "page_size": 50
  }
}
```

## Response groups

```text
meta
policy
filters
sources
metrics
questions
exceptions
data_quality
source_summary
metric_summary
data
warnings
```

## Readiness meaning

A source is available only when:

1. an approved candidate DocType resolves;
2. the current user has read permission;
3. the query succeeds.

A metric is available only when:

1. its source is available;
2. an approved candidate field resolves;
3. all required fields resolve;
4. the calculation can run.

A readable source containing zero matching records remains **available**.

## Drill-down

`action = "drilldown"` requires a valid `metric_id`. The API returns paginated
matched rows for that metric. Page size is restricted to 1–200.

## Status values

- `available`
- `permission_denied`
- `unavailable`
- `unsupported_field`
- `error`
