# Criterion 4 Analytics Mapping

## User flow

```text
Select subcriterion
    ↓
resolve policy
    ↓
resolve readable sources
    ↓
resolve metric fields
    ↓
calculate metrics
    ↓
answer management questions
    ↓
identify exceptions
    ↓
open drill-down records
```

## Management questions

| Section | Question ID | Question | Metric | Calculation description |
| --- | --- | --- | --- | --- |
| 4.1.1 | q411-1 | How many pre-course counselling declarations are recorded? | c411-counselling | Count Pre Course Counselling Declaration records in the current filter scope. |
| 4.1.1 | q411-2 | How many applicants acknowledged that the pre-course information was communicated? | c411-acknowledged | Count Pre Course Counselling Declaration.declaration_check values that are enabled. |
| 4.1.1 | q411-3 | How many applicants provided PDPA consent? | c411-pdpa | Count Pre Course Counselling Declaration.pdpa_check values that are enabled. |
| 4.1.1 | q411-4 | How many counselling declarations contain both the staff representative and declaration date? | c411-staff-complete | Count records with name_of_staff and date populated. |
| 4.1.1 | q411-5 | How many applications are approved or admitted? | c411-complete | Count Student Applicant records with approved, admitted or enrolled status. |
| 4.1.1 | q411-6 | How many admissions remain conditional? | c411-conditional | Count Student Admission UCC records where conditional is enabled. |
| 4.1.1 | q411-7 | How many late-admission requests require monitoring? | c411-late | Count Late Admission rows in Student Log course adjustments. |
| 4.2.1 | q421-1 | How many student contracts have been generated? | c421-generated | Count Student Admission UCC records with a contract URL or contract content. |
| 4.2.1 | q421-2 | How many contracts have an approved admission status? | c421-approved | Count approved, enrolled or completed admission records. |
| 4.2.1 | q421-3 | How many contracts have been signed by the student? | c421-signed | Count records with a student contract signed date. |
| 4.2.1 | q421-4 | How many sent contracts are still unsigned? | c421-pending | Count records with contract sent date and no student signed date. |
| 4.2.2 | q422-1 | How many admissions have a linked sales invoice? | c422-invoiced | Count Student Admission UCC records with sales_invoice populated. |
| 4.2.2 | q422-2 | How many submitted incoming payment records are available? | c422-paid | Count submitted Payment Entry records with Receive payment type. |
| 4.2.2 | q422-3 | How many FPS declarations are processed or approved? | c422-fps | Count FPS Record rows with Processed or Approved status. |
| 4.2.2 | q422-4 | How many invoices are overdue? | c422-late | Count Sales Invoice records with Overdue status. |
| 4.3.1 | q431-1 | How many course transfer requests are recorded? | c431-transfer | Count Course Transfer child rows under Student Log. |
| 4.3.1 | q431-2 | How many course deferment requests are recorded? | c431-defer | Count Course Deferment child rows under Student Log. |
| 4.3.1 | q431-3 | How many course withdrawal requests are recorded? | c431-withdraw | Count Course Withdrawal child rows under Student Log. |
| 4.3.1 | q431-4 | How many movement requests exceed the processing threshold? | c431-overdue | Count applicable requests older than the configured working-day approximation. |
| 4.4.1 | q441-1 | How many refund requests are recorded? | c441-open | Count Refund rows in Student Log course adjustments. |
| 4.4.1 | q441-2 | How many refund requests have an approval date? | c441-eligible | Count refund rows with approved_date populated. |
| 4.4.1 | q441-3 | How many refund cases are marked complete by the available workflow evidence? | c441-paid | Count refund rows matching the confirmed completion rule. |
| 4.4.1 | q441-4 | How many refund requests exceed seven working days? | c441-overdue | Count refund requests older than the configured calendar-day approximation. |
| 4.5.1 | q451-1 | How many student support service records are available? | c451-services | Count readable intervention or counselling records. |
| 4.5.1 | q451-2 | How many student support cases are recorded? | c451-cases | Count Student Log rows containing support, intervention, counselling, wellness or academic terms. |
| 4.5.1 | q451-3 | How many support cases require follow-up? | c451-followup | Count Student Log rows containing follow-up, action-plan, pending or review terms. |
| 4.5.1 | q451-4 | How many support cases contain an outcome? | c451-outcomes | Count Student Log rows containing resolved, completed, closed, outcome or effective terms. |
| 4.6.1 | q461-1 | How many attendance records are available? | c461-attendance | Count readable Student Attendance records. |
| 4.6.1 | q461-2 | How many attendance records indicate absence or lateness? | c461-risk | Count Student Attendance rows with Absent or Late status. |
| 4.6.1 | q461-3 | How many attendance warning or dismissal records are available? | c461-warning | Count readable warning or dismissal records. |
| 4.6.1 | q461-4 | How many conduct or attendance interventions are open in Student Log evidence? | c461-intervention | Count Student Log rows containing intervention, warning, dismissal, attendance or counselling terms. |

## Exception metrics

- `c411-unacknowledged`
- `c411-pdpa-missing`
- `c411-conditional`
- `c411-late`
- `c421-pending`
- `c422-late`
- `c431-overdue`
- `c441-open`
- `c441-overdue`
- `c451-followup`
- `c461-risk`
- `c461-intervention`

## Source and metric summaries

```json
{
  "source_summary": {
    "total": 4,
    "available": 4,
    "issues": 0
  },
  "metric_summary": {
    "total": 4,
    "available": 4,
    "issues": 0
  }
}
```

These values produce the visible readiness line, for example:

```text
PPD-SSO-SS-4.6.1 v2.2
· 4/4 sources available
· 4/4 metrics available
```

## Filters

The Server Script accepts a filter object. Field application is permission-aware
and depends on whether the target source contains the approved filter field.

## Data-quality results

Every unavailable source or metric creates a data-quality row containing:

- criterion;
- check;
- source;
- status;
- detail.
