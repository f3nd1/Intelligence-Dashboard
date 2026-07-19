# Criterion 6 Analytics Mapping

## Business flow

```text
Audit / review / feedback / risk / opportunity
    ↓
Quality Action
    ↓
Quality Action Resolution
    ↓
Implementation and evidence
    ↓
Performance indicators and QIPI
    ↓
Cost and time outcomes
    ↓
Management Review
    ↓
Verification and continual improvement
```

## 6.1.1 Internal Assessment and Quality Audits

### Available now

- Quality Action
- Quality Action Resolution
- Management Review audit-result and nonconformity tables

### Candidate metrics

- finding distribution: OBS, OFI, NC, Min. NC, Maj. NC;
- open and overdue resolutions;
- corrective versus preventive actions;
- ownership completeness;
- target-date completeness;
- resolution completion duration;
- closure verification;
- compliance-tracking coverage;
- evidence and sign-off coverage.

### Missing before live implementation

- Oversight Framework DocType;
- audit plan and audit schedule fields;
- auditor and auditee child tables;
- audit finding parent record;
- audit-method fields;
- exact audit-cycle completion rule.

## 6.2.1 Management Review

### Available now

- Management Review
- Quality Action
- Management Review Quality Action child table

### Candidate metrics

- reviews by status;
- scheduled versus completed reviews;
- review cadence;
- postponed reviews;
- next-review due and overdue;
- chairperson and minutes completeness;
- THESIS section completeness;
- audit-result coverage;
- provider-review coverage;
- risk/opportunity coverage;
- Quality Action ownership and closure;
- performance-outcome coverage.

## 6.3.1 Innovation and Continual Improvement

### Available now

- Quality Action
- Quality Action Resolution
- Operational Outcomes Cost Time Saving

### Candidate metrics

- innovation versus continual-improvement count;
- innovation type:
  Disruptive, Radical, Incremental, Architectural;
- innovation category:
  Architectural, Business Model, Organisational, Process, Service, Technology;
- QIPI;
- TACEI;
- CEI;
- implementation duration;
- people saving;
- total cost saving;
- gross and net annual saving;
- benchmark variance;
- budget versus actual spending;
- priority score;
- risk and resource completeness;
- improvement-resolution completion.

## 6.4.1 Provider Accreditation and Evaluation

### Reusable sources

- Provider Rating from Criterion 3 documentation;
- Management Review provider-performance table.

### Missing before live implementation

- Provider master definition;
- accreditation screening fields;
- tier and compliance classification;
- Provider Rating child-template fields;
- Purchase Receipt and Quality Inspection field mapping;
- approval and renewal rules.

## 6.5.3 Hazard Identification and Risk Assessment

### Available now

- Quality Action risk-identification and risk-mitigation child tables;
- Management Review risk and opportunity table.

### Candidate metrics

- Quality Actions with risk assessments;
- Quality Actions with mitigation plans;
- high-priority actions;
- mitigation ownership;
- mitigation due dates;
- Management Review risk coverage.

### Missing before live implementation

- Risk Register and Mitigation Plans DocType;
- Helpdesk-Ticket hazard classification;
- 5×5 likelihood and severity fields;
- initial and residual risk scores;
- incident investigation fields;
- review and control effectiveness.

## Implemented partial API contract

The included API uses:

```text
ucc_analytics_criterion_6
```

This method is included as a permission-aware partial live foundation.

The future response should follow the Criterion 4 readiness contract:

```json
{
  "policy": {},
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
