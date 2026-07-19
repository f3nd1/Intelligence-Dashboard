# Criterion 1 API Contract

```text
Visible name: UCC Analytics - Criterion 1
API method: ucc_analytics_criterion_1
Allow Guest: No
```

Actions:

- `summary`
- `source_status`
- `policy_registry`
- `drilldown`

Supported subcriteria:

- `1.1.1`
- `1.2.1`

The response follows the Criterion 4 readiness structure:

```text
policy
source_summary
metric_summary
sources
metrics
questions
exceptions
data_quality
```
