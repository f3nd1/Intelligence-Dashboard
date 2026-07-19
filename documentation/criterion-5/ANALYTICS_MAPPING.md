# Criterion 5 Analytics Mapping

## Navigation hierarchy

```text
Overview
├── 5.1 Design and Review
│   ├── 5.1 Overview
│   ├── 5.1.1 Course Design and Development
│   └── 5.1.2 Course Review
├── 5.2 Planning and Delivery
│   ├── 5.2 Overview
│   ├── 5.2.1 Course Planning
│   └── 5.2.2 Course Delivery
├── 5.3 Partnerships
│   ├── 5.3 Overview
│   └── 5.3.1 Partnership Management
├── 5.4 Student Learning
├── 5.5 Student Assessment
├── Data Quality
└── Sources
```

## Readiness metrics

| Section | Metric | Required source |
| --- | --- | --- |
| Criterion 5 Overview | Courses in selected scope | Course |
| Criterion 5 Overview | Module readiness | Course |
| Criterion 5 Overview | Course-to-programme mapping | Course, Program |
| Criterion 5 Overview | Source availability | Calculated in browser / registry |
| Criterion 5 Overview | Questions answered | Calculated in browser / registry |
| Criterion 5 Overview | Open exceptions | Calculated in browser / registry |
| Criterion 5.1 | Course mapping | Course, Program |
| Criterion 5.1 | Configuration readiness | Course |
| Criterion 5.1 | Assessment planning coverage | Assessment Plan |
| Criterion 5.1 | Assessment result coverage | Assessment Result |
| Criterion 5.1 | Evidence completeness | Course |
| Criterion 5.1 | Management questions | Calculated in browser / registry |
| Criterion 5.1.1 | Proposal approval | Course Proposal |
| Criterion 5.1.1 | Proposal decision time | Course Proposal |
| Criterion 5.1.1 | Module evidence completeness | Course |
| Criterion 5.1.1 | Learning outcomes coverage | Course |
| Criterion 5.1.1 | Lesson-plan coverage | Course |
| Criterion 5.1.1 | Assessment-design coverage | Assessment Plan |
| Criterion 5.1.1 | Review status | Course Review |
| Criterion 5.1.1 | Result coverage | Assessment Result |
| Criterion 5.1.2 | Module review coverage | Module Review |
| Criterion 5.1.2 | Course review coverage | Course Review |
| Criterion 5.1.2 | Review status | Module Review, Course Review |
| Criterion 5.1.2 | Overdue reviews | Course Review |
| Criterion 5.1.2 | Action-plan availability | Module Review |
| Criterion 5.1.2 | Recommendation follow-up | Course Review |
| Criterion 5.2 | Scheduled classes | Course Schedule |
| Criterion 5.2 | Enrollment coverage | Course Enrollment |
| Criterion 5.2 | Attendance coverage | Student Attendance |
| Criterion 5.2 | Teacher assignment | Course Schedule |
| Criterion 5.2 | Room readiness | Course Schedule |
| Criterion 5.2 | Delivery controls | Course Schedule |
| Criterion 5.2.1 | Intake readiness | Student Intake No |
| Criterion 5.2.1 | Module class readiness | Module Class Details |
| Criterion 5.2.1 | Admission coverage | Student Admission UCC |
| Criterion 5.2.1 | Schedule coverage | Course Schedule |
| Criterion 5.2.1 | Teacher assignment | Module Class Details |
| Criterion 5.2.1 | Contract date completeness | Student Admission UCC |
| Criterion 5.2.2 | Delivery readiness | Module Class Details |
| Criterion 5.2.2 | Observation coverage | Classroom Observation |
| Criterion 5.2.2 | Observation ratings | Classroom Observation |
| Criterion 5.2.2 | Survey coverage | Survey Response |
| Criterion 5.2.2 | Delivery exceptions | Classroom Observation |
| Criterion 5.2.2 | Teacher coverage | Module Class Details |
| Criterion 5.3 | Active agreements | Partnership Agreement |
| Criterion 5.3 | Agreement monitoring | Partnerships Agreement Management |
| Criterion 5.3 | Provider rating | Supplier Rating |
| Criterion 5.3 | Expiry coverage | Partnership Agreement |
| Criterion 5.3 | Evaluation coverage | Partnerships Agreement Management |
| Criterion 5.3 | Open partnership risks | Calculated in browser / registry |
| Criterion 5.3.1 | Agreement lifecycle | Partnership Agreement |
| Criterion 5.3.1 | Signature completion | Partnership Agreement |
| Criterion 5.3.1 | Monitoring frequency | Partnerships Agreement Management |
| Criterion 5.3.1 | Evaluation outcome | Partnerships Agreement Management |
| Criterion 5.3.1 | Provider rating | Supplier Rating |
| Criterion 5.3.1 | Renewal readiness | Partnership Agreement, Supplier Rating |
| Criterion 5.4 | Survey response coverage | Survey Response |
| Criterion 5.4 | Module survey score | Survey Response |
| Criterion 5.4 | Question-level score | Survey Response |
| Criterion 5.4 | Learning attendance | Student Attendance |
| Criterion 5.4 | Scheduled learning sessions | Course Schedule |
| Criterion 5.4 | At-risk indicators | Student Attendance |
| Criterion 5.5 | Assessment-plan coverage | Assessment Plan |
| Criterion 5.5 | Assessment-result coverage | Assessment Result |
| Criterion 5.5 | Grade availability | Assessment Result |
| Criterion 5.5 | Examiner assignment | Assessment Plan |
| Criterion 5.5 | Room assignment | Assessment Plan |
| Criterion 5.5 | Course assessment coverage | Course, Assessment Plan |
| Criterion 5 Data Quality | Missing fields | Course |
| Criterion 5 Data Quality | Invalid date order | Course Schedule |
| Criterion 5 Data Quality | Result completeness | Assessment Result |
| Criterion 5 Data Quality | Source availability | Calculated in browser / registry |
| Criterion 5 Sources | Source registry | Calculated in browser / registry |
| Criterion 5 Sources | Readable sources | Calculated in browser / registry |
| Criterion 5 Sources | Permission status | Calculated in browser / registry |
| Criterion 5 Sources | Record counts | Calculated in browser / registry |

## Confirmed calculation rules

### Attendance capture

```text
distinct selected Student Attendance.course_schedule
divided by
distinct selected Course Schedule.name
```

### Assessment-result coverage

```text
distinct selected Assessment Result.assessment_plan
divided by
selected Assessment Plan.name
```

### Course scope

```text
selected Student Group → use its course
otherwise selected Program → use Program child courses
otherwise → use all readable Course records
```

### Academic-Year schedule scope

Course Schedule does not provide a direct Academic Year field in the current
mapping. Schedule scope is derived through Student Group records associated
with the selected Academic Year.

## Readiness strip

Criterion 5 calculates expected source and metric availability for the active
section. Policy code remains “not configured” until an official code and
version are supplied.

## Empty data rule

A readable source with zero matching rows is available. Zero is a valid result,
not a missing metric.
