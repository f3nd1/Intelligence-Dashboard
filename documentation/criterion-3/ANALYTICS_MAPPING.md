# Criterion 3 Analytics Mapping

## Business workflow

```text
Agent application
    ↓
Identification and screening
    ↓
Internal processing and approval
    ↓
Contract and NDA
    ↓
External onboarding
    ↓
Training and monitoring
    ↓
Annual performance review
    ↓
Renewal / continuation / hold / termination
    ↓
External offboarding
```

## Criterion 3.1 — Selection and Appointment

### Confirmed sources

| Source | Primary use |
|---|---|
| Agent | application, company, experience, documents, approval, selection ratings and risk |
| Provider Rating | identification-and-screening evaluation |
| Supplier Rating Assessment Childtable | weighted evaluation criteria |
| Agent Contract | first-time appointment, signatures, dates and NDA requirement |
| Non Disclosure Agreement | NDA approval, response and signature |
| External Onboarding | onboarding start, activities and signatures |
| Student Applicant | reuse Criterion 4 source mapping when applicant outcomes are required |

### Candidate live metrics

| Metric | Source and field logic | Confidence |
|---|---|---|
| Applications in scope | Agent count by application date/status | Confirmed |
| Application status distribution | Agent.`status` | Confirmed |
| Application evidence completeness | required Agent document and declaration fields | Inferred; business rule must be approved |
| Processing turnaround | Agent.`processed_date` − `custom_ra_application_form_date` | Confirmed fields; threshold unknown |
| Approval turnaround | Agent.`approved_date` − `custom_ra_application_form_date` | Confirmed fields; threshold unknown |
| Selection-rating completeness | nine Agent selection rating fields populated | Confirmed |
| Selection-rating average | average of supplied rating fields | Confirmed fields; aggregation rule must be approved |
| Identification-screening rating | Provider Rating where `evaluation_stage = Identification and Screening` | Confirmed |
| Risk assessment coverage | Agent.`risk_assessment` and `risk_management` child rows | Confirmed relationship; child fields unknown |
| Contract coverage | Agent with linked Agent Contract | Confirmed |
| Signed contract coverage | contract signatures/dates and submitted state | Confirmed fields; exact rule to approve |
| NDA-required population | Agent Contract.`requires_nda` | Confirmed |
| NDA completion | linked NDA status, signatures and dates | Confirmed |
| Onboarding coverage | External Onboarding linked by `agent_id` | Confirmed |
| Onboarding completion | activity completion and signature | Inferred; child fields unknown |

## Criterion 3.2 — Management and Evaluation

### Confirmed sources

| Source | Primary use |
|---|---|
| Agent | active status, training, monitoring, evaluation, student feedback, renewal and exit |
| Agent Annual Performance Review | yearly activity, survey, targets and internal review |
| Provider Rating | regular review, continuation, hold and termination |
| Agent Contract | renewal and expiry monitoring |
| Agent Claim Form | commissions and claim processing |
| External Offboarding | separation activity and signature |
| Student Applicant | applicant volumes and outcomes by Agent |

### Candidate live metrics

| Metric | Source and field logic | Confidence |
|---|---|---|
| Active agents | Agent.`status = Active` | Confirmed |
| Agents under review | Agent.`status = Under Review` | Confirmed |
| Suspended or terminated agents | Agent.`status` | Confirmed |
| Contract expiry window | Agent Contract.`end_date` | Confirmed |
| Renewal contract coverage | Agent Contract.`contract_type = Renewal` | Confirmed |
| Annual-review coverage | Agent Annual Performance Review by Agent and Academic Year | Confirmed |
| Average annual survey score | supplied survey rating fields | Confirmed fields; aggregation rule to approve |
| Training coverage | Agent.`training_log` | Confirmed relationship; child fields unknown |
| Consent/onboarding survey completion | Agent.`done_consent_and_onboarding_survey` | Confirmed |
| Monitoring coverage | Agent.`agent_monitoring_childtable` | Confirmed relationship; child fields unknown |
| Provider continuation outcome | Provider Rating status and evaluation stage | Confirmed |
| Recruitment target | Agent quarterly targets or annual review target rows | Confirmed |
| Applicant volume by agent | Student Applicant linked to Agent | Confirmed by existing mapping |
| Applicant conversion by agent | reuse the approved Criterion 4 applicant/admission outcome rules | Confirmed source; exact status rule reused |
| Claim amount and submission | Agent Claim Form totals and `docstatus` | Confirmed |
| Offboarding coverage | External Offboarding linked by Agent | Confirmed |
| Exit completeness | offboarding activities and signature | Inferred; child fields unknown |

## Implemented Criterion 3 API readiness contract

```json
{
  "policy": {
    "criterion": "3.1",
    "policy": "PPD-SES-SL-3.1.1",
    "version": "1.2"
  },
  "source_summary": {
    "available": 0,
    "total": 0,
    "issues": 0
  },
  "metric_summary": {
    "available": 0,
    "total": 0,
    "issues": 0
  },
  "sources": [],
  "metrics": [],
  "questions": [],
  "exceptions": []
}
```

A source is available only when the DocType exists, the current user has read
permission, required fields exist and the query succeeds.

A readable source with zero matching records remains **available**.

## Recommended joins

```text
Agent
├── Agent Contract
│   └── Non Disclosure Agreement
├── External Onboarding
├── External Offboarding
├── Provider Rating
│   └── Supplier Rating Assessment Childtable
├── Agent Annual Performance Review
├── Agent Claim Form
└── Student Applicant
```

### Join keys

- Agent Contract → Agent:
  `ac_agent_link_agent_contract`
- NDA → Agent Contract:
  `agent_contract`
- External Onboarding → Agent:
  `agent_id`
- External Offboarding → Agent:
  `agent_id`
- Agent Annual Performance Review → Agent:
  `agent_name`
- Provider Rating → Agent:
  Dynamic Link using `type = "Agent"` and `document = Agent.name`
- Student Applicant → Agent:
  reuse the existing Criterion 4 field mapping
- Agent Claim Form → Agent:
  supplied `agent` field is Data, not Link; verify stored value before joining

## Important unknowns

Do not invent calculations for:

- complaints and breach records;
- child-table completion fields;
- exact workflow-state logic;
- approval and renewal SLA thresholds;
- contract-signature completion rule;
- student-applicant conversion statuses;
- claim-to-invoice reconciliation.

These require live metadata or business-owner confirmation.
