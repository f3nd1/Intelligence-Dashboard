# Criterion 5 Field Reference

## Active frontend fields

| DocType | Purpose | Configured fields |
| --- | --- | --- |
| Academic Year | Academic year filter | name, academic_year_name, year_start_date, year_end_date |
| Student Group | Module Class Details filter and class scope | name, student_group_name, academic_year, program, course, batch, disabled, max_strength |
| Course | 5.1 course design | name, course_name, department, modified |
| Program | 5.1 programme-course mapping | name, program_name, department, modified |
| Assessment Plan | 5.1 and 5.5 assessment planning | name, assessment_name, student_group, course, program, academic_year, schedule_date, room, examiner, supervisor, maximum_assessment_score |
| Assessment Result | 5.1 and 5.5 result coverage | name, assessment_plan, program, course, academic_year, student, student_name, student_group, maximum_score, total_score, grade |
| Course Schedule | 5.2 class delivery | name, student_group, instructor, instructor_name, course, schedule_date, room, from_time, to_time, program |
| Course Enrollment | 5.2 enrollment proxy | name, student, student_name, course, program, enrollment_date |
| Student Attendance | 5.2 attendance | name, student, course_schedule, date, student_group, status, duration_attended, expected_duration |
| Module Review | 5.1.2 module review records | name, course, module, module_class_details, date_of_review, status, type_of_review, recommendation, modified |
| Course Review | 5.1.2 course review records | name, course, review_date, next_review_date, review_type, review_status, modified |
| Student Intake No | 5.2.1 intake planning | name, batch_name, program, course_start_date, course_end_date, modified |
| Module Class Details | 5.2.1 and 5.2.2 module operations | name, program, course, custom_module_status, custom_instructor, custom_instructor_full_name, academic_year, modified |
| Student Admission UCC | 5.2.1 Shortlisted Applicants admissions and contracts | name, student_name, program, student_batch, application_status, contract_start, contract_end, modified |
| Classroom Observation | 5.2.2 teaching observation | name, date_of_observation, type_of_observation, module_class_details, course, module_name, name_of_teacher, platform_delivery, modified |
| Partnership Agreement | 5.3.1 signed partnership agreements | name, party_name, posting_date, start_date, end_date, pa_agreement_type, pa_partner_name, requires_nda, nda_acknowledged, signed_date, ucc_signed_date, modified |
| Partnerships Agreement Management | 5.3.1 partnership identification, monitoring and evaluation | name, agreement_title, party_name, type, status, agreement_date, expiry_date, average_identification_and_selection_score, modified |
| Supplier Rating | 5.3.1 Provider Rating evaluation records | name, posting_date, year, status, type, document, supplier, evaluation_stage, rating, rating_likert, modified |
| Survey Response | 5.4 survey scores and open-ended responses | name, title, email, program, course, posting_date, frequency, modified |

## Server Script migration fields

| API action | DocType | Fields requested |
| --- | --- | --- |
| base | Academic Year | name, academic_year_name, year_start_date, year_end_date |
| base | Student Group | name, student_group_name, academic_year, program, course, disabled |
| base | Course | name, course_name, department, modified |
| base | Program | name, program_name, department, modified |
| overview | Academic Year | name, academic_year_name, year_start_date, year_end_date |
| overview | Student Group | name, student_group_name, academic_year, program, course, disabled |
| overview | Course | name, course_name, department, modified |
| overview | Program | name, program_name, department, modified |
| c511_summary | Course Proposal | name, course_title, approval_status, proposed_date, decision_date, ssg_approval_date, modified |
| c511_summary | Course | name, course_name, department, modified |
| c511_summary | Program | name, program_name, department, modified |
| c511_summary | Course Review | name, course, review_date, review_status, next_review_date, modified |
| c511_summary | Assessment Plan | name, course, program, academic_year, assessment_name, modified |
| c511_proposals | Course Proposal | name, course_title, approval_status, proposed_date, decision_date, ssg_approval_date, modified |
| c511_modules | Course | name, course_name, department, modified |
| c511_modules | Program | name, program_name, department, modified |
| c511_modules | Assessment Plan | name, course, program, academic_year, assessment_name, modified |
| c511_reviews | Course Review | name, course, review_date, review_status, next_review_date, modified |
| c511_gaps | Course Proposal | name, course_title, approval_status, proposed_date, decision_date, ssg_approval_date, modified |
| c511_gaps | Course | name, course_name, department, modified |
| c511_gaps | Course Review | name, course, review_date, review_status, next_review_date, modified |

## Criterion 5.1.1 extended field groups

The active frontend groups Course Proposal content into:

- overview;
- strategy;
- learner;
- pedagogy;
- curriculum;
- assessment;
- risk;
- approval.

The exact active group registry is preserved in
`RUNTIME_CONFIG_REFERENCE.md`.

## Load behavior

Sources marked `full: true` are loaded as richer operational records in the
frontend. Other sources use a selected field allow-list.

Full-record loading should be reduced during API migration where possible.
