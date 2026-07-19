# Criterion 4 DocType Inventory

## Section source inventory

| Section | Business area | Source key | Approved DocType candidates | Resolution |
| --- | --- | --- | --- | --- |
| 4.1.1 | Pre-Course Counselling, Selection and Admissions | applicant | Student Applicant | Runtime candidate resolution |
| 4.1.1 | Pre-Course Counselling, Selection and Admissions | admission | Student Admission UCC | Runtime candidate resolution |
| 4.1.1 | Pre-Course Counselling, Selection and Admissions | counselling | Pre Course Counselling Declaration | Runtime candidate resolution |
| 4.1.1 | Pre-Course Counselling, Selection and Admissions | adjustments | Student Log | Runtime candidate resolution |
| 4.2.1 | Student Contract | contract | Student Admission UCC | Runtime candidate resolution |
| 4.2.1 | Student Contract | invoice | Sales Invoice | Runtime candidate resolution |
| 4.2.2 | Fee Collection and Fee Protection Scheme | contract | Student Admission UCC | Runtime candidate resolution |
| 4.2.2 | Fee Collection and Fee Protection Scheme | invoice | Sales Invoice | Runtime candidate resolution |
| 4.2.2 | Fee Collection and Fee Protection Scheme | payment | Payment Entry | Runtime candidate resolution |
| 4.2.2 | Fee Collection and Fee Protection Scheme | fps | FPS Record | Runtime candidate resolution |
| 4.3.1 | Course Transfer, Deferment and Withdrawal | adjustments | Student Log | Runtime candidate resolution |
| 4.3.1 | Course Transfer, Deferment and Withdrawal | contract | Student Admission UCC | Runtime candidate resolution |
| 4.3.1 | Course Transfer, Deferment and Withdrawal | fps | FPS Record | Runtime candidate resolution |
| 4.4.1 | Refund | adjustments | Student Log | Runtime candidate resolution |
| 4.4.1 | Refund | payment | Payment Entry | Runtime candidate resolution |
| 4.4.1 | Refund | contract | Student Admission UCC | Runtime candidate resolution |
| 4.5.1 | Student Support Services | student_log | Student Log | Runtime candidate resolution |
| 4.5.1 | Student Support Services | academic_support | Intervention Issue Academic Support | Runtime candidate resolution |
| 4.5.1 | Student Support Services | wellness_support | Intervention Issue Wellness Services | Runtime candidate resolution |
| 4.5.1 | Student Support Services | integrity_support | Intervention Issue Academic Integrity | Runtime candidate resolution |
| 4.6.1 | Student Conduct and Attendance | attendance | Student Attendance | Runtime candidate resolution |
| 4.6.1 | Student Conduct and Attendance | student_log | Student Log | Runtime candidate resolution |
| 4.6.1 | Student Conduct and Attendance | warning | Dismissal Letters due to Attendance Requirements | Runtime candidate resolution |
| 4.6.1 | Student Conduct and Attendance | leave | Student Leave Application | Runtime candidate resolution |

## Repository-confirmed sources

- Student Applicant
- Student Admission UCC
- Student Contract
- New Student Counselling and Monitoring Form
- Student Attendance
- Student Leave Application
- Student Log
- Dismissal Letters due to Attendance Requirements
- HD Ticket
- Sales Invoice
- Payment Entry
- Course Adjustment Request Form
- Intervention Issue Academic Support
- Intervention Issue Academic Integrity
- Intervention Issue Wellness Services

## Runtime-only or not confirmed in uploaded repository source

- FPS Record
- Student Support Service Strategy Insights
- Joining an On-going Class

These sources may still exist as site customisations. Their presence must be
confirmed using live metadata and permissions.

## Important child-table relationship

Student movement and refund calculations may read:

```text
Student Log
└── custom_course_adjustment
    └── Course Adjustment Request Form
```

Child rows are queried only after the current user can read the parent
`Student Log`.

## Translation-safe source rule

`Student Admission UCC` and `Student Applicant` may both display to users as
“Shortlisted Applicants”. API calls must continue to use the canonical
technical DocType name.
