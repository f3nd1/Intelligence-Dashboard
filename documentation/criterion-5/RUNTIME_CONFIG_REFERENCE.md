# Criterion 5 Runtime Configuration Reference

This file preserves the active source and section registries.

## Server Script allowed actions

```json
[
  "base",
  "overview",
  "c511_summary",
  "c511_proposals",
  "c511_modules",
  "c511_reviews",
  "c511_gaps"
]
```

## Server Script source map

```json
{
  "base": [
    [
      "Academic Year",
      [
        "name",
        "academic_year_name",
        "year_start_date",
        "year_end_date"
      ]
    ],
    [
      "Student Group",
      [
        "name",
        "student_group_name",
        "academic_year",
        "program",
        "course",
        "disabled"
      ]
    ],
    [
      "Course",
      [
        "name",
        "course_name",
        "department",
        "modified"
      ]
    ],
    [
      "Program",
      [
        "name",
        "program_name",
        "department",
        "modified"
      ]
    ]
  ],
  "overview": [
    [
      "Academic Year",
      [
        "name",
        "academic_year_name",
        "year_start_date",
        "year_end_date"
      ]
    ],
    [
      "Student Group",
      [
        "name",
        "student_group_name",
        "academic_year",
        "program",
        "course",
        "disabled"
      ]
    ],
    [
      "Course",
      [
        "name",
        "course_name",
        "department",
        "modified"
      ]
    ],
    [
      "Program",
      [
        "name",
        "program_name",
        "department",
        "modified"
      ]
    ]
  ],
  "c511_summary": [
    [
      "Course Proposal",
      [
        "name",
        "course_title",
        "approval_status",
        "proposed_date",
        "decision_date",
        "ssg_approval_date",
        "modified"
      ]
    ],
    [
      "Course",
      [
        "name",
        "course_name",
        "department",
        "modified"
      ]
    ],
    [
      "Program",
      [
        "name",
        "program_name",
        "department",
        "modified"
      ]
    ],
    [
      "Course Review",
      [
        "name",
        "course",
        "review_date",
        "review_status",
        "next_review_date",
        "modified"
      ]
    ],
    [
      "Assessment Plan",
      [
        "name",
        "course",
        "program",
        "academic_year",
        "assessment_name",
        "modified"
      ]
    ]
  ],
  "c511_proposals": [
    [
      "Course Proposal",
      [
        "name",
        "course_title",
        "approval_status",
        "proposed_date",
        "decision_date",
        "ssg_approval_date",
        "modified"
      ]
    ]
  ],
  "c511_modules": [
    [
      "Course",
      [
        "name",
        "course_name",
        "department",
        "modified"
      ]
    ],
    [
      "Program",
      [
        "name",
        "program_name",
        "department",
        "modified"
      ]
    ],
    [
      "Assessment Plan",
      [
        "name",
        "course",
        "program",
        "academic_year",
        "assessment_name",
        "modified"
      ]
    ]
  ],
  "c511_reviews": [
    [
      "Course Review",
      [
        "name",
        "course",
        "review_date",
        "review_status",
        "next_review_date",
        "modified"
      ]
    ]
  ],
  "c511_gaps": [
    [
      "Course Proposal",
      [
        "name",
        "course_title",
        "approval_status",
        "proposed_date",
        "decision_date",
        "ssg_approval_date",
        "modified"
      ]
    ],
    [
      "Course",
      [
        "name",
        "course_name",
        "department",
        "modified"
      ]
    ],
    [
      "Course Review",
      [
        "name",
        "course",
        "review_date",
        "review_status",
        "next_review_date",
        "modified"
      ]
    ]
  ]
}
```

## Active frontend CFG registry

```json
{
  "Academic Year": {
    "mode": "core",
    "purpose": "Academic year filter",
    "fields": [
      "name",
      "academic_year_name",
      "year_start_date",
      "year_end_date"
    ],
    "full": false
  },
  "Student Group": {
    "mode": "core",
    "purpose": "Module Class Details filter and class scope",
    "fields": [
      "name",
      "student_group_name",
      "academic_year",
      "program",
      "course",
      "batch",
      "disabled",
      "max_strength"
    ],
    "full": false
  },
  "Course": {
    "mode": "core",
    "purpose": "5.1 course design",
    "fields": [
      "name",
      "course_name",
      "department",
      "modified"
    ],
    "full": false
  },
  "Program": {
    "mode": "core",
    "purpose": "5.1 programme-course mapping",
    "fields": [
      "name",
      "program_name",
      "department",
      "modified"
    ],
    "full": false
  },
  "Assessment Plan": {
    "mode": "core",
    "purpose": "5.1 and 5.5 assessment planning",
    "fields": [
      "name",
      "assessment_name",
      "student_group",
      "course",
      "program",
      "academic_year",
      "schedule_date",
      "room",
      "examiner",
      "supervisor",
      "maximum_assessment_score"
    ],
    "full": false
  },
  "Assessment Result": {
    "mode": "core",
    "purpose": "5.1 and 5.5 result coverage",
    "fields": [
      "name",
      "assessment_plan",
      "program",
      "course",
      "academic_year",
      "student",
      "student_name",
      "student_group",
      "maximum_score",
      "total_score",
      "grade"
    ],
    "full": false
  },
  "Course Schedule": {
    "mode": "core",
    "purpose": "5.2 class delivery",
    "fields": [
      "name",
      "student_group",
      "instructor",
      "instructor_name",
      "course",
      "schedule_date",
      "room",
      "from_time",
      "to_time",
      "program"
    ],
    "full": false
  },
  "Course Enrollment": {
    "mode": "core",
    "purpose": "5.2 enrollment proxy",
    "fields": [
      "name",
      "student",
      "student_name",
      "course",
      "program",
      "enrollment_date"
    ],
    "full": false
  },
  "Student Attendance": {
    "mode": "core",
    "purpose": "5.2 attendance",
    "fields": [
      "name",
      "student",
      "course_schedule",
      "date",
      "student_group",
      "status",
      "duration_attended",
      "expected_duration"
    ],
    "full": false
  },
  "Module Review": {
    "mode": "core",
    "purpose": "5.1.2 module review records",
    "fields": [
      "name",
      "course",
      "module",
      "module_class_details",
      "date_of_review",
      "status",
      "type_of_review",
      "recommendation",
      "modified"
    ],
    "full": true
  },
  "Course Review": {
    "mode": "core",
    "purpose": "5.1.2 course review records",
    "fields": [
      "name",
      "course",
      "review_date",
      "next_review_date",
      "review_type",
      "review_status",
      "modified"
    ],
    "full": true
  },
  "Student Intake No": {
    "mode": "core",
    "purpose": "5.2.1 intake planning",
    "fields": [
      "name",
      "batch_name",
      "program",
      "course_start_date",
      "course_end_date",
      "modified"
    ],
    "full": true
  },
  "Module Class Details": {
    "mode": "core",
    "purpose": "5.2.1 and 5.2.2 module operations",
    "fields": [
      "name",
      "program",
      "course",
      "custom_module_status",
      "custom_instructor",
      "custom_instructor_full_name",
      "academic_year",
      "modified"
    ],
    "full": true
  },
  "Student Admission UCC": {
    "mode": "core",
    "purpose": "5.2.1 Shortlisted Applicants admissions and contracts",
    "fields": [
      "name",
      "student_name",
      "program",
      "student_batch",
      "application_status",
      "contract_start",
      "contract_end",
      "modified"
    ],
    "full": true
  },
  "Classroom Observation": {
    "mode": "core",
    "purpose": "5.2.2 teaching observation",
    "fields": [
      "name",
      "date_of_observation",
      "type_of_observation",
      "module_class_details",
      "course",
      "module_name",
      "name_of_teacher",
      "platform_delivery",
      "modified"
    ],
    "full": true
  },
  "Partnership Agreement": {
    "mode": "core",
    "purpose": "5.3.1 signed partnership agreements",
    "fields": [
      "name",
      "party_name",
      "posting_date",
      "start_date",
      "end_date",
      "pa_agreement_type",
      "pa_partner_name",
      "requires_nda",
      "nda_acknowledged",
      "signed_date",
      "ucc_signed_date",
      "modified"
    ],
    "full": true
  },
  "Partnerships Agreement Management": {
    "mode": "core",
    "purpose": "5.3.1 partnership identification, monitoring and evaluation",
    "fields": [
      "name",
      "agreement_title",
      "party_name",
      "type",
      "status",
      "agreement_date",
      "expiry_date",
      "average_identification_and_selection_score",
      "modified"
    ],
    "full": true
  },
  "Supplier Rating": {
    "mode": "core",
    "purpose": "5.3.1 Provider Rating evaluation records",
    "fields": [
      "name",
      "posting_date",
      "year",
      "status",
      "type",
      "document",
      "supplier",
      "evaluation_stage",
      "rating",
      "rating_likert",
      "modified"
    ],
    "full": true
  },
  "Survey Response": {
    "mode": "core",
    "purpose": "5.4 survey scores and open-ended responses",
    "fields": [
      "name",
      "title",
      "email",
      "program",
      "course",
      "posting_date",
      "frequency",
      "modified"
    ],
    "full": true
  }
}
```

## Active section registry — raw JavaScript

```javascript
const SECTION_REGISTRY = {
c51:{children:[
{id:"c51",label:"5.1 Overview"},
{id:"c511",label:"5.1.1 Course Design & Development"},
{id:"c512",label:"5.1.2 Course Review"}
]},
c52:{children:[
{id:"c52",label:"5.2 Overview"},
{id:"c521",label:"5.2.1 Course Planning"},
{id:"c522",label:"5.2.2 Course Delivery"}
]},
c53:{children:[
{id:"c53",label:"5.3 Overview"},
{id:"c531",label:"5.3.1 Partnerships"}
]}
};
```

## 5.1.1 source registry — raw JavaScript

```javascript
const C511_SOURCES = {
"Course Proposal":{fields:["name","creation","modified","owner","docstatus"],purpose:"Proposal and approvals"},
"Course Review":{fields:["name","creation","modified","owner","docstatus"],purpose:"Validation and improvement"}
};
```

## 5.1.1 field groups — raw JavaScript

```javascript
const C511_GROUPS = {
overview:["course_title","mode_of_delivery","academic_level","course_language","programme_structure","proposed_date"],
strategy:["overall_achievement","industry_relevance","skills_development","target_headcount","competitors"],
learner:["target_audience_industry","minimum_age","industry_experience","cognitive_level","prior_knowledge","learning_style","cognitive_development_focus","motivation_level","emotional_state","stress_resilience","social_engagement_level","peer_learning_engagement","teamwork_and_collaboration_skills","special_educational_needs","inclusivity_measures","learning_environment_support","learner_profile_characteristic","mer_academic","mer_language"],
pedagogy:["table_teqa","teaching_technique_offline","teacher_student_ratio_offline","teaching_technique_online","teacher_student_ratio_online","total_duration_ft","total_duration_pt","days_per_week_ft","hour_per_day_ft","days_per_week_pt","hour_per_day_pt","ft_contact_hour_total","pt_contact_hour_total"],
curriculum:["learning_outcomes","module_list","sequencing_and_rationale","course_developer","industrial_attachment_needead","industrial_attachment_details","articulation_pathway","pathway_programme_details","accrediation_y_n","accrediation_details","association_y_n","association_details"],
assessment:["assessment_criteria","assessmnet_descriptions"],
risk:["table_ornh","budget_management","total_budget_fee","total_actual_spending","resource_childable","risk_table","risk_mitigation_childtable","table_odgh","stakeholder_note","documentation_table"],
approval:["approval_status","decision_date","quality_meeting","ssg_approval_date","decision_summary"]
};
```

## Criterion 5 readiness registry — raw JavaScript

```javascript
const C5_READINESS = Object.freeze({
overview:{label:"Criterion 5 Overview",sources:["Academic Year","Student Group","Course","Program"],metrics:[["Courses in selected scope",["Course"]],["Module readiness",["Course"]],["Course-to-programme mapping",["Course","Program"]],["Source availability",[]],["Questions answered",[]],["Open exceptions",[]]]},
c51:{label:"Criterion 5.1",sources:["Course","Program","Assessment Plan","Assessment Result"],metrics:[["Course mapping",["Course","Program"]],["Configuration readiness",["Course"]],["Assessment planning coverage",["Assessment Plan"]],["Assessment result coverage",["Assessment Result"]],["Evidence completeness",["Course"]],["Management questions",[]]]},
c511:{label:"Criterion 5.1.1",sources:["Course","Program","Course Proposal","Course Review","Assessment Plan","Assessment Result"],metrics:[["Proposal approval",["Course Proposal"]],["Proposal decision time",["Course Proposal"]],["Module evidence completeness",["Course"]],["Learning outcomes coverage",["Course"]],["Lesson-plan coverage",["Course"]],["Assessment-design coverage",["Assessment Plan"]],["Review status",["Course Review"]],["Result coverage",["Assessment Result"]]]},
c512:{label:"Criterion 5.1.2",sources:["Module Review","Course Review"],metrics:[["Module review coverage",["Module Review"]],["Course review coverage",["Course Review"]],["Review status",["Module Review","Course Review"]],["Overdue reviews",["Course Review"]],["Action-plan availability",["Module Review"]],["Recommendation follow-up",["Course Review"]]]},
c52:{label:"Criterion 5.2",sources:["Course Schedule","Course Enrollment","Student Attendance"],metrics:[["Scheduled classes",["Course Schedule"]],["Enrollment coverage",["Course Enrollment"]],["Attendance coverage",["Student Attendance"]],["Teacher assignment",["Course Schedule"]],["Room readiness",["Course Schedule"]],["Delivery controls",["Course Schedule"]]]},
c521:{label:"Criterion 5.2.1",sources:["Student Intake No","Module Class Details","Student Admission UCC","Course Schedule"],metrics:[["Intake readiness",["Student Intake No"]],["Module class readiness",["Module Class Details"]],["Admission coverage",["Student Admission UCC"]],["Schedule coverage",["Course Schedule"]],["Teacher assignment",["Module Class Details"]],["Contract date completeness",["Student Admission UCC"]]]},
c522:{label:"Criterion 5.2.2",sources:["Module Class Details","Classroom Observation","Survey Response"],metrics:[["Delivery readiness",["Module Class Details"]],["Observation coverage",["Classroom Observation"]],["Observation ratings",["Classroom Observation"]],["Survey coverage",["Survey Response"]],["Delivery exceptions",["Classroom Observation"]],["Teacher coverage",["Module Class Details"]]]},
c53:{label:"Criterion 5.3",sources:["Partnership Agreement","Partnerships Agreement Management","Supplier Rating"],metrics:[["Active agreements",["Partnership Agreement"]],["Agreement monitoring",["Partnerships Agreement Management"]],["Provider rating",["Supplier Rating"]],["Expiry coverage",["Partnership Agreement"]],["Evaluation coverage",["Partnerships Agreement Management"]],["Open partnership risks",[]]]},
c531:{label:"Criterion 5.3.1",sources:["Partnership Agreement","Partnerships Agreement Management","Supplier Rating"],metrics:[["Agreement lifecycle",["Partnership Agreement"]],["Signature completion",["Partnership Agreement"]],["Monitoring frequency",["Partnerships Agreement Management"]],["Evaluation outcome",["Partnerships Agreement Management"]],["Provider rating",["Supplier Rating"]],["Renewal readiness",["Partnership Agreement","Supplier Rating"]]]},
c54:{label:"Criterion 5.4",sources:["Survey Response","Course Schedule","Student Attendance"],metrics:[["Survey response coverage",["Survey Response"]],["Module survey score",["Survey Response"]],["Question-level score",["Survey Response"]],["Learning attendance",["Student Attendance"]],["Scheduled learning sessions",["Course Schedule"]],["At-risk indicators",["Student Attendance"]]]},
c55:{label:"Criterion 5.5",sources:["Assessment Plan","Assessment Result","Course","Student Group"],metrics:[["Assessment-plan coverage",["Assessment Plan"]],["Assessment-result coverage",["Assessment Result"]],["Grade availability",["Assessment Result"]],["Examiner assignment",["Assessment Plan"]],["Room assignment",["Assessment Plan"]],["Course assessment coverage",["Course","Assessment Plan"]]]},
quality:{label:"Criterion 5 Data Quality",sources:["Course","Program","Course Schedule","Assessment Result"],metrics:[["Missing fields",["Course"]],["Invalid date order",["Course Schedule"]],["Result completeness",["Assessment Result"]],["Source availability",[]]]},
sources:{label:"Criterion 5 Sources",sources:Object.keys(CFG),metrics:[["Source registry",[]],["Readable sources",[]],["Permission status",[]],["Record counts",[]]]}
});
```
