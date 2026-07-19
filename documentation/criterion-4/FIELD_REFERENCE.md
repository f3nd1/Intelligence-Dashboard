# Criterion 4 Field Reference

## Active metric fields

| Section | Metric ID | Metric | Source key | Field candidates | Mode | Additional requirements |
| --- | --- | --- | --- | --- | --- | --- |
| 4.1.1 | c411-counselling | Counselling declarations | counselling | name | all | — |
| 4.1.1 | c411-acknowledged | Applicant acknowledgements | counselling | declaration_check | truthy | — |
| 4.1.1 | c411-pdpa | PDPA consents | counselling | pdpa_check | truthy | — |
| 4.1.1 | c411-staff-complete | Staff declarations completed | counselling | name_of_staff | truthy | date:truthy |
| 4.1.1 | c411-unacknowledged | Applicant acknowledgement missing | counselling | declaration_check | falsy | — |
| 4.1.1 | c411-pdpa-missing | PDPA consent missing | counselling | pdpa_check | falsy | — |
| 4.1.1 | c411-complete | Approved applications | applicant | application_status | contains | — |
| 4.1.1 | c411-conditional | Conditional admissions | admission | conditional | truthy | — |
| 4.1.1 | c411-late | Late-admission requests | adjustments | type | equals | child Course Adjustment Request Form via custom_course_adjustment |
| 4.2.1 | c421-generated | Contracts generated | contract | contract_url, student_contract | truthy | — |
| 4.2.1 | c421-approved | Approved contracts | contract | application_status | contains | — |
| 4.2.1 | c421-signed | Signed contracts | contract | contract_signed_by_student_date, student_signed_date | truthy | — |
| 4.2.1 | c421-pending | Sent but not signed | contract | contract_sent_date | truthy | contract_signed_by_student_date/student_signed_date:falsy |
| 4.2.2 | c422-invoiced | Students invoiced | contract | sales_invoice | truthy | — |
| 4.2.2 | c422-paid | Submitted receipts | payment | payment_type | contains | docstatus:equals |
| 4.2.2 | c422-fps | FPS declarations processed | fps | fps_status | contains | — |
| 4.2.2 | c422-late | Late-payment exceptions | invoice | status | contains | — |
| 4.3.1 | c431-overdue | Open requests beyond 21 working days | adjustments | posting_date | older_than_days | type:contains; approved_date:falsy; child Course Adjustment Request Form via custom_course_adjustment |
| 4.3.1 | c431-transfer | Transfer requests | adjustments | type | equals | child Course Adjustment Request Form via custom_course_adjustment |
| 4.3.1 | c431-defer | Deferment requests | adjustments | type | equals | child Course Adjustment Request Form via custom_course_adjustment |
| 4.3.1 | c431-withdraw | Withdrawal requests | adjustments | type | equals | child Course Adjustment Request Form via custom_course_adjustment |
| 4.4.1 | c441-open | Open refund requests | adjustments | type | equals | approved_date:falsy; child Course Adjustment Request Form via custom_course_adjustment |
| 4.4.1 | c441-eligible | Approved refund requests | adjustments | type | equals | approved_date:truthy; child Course Adjustment Request Form via custom_course_adjustment |
| 4.4.1 | c441-overdue | Open refunds beyond 7 days | adjustments | posting_date | older_than_days | type:equals; approved_date:falsy; child Course Adjustment Request Form via custom_course_adjustment |
| 4.4.1 | c441-paid | Refund payments recorded | payment | remarks | contains | payment_type:contains; docstatus:equals |
| 4.5.1 | c451-services | Student Logs | student_log | name | all | — |
| 4.5.1 | c451-cases | Academic-support records | academic_support | name | all | — |
| 4.5.1 | c451-followup | Wellness-support records | wellness_support | name | all | — |
| 4.5.1 | c451-outcomes | Academic-integrity records | integrity_support | name | all | — |
| 4.6.1 | c461-attendance | Attendance records | attendance | name | all | — |
| 4.6.1 | c461-risk | Absent or late records | attendance | status | contains | — |
| 4.6.1 | c461-warning | Attendance-dismissal records | warning | name | all | — |
| 4.6.1 | c461-intervention | Student Logs | student_log | name | all | — |

## Runtime mapping strategy

The active Server Script resolves:

```text
approved source candidates
        ↓
first existing readable DocType
        ↓
approved field candidates
        ↓
first existing field
        ↓
permission-aware calculation
```

## Extended candidate mappings

The complete extended mapping is maintained in
`reference/field-mappings.json`.

It includes additional approved candidate fields for:

- counselling acknowledgements and PDPA;
- student contracts and signatures;
- fee, payment and FPS status;
- transfer, deferment and withdrawal;
- refunds;
- support-service status;
- conduct, attendance and intervention.
