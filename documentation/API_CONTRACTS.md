# API Contracts — v1.8.7

## General controls

- Signed-in users only.
- `Allow Guest` disabled.
- Frappe DocType permissions enforced.
- Approved source and field allow-lists.
- Page size limited to 200.
- Zero-row readable sources remain available.
- Sensitive fields and unrestricted attachments are excluded.

## Shared live-foundation contract

Criteria 1, 2, 3, 4, 6 and 7 support:

```text
summary
source_status
policy_registry
drilldown
```

Common request:

```json
{
  "payload": {
    "action": "summary",
    "subcriterion": "1.1.1",
    "filters": {}
  }
}
```

Common response groups:

```text
ok
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
warnings
```

## Methods

| Method | Status |
|---|---|
| `ucc_analytics_bootstrap` | Ready |
| `ucc_analytics_criterion_catalogue` | Ready |
| `ucc_analytics_criterion_1` | Live foundation |
| `ucc_analytics_criterion_2` | Live foundation |
| `ucc_analytics_criterion_3` | Live foundation |
| `ucc_analytics_criterion_4` | Mature live |
| `ucc_analytics_criterion_5` | Migration API; validated frontend remains live |
| `ucc_analytics_criterion_6` | Live foundation |
| `ucc_analytics_criterion_7` | Live foundation |
| `ucc_analytics_placeholder_preview` | Legacy; not used by active dashboards |

## Criterion 1 sections

- 1.1.1 Leadership and Corporate Governance
- 1.2.1 Strategic Planning

## Criterion 2 sections

- 2.1.1 Staff Selection and Management
- 2.1.2 Staff Training and Development
- 2.2.1 Internal and External Communication
- 2.3.1 Data and Information Management
- 2.3.2 Knowledge Management
- 2.4.1 Feedback Management
- 2.4.2 Student Satisfaction Survey
- 2.4.3 Staff Satisfaction Survey

## Criterion 3 sections

- 3.1.1 Selection and Appointment of External Recruitment Agents
- 3.2.1 Management and Evaluation of Recruitment Agents

## Criterion 4 sections

- 4.1.1 through 4.6.1 as defined in its policy registry.

## Criterion 5

The existing validated direct-client calculation path remains active. Its Server
Script is still a staged migration foundation and must not be described as full
calculation ownership.

## Criterion 6 sections

- 6.1.1 Internal Assessment and Quality Audits
- 6.2.1 Management Review
- 6.3.1 Innovation and Continual Improvement
- 6.4.1 Provider Accreditation and Evaluation
- 6.5.3 Hazard Identification and Risk Assessment

## Criterion 7 sections

- 7.1.1 Measurement of Outcomes

No active 7.2 contract is included.

## Ask UCC

```text
ucc_ask_student_journey
ucc_ask_recruitment_agent
ucc_ask_quality_action
```

Existing request formats remain unchanged.
