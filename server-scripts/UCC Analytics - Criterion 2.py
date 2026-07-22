"""
UCC Intelligence Platform Server Script

Visible name:
    UCC Analytics - Criterion 2

Script type:
    API

API method:
    ucc_analytics_criterion_2

Purpose:
    Return a permission-aware, evidence-based management analytics catalogue for
    EduTrust Criterion 2. The script separates management questions from
    supporting record counts, adds Criterion 2.2.2, and does not infer compliance
    where the required relationship, denominator, approval trail or field is not
    installed.

Revision:
    Criterion 2 catalogue version 2.0.0
    UCC Intelligence Platform version 1.10.0

Deployment:
    Allow Guest must remain disabled.

Important design rules:
    1. Missing evidence is reported as unavailable, not converted to zero.
    2. Partial proxy calculations are labelled clearly and never presented as
       full compliance conclusions.
    3. Permission-aware frappe.get_list calls are used for all live records.
    4. Drill-down rows are restricted to approved safe fields.
"""

payload_input = frappe.form_dict.get("payload") or {}
payload = json.loads(payload_input) if isinstance(payload_input, str) else payload_input
if not isinstance(payload, dict):
    payload = {}

action = payload.get("action") or "summary"
subcriterion = payload.get("subcriterion") or "2.1.1"
filters = payload.get("filters") or {}
metric_id = payload.get("metric_id")
page = payload.get("page") or 1
page_size = payload.get("page_size") or 50
row_limit = payload.get("limit") or 2000

try:
    page = max(1, int(page))
except Exception:
    page = 1

try:
    page_size = max(1, min(int(page_size), 200))
except Exception:
    page_size = 50

try:
    row_limit = max(1, min(int(row_limit), 5000))
except Exception:
    row_limit = 2000

ALLOWED_ACTIONS = [
    "summary",
    "source_status",
    "policy_registry",
    "question_catalogue",
    "drilldown"
]
if action not in ALLOWED_ACTIONS:
    frappe.throw("Unsupported Criterion 2 action.")

POLICY_REGISTRY = {
    "overview": {
        "title": "Criterion 2 Overview",
        "policy": "Criterion 2 consolidated management view",
        "version": "2.0.0",
        "notes": "The overview combines only known, requirement-scoped exception proxies."
    },
    "2.1.1": {
        "title": "Staff Selection and Management",
        "policy": "PPD-OEE-HR-2.1.1",
        "version": "2.2"
    },
    "2.1.2": {
        "title": "Staff Training and Development",
        "policy": "PPD-OEE-HR-2.1.2",
        "version": "1.2"
    },
    "2.2.1": {
        "title": "Internal Communication",
        "policy": "PPD-SES-MG-2.2.1",
        "version": "1.2"
    },
    "2.2.2": {
        "title": "External Communication including Marketing",
        "policy": "PPD-SES-MG-2.2.1",
        "version": "1.2",
        "notes": "This subcriterion is governed by the combined Internal and External Communication procedure."
    },
    "2.3.1": {
        "title": "Data and Information Management",
        "policy": "PPD-OEE-IT-2.3.1",
        "version": "1.2"
    },
    "2.3.2": {
        "title": "Knowledge Management",
        "policy": "PPD-OE-IT-2.3.2",
        "version": "1.2"
    },
    "2.4.1": {
        "title": "Feedback Management",
        "policy": "PPD-SGL-SQ-2.4.1",
        "version": "2.3"
    },
    "2.4.2": {
        "title": "Student Satisfaction Survey",
        "policy": "PPD-SGL-SQ-2.4.2",
        "version": "2.2",
        "notes": "The controlled procedure contains a requirement-numbering inconsistency; the analytics uses the subcriterion title rather than the disputed requirement numbers."
    },
    "2.4.3": {
        "title": "Staff Satisfaction Survey",
        "policy": "PPD-SGL-SQ-2.4.3",
        "version": "2.2"
    }
}

SOURCE_CANDIDATES = {
    "employee": ["Employee"],
    "job_applicant": ["Job Applicant"],
    "job_requisition": ["Job Requisition"],
    "interview_feedback": ["Interview Feedback"],
    "employee_onboarding": ["Employee Onboarding"],
    "employee_separation": ["Employee Separation"],
    "exit_interview": ["Exit Interview", "Exit Interview Form"],
    "appraisal": ["Appraisal", "Performance Appraisal"],
    "training_event": ["Training Event"],
    "tna": ["Training Needs Analysis", "Training Needs Assessment"],
    "training_program": ["Training Program"],
    "training_result": ["Training Result"],
    "training_feedback": ["Training Feedback"],
    "training_sponsorship": ["Training Sponsorship Application"],
    "stakeholder_registry": ["Stakeholder Registry"],
    "stakeholder_engagement": ["Stakeholder Engagement Strategy"],
    "material_vetting": ["Material Vetting", "Material Vetting Form"],
    "essential_information": ["Essential Information"],
    "document_control": ["Document Control"],
    "quality_performance": ["Quality Performance Outcomes"],
    "quality_monitoring": ["Quality Monitoring Record", "QMR"],
    "quality_meeting": ["Quality Meeting"],
    "quality_action": ["Quality Action"],
    "survey_management": ["Survey Management"],
    "survey_tracking": ["Survey Tracking", "Survey Response"],
    "helpdesk_ticket": ["HD Ticket", "Issue", "Helpdesk Ticket"],
    "employee_grievance": ["Employee Grievance"],
    "manpower_planning": ["Manpower Planning and Deployment"],
    "salary_structure": ["Salary Structure"],
    "salary_component": ["Salary Component"],
    "todo": ["ToDo", "To Do"],
    "print_format": ["Print Format"],
    "letter_head": ["Letter Head"],
    "data_asset_inventory": ["Data Asset Inventory"],
    "course_review": ["Course Review Report", "Course Review"],
    "module_review": ["Module Review Report", "Module Review"],
    "student_onboarding_survey": ["Student Onboarding Survey"],
    "end_module_survey": ["End of Module Survey (Student)", "End of Module Survey"],
    "end_course_survey": ["End of Course Survey"],
    "staff_onboarding_survey": ["Staff Onboarding Survey"],
    "staff_survey": ["Staff Survey"],
    "exit_interview_survey": ["Exit Interview Survey"]
}

SAFE_FIELDS = {
    "employee": [
        "name", "employee_name", "status", "department", "designation",
        "date_of_joining", "relieving_date", "employment_type", "company",
        "user_id", "modified"
    ],
    "job_applicant": [
        "name", "applicant_name", "status", "job_title", "job_opening",
        "email_id", "creation", "modified"
    ],
    "job_requisition": [
        "name", "designation", "department", "status", "requested_by",
        "expected_by", "no_of_positions", "reason_for_request",
        "description", "creation", "modified"
    ],
    "interview_feedback": [
        "name", "interview", "interviewer", "job_applicant", "result",
        "average_rating", "modified"
    ],
    "employee_onboarding": [
        "name", "employee", "employee_name", "job_applicant",
        "date_of_joining", "boarding_status", "status", "modified"
    ],
    "employee_separation": [
        "name", "employee", "employee_name", "separation_date",
        "boarding_status", "status", "modified"
    ],
    "exit_interview": [
        "name", "employee", "employee_name", "date", "status",
        "reason_for_leaving", "modified"
    ],
    "appraisal": [
        "name", "employee", "employee_name", "status", "start_date",
        "end_date", "appraisal_cycle", "final_score", "modified"
    ],
    "training_event": [
        "name", "event_name", "training_program", "status", "start_time",
        "end_time", "type", "trainer_name", "modified"
    ],
    "tna": [
        "name", "participant_type", "participant_doctype", "participant",
        "participant_full_name", "employee_id", "employee_full_name",
        "source_type", "department", "manpower_planning_and_development",
        "employee_onboarding", "appraisal_link", "academic_year",
        "assessment_date", "assessed_by", "assessed_by_full_name",
        "review_date", "reviewed_by", "reviewed_by_full_name",
        "performance_evaluation", "index_value", "improvement_average",
        "conclusion", "list_of_trainings", "total_estimated_cost",
        "appraisal", "amended_from", "modified"
    ],
    "training_program": [
        "name", "training_program", "program_name", "status", "start_date",
        "end_date", "modified"
    ],
    "training_result": [
        "name", "employee", "training_event", "status", "result", "score",
        "modified"
    ],
    "training_feedback": [
        "name", "employee", "training_event", "rating", "score", "status",
        "modified"
    ],
    "training_sponsorship": [
        "name", "employee", "training_program", "status", "amount",
        "posting_date", "modified"
    ],
    "stakeholder_registry": [
        "name", "stakeholder_name", "stakeholder_type", "category", "status",
        "department", "modified"
    ],
    "stakeholder_engagement": [
        "name", "stakeholder", "stakeholder_group", "engagement_type",
        "communication_channel", "channel", "frequency",
        "engagement_frequency", "content_purpose", "purpose", "owner",
        "responsible_person", "status", "engagement_date",
        "next_engagement_date", "modified"
    ],
    "material_vetting": [
        "name", "naming_series", "material_name", "type", "requestor_name",
        "full_name", "department", "posting_date", "duration_of_use",
        "marketing_channel", "target_audience", "geographic_scope",
        "version_no", "material_attachment", "description_of_request",
        "reason_for_request", "impact_analysis", "impact_description",
        "external_parties", "vetter", "vetter_name", "amendments",
        "general_comment", "final_approval_date", "approval_status",
        "workflow_state", "approved_by", "approved_by_full_name",
        "approval_remarks", "publication_date", "published_on",
        "published_version", "modified"
    ],
    "essential_information": [
        "name", "title", "information_type", "status", "effective_date",
        "review_date", "next_review_date", "owner", "approval_status",
        "workflow_state", "approved_by", "approved_on", "disseminated_on",
        "communication_channel", "modified"
    ],
    "document_control": [
        "name", "document_title", "document_type", "document_code", "version",
        "status", "effective_date", "review_date", "next_review_date",
        "department", "owner", "prepared_by", "reviewed_by", "approved_by",
        "approval_date", "change_summary", "request_reference",
        "archive_date", "retention_end_date", "disposal_status",
        "disposal_date", "modified"
    ],
    "quality_performance": [
        "name", "outcome", "outcome_category", "indicator", "status",
        "target", "actual", "measurement_date", "owner", "procedure",
        "criterion", "modified"
    ],
    "quality_monitoring": [
        "name", "status", "review_period", "year", "meeting_date",
        "procedure", "criterion", "owner", "modified"
    ],
    "quality_meeting": [
        "name", "meeting_date", "status", "review", "procedure", "criterion",
        "minutes", "decision", "modified"
    ],
    "quality_action": [
        "name", "status", "custom_status_updates", "date",
        "custom_proposed_date", "custom_completed_date", "feedback",
        "criterion", "subcriterion", "procedure", "reference_type",
        "reference_name", "assigned_to", "owner", "effectiveness_status",
        "modified"
    ],
    "survey_management": [
        "name", "survey_name", "survey_type", "status", "start_date",
        "end_date", "audience", "approval_status", "approved_by",
        "approved_on", "survey_cycle", "target_score", "rating_scale",
        "modified"
    ],
    "survey_tracking": [
        "name", "survey", "survey_type", "respondent_type", "status",
        "response_date", "rating", "score", "employee", "student",
        "survey_cycle", "valid_response", "modified"
    ],
    "helpdesk_ticket": [
        "name", "subject", "status", "priority", "ticket_type", "category",
        "sub_category", "agreement_status", "opening_date", "response_by",
        "first_response_time", "acknowledgement_date", "resolution_by",
        "resolution_date", "feedback_rating", "urgency", "impact",
        "priority_score", "assigned_to", "modified"
    ],
    "employee_grievance": [
        "name", "employee", "employee_name", "status", "grievance_type",
        "posting_date", "resolution_date", "escalation_stage", "outcome",
        "modified"
    ],
    "manpower_planning": [
        "name", "department", "status", "year", "number_of_positions",
        "required_positions", "current_headcount", "gap", "owner",
        "review_date", "approved_by", "approval_date", "modified"
    ],
    "salary_structure": [
        "name", "is_active", "company", "payroll_frequency", "currency",
        "modified"
    ],
    "salary_component": [
        "name", "type", "depends_on_payment_days", "is_tax_applicable",
        "disabled", "modified"
    ],
    "todo": [
        "name", "status", "priority", "date", "allocated_to",
        "reference_type", "reference_name", "description", "modified"
    ],
    "print_format": [
        "name", "doc_type", "disabled", "standard", "custom_format",
        "modified"
    ],
    "letter_head": ["name", "is_default", "disabled", "modified"],
    "data_asset_inventory": [
        "name", "asset_name", "status", "owner", "retention_period",
        "retention_end_date", "backup_status", "disposal_status", "modified"
    ],
    "course_review": [
        "name", "course", "status", "review_date", "approved_by",
        "approval_date", "quality_action", "modified"
    ],
    "module_review": [
        "name", "module", "status", "review_date", "approved_by",
        "approval_date", "quality_action", "modified"
    ],
    "student_onboarding_survey": [
        "name", "student", "status", "survey_date", "rating", "score",
        "modified"
    ],
    "end_module_survey": [
        "name", "student", "module", "program", "status", "survey_date",
        "rating", "score", "modified"
    ],
    "end_course_survey": [
        "name", "student", "program", "status", "survey_date", "rating",
        "score", "modified"
    ],
    "staff_onboarding_survey": [
        "name", "employee", "status", "survey_date", "rating", "score",
        "modified"
    ],
    "staff_survey": [
        "name", "employee", "status", "survey_date", "rating", "score",
        "modified"
    ],
    "exit_interview_survey": [
        "name", "employee", "status", "survey_date", "rating", "score",
        "modified"
    ]
}

FILTER_FIELD_CANDIDATES = {
    "status": ["status", "boarding_status", "agreement_status"],
    "year": ["year", "academic_year", "monitoring_year"],
    "review_year": ["year", "academic_year", "monitoring_year"],
    "department": ["department"],
    "employee": ["employee", "employee_name"],
    "survey_type": ["survey_type", "type"],
    "survey_cycle": ["survey_cycle"],
    "month": ["month"]
}

FEEDBACK_SCOPE_GROUP = {
    "logic": "any",
    "required": True,
    "conditions": [
        {
            "field": ["ticket_type"],
            "op": "contains_any",
            "values": ["feedback", "complaint", "grievance", "dispute"],
            "optional": True
        },
        {
            "field": ["category"],
            "op": "contains_any",
            "values": ["feedback", "complaint", "grievance", "dispute"],
            "optional": True
        },
        {
            "field": ["subject"],
            "op": "contains_any",
            "values": ["feedback", "complaint", "grievance", "dispute"],
            "optional": True
        }
    ]
}

STUDENT_SURVEY_SCOPE_GROUP = {
    "logic": "any",
    "required": True,
    "conditions": [
        {
            "field": ["respondent_type"],
            "op": "contains_any",
            "values": ["student", "learner"],
            "optional": True
        },
        {
            "field": ["survey_type"],
            "op": "contains_any",
            "values": ["student"],
            "optional": True
        }
    ]
}

STAFF_SURVEY_SCOPE_GROUP = {
    "logic": "any",
    "required": True,
    "conditions": [
        {
            "field": ["respondent_type"],
            "op": "contains_any",
            "values": ["staff", "employee"],
            "optional": True
        },
        {
            "field": ["survey_type"],
            "op": "contains_any",
            "values": ["staff", "employee"],
            "optional": True
        }
    ]
}


def unsupported_metric(metric_id_value, label, message, support_status, requirement_basis, decision_use):
    return {
        "id": metric_id_value,
        "label": label,
        "mode": "unsupported",
        "category": "management",
        "support_status": support_status,
        "message": message,
        "requirement_basis": requirement_basis,
        "decision_use": decision_use
    }


CONFIG = {
    "overview": {
        "sources": [
            "job_requisition", "material_vetting", "essential_information",
            "document_control", "helpdesk_ticket"
        ],
        "metrics": [
            {
                "id": "ov-open-requisitions",
                "label": "Open or pending job requisitions",
                "source": "job_requisition",
                "mode": "in",
                "field": ["status"],
                "values": ["Open", "Pending"],
                "category": "supporting",
                "is_exception": True
            },
            {
                "id": "ov-pending-communications",
                "label": "Pending communication approvals",
                "source": "material_vetting",
                "mode": "in",
                "field": ["approval_status", "workflow_state"],
                "values": [
                    "Pending", "In Progress", "Requires Amendments",
                    "Waiting to Vet", "Waiting for Approval", "Draft"
                ],
                "category": "supporting",
                "is_exception": True
            },
            {
                "id": "ov-overdue-essential",
                "label": "Essential Information overdue for review",
                "source": "essential_information",
                "mode": "date_before_today",
                "field": ["next_review_date"],
                "category": "supporting",
                "is_exception": True
            },
            {
                "id": "ov-overdue-documents",
                "label": "Controlled documents overdue for review",
                "source": "document_control",
                "mode": "date_before_today",
                "field": ["next_review_date"],
                "category": "supporting",
                "is_exception": True
            },
            {
                "id": "ov-feedback-sla-failed",
                "label": "Feedback or complaint tickets with failed SLA",
                "source": "helpdesk_ticket",
                "mode": "conditions",
                "condition_groups": [
                    FEEDBACK_SCOPE_GROUP,
                    {
                        "logic": "all",
                        "required": True,
                        "conditions": [
                            {
                                "field": ["agreement_status"],
                                "op": "equals",
                                "value": "Failed"
                            }
                        ]
                    }
                ],
                "category": "supporting",
                "is_exception": True
            },
            {
                "id": "ov-known-attention-total",
                "label": "Known live exception records requiring attention",
                "mode": "derived_sum",
                "refs": [
                    "ov-open-requisitions", "ov-pending-communications",
                    "ov-overdue-essential", "ov-overdue-documents",
                    "ov-feedback-sla-failed"
                ],
                "category": "management",
                "support_status": "partial",
                "limitations": [
                    "This total combines known live exception proxies and is not a count of unique controls.",
                    "Unsupported mandatory evidence gaps are reported separately and are not included in the numeric total."
                ],
                "requirement_basis": "Criterion 2 management attention queue",
                "decision_use": "Prioritise immediate follow-up on known open, pending, overdue or failed-SLA records.",
                "is_exception": True
            },
            unsupported_metric(
                "ov-requirement-evidence-coverage",
                "Requirement evidence coverage",
                "An approved requirement-to-evidence registry and evidence-state rules are required before requirement coverage can be calculated.",
                "requires_additional_field",
                "Criterion 2 audit readiness",
                "Determine which mandatory requirements have live, document-only or missing evidence."
            )
        ]
    },
    "2.1.1": {
        "sources": [
            "employee", "job_requisition", "job_applicant",
            "interview_feedback", "employee_onboarding", "appraisal",
            "employee_separation", "exit_interview", "manpower_planning",
            "salary_structure", "salary_component"
        ],
        "metrics": [
            {
                "id": "c211-active-employees",
                "label": "Active employees",
                "source": "employee",
                "mode": "equals",
                "field": ["status"],
                "value": "Active",
                "category": "supporting"
            },
            {
                "id": "c211-requisitions",
                "label": "Job requisitions",
                "source": "job_requisition",
                "mode": "all",
                "category": "supporting"
            },
            {
                "id": "c211-open-requisitions",
                "label": "Open or pending job requisitions",
                "source": "job_requisition",
                "mode": "in",
                "field": ["status"],
                "values": ["Open", "Pending"],
                "category": "supporting",
                "is_exception": True
            },
            {
                "id": "c211-approved-requisitions",
                "label": "Approved job requisitions",
                "source": "job_requisition",
                "mode": "equals",
                "field": ["status"],
                "value": "Approved",
                "category": "supporting"
            },
            {
                "id": "c211-complete-approved-requisitions",
                "label": "Approved requisitions with the available required fields",
                "source": "job_requisition",
                "mode": "conditions",
                "required_fields": [
                    ["designation"], ["department"], ["requested_by"],
                    ["expected_by"], ["no_of_positions"]
                ],
                "condition_groups": [
                    {
                        "logic": "all",
                        "required": True,
                        "conditions": [
                            {
                                "field": ["status"],
                                "op": "equals",
                                "value": "Approved"
                            }
                        ]
                    }
                ],
                "category": "supporting"
            },
            {
                "id": "c211-requisition-compliance-proxy",
                "label": "Approved requisition completeness proxy",
                "mode": "derived_percent",
                "numerator_ref": "c211-complete-approved-requisitions",
                "denominator_ref": "c211-approved-requisitions",
                "category": "management",
                "support_status": "partial",
                "limitations": [
                    "This proxy checks only installed requisition fields.",
                    "It does not prove that every recruitment exercise began with the requisition or that the correct approval authority acted before sourcing."
                ],
                "requirement_basis": "Approved job requisition and role definition",
                "decision_use": "Identify approved requisitions that are incomplete before recruitment continues."
            },
            {
                "id": "c211-selected-applicants",
                "label": "Selected or accepted applicants",
                "source": "job_applicant",
                "mode": "in",
                "field": ["status"],
                "values": ["Accepted", "Selected", "Offer Accepted", "Approved"],
                "category": "supporting"
            },
            {
                "id": "c211-onboardings",
                "label": "Employee onboarding records",
                "source": "employee_onboarding",
                "mode": "all",
                "category": "supporting"
            },
            {
                "id": "c211-completed-onboardings",
                "label": "Completed employee onboarding records",
                "source": "employee_onboarding",
                "mode": "in",
                "field": ["boarding_status", "status"],
                "values": ["Completed", "Closed"],
                "category": "supporting"
            },
            {
                "id": "c211-onboarding-completion-proxy",
                "label": "Onboarding status completion proxy",
                "mode": "derived_percent",
                "numerator_ref": "c211-completed-onboardings",
                "denominator_ref": "c211-onboardings",
                "category": "management",
                "support_status": "partial",
                "limitations": [
                    "A completed status does not prove completion of each required induction, access, acknowledgement or document checklist item."
                ],
                "requirement_basis": "Staff onboarding and service readiness",
                "decision_use": "Follow up onboarding records that are not completed."
            },
            {
                "id": "c211-appraisals",
                "label": "Performance appraisal records",
                "source": "appraisal",
                "mode": "all",
                "category": "supporting"
            },
            {
                "id": "c211-separations",
                "label": "Employee separation records",
                "source": "employee_separation",
                "mode": "all",
                "category": "supporting"
            },
            {
                "id": "c211-exit-interviews",
                "label": "Exit interview records",
                "source": "exit_interview",
                "mode": "all",
                "category": "supporting"
            },
            {
                "id": "c211-manpower-plans",
                "label": "Manpower planning records",
                "source": "manpower_planning",
                "mode": "all",
                "category": "supporting"
            },
            {
                "id": "c211-salary-structures",
                "label": "Salary structures",
                "source": "salary_structure",
                "mode": "all",
                "category": "supporting"
            },
            {
                "id": "c211-salary-components",
                "label": "Salary components",
                "source": "salary_component",
                "mode": "all",
                "category": "supporting"
            },
            unsupported_metric(
                "c211-manpower-treatment",
                "Manpower gaps with approved treatment",
                "A relationship from each positive manpower gap to an approved requisition, redeployment decision or documented deferment is required.",
                "requires_relationship",
                "Manpower planning and deployment",
                "Approve recruitment, redeployment or a documented decision to defer action."
            ),
            unsupported_metric(
                "c211-candidate-compliance",
                "Candidate competency, qualification and approval compliance",
                "Candidate-level links to the approved competency threshold, qualification evidence, and applicable HOD, HR, Principal, Academic Board and SSG approvals are required.",
                "requires_relationship",
                "Competency-based recruitment and teaching staff approval controls",
                "Prevent appointment or deployment when mandatory evidence is incomplete."
            ),
            unsupported_metric(
                "c211-appraisal-decision-traceability",
                "Appraisal and decision traceability",
                "The approved appraisal population and links from appraisal results to development, reward, retention and succession decisions are required.",
                "requires_relationship",
                "Performance management, rewards, retention and succession",
                "Confirm overdue appraisals and untraceable management decisions."
            ),
            unsupported_metric(
                "c211-offboarding-completeness",
                "Offboarding and access removal completeness",
                "A separation checklist linking clearance, returned assets, exit feedback and access revocation is required.",
                "requires_relationship",
                "Employee offboarding and retention review",
                "Escalate incomplete separation controls and recurring retention risks."
            )
        ]
    },
    "2.1.2": {
        "sources": [
            "employee", "appraisal", "training_event", "tna",
            "training_program", "training_result", "training_feedback",
            "training_sponsorship"
        ],
        "metrics": [
            {
                "id": "c212-training-events",
                "label": "Training events",
                "source": "training_event",
                "mode": "all",
                "category": "supporting"
            },
            {
                "id": "c212-completed-events",
                "label": "Completed training events",
                "source": "training_event",
                "mode": "in",
                "field": ["status"],
                "values": ["Completed", "Closed"],
                "category": "supporting"
            },
            {
                "id": "c212-tna",
                "label": "Training needs assessments",
                "source": "tna",
                "mode": "all",
                "category": "supporting"
            },
            {
                "id": "c212-reviewed-tna",
                "label": "Training needs assessments with reviewer and review date",
                "source": "tna",
                "mode": "all_required",
                "required_fields": [["reviewed_by"], ["review_date"]],
                "category": "supporting"
            },
            {
                "id": "c212-tna-review-proxy",
                "label": "TNA review completion proxy",
                "mode": "derived_percent",
                "numerator_ref": "c212-reviewed-tna",
                "denominator_ref": "c212-tna",
                "category": "management",
                "support_status": "partial",
                "limitations": [
                    "This proxy checks reviewer and review date only.",
                    "It does not prove discussion, Principal approval, priority, approved budget or coverage of the applicable staff population."
                ],
                "requirement_basis": "Training needs identification, discussion, review and approval",
                "decision_use": "Follow up TNA records without a reviewer or review date."
            },
            {
                "id": "c212-programs",
                "label": "Training programmes",
                "source": "training_program",
                "mode": "all",
                "category": "supporting"
            },
            {
                "id": "c212-results",
                "label": "Training result records",
                "source": "training_result",
                "mode": "all",
                "category": "supporting"
            },
            {
                "id": "c212-completed-results",
                "label": "Completed or passed training results",
                "source": "training_result",
                "mode": "in",
                "field": ["status", "result"],
                "values": ["Completed", "Passed", "Pass"],
                "category": "supporting"
            },
            {
                "id": "c212-feedback",
                "label": "Training feedback records",
                "source": "training_feedback",
                "mode": "all",
                "category": "supporting"
            },
            {
                "id": "c212-feedback-rating",
                "label": "Average training feedback rating",
                "source": "training_feedback",
                "mode": "average_fields",
                "fields": [["rating", "score"]],
                "unit": "rating",
                "category": "supporting",
                "support_status": "partial",
                "limitations": [
                    "The rating scale and target are not defined in this analytics script.",
                    "Reaction feedback is not equivalent to learning, workplace application or organisational impact."
                ]
            },
            {
                "id": "c212-sponsorship",
                "label": "Training sponsorship applications",
                "source": "training_sponsorship",
                "mode": "all",
                "category": "supporting"
            },
            unsupported_metric(
                "c212-plan-sufficiency",
                "Approved training plan sufficiency",
                "A link from approved TNA priorities to the annual training plan, schedule and approved funding is required.",
                "requires_relationship",
                "Training planning, scheduling and budget",
                "Identify priority training needs that are not scheduled or funded."
            ),
            unsupported_metric(
                "c212-mandatory-training-completion",
                "Mandatory and role-specific training completion",
                "Employee-to-training assignment, attendance and completion child-table relationships are required.",
                "requires_relationship",
                "Mandatory, onboarding and role-specific training",
                "Escalate overdue or incomplete required training."
            ),
            unsupported_metric(
                "c212-effectiveness",
                "Training effectiveness",
                "Linked evidence is required for learning assessment, workplace application and organisational outcomes. Attendance, pass status and satisfaction alone are insufficient.",
                "requires_relationship",
                "Training effectiveness and continual improvement",
                "Retain, revise or discontinue training based on verified effectiveness."
            )
        ]
    },
    "2.2.1": {
        "sources": [
            "stakeholder_registry", "stakeholder_engagement",
            "essential_information", "survey_management", "survey_tracking",
            "quality_meeting", "quality_action"
        ],
        "metrics": [
            {
                "id": "c221-stakeholders",
                "label": "Stakeholders in the registry",
                "source": "stakeholder_registry",
                "mode": "all",
                "category": "supporting"
            },
            {
                "id": "c221-engagements",
                "label": "Stakeholder communication plan records",
                "source": "stakeholder_engagement",
                "mode": "all",
                "category": "supporting"
            },
            {
                "id": "c221-complete-engagements",
                "label": "Communication plan records with group, channel, frequency, purpose and owner",
                "source": "stakeholder_engagement",
                "mode": "all_required",
                "required_fields": [
                    ["stakeholder_group", "stakeholder"],
                    ["communication_channel", "channel"],
                    ["frequency", "engagement_frequency"],
                    ["content_purpose", "purpose"],
                    ["responsible_person", "owner"]
                ],
                "category": "supporting"
            },
            {
                "id": "c221-plan-completeness-proxy",
                "label": "Communication plan record completeness proxy",
                "mode": "derived_percent",
                "numerator_ref": "c221-complete-engagements",
                "denominator_ref": "c221-engagements",
                "category": "management",
                "support_status": "partial",
                "limitations": [
                    "The denominator is existing plan records, not the approved list of required stakeholder groups.",
                    "The proxy does not prove that the plan is current, approved or implemented."
                ],
                "requirement_basis": "Approved stakeholder communication framework",
                "decision_use": "Complete missing channel, frequency, purpose or owner details."
            },
            {
                "id": "c221-essential-info",
                "label": "Essential Information records",
                "source": "essential_information",
                "mode": "all",
                "category": "supporting"
            },
            {
                "id": "c221-overdue-info-review",
                "label": "Essential Information overdue for review",
                "source": "essential_information",
                "mode": "date_before_today",
                "field": ["next_review_date"],
                "category": "supporting",
                "is_exception": True
            },
            unsupported_metric(
                "c221-essential-info-dissemination",
                "Essential Information approval and dissemination compliance",
                "The required approval tier, approval date, dissemination date, channel and recipient evidence must be linked to each Essential Information revision.",
                "requires_additional_field",
                "Accuracy and timely dissemination of Essential Information",
                "Block release or follow up information that was not correctly reviewed and disseminated."
            ),
            unsupported_metric(
                "c221-internal-effectiveness",
                "Internal communication effectiveness and follow-up",
                "Approved communication-effectiveness indicators and links from material findings to owned actions and effectiveness reviews are required.",
                "requires_relationship",
                "Two-way communication and continual review",
                "Change channels, timing or controls when communication is ineffective."
            )
        ]
    },
    "2.2.2": {
        "sources": ["material_vetting", "quality_action"],
        "metrics": [
            {
                "id": "c222-materials",
                "label": "External and marketing materials submitted",
                "source": "material_vetting",
                "mode": "all",
                "category": "supporting"
            },
            {
                "id": "c222-approved-materials",
                "label": "Approved external and marketing materials",
                "source": "material_vetting",
                "mode": "in",
                "field": ["approval_status", "workflow_state"],
                "values": ["Approved", "Final Approval", "Conditionally Approved"],
                "category": "supporting"
            },
            {
                "id": "c222-prepublication-approval-proxy",
                "label": "Material approval proxy",
                "mode": "derived_percent",
                "numerator_ref": "c222-approved-materials",
                "denominator_ref": "c222-materials",
                "category": "management",
                "support_status": "partial",
                "limitations": [
                    "This proxy shows approved records as a proportion of submitted records.",
                    "It does not prove that approval occurred before publication or that every published material is represented."
                ],
                "requirement_basis": "Vetting and formal approval before publication",
                "decision_use": "Identify submitted materials that have not reached an approved state."
            },
            {
                "id": "c222-pending-materials",
                "label": "Pending external communication approvals",
                "source": "material_vetting",
                "mode": "in",
                "field": ["approval_status", "workflow_state"],
                "values": [
                    "Pending", "In Progress", "Requires Amendments",
                    "Waiting to Vet", "Waiting for Approval", "Draft"
                ],
                "category": "supporting",
                "is_exception": True
            },
            {
                "id": "c222-rejected-materials",
                "label": "Rejected external communication materials",
                "source": "material_vetting",
                "mode": "in",
                "field": ["approval_status", "workflow_state"],
                "values": ["Rejected", "Declined", "Not Approved"],
                "category": "supporting",
                "is_exception": True
            },
            {
                "id": "c222-exception-register",
                "label": "Pending or rejected external communication records",
                "mode": "derived_sum",
                "refs": ["c222-pending-materials", "c222-rejected-materials"],
                "category": "management",
                "support_status": "partial",
                "limitations": [
                    "Expiry, unauthorised publication, released-version mismatch and corrective-action checks require additional fields and links."
                ],
                "requirement_basis": "External communication exception control",
                "decision_use": "Prioritise pending or rejected materials and prevent unauthorised release.",
                "is_exception": True
            },
            unsupported_metric(
                "c222-release-version-compliance",
                "Released-version and approval-tier compliance",
                "The released publication, approved attachment/version, publication date, required approval tier and formal role-authority chain must be linked.",
                "requires_relationship",
                "Accuracy, approval authority and release control",
                "Withdraw or correct material released without the required evidence."
            )
        ]
    },
    "2.3.1": {
        "sources": [
            "quality_performance", "quality_monitoring", "quality_meeting",
            "quality_action", "helpdesk_ticket", "data_asset_inventory"
        ],
        "metrics": [
            {
                "id": "c231-performance-outcomes",
                "label": "Quality Performance Outcomes",
                "source": "quality_performance",
                "mode": "all",
                "category": "supporting"
            },
            {
                "id": "c231-quality-monitoring",
                "label": "Quality Monitoring Records",
                "source": "quality_monitoring",
                "mode": "all",
                "category": "supporting"
            },
            {
                "id": "c231-quality-meetings",
                "label": "Quality Meetings",
                "source": "quality_meeting",
                "mode": "all",
                "category": "supporting"
            },
            {
                "id": "c231-data-assets",
                "label": "Data Asset Inventory records",
                "source": "data_asset_inventory",
                "mode": "all",
                "category": "supporting"
            },
            unsupported_metric(
                "c231-dataset-use",
                "Required dataset completeness, currency and management use",
                "An approved dataset registry, reporting period, validation state and link to the scheduled management decision are required.",
                "requires_relationship",
                "KPI and operational data collection and use",
                "Correct incomplete datasets and confirm that current data informed management decisions."
            ),
            unsupported_metric(
                "c231-data-quality",
                "Unresolved data-quality exceptions",
                "A validation-exception source with dataset, severity, status, age and affected report or decision is required.",
                "requires_new_doctype_or_child_table",
                "Data accuracy and reliability",
                "Correct data errors and assess whether affected reports or decisions must be revised."
            ),
            unsupported_metric(
                "c231-access-timeliness",
                "Access appropriateness and data availability",
                "Role-based access assignments, access reviews, access-request timestamps and approved role requirements are required.",
                "requires_new_doctype_or_child_table",
                "Data accessibility and timely availability",
                "Grant, remove or revise access and resolve delayed information availability."
            ),
            unsupported_metric(
                "c231-consent-processing",
                "Consent, withdrawal and file-access request processing",
                "Consent, withdrawal, additional-purpose and file-access request records must be linked to acknowledgement, decision and record-update evidence.",
                "requires_new_doctype_or_child_table",
                "Consent and controlled stakeholder access",
                "Process outstanding requests and prevent unauthorised use or disclosure."
            ),
            unsupported_metric(
                "c231-security-comparative-review",
                "Security, confidentiality and comparative-analysis review",
                "Scheduled security reviews and operational, biannual and annual comparative analyses must be linked to findings, decisions, actions and effectiveness verification.",
                "requires_relationship",
                "Confidentiality, comparative analysis and continual review",
                "Approve corrective actions, revise plans or strengthen controls."
            )
        ]
    },
    "2.3.2": {
        "sources": [
            "document_control", "quality_meeting", "quality_action",
            "helpdesk_ticket", "data_asset_inventory", "print_format",
            "letter_head"
        ],
        "metrics": [
            {
                "id": "c232-documents",
                "label": "Knowledge documents in scope",
                "source": "document_control",
                "mode": "all",
                "category": "supporting"
            },
            {
                "id": "c232-current-documents",
                "label": "Approved or current knowledge documents",
                "source": "document_control",
                "mode": "in",
                "field": ["status"],
                "values": ["Approved", "Current", "Active"],
                "category": "supporting"
            },
            {
                "id": "c232-current-document-proxy",
                "label": "Current-document status proxy",
                "mode": "derived_percent",
                "numerator_ref": "c232-current-documents",
                "denominator_ref": "c232-documents",
                "category": "management",
                "support_status": "partial",
                "limitations": [
                    "The denominator includes all readable Document Control records and is not an approved list of required active policies and manuals.",
                    "The proxy does not prove staff access or removal of obsolete copies from active use."
                ],
                "requirement_basis": "Current and accessible policy and operations manuals",
                "decision_use": "Review documents that are not in an approved, current or active state."
            },
            {
                "id": "c232-obsolete-documents",
                "label": "Obsolete, archived or superseded documents",
                "source": "document_control",
                "mode": "in",
                "field": ["status"],
                "values": ["Obsolete", "Archived", "Superseded"],
                "category": "supporting",
                "limitations": [
                    "Properly archived records are compliant lifecycle evidence and are not automatically exceptions."
                ]
            },
            {
                "id": "c232-overdue-documents",
                "label": "Knowledge documents overdue for review",
                "source": "document_control",
                "mode": "date_before_today",
                "field": ["next_review_date"],
                "category": "supporting",
                "is_exception": True
            },
            {
                "id": "c232-print-formats",
                "label": "Controlled print formats",
                "source": "print_format",
                "mode": "all",
                "category": "supporting"
            },
            {
                "id": "c232-letter-heads",
                "label": "Controlled letter heads",
                "source": "letter_head",
                "mode": "all",
                "category": "supporting"
            },
            unsupported_metric(
                "c232-document-approval-control",
                "Document request, revision history and approval-authority compliance",
                "Each new or revised document requires links to the approved request, complete version-control fields, formal approval roles and approval before implementation.",
                "requires_additional_field",
                "Document control and revision approval",
                "Reject invalid documents or prevent implementation before approval."
            ),
            unsupported_metric(
                "c232-retention-disposal",
                "Retention, backup, archival and disposal compliance",
                "Retention triggers, backup evidence, archival status, Principal-approved disposal and disposal completion must be linked at record level.",
                "requires_new_doctype_or_child_table",
                "Record retention, preservation and disposal",
                "Continue retention, archive or approve secure disposal."
            ),
            unsupported_metric(
                "c232-system-review",
                "Knowledge Management review and effective closure",
                "An annual APSR review scoped to Knowledge Management and linked to findings, actions and effectiveness confirmation is required.",
                "requires_relationship",
                "Review of Knowledge Management for continual improvement",
                "Improve the knowledge system and verify that identified gaps were resolved."
            )
        ]
    },
    "2.4.1": {
        "sources": [
            "helpdesk_ticket", "employee_grievance", "quality_action", "todo",
            "survey_management", "survey_tracking"
        ],
        "metrics": [
            {
                "id": "c241-feedback-tickets",
                "label": "Feedback, complaint, grievance or dispute tickets",
                "source": "helpdesk_ticket",
                "mode": "conditions",
                "condition_groups": [FEEDBACK_SCOPE_GROUP],
                "category": "supporting"
            },
            {
                "id": "c241-open-feedback-tickets",
                "label": "Open feedback or complaint tickets",
                "source": "helpdesk_ticket",
                "mode": "conditions",
                "condition_groups": [
                    FEEDBACK_SCOPE_GROUP,
                    {
                        "logic": "all",
                        "required": True,
                        "conditions": [
                            {
                                "field": ["status"],
                                "op": "not_in",
                                "values": ["Closed", "Resolved", "Cancelled"]
                            }
                        ]
                    }
                ],
                "category": "supporting",
                "is_exception": True
            },
            {
                "id": "c241-closed-feedback-tickets",
                "label": "Closed or resolved feedback or complaint tickets",
                "source": "helpdesk_ticket",
                "mode": "conditions",
                "condition_groups": [
                    FEEDBACK_SCOPE_GROUP,
                    {
                        "logic": "all",
                        "required": True,
                        "conditions": [
                            {
                                "field": ["status"],
                                "op": "in",
                                "values": ["Closed", "Resolved"]
                            }
                        ]
                    }
                ],
                "category": "supporting"
            },
            {
                "id": "c241-sla-failed",
                "label": "Feedback or complaint tickets with failed SLA",
                "source": "helpdesk_ticket",
                "mode": "conditions",
                "condition_groups": [
                    FEEDBACK_SCOPE_GROUP,
                    {
                        "logic": "all",
                        "required": True,
                        "conditions": [
                            {
                                "field": ["agreement_status"],
                                "op": "equals",
                                "value": "Failed"
                            }
                        ]
                    }
                ],
                "category": "supporting",
                "is_exception": True
            },
            {
                "id": "c241-sla-failure-proxy",
                "label": "Feedback SLA failure proxy",
                "mode": "derived_percent",
                "numerator_ref": "c241-sla-failed",
                "denominator_ref": "c241-feedback-tickets",
                "category": "management",
                "support_status": "partial",
                "limitations": [
                    "The calculation depends on the installed Helpdesk agreement-status logic.",
                    "It does not separate acknowledgement and resolution SLAs or verify urgency, impact and priority scoring."
                ],
                "requirement_basis": "Feedback prioritisation and timely resolution",
                "decision_use": "Escalate failed-SLA feedback and complaint cases."
            },
            {
                "id": "c241-grievances",
                "label": "Employee grievance records",
                "source": "employee_grievance",
                "mode": "all",
                "category": "supporting"
            },
            {
                "id": "c241-closed-grievances",
                "label": "Closed or resolved employee grievances",
                "source": "employee_grievance",
                "mode": "in",
                "field": ["status"],
                "values": ["Closed", "Resolved"],
                "category": "supporting"
            },
            {
                "id": "c241-grievance-closure-proxy",
                "label": "Grievance closure proxy",
                "mode": "derived_percent",
                "numerator_ref": "c241-closed-grievances",
                "denominator_ref": "c241-grievances",
                "category": "management",
                "support_status": "partial",
                "limitations": [
                    "Closure status does not prove that the required internal or external escalation process and stakeholder communication were completed."
                ],
                "requirement_basis": "Grievance and dispute resolution",
                "decision_use": "Follow up unresolved grievance records."
            },
            {
                "id": "c241-feedback-quality-actions",
                "label": "Quality Actions with a feedback reference",
                "source": "quality_action",
                "mode": "truthy",
                "field": ["feedback"],
                "category": "supporting"
            },
            unsupported_metric(
                "c241-capture-ack-classification",
                "Feedback capture, acknowledgement and classification compliance",
                "Feedback case type, receipt time, acknowledgement time, classification and the applicable working-day SLA must be available at case level.",
                "requires_additional_field",
                "Closed-loop feedback capture and acknowledgement",
                "Assign ownership and escalate cases that were not captured, acknowledged or classified on time."
            ),
            unsupported_metric(
                "c241-action-effectiveness",
                "Feedback action ownership, implementation, updates and effectiveness",
                "Each qualifying feedback case must link to an approved action owner, due date, stakeholder updates, implementation record and effectiveness result.",
                "requires_relationship",
                "Corrective and improvement actions",
                "Approve, extend, close or reopen actions based on verified effectiveness."
            ),
            unsupported_metric(
                "c241-experience-drivers",
                "Positive and negative experience drivers",
                "A controlled feedback-driver taxonomy and trend relationship to recognition, standardisation or improvement decisions are required.",
                "requires_new_doctype_or_child_table",
                "Positive Experience Enhancement and continual review",
                "Recognise effective practices and address recurring negative drivers."
            )
        ]
    },
    "2.4.2": {
        "sources": [
            "survey_management", "survey_tracking", "student_onboarding_survey",
            "end_module_survey", "end_course_survey", "course_review",
            "module_review", "quality_action"
        ],
        "metrics": [
            {
                "id": "c242-surveys",
                "label": "Student satisfaction survey instruments",
                "source": "survey_management",
                "mode": "conditions",
                "condition_groups": [
                    {
                        "logic": "any",
                        "required": True,
                        "conditions": [
                            {
                                "field": ["survey_type"],
                                "op": "contains_any",
                                "values": ["student"],
                                "optional": True
                            },
                            {
                                "field": ["survey_name"],
                                "op": "contains_any",
                                "values": ["student", "module", "course", "graduate", "alumni"],
                                "optional": True
                            }
                        ]
                    }
                ],
                "category": "supporting"
            },
            {
                "id": "c242-responses",
                "label": "Student satisfaction response records",
                "source": "survey_tracking",
                "mode": "conditions",
                "condition_groups": [STUDENT_SURVEY_SCOPE_GROUP],
                "category": "supporting"
            },
            {
                "id": "c242-completed-responses",
                "label": "Completed student satisfaction response records",
                "source": "survey_tracking",
                "mode": "conditions",
                "condition_groups": [
                    STUDENT_SURVEY_SCOPE_GROUP,
                    {
                        "logic": "all",
                        "required": True,
                        "conditions": [
                            {
                                "field": ["status"],
                                "op": "in",
                                "values": ["Completed", "Submitted"]
                            }
                        ]
                    }
                ],
                "category": "supporting"
            },
            {
                "id": "c242-response-record-completion-proxy",
                "label": "Student response-record completion proxy",
                "mode": "derived_percent",
                "numerator_ref": "c242-completed-responses",
                "denominator_ref": "c242-responses",
                "category": "supporting",
                "support_status": "partial",
                "limitations": [
                    "This is not the survey response rate because the eligible-student denominator is unavailable."
                ]
            },
            {
                "id": "c242-rating",
                "label": "Average student satisfaction score",
                "source": "survey_tracking",
                "mode": "average_fields",
                "fields": [["rating", "score"]],
                "condition_groups": [STUDENT_SURVEY_SCOPE_GROUP],
                "unit": "rating",
                "category": "supporting",
                "support_status": "partial",
                "limitations": [
                    "The approved scale, target, survey dimension and comparable survey cycle are not defined."
                ]
            },
            {
                "id": "c242-onboarding-surveys",
                "label": "Student onboarding survey records",
                "source": "student_onboarding_survey",
                "mode": "all",
                "category": "supporting"
            },
            {
                "id": "c242-module-surveys",
                "label": "End-of-module survey records",
                "source": "end_module_survey",
                "mode": "all",
                "category": "supporting"
            },
            {
                "id": "c242-course-surveys",
                "label": "End-of-course survey records",
                "source": "end_course_survey",
                "mode": "all",
                "category": "supporting"
            },
            unsupported_metric(
                "c242-required-survey-schedule",
                "Required student survey schedule compliance",
                "Approved survey cycles must be linked to eligible students, courses, modules, lifecycle triggers, approval dates and required response windows.",
                "requires_relationship",
                "Required student survey types, approval and timing",
                "Run missing surveys and correct late or unapproved administration."
            ),
            unsupported_metric(
                "c242-dimension-coverage",
                "Student survey dimension coverage",
                "Survey questions must be linked to an approved coverage matrix for each applicable GD4 satisfaction dimension and survey type.",
                "requires_new_doctype_or_child_table",
                "Student survey questionnaire coverage",
                "Revise survey instruments with missing required dimensions."
            ),
            unsupported_metric(
                "c242-eligible-response-rate",
                "Eligible student valid response rate",
                "The eligible-student population, survey assignment, valid-response rule and response window must be linked at survey-cycle level.",
                "requires_relationship",
                "Student survey participation and validity",
                "Improve participation or investigate coverage and response bias."
            ),
            unsupported_metric(
                "c242-target-trend",
                "Student satisfaction target and trend analysis",
                "Approved scale, direction, dimension, target and comparable survey-cycle data are required.",
                "requires_additional_field",
                "Student satisfaction monitoring and strategic targets",
                "Prioritise dimensions below target or showing material deterioration."
            ),
            unsupported_metric(
                "c242-action-effectiveness",
                "Student survey action and effectiveness traceability",
                "Material findings must link to Course or Module Review decisions, approved owners, due dates, communication, implementation and subsequent-cycle effectiveness.",
                "requires_relationship",
                "Use of student survey findings and continual review",
                "Approve, monitor and verify improvement actions arising from student feedback."
            )
        ]
    },
    "2.4.3": {
        "sources": [
            "survey_management", "survey_tracking", "employee",
            "employee_separation", "staff_onboarding_survey", "staff_survey",
            "exit_interview_survey", "quality_action"
        ],
        "metrics": [
            {
                "id": "c243-surveys",
                "label": "Staff satisfaction survey instruments",
                "source": "survey_management",
                "mode": "conditions",
                "condition_groups": [
                    {
                        "logic": "any",
                        "required": True,
                        "conditions": [
                            {
                                "field": ["survey_type"],
                                "op": "contains_any",
                                "values": ["staff", "employee"],
                                "optional": True
                            },
                            {
                                "field": ["survey_name"],
                                "op": "contains_any",
                                "values": ["staff", "employee", "exit", "onboarding"],
                                "optional": True
                            }
                        ]
                    }
                ],
                "category": "supporting"
            },
            {
                "id": "c243-responses",
                "label": "Staff satisfaction response records",
                "source": "survey_tracking",
                "mode": "conditions",
                "condition_groups": [STAFF_SURVEY_SCOPE_GROUP],
                "category": "supporting"
            },
            {
                "id": "c243-completed-responses",
                "label": "Completed staff satisfaction response records",
                "source": "survey_tracking",
                "mode": "conditions",
                "condition_groups": [
                    STAFF_SURVEY_SCOPE_GROUP,
                    {
                        "logic": "all",
                        "required": True,
                        "conditions": [
                            {
                                "field": ["status"],
                                "op": "in",
                                "values": ["Completed", "Submitted"]
                            }
                        ]
                    }
                ],
                "category": "supporting"
            },
            {
                "id": "c243-response-record-completion-proxy",
                "label": "Staff response-record completion proxy",
                "mode": "derived_percent",
                "numerator_ref": "c243-completed-responses",
                "denominator_ref": "c243-responses",
                "category": "supporting",
                "support_status": "partial",
                "limitations": [
                    "This is not the staff survey response rate because the eligible-staff denominator and assignment relationship are unavailable."
                ]
            },
            {
                "id": "c243-rating",
                "label": "Average staff satisfaction score",
                "source": "survey_tracking",
                "mode": "average_fields",
                "fields": [["rating", "score"]],
                "condition_groups": [STAFF_SURVEY_SCOPE_GROUP],
                "unit": "rating",
                "category": "supporting",
                "support_status": "partial",
                "limitations": [
                    "The approved scale, target, survey dimension, staff group and comparable survey cycle are not defined."
                ]
            },
            {
                "id": "c243-active-staff",
                "label": "Active staff population",
                "source": "employee",
                "mode": "equals",
                "field": ["status"],
                "value": "Active",
                "category": "supporting"
            },
            {
                "id": "c243-onboarding-surveys",
                "label": "Staff onboarding survey records",
                "source": "staff_onboarding_survey",
                "mode": "all",
                "category": "supporting"
            },
            {
                "id": "c243-staff-surveys",
                "label": "Annual staff survey records",
                "source": "staff_survey",
                "mode": "all",
                "category": "supporting"
            },
            {
                "id": "c243-exit-surveys",
                "label": "Exit interview survey records",
                "source": "exit_interview_survey",
                "mode": "all",
                "category": "supporting"
            },
            unsupported_metric(
                "c243-required-survey-schedule",
                "Required staff survey schedule compliance",
                "Approved staff onboarding, annual staff and exit survey cycles must be linked to the applicable employee population and required response windows.",
                "requires_relationship",
                "Staff survey coverage, approval and timing",
                "Run missing surveys and correct late or unapproved administration."
            ),
            unsupported_metric(
                "c243-dimension-coverage",
                "Staff survey dimension and population coverage",
                "Survey questions must be linked to the approved coverage matrix and applicable full-time, part-time and academic staff groups.",
                "requires_new_doctype_or_child_table",
                "Staff survey questionnaire coverage",
                "Revise survey instruments with missing dimensions or staff groups."
            ),
            unsupported_metric(
                "c243-eligible-response-rate",
                "Eligible staff valid response rate",
                "The eligible staff population, survey assignment, valid-response rule and response window must be linked at survey-cycle level.",
                "requires_relationship",
                "Staff survey participation and validity",
                "Improve participation or assess response bias."
            ),
            unsupported_metric(
                "c243-target-retention-trend",
                "Staff satisfaction, retention and turnover trend analysis",
                "Approved scale, dimension, target, comparable survey cycles and links to retention and separation indicators are required.",
                "requires_relationship",
                "Staff satisfaction, retention and operational risk",
                "Prioritise dimensions below target and address related retention or turnover risks."
            ),
            unsupported_metric(
                "c243-action-effectiveness",
                "Staff survey action and effectiveness traceability",
                "Material findings must link to meeting decisions, Principal approval, action ownership, implementation, communication and later-cycle effectiveness.",
                "requires_relationship",
                "Use of staff survey findings and continual review",
                "Approve, monitor and verify workplace or retention improvements."
            )
        ]
    }
}

QUESTION_REGISTRY = {
    "overview": [
        {
            "id": "O-01",
            "question": "Which Criterion 2 controls require management attention now?",
            "metric_id": "ov-known-attention-total",
            "requirement_basis": "Criterion 2 management attention queue",
            "decision_use": "Prioritise immediate follow-up on known live exceptions and review unsupported evidence gaps."
        },
        {
            "id": "O-02",
            "question": "What proportion of Criterion 2 requirements has current live evidence, document-only evidence or no usable evidence?",
            "metric_id": "ov-requirement-evidence-coverage",
            "requirement_basis": "Criterion 2 audit readiness",
            "decision_use": "Direct evidence collection and system-development priorities."
        }
    ],
    "2.1.1": [
        {
            "id": "HR-01",
            "question": "Are current manpower gaps supported by approved staffing or deployment decisions?",
            "metric_id": "c211-manpower-treatment",
            "requirement_basis": "Manpower planning and deployment",
            "decision_use": "Approve recruitment, redeployment or a documented decision to defer action."
        },
        {
            "id": "HR-02",
            "question": "Did every recruitment exercise begin with a complete and approved requisition?",
            "metric_id": "c211-requisition-compliance-proxy",
            "requirement_basis": "Approved job requisition and role definition",
            "decision_use": "Stop or correct recruitment activity without complete prior approval."
        },
        {
            "id": "HR-03",
            "question": "Did appointed candidates meet the required competency, qualification and approval conditions before appointment or deployment?",
            "metric_id": "c211-candidate-compliance",
            "requirement_basis": "Competency-based recruitment and teaching staff approval controls",
            "decision_use": "Prevent appointment or deployment when mandatory evidence is incomplete."
        },
        {
            "id": "HR-04",
            "question": "Did all appointed staff complete the required onboarding controls within the approved timeframe?",
            "metric_id": "c211-onboarding-completion-proxy",
            "requirement_basis": "Staff onboarding and service readiness",
            "decision_use": "Escalate incomplete or late onboarding."
        },
        {
            "id": "HR-05",
            "question": "Are appraisals completed on schedule, and are development, reward, retention and succession decisions traceable to the results?",
            "metric_id": "c211-appraisal-decision-traceability",
            "requirement_basis": "Performance management, rewards, retention and succession",
            "decision_use": "Complete overdue appraisals and formalise decisions arising from results."
        },
        {
            "id": "HR-06",
            "question": "Are offboarding, clearance, exit feedback and access removal complete, and have recurring retention risks been addressed?",
            "metric_id": "c211-offboarding-completeness",
            "requirement_basis": "Employee offboarding and retention review",
            "decision_use": "Close outstanding separation controls and approve retention actions."
        }
    ],
    "2.1.2": [
        {
            "id": "TD-01",
            "question": "Have training needs for the applicable staff population been identified, discussed, reviewed and approved?",
            "metric_id": "c212-tna-review-proxy",
            "requirement_basis": "Training needs identification, discussion, review and approval",
            "decision_use": "Complete missing reviews and approve priority needs."
        },
        {
            "id": "TD-02",
            "question": "Is the approved training plan complete, funded and sufficient to address identified priority gaps?",
            "metric_id": "c212-plan-sufficiency",
            "requirement_basis": "Training planning, scheduling and budget",
            "decision_use": "Schedule or fund unmet priority needs."
        },
        {
            "id": "TD-03",
            "question": "Have all staff completed the mandatory, onboarding and role-specific training assigned to them?",
            "metric_id": "c212-mandatory-training-completion",
            "requirement_basis": "Mandatory, onboarding and role-specific training",
            "decision_use": "Escalate overdue or incomplete required training."
        },
        {
            "id": "TD-04",
            "question": "Was training effective in improving learning, workplace application and relevant organisational outcomes?",
            "metric_id": "c212-effectiveness",
            "requirement_basis": "Training effectiveness and continual improvement",
            "decision_use": "Retain, revise or discontinue training based on verified effectiveness."
        }
    ],
    "2.2.1": [
        {
            "id": "IC-01",
            "question": "Are all required stakeholder groups covered by a current approved communication channel, content purpose, frequency and responsible owner?",
            "metric_id": "c221-plan-completeness-proxy",
            "requirement_basis": "Approved stakeholder communication framework",
            "decision_use": "Complete missing communication arrangements."
        },
        {
            "id": "IC-02",
            "question": "Was Essential Information reviewed, approved and disseminated through the correct channels within the required timeframe?",
            "metric_id": "c221-essential-info-dissemination",
            "requirement_basis": "Accuracy and timely dissemination of Essential Information",
            "decision_use": "Block release or correct late and unapproved dissemination."
        },
        {
            "id": "IC-03",
            "question": "Is internal communication effective, and were identified weaknesses reviewed and addressed?",
            "metric_id": "c221-internal-effectiveness",
            "requirement_basis": "Two-way communication and continual review",
            "decision_use": "Revise channels, timing or controls and verify improvement."
        }
    ],
    "2.2.2": [
        {
            "id": "EC-01",
            "question": "Were all external and marketing materials vetted and formally approved before publication?",
            "metric_id": "c222-prepublication-approval-proxy",
            "requirement_basis": "Vetting and formal approval before publication",
            "decision_use": "Prevent publication without approval."
        },
        {
            "id": "EC-02",
            "question": "Did the released material match the approved version and satisfy the required approval tier and compliance checks?",
            "metric_id": "c222-release-version-compliance",
            "requirement_basis": "Accuracy, approval authority and release control",
            "decision_use": "Withdraw or correct non-compliant published material."
        },
        {
            "id": "EC-03",
            "question": "Which external communications are pending, rejected, expired, published without approval or awaiting corrective action?",
            "metric_id": "c222-exception-register",
            "requirement_basis": "External communication exception control",
            "decision_use": "Prioritise material review and corrective action."
        }
    ],
    "2.3.1": [
        {
            "id": "DI-01",
            "question": "Are all required KPI and operational datasets complete, current and used in scheduled management decisions?",
            "metric_id": "c231-dataset-use",
            "requirement_basis": "KPI and operational data collection and use",
            "decision_use": "Correct incomplete datasets and confirm evidence-based decisions."
        },
        {
            "id": "DI-02",
            "question": "Which data-quality exceptions remain unresolved, and which decisions or reports may be affected?",
            "metric_id": "c231-data-quality",
            "requirement_basis": "Data accuracy and reliability",
            "decision_use": "Correct errors and reassess affected reports or decisions."
        },
        {
            "id": "DI-03",
            "question": "Are access rights appropriate and current, and can authorised stakeholders obtain required information within the expected timeframe?",
            "metric_id": "c231-access-timeliness",
            "requirement_basis": "Data accessibility and timely availability",
            "decision_use": "Grant, remove or revise access and resolve delays."
        },
        {
            "id": "DI-04",
            "question": "Are consent, withdrawal, additional-purpose and stakeholder file-access requests processed completely and on time?",
            "metric_id": "c231-consent-processing",
            "requirement_basis": "Consent and controlled stakeholder access",
            "decision_use": "Process outstanding requests and prevent unauthorised data use."
        },
        {
            "id": "DI-05",
            "question": "Are data security, confidentiality and comparative-analysis controls producing reviewed findings and effective follow-up actions?",
            "metric_id": "c231-security-comparative-review",
            "requirement_basis": "Confidentiality, comparative analysis and continual review",
            "decision_use": "Approve corrective actions and revise controls or plans."
        }
    ],
    "2.3.2": [
        {
            "id": "KM-01",
            "question": "Are staff able to access the current approved version of every required policy and manual, with obsolete copies removed from active use?",
            "metric_id": "c232-current-document-proxy",
            "requirement_basis": "Current and accessible policy and operations manuals",
            "decision_use": "Publish current versions and remove obsolete active access."
        },
        {
            "id": "KM-02",
            "question": "Do all new and revised controlled documents have an approved request, complete revision history and correct approval authority before implementation?",
            "metric_id": "c232-document-approval-control",
            "requirement_basis": "Document control and revision approval",
            "decision_use": "Reject invalid documents or prevent implementation before approval."
        },
        {
            "id": "KM-03",
            "question": "Are retention, backup, archival and disposal controls completed according to approved schedules and decisions?",
            "metric_id": "c232-retention-disposal",
            "requirement_basis": "Record retention, preservation and disposal",
            "decision_use": "Continue retention, archive or approve secure disposal."
        },
        {
            "id": "KM-04",
            "question": "Was the Knowledge Management system reviewed, and were knowledge-access, enablement or document-control gaps effectively resolved?",
            "metric_id": "c232-system-review",
            "requirement_basis": "Review of Knowledge Management for continual improvement",
            "decision_use": "Improve the knowledge system and verify closure."
        }
    ],
    "2.4.1": [
        {
            "id": "FM-01",
            "question": "Is all formal and escalated informal feedback captured, acknowledged and correctly classified within the applicable SLA?",
            "metric_id": "c241-capture-ack-classification",
            "requirement_basis": "Closed-loop feedback capture and acknowledgement",
            "decision_use": "Assign ownership and escalate late or unclassified cases."
        },
        {
            "id": "FM-02",
            "question": "Are urgency, impact and priority correctly assessed, and are high or critical cases escalated and resolved on time?",
            "metric_id": "c241-sla-failure-proxy",
            "requirement_basis": "Feedback prioritisation and timely resolution",
            "decision_use": "Escalate high-risk and failed-SLA cases."
        },
        {
            "id": "FM-03",
            "question": "Do feedback cases requiring action have an approved owner, timeline, stakeholder update and effectiveness result?",
            "metric_id": "c241-action-effectiveness",
            "requirement_basis": "Corrective and improvement actions",
            "decision_use": "Approve, extend, close or reopen actions."
        },
        {
            "id": "FM-04",
            "question": "Are grievances and disputes resolved or escalated through the required process and communicated to the affected student or staff member?",
            "metric_id": "c241-grievance-closure-proxy",
            "requirement_basis": "Grievance and dispute resolution",
            "decision_use": "Resolve or escalate outstanding cases."
        },
        {
            "id": "FM-05",
            "question": "What recurring positive and negative experience drivers require recognition, standardisation or system improvement?",
            "metric_id": "c241-experience-drivers",
            "requirement_basis": "Positive Experience Enhancement and continual review",
            "decision_use": "Recognise effective practices and address recurring weaknesses."
        }
    ],
    "2.4.2": [
        {
            "id": "SS-01",
            "question": "Were all required student survey types approved and administered at the required lifecycle points and within the specified survey windows?",
            "metric_id": "c242-required-survey-schedule",
            "requirement_basis": "Required student survey types, approval and timing",
            "decision_use": "Run missing surveys and correct late or unapproved administration."
        },
        {
            "id": "SS-02",
            "question": "Does each current student survey instrument cover the required GD4 satisfaction dimensions applicable to that survey type?",
            "metric_id": "c242-dimension-coverage",
            "requirement_basis": "Student survey questionnaire coverage",
            "decision_use": "Revise instruments with missing required dimensions."
        },
        {
            "id": "SS-03",
            "question": "What proportion of eligible students submitted valid responses within the defined response period?",
            "metric_id": "c242-eligible-response-rate",
            "requirement_basis": "Student survey participation and validity",
            "decision_use": "Improve participation or investigate response bias."
        },
        {
            "id": "SS-04",
            "question": "Which survey types and satisfaction dimensions are below target, declining or materially different across student groups?",
            "metric_id": "c242-target-trend",
            "requirement_basis": "Student satisfaction monitoring and strategic targets",
            "decision_use": "Prioritise weak or deteriorating dimensions."
        },
        {
            "id": "SS-05",
            "question": "Were material student-survey findings reviewed, communicated and converted into approved actions whose effectiveness was verified?",
            "metric_id": "c242-action-effectiveness",
            "requirement_basis": "Use of student survey findings and continual review",
            "decision_use": "Approve, monitor and verify improvement actions."
        }
    ],
    "2.4.3": [
        {
            "id": "ST-01",
            "question": "Were staff onboarding, annual staff and exit surveys approved and administered to the applicable population within the required periods?",
            "metric_id": "c243-required-survey-schedule",
            "requirement_basis": "Staff survey coverage, approval and timing",
            "decision_use": "Run missing surveys and correct late or unapproved administration."
        },
        {
            "id": "ST-02",
            "question": "Does each current staff survey cover all required dimensions and the applicable full-time, part-time and academic staff groups?",
            "metric_id": "c243-dimension-coverage",
            "requirement_basis": "Staff survey questionnaire coverage",
            "decision_use": "Revise instruments with missing dimensions or staff groups."
        },
        {
            "id": "ST-03",
            "question": "What proportion of eligible staff submitted valid responses within the defined period?",
            "metric_id": "c243-eligible-response-rate",
            "requirement_basis": "Staff survey participation and validity",
            "decision_use": "Improve participation or assess response bias."
        },
        {
            "id": "ST-04",
            "question": "Which staff-satisfaction dimensions are below target or declining, and what retention, turnover or operational risks do they indicate?",
            "metric_id": "c243-target-retention-trend",
            "requirement_basis": "Staff satisfaction, retention and operational risk",
            "decision_use": "Prioritise weak dimensions and related retention actions."
        },
        {
            "id": "ST-05",
            "question": "Were material staff-survey findings reviewed, communicated and converted into approved improvements whose effectiveness was verified?",
            "metric_id": "c243-action-effectiveness",
            "requirement_basis": "Use of staff survey findings and continual review",
            "decision_use": "Approve, monitor and verify workplace improvements."
        }
    ]
}

STANDARD_FIELDS = [
    "name", "owner", "creation", "modified", "modified_by", "docstatus", "idx"
]


def clean_text(value):
    if value is None:
        return ""
    return str(value).strip()


def lower_text(value):
    return clean_text(value).lower()


def is_truthy(value):
    if value in [None, "", 0, "0", False]:
        return False
    if lower_text(value) in ["false", "no", "unchecked", "none", "null"]:
        return False
    return True


def to_number(value):
    try:
        if value in [None, ""]:
            return None
        return float(value)
    except Exception:
        return None


def is_permission_error(error):
    text = lower_text(error)
    return (
        "permission" in text
        or "not permitted" in text
        or "not allowed" in text
    )


def clone_dict(source):
    output = {}
    for key in source or {}:
        output[key] = source.get(key)
    return output


def resolve_source(alias):
    candidates = SOURCE_CANDIDATES.get(alias) or []
    attempts = []

    for candidate_index in range(len(candidates)):
        doctype = candidates[candidate_index]
        attempt = {
            "doctype": doctype,
            "status": "checking",
            "stage": "metadata",
            "message": ""
        }

        try:
            frappe.get_meta(doctype)
            attempt["metadata"] = "available"
        except Exception as error:
            attempt["status"] = "unavailable"
            attempt["message"] = clean_text(error)
            attempts.append(attempt)
            continue

        try:
            rows = frappe.get_list(
                doctype,
                fields=["name"],
                limit_start=0,
                limit_page_length=1,
                order_by="modified desc"
            ) or []
            attempt["stage"] = "list"
            attempt["status"] = "available"
            attempt["message"] = "Readable by the signed-in user."
            attempts.append(attempt)
            return {
                "key": alias,
                "doctype": doctype,
                "candidates": candidates,
                "status": "available",
                "sample_count": len(rows),
                "probe": "frappe.get_list",
                "fallback_used": candidate_index > 0,
                "resolution_attempts": attempts
            }
        except Exception as error:
            message = clean_text(error)
            attempt["stage"] = "list"
            attempt["status"] = "permission_denied" if is_permission_error(error) else "unavailable"
            attempt["message"] = message
            attempts.append(attempt)
            if is_permission_error(error):
                return {
                    "key": alias,
                    "doctype": doctype,
                    "candidates": candidates,
                    "status": "permission_denied",
                    "sample_count": 0,
                    "message": message,
                    "probe": "frappe.get_list",
                    "fallback_used": False,
                    "resolution_attempts": attempts
                }

    return {
        "key": alias,
        "doctype": None,
        "candidates": candidates,
        "status": "unavailable",
        "sample_count": 0,
        "message": "No approved candidate DocType could be resolved. Review the candidate-level errors.",
        "resolution_attempts": attempts,
        "fallback_used": False
    }


def get_meta(doctype):
    try:
        return frappe.get_meta(doctype)
    except Exception:
        return None


def field_exists(meta, fieldname):
    if not fieldname:
        return False
    if fieldname in STANDARD_FIELDS:
        return True
    try:
        for meta_field in meta.fields or []:
            if meta_field.fieldname == fieldname:
                return True
    except Exception:
        pass
    try:
        return bool(meta.has_field(fieldname))
    except Exception:
        return False


def resolve_field(doctype, candidates):
    meta = get_meta(doctype)
    if not meta:
        return ""
    for fieldname in candidates or []:
        if field_exists(meta, fieldname):
            return fieldname
    return ""


def applied_filters(doctype):
    meta = get_meta(doctype)
    output = {}
    if not meta:
        return output
    for filter_key in FILTER_FIELD_CANDIDATES:
        requested = filters.get(filter_key)
        if requested in [None, "", "All", "all"]:
            continue
        for candidate in FILTER_FIELD_CANDIDATES.get(filter_key) or []:
            if field_exists(meta, candidate):
                output[candidate] = requested
                break
    return output


def safe_fields(doctype, fields):
    meta = get_meta(doctype)
    output = []
    if not meta:
        return output
    for fieldname in fields or []:
        if fieldname not in output and field_exists(meta, fieldname):
            output.append(fieldname)
    if "name" not in output:
        output.insert(0, "name")
    return output


row_cache = {}


def fetch_rows(source_alias, source, requested_fields=None):
    doctype = source.get("doctype")
    if source.get("status") != "available" or not doctype:
        return []

    fields_to_fetch = safe_fields(
        doctype,
        ["name"] + (requested_fields or [])
    )
    cache_key = source_alias + "|" + ",".join(fields_to_fetch)
    if row_cache.get(cache_key) is not None:
        return row_cache.get(cache_key)

    try:
        rows = frappe.get_list(
            doctype,
            fields=fields_to_fetch,
            filters=applied_filters(doctype),
            limit_page_length=row_limit,
            order_by="modified desc"
        ) or []
        row_cache[cache_key] = rows
        return rows
    except Exception:
        row_cache[cache_key] = []
        return []


def compare(row, fieldname, op, expected=None, values=None, days=None):
    value = row.get(fieldname) if fieldname else None

    if op == "truthy":
        return is_truthy(value)
    if op == "falsy":
        return not is_truthy(value)
    if op == "equals":
        return lower_text(value) == lower_text(expected)
    if op == "not_equals":
        return lower_text(value) != lower_text(expected)
    if op == "in":
        allowed = [lower_text(item) for item in (values or [])]
        return lower_text(value) in allowed
    if op == "not_in":
        blocked = [lower_text(item) for item in (values or [])]
        return lower_text(value) not in blocked
    if op == "contains":
        return lower_text(expected) in lower_text(value)
    if op == "contains_any":
        text = lower_text(value)
        for item in values or []:
            if lower_text(item) in text:
                return True
        return False
    if op == "not_contains_any":
        text = lower_text(value)
        for item in values or []:
            if lower_text(item) in text:
                return False
        return True
    if op in ["gt", "gte", "lt", "lte"]:
        left = to_number(value)
        right = to_number(expected)
        if left is None or right is None:
            return False
        if op == "gt":
            return left > right
        if op == "gte":
            return left >= right
        if op == "lt":
            return left < right
        return left <= right
    if op == "date_next_days":
        if not value:
            return False
        try:
            date_value = frappe.utils.getdate(value)
            today_value = frappe.utils.getdate(frappe.utils.today())
            end_date = frappe.utils.getdate(
                frappe.utils.add_days(today_value, int(days or 0))
            )
            return date_value >= today_value and date_value <= end_date
        except Exception:
            return False
    if op == "date_before_today":
        if not value:
            return False
        try:
            return frappe.utils.getdate(value) < frappe.utils.getdate(frappe.utils.today())
        except Exception:
            return False
    return False


def resolve_metric_fields(metric, doctype):
    output = {
        "primary_fields": [],
        "value_fields": [],
        "required_fields": [],
        "condition_groups": [],
        "missing": []
    }

    if metric.get("field"):
        fieldname = resolve_field(doctype, metric.get("field"))
        if fieldname:
            output["primary_fields"].append(fieldname)
        else:
            output["missing"].append(metric.get("field"))

    for candidates in metric.get("fields") or []:
        fieldname = resolve_field(doctype, candidates)
        if fieldname:
            output["value_fields"].append(fieldname)
        else:
            output["missing"].append(candidates)

    for candidates in metric.get("required_fields") or []:
        fieldname = resolve_field(doctype, candidates)
        if fieldname:
            output["required_fields"].append(fieldname)
        else:
            output["missing"].append(candidates)

    condition_groups = metric.get("condition_groups") or []
    if not condition_groups and metric.get("conditions"):
        condition_groups = [{
            "logic": "all",
            "required": True,
            "conditions": metric.get("conditions")
        }]

    for group in condition_groups:
        resolved_group = {
            "logic": group.get("logic") or "all",
            "conditions": []
        }
        unresolved_required = []

        for condition in group.get("conditions") or []:
            fieldname = resolve_field(doctype, condition.get("field") or [])
            if fieldname:
                item = clone_dict(condition)
                item["resolved_field"] = fieldname
                resolved_group["conditions"].append(item)
            elif not condition.get("optional"):
                unresolved_required.append(condition.get("field") or [])

        if unresolved_required:
            output["missing"].extend(unresolved_required)

        if group.get("required") and not resolved_group["conditions"]:
            output["missing"].append({
                "condition_group": group.get("logic") or "all",
                "candidates": [
                    item.get("field") for item in group.get("conditions") or []
                ]
            })

        output["condition_groups"].append(resolved_group)

    return output


def group_matches(row, group):
    conditions = group.get("conditions") or []
    if not conditions:
        return True

    results = []
    for condition in conditions:
        results.append(compare(
            row,
            condition.get("resolved_field"),
            condition.get("op"),
            expected=condition.get("value"),
            values=condition.get("values"),
            days=condition.get("days")
        ))

    if group.get("logic") == "any":
        for result_value in results:
            if result_value:
                return True
        return False

    for result_value in results:
        if not result_value:
            return False
    return True


def row_matches(row, metric, resolved):
    for fieldname in resolved.get("required_fields") or []:
        if not is_truthy(row.get(fieldname)):
            return False

    for group in resolved.get("condition_groups") or []:
        if not group_matches(row, group):
            return False

    mode = metric.get("mode")
    primary_fields = resolved.get("primary_fields") or []

    if mode in ["all", "all_required", "conditions", "average_fields", "sum"]:
        return True

    if mode in [
        "truthy", "falsy", "equals", "not_equals", "in", "not_in",
        "contains", "contains_any", "not_contains_any", "date_next_days",
        "date_before_today", "gt", "gte", "lt", "lte"
    ]:
        if not primary_fields:
            return False
        return compare(
            row,
            primary_fields[0],
            mode,
            expected=metric.get("value"),
            values=metric.get("values"),
            days=metric.get("days")
        )

    return False


def metric_output_base(metric):
    return {
        "id": metric.get("id"),
        "label": metric.get("label"),
        "category": metric.get("category") or "supporting",
        "support_status": metric.get("support_status") or "live",
        "requirement_basis": metric.get("requirement_basis"),
        "decision_use": metric.get("decision_use"),
        "limitations": metric.get("limitations") or [],
        "is_exception": bool(metric.get("is_exception"))
    }


def evaluate_base_metric(metric, include_rows=False):
    output = metric_output_base(metric)

    if metric.get("mode") == "unsupported":
        output.update({
            "source": metric.get("source"),
            "doctype": None,
            "value": None,
            "unit": metric.get("unit") or "records",
            "record_count": 0,
            "status": "unsupported",
            "message": metric.get("message"),
            "rows": [],
            "total": 0
        })
        return output

    source_alias = metric.get("source")
    source = resolved_sources.get(source_alias) or {}
    output["source"] = source_alias
    output["doctype"] = source.get("doctype")

    if source.get("status") != "available":
        output.update({
            "value": None,
            "unit": metric.get("unit") or "records",
            "record_count": 0,
            "status": source.get("status") or "unavailable",
            "message": source.get("message") or "Required source is unavailable.",
            "rows": [],
            "total": 0
        })
        return output

    doctype = source.get("doctype")
    resolved = resolve_metric_fields(metric, doctype)
    missing = resolved.get("missing") or []

    if metric.get("mode") != "all" and missing:
        output.update({
            "value": None,
            "unit": metric.get("unit") or "records",
            "record_count": 0,
            "status": "unsupported_field",
            "message": "Required field or field group is not installed.",
            "missing_field_candidates": missing,
            "rows": [],
            "total": 0
        })
        return output

    requested = []
    for fieldname in resolved.get("primary_fields") or []:
        if fieldname not in requested:
            requested.append(fieldname)
    for fieldname in resolved.get("value_fields") or []:
        if fieldname not in requested:
            requested.append(fieldname)
    for fieldname in resolved.get("required_fields") or []:
        if fieldname not in requested:
            requested.append(fieldname)
    for group in resolved.get("condition_groups") or []:
        for condition in group.get("conditions") or []:
            fieldname = condition.get("resolved_field")
            if fieldname and fieldname not in requested:
                requested.append(fieldname)

    if include_rows:
        for fieldname in SAFE_FIELDS.get(source_alias) or []:
            if fieldname not in requested:
                requested.append(fieldname)

    rows = fetch_rows(source_alias, source, requested)
    matched = []
    for row in rows:
        if row_matches(row, metric, resolved):
            matched.append(row)

    mode = metric.get("mode")
    value = len(matched)
    record_count = len(matched)

    if mode == "average_fields":
        numbers = []
        for row in matched:
            for fieldname in resolved.get("value_fields") or []:
                number = to_number(row.get(fieldname))
                if number is not None:
                    numbers.append(number)
                    break
        value = round(sum(numbers) / len(numbers), 2) if numbers else 0
        record_count = len(numbers)

    if mode == "sum":
        total_value = 0
        for row in matched:
            for fieldname in resolved.get("value_fields") or []:
                number = to_number(row.get(fieldname))
                if number is not None:
                    total_value = total_value + number
                    break
        value = round(total_value, 2)

    output_rows = []
    if include_rows:
        start = (page - 1) * page_size
        end = start + page_size
        output_fields = safe_fields(
            doctype,
            SAFE_FIELDS.get(source_alias) or ["name"]
        )
        for row in matched[start:end]:
            item = {}
            for fieldname in output_fields:
                item[fieldname] = row.get(fieldname)
            output_rows.append(item)

    output.update({
        "value": value,
        "unit": metric.get("unit") or "records",
        "record_count": record_count,
        "status": "available",
        "resolved_fields": {
            "primary": resolved.get("primary_fields") or [],
            "values": resolved.get("value_fields") or [],
            "required": resolved.get("required_fields") or []
        },
        "rows": output_rows,
        "total": len(matched),
        "truncated": len(rows) >= row_limit
    })
    return output


def find_metric(metrics_by_id, selected_id):
    return metrics_by_id.get(selected_id) or {}


def evaluate_derived_metric(metric, metrics_by_id):
    output = metric_output_base(metric)
    output["source"] = "derived"
    output["doctype"] = None

    if metric.get("mode") == "derived_sum":
        total_value = 0
        available_refs = 0
        unavailable_refs = []
        for ref_id in metric.get("refs") or []:
            selected = find_metric(metrics_by_id, ref_id)
            if selected.get("status") == "available":
                total_value = total_value + (to_number(selected.get("value")) or 0)
                available_refs = available_refs + 1
            else:
                unavailable_refs.append(ref_id)

        if available_refs == 0:
            output.update({
                "value": None,
                "unit": metric.get("unit") or "records",
                "record_count": 0,
                "status": "unavailable",
                "message": "None of the referenced live metrics is available.",
                "unavailable_refs": unavailable_refs,
                "rows": [],
                "total": 0
            })
            return output

        output.update({
            "value": round(total_value, 2),
            "unit": metric.get("unit") or "records",
            "record_count": available_refs,
            "status": "available",
            "message": "Some referenced metrics are unavailable." if unavailable_refs else "",
            "unavailable_refs": unavailable_refs,
            "rows": [],
            "total": round(total_value, 2)
        })
        return output

    if metric.get("mode") == "derived_percent":
        numerator = find_metric(metrics_by_id, metric.get("numerator_ref"))
        denominator = find_metric(metrics_by_id, metric.get("denominator_ref"))

        if numerator.get("status") != "available" or denominator.get("status") != "available":
            output.update({
                "value": None,
                "unit": "percent",
                "record_count": 0,
                "status": "unavailable",
                "message": "The numerator or denominator metric is unavailable.",
                "rows": [],
                "total": 0
            })
            return output

        denominator_value = to_number(denominator.get("value"))
        numerator_value = to_number(numerator.get("value"))
        if denominator_value in [None, 0]:
            output.update({
                "value": None,
                "unit": "percent",
                "record_count": 0,
                "status": "not_applicable",
                "message": "No denominator records match the current filters.",
                "rows": [],
                "total": 0
            })
            return output

        percentage = round((numerator_value or 0) * 100.0 / denominator_value, 2)
        output.update({
            "value": percentage,
            "unit": "percent",
            "record_count": int(denominator_value),
            "numerator": numerator_value or 0,
            "denominator": denominator_value,
            "status": "available",
            "rows": [],
            "total": denominator_value
        })
        return output

    output.update({
        "value": None,
        "unit": metric.get("unit") or "records",
        "record_count": 0,
        "status": "unsupported",
        "message": "Unsupported derived metric mode.",
        "rows": [],
        "total": 0
    })
    return output


if subcriterion not in CONFIG:
    frappe.throw("Unsupported Criterion 2 subcriterion.")

resolved_sources = {}
for alias in CONFIG[subcriterion].get("sources") or []:
    resolved_sources[alias] = resolve_source(alias)

metrics = []
metrics_by_id = {}

for configured_metric in CONFIG[subcriterion].get("metrics") or []:
    if configured_metric.get("mode") not in ["derived_sum", "derived_percent"]:
        evaluated = evaluate_base_metric(configured_metric, False)
        metrics.append(evaluated)
        metrics_by_id[evaluated.get("id")] = evaluated

for configured_metric in CONFIG[subcriterion].get("metrics") or []:
    if configured_metric.get("mode") in ["derived_sum", "derived_percent"]:
        evaluated = evaluate_derived_metric(configured_metric, metrics_by_id)
        metrics.append(evaluated)
        metrics_by_id[evaluated.get("id")] = evaluated


def format_limitations(limitations):
    values = []
    for item in limitations or []:
        text = clean_text(item)
        if text:
            values.append(text)
    return " ".join(values)


def answer_for_metric(selected_metric):
    if not selected_metric:
        return {
            "answer": "Unavailable: the linked metric is not configured.",
            "status": "unavailable",
            "confidence": "Unavailable"
        }

    if selected_metric.get("status") == "available":
        unit = selected_metric.get("unit") or "records"
        value = selected_metric.get("value")
        record_count = selected_metric.get("record_count") or 0

        if unit == "rating":
            answer = (
                str(value)
                + " is the live average from "
                + str(record_count)
                + " matching numeric response record(s)."
            )
        elif unit == "percent":
            answer = (
                str(value)
                + "% is the available calculation based on "
                + str(record_count)
                + " denominator record(s)."
            )
        elif unit == "SGD":
            answer = "SGD " + str(value) + " matches the current filters."
        else:
            answer = str(value or 0) + " record(s) match the current filters."

        support_status = selected_metric.get("support_status") or "live"
        limitations_text = format_limitations(selected_metric.get("limitations"))
        if support_status == "partial":
            answer = answer + " Partial evidence only."
            if limitations_text:
                answer = answer + " " + limitations_text
            confidence = "Partial"
        else:
            confidence = "Live"

        return {
            "answer": answer,
            "status": "available",
            "confidence": confidence
        }

    return {
        "answer": "Unavailable: " + clean_text(
            selected_metric.get("message")
            or selected_metric.get("status")
            or "required source, field or relationship is unavailable"
        ),
        "status": selected_metric.get("status") or "unavailable",
        "confidence": "Unavailable"
    }


questions = []
for question in QUESTION_REGISTRY.get(subcriterion) or []:
    selected_metric = metrics_by_id.get(question.get("metric_id")) or {}
    answer_result = answer_for_metric(selected_metric)
    questions.append({
        "id": question.get("id"),
        "criterion": subcriterion,
        "question": question.get("question"),
        "answer": answer_result.get("answer"),
        "metric_id": question.get("metric_id"),
        "status": answer_result.get("status"),
        "confidence": answer_result.get("confidence"),
        "support_status": selected_metric.get("support_status") or "unavailable",
        "requirement_basis": question.get("requirement_basis") or selected_metric.get("requirement_basis"),
        "decision_use": question.get("decision_use") or selected_metric.get("decision_use"),
        "limitations": selected_metric.get("limitations") or [],
        "doctype": selected_metric.get("doctype")
    })

sources = []
for alias in CONFIG[subcriterion].get("sources") or []:
    sources.append(resolved_sources.get(alias))

management_metrics = []
supporting_metrics = []
exceptions = []
evidence_gaps = []
data_quality = []

for metric in metrics:
    if metric.get("category") == "management":
        management_metrics.append(metric)
    else:
        supporting_metrics.append(metric)

    if metric.get("is_exception"):
        exceptions.append(metric)

    if metric.get("category") == "management" and metric.get("status") != "available":
        evidence_gaps.append({
            "criterion": subcriterion,
            "metric_id": metric.get("id"),
            "requirement_basis": metric.get("requirement_basis"),
            "support_status": metric.get("support_status"),
            "status": metric.get("status"),
            "detail": metric.get("message") or "Required evidence is unavailable."
        })

for source in sources:
    if source and source.get("status") != "available":
        data_quality.append({
            "criterion": subcriterion,
            "check": "Source availability",
            "source": source.get("doctype") or " / ".join(source.get("candidates") or []),
            "status": source.get("status"),
            "detail": source.get("message") or "Source is unavailable."
        })

for metric in metrics:
    if metric.get("status") in ["unsupported_field", "permission_denied", "unavailable"]:
        data_quality.append({
            "criterion": subcriterion,
            "check": metric.get("label"),
            "source": metric.get("doctype") or metric.get("source"),
            "status": metric.get("status"),
            "detail": metric.get("message") or "Metric is unavailable."
        })

available_sources = 0
for source in sources:
    if source and source.get("status") == "available":
        available_sources = available_sources + 1

available_metrics = 0
partial_metrics = 0
unavailable_metrics = 0
for metric in metrics:
    if metric.get("status") == "available":
        available_metrics = available_metrics + 1
        if metric.get("support_status") == "partial":
            partial_metrics = partial_metrics + 1
    else:
        unavailable_metrics = unavailable_metrics + 1

available_questions = 0
partial_questions = 0
unavailable_questions = 0
for question in questions:
    if question.get("status") == "available":
        available_questions = available_questions + 1
        if question.get("confidence") == "Partial":
            partial_questions = partial_questions + 1
    else:
        unavailable_questions = unavailable_questions + 1

result = {
    "ok": True,
    "meta": {
        "api_method": "ucc_analytics_criterion_2",
        "platform_version": "1.10.0",
        "catalogue_version": "2.0.0",
        "status": "revised_management_catalogue",
        "generated_at": frappe.utils.now(),
        "action": action,
        "subcriterion": subcriterion,
        "row_limit": row_limit,
        "management_question_count": len(questions)
    },
    "policy": POLICY_REGISTRY.get(subcriterion),
    "filters": filters,
    "sources": sources,
    "metrics": metrics,
    "management_metrics": management_metrics,
    "supporting_metrics": supporting_metrics,
    "questions": questions,
    "exceptions": exceptions,
    "evidence_gaps": evidence_gaps,
    "data_quality": data_quality,
    "source_summary": {
        "total": len(sources),
        "available": available_sources,
        "issues": len(sources) - available_sources
    },
    "metric_summary": {
        "total": len(metrics),
        "available": available_metrics,
        "partial": partial_metrics,
        "unavailable": unavailable_metrics
    },
    "question_summary": {
        "total": len(questions),
        "available": available_questions,
        "partial": partial_questions,
        "unavailable": unavailable_questions
    },
    "data": {
        "sources": sources,
        "metrics": metrics,
        "management_metrics": management_metrics,
        "supporting_metrics": supporting_metrics,
        "questions": questions,
        "exceptions": exceptions,
        "evidence_gaps": evidence_gaps,
        "data_quality": data_quality
    },
    "warnings": [
        "Criterion 2 spans HR, communication, data, knowledge and feedback sources.",
        "Criterion 2.2.2 has been added as a distinct analytics subcriterion under the combined communication procedure.",
        "Raw record counts are supporting metrics and are not automatically treated as compliance conclusions.",
        "Partial proxy metrics are labelled and retain their stated limitations.",
        "Missing fields, denominators, approval trails and child-table relationships are reported as unavailable rather than zero.",
        "The Student Satisfaction Survey procedure contains a controlled-document requirement-numbering inconsistency that should be corrected separately."
    ]
}

if action == "policy_registry":
    result["registry"] = POLICY_REGISTRY

if action == "question_catalogue":
    result["catalogue"] = QUESTION_REGISTRY

if action == "source_status":
    result["source_status"] = sources

if action == "drilldown":
    selected_config = None
    for configured_metric in CONFIG[subcriterion].get("metrics") or []:
        if configured_metric.get("id") == metric_id:
            selected_config = configured_metric
            break

    if not selected_config:
        frappe.throw("Unknown Criterion 2 metric.")

    if selected_config.get("mode") in ["derived_sum", "derived_percent"]:
        result["drilldown"] = metrics_by_id.get(metric_id)
    elif selected_config.get("mode") == "unsupported":
        result["drilldown"] = metrics_by_id.get(metric_id)
    else:
        result["drilldown"] = evaluate_base_metric(selected_config, True)

frappe.response["message"] = result
