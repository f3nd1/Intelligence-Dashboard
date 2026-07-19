# Criterion 5 DocType Inventory

## Active frontend source registry

| DocType | Purpose | Mode | Load style | Configured fields |
| --- | --- | --- | --- | --- |
| Academic Year | Academic year filter | core | Selected fields | 4 |
| Student Group | Module Class Details filter and class scope | core | Selected fields | 8 |
| Course | 5.1 course design | core | Selected fields | 4 |
| Program | 5.1 programme-course mapping | core | Selected fields | 4 |
| Assessment Plan | 5.1 and 5.5 assessment planning | core | Selected fields | 11 |
| Assessment Result | 5.1 and 5.5 result coverage | core | Selected fields | 11 |
| Course Schedule | 5.2 class delivery | core | Selected fields | 10 |
| Course Enrollment | 5.2 enrollment proxy | core | Selected fields | 6 |
| Student Attendance | 5.2 attendance | core | Selected fields | 8 |
| Module Review | 5.1.2 module review records | core | Full record | 9 |
| Course Review | 5.1.2 course review records | core | Full record | 7 |
| Student Intake No | 5.2.1 intake planning | core | Full record | 6 |
| Module Class Details | 5.2.1 and 5.2.2 module operations | core | Full record | 8 |
| Student Admission UCC | 5.2.1 Shortlisted Applicants admissions and contracts | core | Full record | 8 |
| Classroom Observation | 5.2.2 teaching observation | core | Full record | 9 |
| Partnership Agreement | 5.3.1 signed partnership agreements | core | Full record | 12 |
| Partnerships Agreement Management | 5.3.1 partnership identification, monitoring and evaluation | core | Full record | 9 |
| Supplier Rating | 5.3.1 Provider Rating evaluation records | core | Full record | 11 |
| Survey Response | 5.4 survey scores and open-ended responses | core | Full record | 8 |

## Section-to-source ownership

| Section | Expected sources | Readiness metrics |
| --- | --- | --- |
| Criterion 5 Overview | Academic Year, Student Group, Course, Program | 6 |
| Criterion 5.1 | Course, Program, Assessment Plan, Assessment Result | 6 |
| Criterion 5.1.1 | Course, Program, Course Proposal, Course Review, Assessment Plan, Assessment Result | 8 |
| Criterion 5.1.2 | Module Review, Course Review | 6 |
| Criterion 5.2 | Course Schedule, Course Enrollment, Student Attendance | 6 |
| Criterion 5.2.1 | Student Intake No, Module Class Details, Student Admission UCC, Course Schedule | 6 |
| Criterion 5.2.2 | Module Class Details, Classroom Observation, Survey Response | 6 |
| Criterion 5.3 | Partnership Agreement, Partnerships Agreement Management, Supplier Rating | 6 |
| Criterion 5.3.1 | Partnership Agreement, Partnerships Agreement Management, Supplier Rating | 6 |
| Criterion 5.4 | Survey Response, Course Schedule, Student Attendance | 6 |
| Criterion 5.5 | Assessment Plan, Assessment Result, Course, Student Group | 6 |
| Criterion 5 Data Quality | Course, Program, Course Schedule, Assessment Result | 4 |
| Criterion 5 Sources | Academic Year, Student Group, Course, Program, Assessment Plan, Assessment Result, Course Schedule, Course Enrollment, Student Attendance, Module Review, Course Review, Student Intake No, Module Class Details, Student Admission UCC, Classroom Observation, Partnership Agreement, Partnerships Agreement Management, Supplier Rating, Survey Response | 4 |

## UCC terminology

| User-facing term | Technical source |
|---|---|
| Course | Program |
| Module | Course |
| Module Class Details | Student Group |
| Shortlisted Applicants | Student Admission UCC |
| Provider Rating | Supplier Rating |
| Teacher | Instructor |

Labels must not be substituted into API calls.

## Key relationships

```text
Academic Year
└── Student Group / Module Class Details
    ├── Course Schedule
    ├── Student Attendance
    ├── Assessment Plan
    └── students and enrolments

Program
└── Course

Assessment Plan
└── Assessment Result

Course Proposal
└── design and approval evidence

Course / Module Review
└── review status, actions and follow-up

Partnership Agreement
├── Partnerships Agreement Management
└── Supplier Rating
```
