"""
UCC Intelligence Platform Server Script

Visible name:
    UCC Shared - Diagnostics

Script type:
    API

API method:
    ucc_shared_diagnostics

Purpose:
    Diagnose approved UCC DocType candidates, current-user readability,
    fallback resolution and available metadata fields. The client cannot pass
    arbitrary DocTypes to this script.
"""

payload_input = frappe.form_dict.get("payload") or {}
payload = json.loads(payload_input) if isinstance(payload_input, str) else payload_input
if not isinstance(payload, dict):
    payload = {}
requested_dashboard = payload.get("dashboard") or ""

APPROVED_SOURCE_GROUPS = [{'key': 'appraisal',
  'label': 'Appraisal',
  'candidates': ['Appraisal', 'Performance Appraisal'],
  'criteria': ['criterion_1', 'criterion_2']},
 {'key': 'business_impact',
  'label': 'Business Impact',
  'candidates': ['Business Impact Analysis'],
  'criteria': ['criterion_1']},
 {'key': 'esg_strategy', 'label': 'Esg Strategy', 'candidates': ['ESG Strategy Insights'], 'criteria': ['criterion_1']},
 {'key': 'esg_tracker', 'label': 'Esg Tracker', 'candidates': ['ESG Impact Tracker'], 'criteria': ['criterion_1']},
 {'key': 'management_review',
  'label': 'Management Review',
  'candidates': ['Management Review'],
  'criteria': ['criterion_1', 'criterion_6', 'criterion_7']},
 {'key': 'oversight', 'label': 'Oversight', 'candidates': ['Oversight Framework'], 'criteria': ['criterion_1']},
 {'key': 'policy_control',
  'label': 'Policies and Procedures',
  'candidates': ['Policies and Standards Type', 'Quality Procedure'],
  'criteria': ['criterion_1']},
 {'key': 'quality_action',
  'label': 'Quality Action',
  'candidates': ['Quality Action'],
  'criteria': ['criterion_1', 'criterion_2', 'criterion_6', 'criterion_7']},
 {'key': 'quality_goal', 'label': 'Quality Goal', 'candidates': ['Quality Goal'], 'criteria': ['criterion_1']},
 {'key': 'risk_register',
  'label': 'Risk Register',
  'candidates': ['Risk Register and Mitigation Plans'],
  'criteria': ['criterion_1']},
 {'key': 'staff_goal', 'label': 'Staff Goal', 'candidates': ['Goal'], 'criteria': ['criterion_1']},
 {'key': 'stakeholder_engagement',
  'label': 'Stakeholder Engagement',
  'candidates': ['Stakeholder Engagement Strategy'],
  'criteria': ['criterion_1', 'criterion_2']},
 {'key': 'stakeholder_registry',
  'label': 'Stakeholder Registry',
  'candidates': ['Stakeholder Registry'],
  'criteria': ['criterion_1', 'criterion_2']},
 {'key': 'document_control',
  'label': 'Document Control',
  'candidates': ['Document Control'],
  'criteria': ['criterion_2']},
 {'key': 'employee', 'label': 'Employee', 'candidates': ['Employee'], 'criteria': ['criterion_2']},
 {'key': 'employee_grievance',
  'label': 'Employee Grievance',
  'candidates': ['Employee Grievance'],
  'criteria': ['criterion_2']},
 {'key': 'employee_onboarding',
  'label': 'Employee Onboarding',
  'candidates': ['Employee Onboarding'],
  'criteria': ['criterion_2']},
 {'key': 'employee_separation',
  'label': 'Employee Separation',
  'candidates': ['Employee Separation'],
  'criteria': ['criterion_2']},
 {'key': 'end_course_survey',
  'label': 'End Course Survey',
  'candidates': ['End of Course Survey'],
  'criteria': ['criterion_2']},
 {'key': 'essential_information',
  'label': 'Essential Information',
  'candidates': ['Essential Information'],
  'criteria': ['criterion_2']},
 {'key': 'exit_interview',
  'label': 'Exit Interview',
  'candidates': ['Exit Interview', 'Exit Interview Form'],
  'criteria': ['criterion_2']},
 {'key': 'exit_interview_survey',
  'label': 'Exit Interview Survey',
  'candidates': ['Exit Interview Survey'],
  'criteria': ['criterion_2']},
 {'key': 'helpdesk_ticket',
  'label': 'Helpdesk Ticket',
  'candidates': ['HD Ticket', 'Issue', 'Helpdesk Ticket'],
  'criteria': ['criterion_2']},
 {'key': 'interview_feedback',
  'label': 'Interview Feedback',
  'candidates': ['Interview Feedback'],
  'criteria': ['criterion_2']},
 {'key': 'job_applicant', 'label': 'Job Applicant', 'candidates': ['Job Applicant'], 'criteria': ['criterion_2']},
 {'key': 'job_requisition', 'label': 'Job Requisition', 'candidates': ['Job Requisition'], 'criteria': ['criterion_2']},
 {'key': 'letter_head', 'label': 'Letter Head', 'candidates': ['Letter Head'], 'criteria': ['criterion_2']},
 {'key': 'manpower_planning',
  'label': 'Manpower Planning',
  'candidates': ['Manpower Planning and Deployment'],
  'criteria': ['criterion_2']},
 {'key': 'material_vetting',
  'label': 'Material Vetting Form',
  'candidates': ['Material Vetting Form'],
  'criteria': ['criterion_2']},
 {'key': 'print_format', 'label': 'Print Format', 'candidates': ['Print Format'], 'criteria': ['criterion_2']},
 {'key': 'quality_meeting',
  'label': 'Quality Meeting',
  'candidates': ['Quality Meeting'],
  'criteria': ['criterion_2', 'criterion_7']},
 {'key': 'quality_performance',
  'label': 'Quality Performance',
  'candidates': ['Quality Performance Outcomes', 'Quality Performance Outcome'],
  'criteria': ['criterion_2', 'criterion_7']},
 {'key': 'salary_component',
  'label': 'Salary Component',
  'candidates': ['Salary Component'],
  'criteria': ['criterion_2']},
 {'key': 'salary_structure',
  'label': 'Salary Structure',
  'candidates': ['Salary Structure'],
  'criteria': ['criterion_2']},
 {'key': 'staff_onboarding_survey',
  'label': 'Staff Onboarding Survey',
  'candidates': ['Staff Onboarding Survey'],
  'criteria': ['criterion_2']},
 {'key': 'staff_survey', 'label': 'Staff Survey', 'candidates': ['Staff Survey'], 'criteria': ['criterion_2']},
 {'key': 'student_onboarding_survey',
  'label': 'Student Onboarding Survey',
  'candidates': ['Student Onboarding Survey'],
  'criteria': ['criterion_2']},
 {'key': 'survey_management',
  'label': 'Survey Management',
  'candidates': ['Survey Management'],
  'criteria': ['criterion_2']},
 {'key': 'survey_tracking',
  'label': 'Survey Tracking',
  'candidates': ['Survey Tracking', 'Survey Response'],
  'criteria': ['criterion_2']},
 {'key': 'tna',
  'label': 'Training Needs Analysis',
  'candidates': ['Training Needs Analysis'],
  'criteria': ['criterion_2']},
 {'key': 'todo', 'label': 'Todo', 'candidates': ['ToDo', 'To Do'], 'criteria': ['criterion_2']},
 {'key': 'training_event', 'label': 'Training Event', 'candidates': ['Training Event'], 'criteria': ['criterion_2']},
 {'key': 'training_feedback',
  'label': 'Training Feedback',
  'candidates': ['Training Feedback'],
  'criteria': ['criterion_2']},
 {'key': 'training_program',
  'label': 'Training Program',
  'candidates': ['Training Program'],
  'criteria': ['criterion_2']},
 {'key': 'training_result', 'label': 'Training Result', 'candidates': ['Training Result'], 'criteria': ['criterion_2']},
 {'key': 'training_sponsorship',
  'label': 'Training Sponsorship',
  'candidates': ['Training Sponsorship Application'],
  'criteria': ['criterion_2']},
 {'key': 'agent', 'label': 'Agent', 'candidates': ['Agent'], 'criteria': ['criterion_3']},
 {'key': 'annual_review',
  'label': 'Annual Review',
  'candidates': ['Agent Annual Performance Review'],
  'criteria': ['criterion_3']},
 {'key': 'applicant', 'label': 'Applicant', 'candidates': ['Student Applicant'], 'criteria': ['criterion_3']},
 {'key': 'claim', 'label': 'Claim', 'candidates': ['Agent Claim Form'], 'criteria': ['criterion_3']},
 {'key': 'contract', 'label': 'Contract', 'candidates': ['Agent Contract'], 'criteria': ['criterion_3']},
 {'key': 'nda', 'label': 'Nda', 'candidates': ['Non Disclosure Agreement'], 'criteria': ['criterion_3']},
 {'key': 'offboarding', 'label': 'Offboarding', 'candidates': ['External Offboarding'], 'criteria': ['criterion_3']},
 {'key': 'onboarding', 'label': 'Onboarding', 'candidates': ['External Onboarding'], 'criteria': ['criterion_3']},
 {'key': 'provider_rating',
  'label': 'Provider Rating',
  'candidates': ['Provider Rating', 'Supplier Rating'],
  'criteria': ['criterion_3', 'criterion_6']},
 {'key': 'c4_academic_support',
  'label': 'Academic Support',
  'candidates': ['Intervention Issue Academic Support'],
  'criteria': ['criterion_4']},
 {'key': 'c4_adjustments', 'label': 'Adjustments', 'candidates': ['Student Log'], 'criteria': ['criterion_4']},
 {'key': 'c4_admission', 'label': 'Admission', 'candidates': ['Student Admission UCC'], 'criteria': ['criterion_4']},
 {'key': 'c4_applicant', 'label': 'Applicant', 'candidates': ['Student Applicant'], 'criteria': ['criterion_4']},
 {'key': 'c4_attendance', 'label': 'Attendance', 'candidates': ['Student Attendance'], 'criteria': ['criterion_4']},
 {'key': 'c4_contract', 'label': 'Contract', 'candidates': ['Student Admission UCC'], 'criteria': ['criterion_4']},
 {'key': 'c4_counselling',
  'label': 'Counselling',
  'candidates': ['Pre Course Counselling Declaration'],
  'criteria': ['criterion_4']},
 {'key': 'c4_fps', 'label': 'Fps', 'candidates': ['FPS Record'], 'criteria': ['criterion_4']},
 {'key': 'c4_integrity_support',
  'label': 'Integrity Support',
  'candidates': ['Intervention Issue Academic Integrity'],
  'criteria': ['criterion_4']},
 {'key': 'c4_invoice', 'label': 'Invoice', 'candidates': ['Sales Invoice'], 'criteria': ['criterion_4']},
 {'key': 'c4_leave', 'label': 'Leave', 'candidates': ['Student Leave Application'], 'criteria': ['criterion_4']},
 {'key': 'c4_payment', 'label': 'Payment', 'candidates': ['Payment Entry'], 'criteria': ['criterion_4']},
 {'key': 'c4_student_log', 'label': 'Student Log', 'candidates': ['Student Log'], 'criteria': ['criterion_4']},
 {'key': 'c4_warning',
  'label': 'Warning',
  'candidates': ['Dismissal Letters due to Attendance Requirements'],
  'criteria': ['criterion_4']},
 {'key': 'c4_wellness_support',
  'label': 'Wellness Support',
  'candidates': ['Intervention Issue Wellness Services'],
  'criteria': ['criterion_4']},
 {'key': 'c5_academic_year', 'label': 'Academic Year', 'candidates': ['Academic Year'], 'criteria': ['criterion_5']},
 {'key': 'c5_assessment_plan',
  'label': 'Assessment Plan',
  'candidates': ['Assessment Plan'],
  'criteria': ['criterion_5']},
 {'key': 'c5_course', 'label': 'Course', 'candidates': ['Course'], 'criteria': ['criterion_5']},
 {'key': 'c5_course_proposal',
  'label': 'Course Proposal',
  'candidates': ['Course Proposal'],
  'criteria': ['criterion_5']},
 {'key': 'c5_course_review', 'label': 'Course Review', 'candidates': ['Course Review'], 'criteria': ['criterion_5']},
 {'key': 'c5_program', 'label': 'Program', 'candidates': ['Program'], 'criteria': ['criterion_5']},
 {'key': 'c5_student_group', 'label': 'Student Group', 'candidates': ['Student Group'], 'criteria': ['criterion_5']},
 {'key': 'operational_outcomes',
  'label': 'Operational Outcomes',
  'candidates': ['Operational Outcomes Cost Time Saving'],
  'criteria': ['criterion_6', 'criterion_7']},
 {'key': 'shared_agent', 'label': 'Agent', 'candidates': ['Agent'], 'criteria': ['shared']},
 {'key': 'shared_agent_contract', 'label': 'Agent Contract', 'candidates': ['Agent Contract'], 'criteria': ['shared']},
 {'key': 'shared_course_enrollment',
  'label': 'Course Enrollment',
  'candidates': ['Course Enrollment'],
  'criteria': ['shared']},
 {'key': 'shared_payment_entry', 'label': 'Payment Entry', 'candidates': ['Payment Entry'], 'criteria': ['shared']},
 {'key': 'shared_provider_rating',
  'label': 'Provider Rating',
  'candidates': ['Provider Rating'],
  'criteria': ['shared']},
 {'key': 'shared_quality_action', 'label': 'Quality Action', 'candidates': ['Quality Action'], 'criteria': ['shared']},
 {'key': 'shared_sales_invoice', 'label': 'Sales Invoice', 'candidates': ['Sales Invoice'], 'criteria': ['shared']},
 {'key': 'shared_student', 'label': 'Student', 'candidates': ['Student'], 'criteria': ['shared']},
 {'key': 'shared_student_admission_ucc',
  'label': 'Student Admission UCC',
  'candidates': ['Student Admission UCC'],
  'criteria': ['shared']},
 {'key': 'shared_student_applicant',
  'label': 'Student Applicant',
  'candidates': ['Student Applicant'],
  'criteria': ['shared']},
 {'key': 'shared_student_attendance',
  'label': 'Student Attendance',
  'candidates': ['Student Attendance'],
  'criteria': ['shared']},
 {'key': 'shared_student_leave_application',
  'label': 'Student Leave Application',
  'candidates': ['Student Leave Application'],
  'criteria': ['shared']},
 {'key': 'shared_supplier_rating',
  'label': 'Supplier Rating',
  'candidates': ['Supplier Rating'],
  'criteria': ['shared']}]

def clean_text(value):
    return str(value or "").strip()

def lower_text(value):
    return clean_text(value).lower()

def is_permission_error(error):
    text = lower_text(error)
    return (
        "permission" in text
        or "not permitted" in text
        or "not allowed" in text
    )

def field_inventory(doctype):
    try:
        meta = frappe.get_meta(doctype)
        fields = []
        for field in meta.fields:
            fieldname = clean_text(field.fieldname)
            if fieldname and fieldname not in fields:
                fields.append(fieldname)
        return {
            "status": "available",
            "field_count": len(fields),
            "fields": fields
        }
    except Exception as error:
        return {
            "status": "unavailable",
            "field_count": 0,
            "fields": [],
            "message": clean_text(error)
        }

def probe_candidate(doctype):
    attempt = {
        "doctype": doctype,
        "exists": False,
        "metadata_status": "not_checked",
        "list_status": "not_checked",
        "status": "unavailable",
        "message": "",
        "field_count": 0,
        "fields": []
    }

    try:
        attempt["exists"] = bool(frappe.db.exists("DocType", doctype))
    except Exception as error:
        attempt["message"] = clean_text(error)

    inventory = field_inventory(doctype)
    attempt["metadata_status"] = inventory.get("status")
    attempt["field_count"] = inventory.get("field_count") or 0
    attempt["fields"] = inventory.get("fields") or []
    if inventory.get("status") != "available":
        attempt["message"] = inventory.get("message") or attempt.get("message") or "DocType metadata is unavailable."
        return attempt

    attempt["exists"] = True
    try:
        rows = frappe.get_list(
            doctype,
            fields=["name"],
            limit_start=0,
            limit_page_length=1,
            order_by="modified desc"
        ) or []
        attempt["list_status"] = "available"
        attempt["status"] = "available"
        attempt["sample_available"] = bool(rows)
        attempt["message"] = "Readable by the signed-in user."
    except Exception as error:
        attempt["list_status"] = "permission_denied" if is_permission_error(error) else "unavailable"
        attempt["status"] = attempt["list_status"]
        attempt["message"] = clean_text(error)
    return attempt

source_groups = []
unresolved = []
fallbacks = []

for definition in APPROVED_SOURCE_GROUPS:
    criteria = definition.get("criteria") or []
    if requested_dashboard and requested_dashboard not in criteria:
        continue
    if not requested_dashboard and criteria == ["shared"]:
        continue

    attempts = []
    resolved_doctype = None
    resolved_index = -1
    group_status = "unavailable"

    candidates = definition.get("candidates") or []
    for candidate_index in range(len(candidates)):
        candidate = candidates[candidate_index]
        attempt = probe_candidate(candidate)
        attempts.append(attempt)
        if attempt.get("status") == "available":
            resolved_doctype = candidate
            resolved_index = candidate_index
            group_status = "fallback" if candidate_index > 0 else "available"
            break
        if attempt.get("status") == "permission_denied":
            group_status = "permission_denied"
            break

    detail = ""
    if resolved_doctype:
        if resolved_index > 0:
            detail = "The first approved candidate was unavailable. The next readable approved fallback was selected."
        else:
            detail = "The primary approved candidate is installed and readable."
    elif attempts:
        detail_parts = []
        for attempt in attempts:
            detail_parts.append(attempt.get("doctype") + ": " + (attempt.get("message") or attempt.get("status") or "unavailable"))
        detail = "; ".join(detail_parts)
    else:
        detail = "No approved candidate is configured."

    row = {
        "key": definition.get("key"),
        "label": definition.get("label"),
        "criteria": criteria,
        "candidates": candidates,
        "resolved_doctype": resolved_doctype,
        "status": group_status,
        "detail": detail,
        "attempts": attempts
    }
    source_groups.append(row)
    if group_status == "fallback":
        fallbacks.append(row)
    elif group_status != "available":
        unresolved.append(row)

frappe.response["message"] = {
    "ok": True,
    "meta": {
        "api_method": "ucc_shared_diagnostics",
        "platform_version": "1.9.5",
        "generated_at": frappe.utils.now(),
        "user": frappe.session.user,
        "dashboard": requested_dashboard,
        "approved_only": True
    },
    "summary": {
        "source_groups": len(source_groups),
        "available": len(source_groups) - len(unresolved) - len(fallbacks),
        "fallbacks": len(fallbacks),
        "unresolved": len(unresolved)
    },
    "source_groups": source_groups,
    "unresolved": unresolved,
    "fallbacks": fallbacks
}
