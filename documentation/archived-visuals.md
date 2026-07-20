# Archived visuals

**Total archived: 415 visuals** (627 -> 212 active).

Visuals cut during the v1.9.7 audit-focused reduction (each criterion trimmed to ~30 active visuals). **Nothing here is deleted** - these visuals are retained in source and simply skipped by the render loop:

- **Criteria 1, 2, 3, 6, 7** (`LIVE_VISUAL_EXPANSION`, `src/js/30-live-foundation-runtime.js`) and **Criterion 4** (`C4_VISUAL_EXPANSION`, `src/js/10-platform-runtime.js`): each cut visual carries `"enabled": false`.
- **Criterion 5** (static HTML): each cut visual's `data-chart` id is listed in `C5_DISABLED_VISUALS` (`src/js/10-platform-runtime.js`); its card is hidden via the `ucc-visual-archived` class.

**To restore a visual:** remove its `"enabled": false` flag (Criteria 1-4, 6, 7) or remove its id from `C5_DISABLED_VISUALS` (Criterion 5), then bump the affected criterion's count in `tools/validate_package.py` (`EXPECTED_VISUALS`) and `VERSION.json` (`diagram_counts`, `visual_targets`).

## Criterion 1 - Leadership and Strategic Planning (54 archived)

### Overview

| Visual Name | Type | Reason cut |
|---|---|---|
| Leadership System Health | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Governance-to-Improvement Lifecycle | lifecycle | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Governance Exception Funnel | radar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Board and Committee Activity | gauge | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Decision Closure Performance | bar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Policy Ownership Coverage | donut | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Policy Review Timeliness | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Strategic Objective Portfolio | lifecycle | Portfolio roll-up - duplicates the retained status/coverage view for this area. |
| Strategic Initiative Progress | radar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Department Contribution Profile | matrix | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Stakeholder Engagement Coverage | gauge | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Management Review Follow-up | trend | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Strategic Risk Exposure | donut | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Action Ownership Readiness | funnel | Additional readiness variation - the section's source/metric readiness indicator is retained. |
| Annual Governance Trend | radar | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Annual Strategy Trend | matrix | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Leadership Control Maturity | gauge | Composite maturity index - not a direct evidence artefact for audit. |
| Strategy Execution Maturity | trend | Composite maturity index - not a direct evidence artefact for audit. |
| Open Governance Actions | bar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Open Strategic Actions | donut | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |

### 1.1.1

| Visual Name | Type | Reason cut |
|---|---|---|
| Leadership Structure Coverage | gauge | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Role Description Completeness | trend | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Delegation and Authority Coverage | bar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Committee Meeting Cadence | donut | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Meeting Attendance Profile | funnel | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Decision Register Status | lifecycle | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Decision Closure Ageing | radar | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Governance Action Funnel | matrix | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Policy Review Calendar | trend | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Policy Owner Distribution | bar | Secondary distribution/breakdown - duplicates a retained summary metric. |
| Governance Risk Matrix | donut | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Stakeholder Accountability | lifecycle | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Communication of Governance Decisions | radar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Management Review Escalations | gauge | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Leadership Exception Profile | trend | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Governance Trend by Period | bar | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Action Effectiveness | donut | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |

### 1.2.1

| Visual Name | Type | Reason cut |
|---|---|---|
| Strategic Gap Funnel | radar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Objective Portfolio by Status | gauge | Portfolio roll-up - duplicates the retained status/coverage view for this area. |
| Initiative Portfolio by Status | trend | Portfolio roll-up - duplicates the retained status/coverage view for this area. |
| Milestone Delay Ageing | funnel | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Department Alignment | lifecycle | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Resource Alignment | radar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Risk-to-Objective Matrix | matrix | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Stakeholder Input Coverage | gauge | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Annual Planning Cycle | bar | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Quarterly Review Cadence | donut | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Management Review Inputs | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Management Review Outputs | lifecycle | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Improvement Action Linkage | radar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Strategic Measure Availability | gauge | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Strategic Exception Profile | trend | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Objective Achievement Trend | bar | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Initiative Completion Trend | donut | Time-series/trend variation - a representative status/coverage view is retained for this area. |

## Criterion 2 - Corporate Administration (69 archived)

### Overview

| Visual Name | Type | Reason cut |
|---|---|---|
| Workforce Control Profile | gauge | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Training Control Profile | trend | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Communication Control Profile | bar | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Information Control Profile | donut | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Knowledge Control Profile | funnel | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |

### 2.1.1

| Visual Name | Type | Reason cut |
|---|---|---|
| Recruitment and Onboarding Funnel | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Hiring Exception Profile | radar | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Employment Lifecycle Trend | matrix | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Manpower Plan Coverage | gauge | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Requisition Approval Readiness | trend | Additional readiness variation - the section's source/metric readiness indicator is retained. |
| Candidate Screening Status | bar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Interview Assessment Coverage | donut | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Appointment and Onboarding Status | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |

### 2.1.2

| Visual Name | Type | Reason cut |
|---|---|---|
| Training Needs Funnel | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Competency Readiness | lifecycle | Additional readiness variation - the section's source/metric readiness indicator is retained. |
| Training Exception Profile | radar | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Training Completion Trend | matrix | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Training Plan Coverage | gauge | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Mandatory Training Status | trend | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Role-Specific Training Coverage | bar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Training Effectiveness | donut | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |

### 2.2.1

| Visual Name | Type | Reason cut |
|---|---|---|
| Communication Approval Funnel | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Channel Readiness | lifecycle | Additional readiness variation - the section's source/metric readiness indicator is retained. |
| Communication Exception Profile | radar | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Communication Trend | matrix | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Internal Communication Activity | gauge | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| External Communication Activity | trend | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Stakeholder Channel Coverage | bar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Approval-Level Distribution | donut | Secondary distribution/breakdown - duplicates a retained summary metric. |

### 2.3.1

| Visual Name | Type | Reason cut |
|---|---|---|
| Data Collection Lifecycle | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Data Exception Profile | radar | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Data Quality Trend | matrix | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Consent Coverage | gauge | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Access Control Coverage | trend | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Data Classification Coverage | bar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Retention and Disposal Status | donut | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Data Source Integration Readiness | funnel | Additional readiness variation - the section's source/metric readiness indicator is retained. |

### 2.3.2

| Visual Name | Type | Reason cut |
|---|---|---|
| Document Lifecycle | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Knowledge Exception Profile | radar | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Document Review Trend | matrix | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Controlled Document Coverage | gauge | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Document Version Currency | trend | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Document Owner Coverage | bar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Obsolete Document Removal | donut | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Knowledge Access Readiness | funnel | Additional readiness variation - the section's source/metric readiness indicator is retained. |

### 2.4.1

| Visual Name | Type | Reason cut |
|---|---|---|
| Feedback Handling Funnel | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Feedback Readiness | lifecycle | Additional readiness variation - the section's source/metric readiness indicator is retained. |
| Feedback Exception Profile | radar | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Feedback Closure Trend | matrix | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Feedback Channel Distribution | gauge | Secondary distribution/breakdown - duplicates a retained summary metric. |
| Feedback Priority Matrix | trend | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Acknowledgement Timeliness | bar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Resolution Timeliness | donut | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |

### 2.4.2

| Visual Name | Type | Reason cut |
|---|---|---|
| Survey Participation Funnel | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Student Survey Exception Profile | radar | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Student Satisfaction Trend | matrix | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Survey Type Distribution | gauge | Secondary distribution/breakdown - duplicates a retained summary metric. |
| Question Response Coverage | trend | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Student Support Satisfaction | bar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Teaching and Learning Satisfaction | donut | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Survey Improvement Actions | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |

### 2.4.3

| Visual Name | Type | Reason cut |
|---|---|---|
| Survey Participation Funnel | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Staff Survey Exception Profile | radar | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Staff Satisfaction Trend | matrix | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Survey Type Distribution | gauge | Secondary distribution/breakdown - duplicates a retained summary metric. |
| Engagement Dimension Profile | trend | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Workplace Satisfaction | bar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Communication Satisfaction | donut | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Staff Improvement Actions | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |

## Criterion 3 - External Recruitment Agents (60 archived)

### Overview

| Visual Name | Type | Reason cut |
|---|---|---|
| Agent Control Health | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Renewal and Evaluation Trend | lifecycle | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Agent Territory Distribution | trend | Secondary distribution/breakdown - duplicates a retained summary metric. |
| Agent Contract Coverage | bar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Agent Onboarding Coverage | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Agent Review Coverage | lifecycle | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Recruitment Contribution | radar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Applicant Conversion Profile | matrix | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Commission Activity | gauge | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Renewal Readiness | trend | Additional readiness variation - the section's source/metric readiness indicator is retained. |
| Suspension and Termination Profile | bar | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Offboarding Readiness | donut | Additional readiness variation - the section's source/metric readiness indicator is retained. |
| Agent Risk Profile | funnel | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Annual Agent Trend | radar | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Contract Expiry Trend | matrix | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Review Outcome Trend | gauge | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Claim Amount Trend | trend | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Agent Performance Radar | bar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Agent Lifecycle Funnel | donut | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Agent Control Matrix | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Agent Source Readiness | radar | Additional readiness variation - the section's source/metric readiness indicator is retained. |
| Agent Metric Readiness | matrix | Additional readiness variation - the section's source/metric readiness indicator is retained. |

### 3.1.1

| Visual Name | Type | Reason cut |
|---|---|---|
| Selection Criteria Weighting | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Selection Score Distribution | lifecycle | Secondary distribution/breakdown - duplicates a retained summary metric. |
| Application Volume | trend | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Application Completeness | bar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Application Processing Time | donut | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Approval Processing Time | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Referee Evidence | radar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Company Evidence | matrix | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Selection Rating Profile | trend | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Risk Assessment Coverage | bar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Risk Mitigation Coverage | donut | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| First-Time Contract Status | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| NDA Requirement Distribution | radar | Secondary distribution/breakdown - duplicates a retained summary metric. |
| Onboarding Initiation | gauge | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Onboarding Activity Completion | trend | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Agent Territory Readiness | bar | Additional readiness variation - the section's source/metric readiness indicator is retained. |
| Appointment Exception Profile | donut | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Appointment Trend | radar | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Approval Outcome Trend | matrix | Time-series/trend variation - a representative status/coverage view is retained for this area. |

### 3.2.1

| Visual Name | Type | Reason cut |
|---|---|---|
| Renewal Checkpoint Flow | radar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Offboarding and Exit Security | gauge | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Active Agent Portfolio | trend | Portfolio roll-up - duplicates the retained status/coverage view for this area. |
| Annual Review Coverage | bar | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Annual Survey Profile | donut | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Recruitment Target Profile | funnel | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Target versus Actual Recruitment | lifecycle | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Applicant Contribution by Agent | radar | Secondary distribution/breakdown - duplicates a retained summary metric. |
| Applicant Conversion by Agent | matrix | Secondary distribution/breakdown - duplicates a retained summary metric. |
| Contract Expiry Ageing | trend | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Continuation and Hold Outcomes | donut | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Claim Submission Activity | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Claim Amount Profile | lifecycle | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Training Log Coverage | radar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Student Feedback Coverage | gauge | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Consent Survey Completion | trend | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Suspension and Termination | bar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Performance Trend | radar | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Renewal Outcome Trend | matrix | Time-series/trend variation - a representative status/coverage view is retained for this area. |

## Criterion 4 - Student Protection and Support Services (54 archived)

### 4.1.1 Admissions

| Visual Name | Type | Reason cut |
|---|---|---|
| Applicant Processing Time | lifecycle | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Selection Decision Profile | radar | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Late Admission Exceptions | matrix | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Admission Evidence Matrix | trend | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Applicant Trend | bar | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Admission Metric Readiness | funnel | Additional readiness variation - the section's source/metric readiness indicator is retained. |
| Admission Exception Profile | lifecycle | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |

### 4.2.1 Student Contract

| Visual Name | Type | Reason cut |
|---|---|---|
| Contract Approval Status | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Unsigned Contract Ageing | lifecycle | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Contract Exception Funnel | matrix | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Contract Date Readiness | gauge | Additional readiness variation - the section's source/metric readiness indicator is retained. |
| Student Contract Status | trend | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Contract Trend | bar | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Contract Metric Readiness | funnel | Additional readiness variation - the section's source/metric readiness indicator is retained. |
| Contract Control Matrix | lifecycle | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |

### 4.2.2 Fees & FPS

| Visual Name | Type | Reason cut |
|---|---|---|
| Outstanding Balance Profile | lifecycle | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Payment Lifecycle | radar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Fee Exception Funnel | matrix | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Collection Trend | trend | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Payment Evidence Matrix | bar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Fee Metric Readiness | funnel | Additional readiness variation - the section's source/metric readiness indicator is retained. |
| Fee Control Health | lifecycle | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |

### 4.3.1 Transfer / Defer / Withdraw

| Visual Name | Type | Reason cut |
|---|---|---|
| Deferment Request Status | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Withdrawal Request Status | lifecycle | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Request Processing Time | radar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Movement Exception Funnel | matrix | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Movement Evidence Matrix | trend | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Movement Trend | bar | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Movement Metric Readiness | funnel | Additional readiness variation - the section's source/metric readiness indicator is retained. |
| Movement Control Health | lifecycle | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |

### 4.4.1 Refunds

| Visual Name | Type | Reason cut |
|---|---|---|
| Refund Processing Time | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Refund Ageing | lifecycle | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Refund Exception Funnel | matrix | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Refund Amount Profile | gauge | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Refund Evidence Matrix | trend | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Refund Trend | bar | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Refund Metric Readiness | funnel | Additional readiness variation - the section's source/metric readiness indicator is retained. |
| Refund Control Health | lifecycle | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |

### 4.5.1 Student Support

| Visual Name | Type | Reason cut |
|---|---|---|
| Support Category Distribution | funnel | Secondary distribution/breakdown - duplicates a retained summary metric. |
| Support Resolution Time | lifecycle | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Support Lifecycle | radar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Support Exception Funnel | matrix | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Support Evidence Matrix | trend | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Support Trend | bar | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Support Metric Readiness | funnel | Additional readiness variation - the section's source/metric readiness indicator is retained. |
| Support Control Health | lifecycle | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |

### 4.6.1 Conduct & Attendance

| Visual Name | Type | Reason cut |
|---|---|---|
| Attendance Risk Profile | donut | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Conduct Case Status | lifecycle | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Attendance Trend | radar | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Conduct Trend | matrix | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Attendance Evidence Matrix | trend | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Conduct Evidence Matrix | bar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Attendance Metric Readiness | funnel | Additional readiness variation - the section's source/metric readiness indicator is retained. |
| Conduct Exception Profile | lifecycle | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |

## Criterion 5 - Academic Systems and Processes (62 archived)

### 5.1.1 Course Design & Development

| Visual Name | Type | Reason cut |
|---|---|---|
| Course → Module Network | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Decision Time by Year | chart | Secondary distribution/breakdown - duplicates a retained summary metric. |
| Proposal Evidence | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Module Evidence Constellation | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Evidence Coverage | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Module Design Evidence | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Review Timeline | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Course Review Evidence | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Gap Distribution by Record Type | chart | Secondary distribution/breakdown - duplicates a retained summary metric. |

### 5.1.2 Course Review

| Visual Name | Type | Reason cut |
|---|---|---|
| Next Review Schedule | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Review Type | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Action Plan Status | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Module Review Evidence Completeness | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Review-cycle status | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Module Review to Course Review coverage | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Action-plan aging | chart | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Completed versus pending actions | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Missing review evidence | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Implementation follow-up trend | chart | Time-series/trend variation - a representative status/coverage view is retained for this area. |

### 5.2 Planning & Delivery

| Visual Name | Type | Reason cut |
|---|---|---|
| Scheduled Classes by Course | chart | Secondary distribution/breakdown - duplicates a retained summary metric. |
| Delivery Controls | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |

### 5.2.1 Course Planning

| Visual Name | Type | Reason cut |
|---|---|---|
| Planning Flow Coverage | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Admission Status | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Room and Timing Readiness | chart | Additional readiness variation - the section's source/metric readiness indicator is retained. |
| Contract Date Completeness | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Intake date completeness | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Module classes without schedules | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Schedule completeness | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Room and time clashes | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Teacher timetable clashes | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Contract versus commencement | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Unsigned or unsent contracts | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |

### 5.2.2 Course Delivery

| Visual Name | Type | Reason cut |
|---|---|---|
| Delivery Platform | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Survey Response Categories | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Prior Notice | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Delivery Concerns | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Planned versus delivered sessions | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Observation coverage by Teacher | chart | Secondary distribution/breakdown - duplicates a retained summary metric. |
| Observation coverage by Module | chart | Secondary distribution/breakdown - duplicates a retained summary metric. |
| Scheduled versus ad-hoc observations | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Observation sign-off aging | chart | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Observation rating distribution | chart | Secondary distribution/breakdown - duplicates a retained summary metric. |
| Common strengths | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Common improvement areas | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Survey response volume | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Delivery exception queue | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |

### 5.3.1 Partnership Management

| Visual Name | Type | Reason cut |
|---|---|---|
| Agreement Type | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Agreement Expiry Window | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Monitoring Type | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Identification Scores | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Provider Rating Stage | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Selection Threshold | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Agreement lifecycle | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Signature completion | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Partnership risk distribution | chart | Secondary distribution/breakdown - duplicates a retained summary metric. |
| Monitoring frequency and recency | chart | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Continuation decisions | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Missing monitoring or evaluation | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Quality-record completeness | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |

### 5.4 Student Learning

| Visual Name | Type | Reason cut |
|---|---|---|
| Question-Level Survey Scores | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Learning Interventions | chart | Mapped to an unconfirmed/unavailable source (renders as no-data); excluded from the audit set. |

### 5.5 Assessment

| Visual Name | Type | Reason cut |
|---|---|---|
| Assessment Data Quality | chart | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |

## Criterion 6 - Quality Assurance, Innovation and Continual Improvement (66 archived)

### Overview

| Visual Name | Type | Reason cut |
|---|---|---|
| Quality Management Cycle | bar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Quality System Health | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Action Status | radar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Audit Portfolio Status | gauge | Portfolio roll-up - duplicates the retained status/coverage view for this area. |
| Management Review Portfolio | trend | Portfolio roll-up - duplicates the retained status/coverage view for this area. |
| Innovation Portfolio | bar | Portfolio roll-up - duplicates the retained status/coverage view for this area. |
| Provider Evaluation Portfolio | donut | Portfolio roll-up - duplicates the retained status/coverage view for this area. |
| Risk Portfolio | funnel | Portfolio roll-up - duplicates the retained status/coverage view for this area. |
| Corrective Action Portfolio | lifecycle | Portfolio roll-up - duplicates the retained status/coverage view for this area. |
| Quality Exception Profile | radar | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Quality Trend | gauge | Time-series/trend variation - a representative status/coverage view is retained for this area. |

### 6.1.1

| Visual Name | Type | Reason cut |
|---|---|---|
| Audit Lifecycle | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Auditor Qualification and Independence | lifecycle | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Audit Plan Completion | gauge | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Audit Schedule Status | trend | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Audit Evidence Completeness | bar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Finding Type Distribution | donut | Secondary distribution/breakdown - duplicates a retained summary metric. |
| Finding Owner Distribution | funnel | Secondary distribution/breakdown - duplicates a retained summary metric. |
| Finding Ageing | lifecycle | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Resolution Status | radar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Overdue Resolution Profile | matrix | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Closure Verification | gauge | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |

### 6.2.1

| Visual Name | Type | Reason cut |
|---|---|---|
| Management Review Preparation | donut | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Action Ageing | radar | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Action Effectiveness | matrix | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Review Cadence | trend | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Chairperson Coverage | bar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Minutes Completion | donut | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Next Review Readiness | funnel | Additional readiness variation - the section's source/metric readiness indicator is retained. |
| Audit Input Coverage | lifecycle | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Provider Input Coverage | radar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Risk Input Coverage | matrix | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Quality Action Follow-up | gauge | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |

### 6.3.1

| Visual Name | Type | Reason cut |
|---|---|---|
| Innovation Performance Categories | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| QIPI Outcome Trend | lifecycle | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Before and After Impact | radar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Innovation Category Mix | gauge | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| TACEI Profile | bar | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| CEI Profile | donut | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| People Saving | funnel | Innovation cost-saving breakdown - low direct audit-evidence value; representative innovation status retained. |
| Technology Saving | lifecycle | Innovation cost-saving breakdown - low direct audit-evidence value; representative innovation status retained. |
| Physical Saving | radar | Innovation cost-saving breakdown - low direct audit-evidence value; representative innovation status retained. |
| Gross and Net Saving | matrix | Innovation cost-saving breakdown - low direct audit-evidence value; representative innovation status retained. |
| Benchmark Variance | gauge | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |

### 6.4.1

| Visual Name | Type | Reason cut |
|---|---|---|
| Compliance Package | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Service Delivery and Purchase Controls | lifecycle | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Provider Rating Weighting | radar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Provider Portfolio Status | gauge | Portfolio roll-up - duplicates the retained status/coverage view for this area. |
| Identification and Screening | trend | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Regular Review Coverage | bar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Exit Evaluation Coverage | donut | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Rating Likert Profile | lifecycle | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Continuation Outcomes | radar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Hold Outcomes | matrix | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Termination Outcomes | gauge | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |

### 6.5.3

| Visual Name | Type | Reason cut |
|---|---|---|
| Risk Treatment Lifecycle | lifecycle | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Residual Risk Trend | radar | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Business Continuity Readiness | matrix | Additional readiness variation - the section's source/metric readiness indicator is retained. |
| Mitigation Plan Coverage | trend | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Risk Owner Coverage | bar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Risk Due-Date Readiness | donut | Additional readiness variation - the section's source/metric readiness indicator is retained. |
| High-Priority Risk Profile | funnel | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Initial Risk Profile | lifecycle | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Residual Risk Profile | radar | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Control Effectiveness | matrix | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Risk Exception Profile | gauge | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |

## Criterion 7 - Performance Outcomes (50 archived)

### Overview

| Visual Name | Type | Reason cut |
|---|---|---|
| Outcome Portfolio | bar | Portfolio roll-up - duplicates the retained status/coverage view for this area. |
| Outcome System Health | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Outcome Measurement Lifecycle | lifecycle | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Outcome Exception Funnel | radar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Indicator Portfolio | gauge | Portfolio roll-up - duplicates the retained status/coverage view for this area. |
| Outcome Category Mix | lifecycle | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Outcome Ownership | radar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Improvement Action Linkage | gauge | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Outcome Trend | trend | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Benchmark Profile | bar | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Student Outcome Profile | donut | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Graduate Outcome Profile | funnel | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Stakeholder Outcome Profile | lifecycle | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Financial Outcome Profile | radar | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Operational Outcome Profile | matrix | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| People Saving Profile | gauge | Innovation cost-saving breakdown - low direct audit-evidence value; representative innovation status retained. |
| Technology Saving Profile | trend | Innovation cost-saving breakdown - low direct audit-evidence value; representative innovation status retained. |
| Physical Saving Profile | bar | Innovation cost-saving breakdown - low direct audit-evidence value; representative innovation status retained. |
| Gross Saving Profile | donut | Innovation cost-saving breakdown - low direct audit-evidence value; representative innovation status retained. |
| Net Saving Profile | funnel | Innovation cost-saving breakdown - low direct audit-evidence value; representative innovation status retained. |
| Outcome Maturity | matrix | Composite maturity index - not a direct evidence artefact for audit. |
| Department Performance | gauge | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Strategic Alignment | trend | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Outcome Risk Profile | bar | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Outcome Metric Readiness | lifecycle | Additional readiness variation - the section's source/metric readiness indicator is retained. |
| Annual Outcome Trend | radar | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Quarterly Outcome Trend | matrix | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Outcome Benchmark Trend | gauge | Time-series/trend variation - a representative status/coverage view is retained for this area. |

### 7.1.1

| Visual Name | Type | Reason cut |
|---|---|---|
| Measurement Lifecycle | gauge | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Outcome Category Distribution | donut | Secondary distribution/breakdown - duplicates a retained summary metric. |
| Indicator Status Funnel | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Measurement Evidence Matrix | radar | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Outcome-to-Strategy Mapping | donut | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Student Outcome Trend | funnel | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Graduate Outcome Trend | lifecycle | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Stakeholder Outcome Trend | radar | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Financial Outcome Trend | matrix | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Operational Outcome Trend | gauge | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Savings Outcome Trend | trend | Innovation cost-saving breakdown - low direct audit-evidence value; representative innovation status retained. |
| Department Outcome Profile | bar | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Outcome Ownership Radar | donut | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Target Achievement Radar | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Outcome Maturity Matrix | lifecycle | Composite maturity index - not a direct evidence artefact for audit. |
| Indicator Exception Profile | radar | Aggregate profile/roll-up - low standalone audit signal; the underlying coverage/status visual is retained. |
| Outcome Risk Matrix | matrix | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Annual Performance Trend | bar | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Quarterly Performance Trend | donut | Time-series/trend variation - a representative status/coverage view is retained for this area. |
| Benchmark Comparison | funnel | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |
| Outcome Reporting Readiness | gauge | Additional readiness variation - the section's source/metric readiness indicator is retained. |
| Measurement Governance | trend | Near-duplicate of a retained visual for this subcriterion; cut to reduce redundancy. |

