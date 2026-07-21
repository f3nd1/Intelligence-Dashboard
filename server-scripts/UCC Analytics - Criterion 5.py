"""
UCC Intelligence Platform Server Script

Visible name:
    UCC Analytics - Criterion 5

Script type:
    API

API method:
    ucc_analytics_criterion_5

Purpose:
    Return permission-aware live analytics foundations for EduTrust Criterion 5.

Current status:
    Live API foundation following the same architecture as Criterion 2. Only the
    selected subcriterion is evaluated. Unsupported fields and unavailable
    sources are reported explicitly instead of being guessed.

Deployment:
    Allow Guest must remain disabled.
"""

payload_input = frappe.form_dict.get("payload") or {}
try:
    payload = json.loads(payload_input) if isinstance(payload_input, str) else payload_input
except Exception:
    payload = {}
if not isinstance(payload, dict):
    payload = {}

action = payload.get("action") or "summary"
subcriterion = payload.get("subcriterion") or "5.1.1"
filters = payload.get("filters") or {}
if not isinstance(filters, dict):
    filters = {}
metric_id = payload.get("metric_id")
page = payload.get("page") or 1
page_size = payload.get("page_size") or 50
row_limit = payload.get("limit") or 500

try:
    page = max(1, int(page))
except Exception:
    page = 1

try:
    page_size = max(1, min(int(page_size), 200))
except Exception:
    page_size = 50

try:
    row_limit = max(1, min(int(row_limit), 2000))
except Exception:
    row_limit = 500

ALLOWED_ACTIONS = ["summary", "source_status", "policy_registry", "drilldown"]
if action not in ALLOWED_ACTIONS:
    frappe.throw("Unsupported Criterion 5 action.")

POLICY_REGISTRY = {'5.1.1': {'title': 'Course Design and Development', 'policy': 'Criterion 5.1.1', 'version': 'Current'},
 '5.1.2': {'title': 'Course Review', 'policy': 'Criterion 5.1.2', 'version': 'Current'},
 '5.2.1': {'title': 'Course Planning', 'policy': 'Criterion 5.2.1', 'version': 'Current'},
 '5.2.2': {'title': 'Course Delivery', 'policy': 'Criterion 5.2.2', 'version': 'Current'},
 '5.3.1': {'title': 'Partnerships', 'policy': 'Criterion 5.3.1', 'version': 'Current'},
 '5.4': {'title': 'Student Feedback and Learning Support', 'policy': 'Criterion 5.4', 'version': 'Current'},
 '5.5': {'title': 'Assessment', 'policy': 'Criterion 5.5', 'version': 'Current'}}

SOURCE_CANDIDATES = {'academic_year': ['Academic Year'],
 'student_group': ['Student Group'],
 'course': ['Course'],
 'program': ['Program'],
 'course_proposal': ['Course Proposal'],
 'course_review': ['Course Review'],
 'module_review': ['Module Review'],
 'assessment_plan': ['Assessment Plan'],
 'assessment_result': ['Assessment Result'],
 'course_schedule': ['Course Schedule'],
 'course_enrollment': ['Course Enrollment'],
 'student_attendance': ['Student Attendance'],
 'student_batch': ['Student Batch Name'],
 'shortlisted_applicant': ['Shortlisted Applicants', 'Student Admission UCC'],
 'classroom_observation': ['Classroom Observation'],
 'survey_response': ['Survey Response'],
 'partnership_agreement': ['Partnership Agreement'],
 'partnership_management': ['Partnerships Agreement Management'],
 'provider_rating': ['Supplier Rating']}

SAFE_FIELDS = {'academic_year': ['name', 'academic_year_name', 'year_start_date', 'year_end_date', 'modified'],
 'student_group': ['name',
                   'student_group_name',
                   'academic_year',
                   'program',
                   'course',
                   'disabled',
                   'max_strength',
                   'custom_module_status',
                   'custom_instructor',
                   'custom_instructor_full_name',
                   'modified'],
 'course': ['name', 'course_name', 'department', 'topics', 'assessment_criteria', 'modified'],
 'program': ['name', 'program_name', 'department', 'modified'],
 'course_proposal': ['name',
                     'course_title',
                     'approval_status',
                     'proposed_date',
                     'decision_date',
                     'ssg_approval_date',
                     'docstatus',
                     'modified'],
 'course_review': ['name',
                   'course',
                   'review_date',
                   'next_review_date',
                   'review_type',
                   'review_status',
                   'recommendation_implementation_status',
                   'modified'],
 'module_review': ['name',
                   'course',
                   'module',
                   'module_class_details',
                   'date_of_review',
                   'status',
                   'type_of_review',
                   'recommendation_implementation_status',
                   'modified'],
 'assessment_plan': ['name',
                     'assessment_name',
                     'student_group',
                     'course',
                     'program',
                     'academic_year',
                     'schedule_date',
                     'room',
                     'examiner',
                     'supervisor',
                     'maximum_assessment_score',
                     'modified'],
 'assessment_result': ['name',
                       'assessment_plan',
                       'program',
                       'course',
                       'academic_year',
                       'student',
                       'student_name',
                       'student_group',
                       'maximum_score',
                       'total_score',
                       'grade',
                       'modified'],
 'course_schedule': ['name',
                     'student_group',
                     'instructor',
                     'instructor_name',
                     'course',
                     'schedule_date',
                     'room',
                     'from_time',
                     'to_time',
                     'program',
                     'modified'],
 'course_enrollment': ['name', 'student', 'student_name', 'course', 'program', 'enrollment_date', 'modified'],
 'student_attendance': ['name',
                        'student',
                        'course_schedule',
                        'date',
                        'student_group',
                        'status',
                        'duration_attended',
                        'expected_duration',
                        'modified'],
 'student_batch': ['name', 'batch_name', 'modified'],
 'shortlisted_applicant': ['name',
                           'student_name',
                           'program',
                           'student_batch',
                           'application_status',
                           'contract_start',
                           'contract_end',
                           'actual_commencement_date',
                           'course_commencement_date',
                           'modified'],
 'classroom_observation': ['name',
                           'date_of_observation',
                           'type_of_observation',
                           'module_class_details',
                           'course',
                           'module_name',
                           'name_of_teacher',
                           'platform_delivery',
                           'prior_notice',
                           'observers_signature',
                           'teachers_signature',
                           'areas_text',
                           'modified'],
 'survey_response': ['name',
                     'title',
                     'email',
                     'program',
                     'course',
                     'posting_date',
                     'frequency',
                     'rating',
                     'score',
                     'modified'],
 'partnership_agreement': ['name',
                           'party_name',
                           'posting_date',
                           'start_date',
                           'end_date',
                           'pa_agreement_type',
                           'pa_partner_name',
                           'requires_nda',
                           'nda_acknowledged',
                           'signed_date',
                           'ucc_signed_date',
                           'modified'],
 'partnership_management': ['name',
                            'agreement_title',
                            'party_name',
                            'type',
                            'status',
                            'agreement_date',
                            'expiry_date',
                            'average_identification_and_selection_score',
                            'modified'],
 'provider_rating': ['name',
                     'posting_date',
                     'year',
                     'status',
                     'type',
                     'document',
                     'supplier',
                     'evaluation_stage',
                     'rating',
                     'rating_likert',
                     'modified']}

FILTER_FIELD_CANDIDATES = {'year': ['academic_year', 'year'],
 'student_group': ['student_group', 'module_class_details'],
 'program': ['program'],
 'status': ['status', 'review_status', 'application_status', 'approval_status']}

CONFIG = {'5.1.1': {'sources': ['course_proposal', 'course', 'program', 'assessment_plan'],
           'metrics': [{'id': 'c511-proposals',
                        'label': 'Course proposals',
                        'source': 'course_proposal',
                        'mode': 'all'},
                       {'id': 'c511-approved-proposals',
                        'label': 'Approved course proposals',
                        'source': 'course_proposal',
                        'mode': 'in',
                        'field': ['approval_status'],
                        'values': ['Approved', 'Accepted', 'Endorsed']},
                       {'id': 'c511-modules', 'label': 'Modules in scope', 'source': 'course', 'mode': 'all'},
                       {'id': 'c511-topics',
                        'label': 'Modules with curriculum topics',
                        'source': 'course',
                        'mode': 'truthy',
                        'field': ['topics', 'custom_list_of_learning_objective']},
                       {'id': 'c511-assessment-criteria',
                        'label': 'Modules with assessment criteria',
                        'source': 'course',
                        'mode': 'truthy',
                        'field': ['assessment_criteria']},
                       {'id': 'c511-assessment-plans',
                        'label': 'Assessment plans',
                        'source': 'assessment_plan',
                        'mode': 'all'},
                       {'id': 'c511-course-mapping',
                        'label': 'Course-to-module mapping coverage',
                        'source': 'program',
                        'mode': 'unsupported',
                        'message': 'Program.courses is a child-table relationship and is not evaluated by the '
                                   'lightweight foundation API.'}]},
 '5.1.2': {'sources': ['module_review', 'course_review'],
           'metrics': [{'id': 'c512-module-reviews',
                        'label': 'Module reviews',
                        'source': 'module_review',
                        'mode': 'all'},
                       {'id': 'c512-approved-module-reviews',
                        'label': 'Approved module reviews',
                        'source': 'module_review',
                        'mode': 'in',
                        'field': ['status'],
                        'values': ['Approved', 'Completed', 'Closed']},
                       {'id': 'c512-course-reviews',
                        'label': 'Course reviews',
                        'source': 'course_review',
                        'mode': 'all'},
                       {'id': 'c512-completed-course-reviews',
                        'label': 'Completed course reviews',
                        'source': 'course_review',
                        'mode': 'in',
                        'field': ['review_status', 'status'],
                        'values': ['Approved', 'Completed', 'Closed']},
                       {'id': 'c512-overdue-reviews',
                        'label': 'Course reviews overdue',
                        'source': 'course_review',
                        'mode': 'date_before_today',
                        'field': ['next_review_date']},
                       {'id': 'c512-pending-recommendations',
                        'label': 'Recommendations not implemented',
                        'source': 'module_review',
                        'mode': 'in',
                        'field': ['recommendation_implementation_status'],
                        'values': ['Not Implemented', 'Pending', 'Open']},
                       {'id': 'c512-action-plans',
                        'label': 'Course-review action-plan completion',
                        'source': 'course_review',
                        'mode': 'unsupported',
                        'message': 'Course Review.actionplan_progress is a child table and is not evaluated by the '
                                   'lightweight foundation API.'}]},
 '5.2.1': {'sources': ['student_batch', 'student_group', 'course_schedule', 'shortlisted_applicant'],
           'metrics': [{'id': 'c521-intakes', 'label': 'Intakes', 'source': 'student_batch', 'mode': 'all'},
                       {'id': 'c521-module-classes',
                        'label': 'Module classes',
                        'source': 'student_group',
                        'mode': 'all'},
                       {'id': 'c521-teachers-assigned',
                        'label': 'Module classes with Teacher assigned',
                        'source': 'student_group',
                        'mode': 'truthy',
                        'field': ['custom_instructor', 'instructor']},
                       {'id': 'c521-sessions',
                        'label': 'Scheduled Module sessions',
                        'source': 'course_schedule',
                        'mode': 'all'},
                       {'id': 'c521-session-teachers',
                        'label': 'Scheduled sessions with Teacher',
                        'source': 'course_schedule',
                        'mode': 'truthy',
                        'field': ['instructor']},
                       {'id': 'c521-session-rooms',
                        'label': 'Scheduled sessions with room',
                        'source': 'course_schedule',
                        'mode': 'truthy',
                        'field': ['room']},
                       {'id': 'c521-admissions',
                        'label': 'Shortlisted Applicants',
                        'source': 'shortlisted_applicant',
                        'mode': 'all'},
                       {'id': 'c521-contract-dates',
                        'label': 'Applicants with complete contract dates',
                        'source': 'shortlisted_applicant',
                        'mode': 'all_required',
                        'fields': [['contract_start'], ['contract_end']]}]},
 '5.2.2': {'sources': ['course_schedule', 'student_attendance', 'classroom_observation', 'student_group'],
           'metrics': [{'id': 'c522-sessions',
                        'label': 'Scheduled Module sessions',
                        'source': 'course_schedule',
                        'mode': 'all'},
                       {'id': 'c522-attendance',
                        'label': 'Attendance records',
                        'source': 'student_attendance',
                        'mode': 'all'},
                       {'id': 'c522-absent',
                        'label': 'Absent attendance records',
                        'source': 'student_attendance',
                        'mode': 'equals',
                        'field': ['status'],
                        'value': 'Absent'},
                       {'id': 'c522-late',
                        'label': 'Late attendance records',
                        'source': 'student_attendance',
                        'mode': 'equals',
                        'field': ['status'],
                        'value': 'Late'},
                       {'id': 'c522-observations',
                        'label': 'Classroom observations',
                        'source': 'classroom_observation',
                        'mode': 'all'},
                       {'id': 'c522-signed-observations',
                        'label': 'Observations with both signatures',
                        'source': 'classroom_observation',
                        'mode': 'all_required',
                        'fields': [['observers_signature'], ['teachers_signature']]},
                       {'id': 'c522-improvement-recorded',
                        'label': 'Observations with improvement areas',
                        'source': 'classroom_observation',
                        'mode': 'truthy',
                        'field': ['areas_text', 'areas_for_improvement']},
                       {'id': 'c522-observation-coverage',
                        'label': 'Module-class observation coverage',
                        'source': 'classroom_observation',
                        'mode': 'unsupported',
                        'message': 'Observation coverage requires an approved cross-DocType denominator between '
                                   'Student Group and Classroom Observation.'}]},
 '5.3.1': {'sources': ['partnership_agreement', 'partnership_management', 'provider_rating'],
           'metrics': [{'id': 'c531-agreements',
                        'label': 'Partnership agreements',
                        'source': 'partnership_agreement',
                        'mode': 'all'},
                       {'id': 'c531-expired',
                        'label': 'Expired partnership agreements',
                        'source': 'partnership_agreement',
                        'mode': 'date_before_today',
                        'field': ['end_date']},
                       {'id': 'c531-expiring',
                        'label': 'Agreements expiring within 90 days',
                        'source': 'partnership_agreement',
                        'mode': 'date_next_days',
                        'field': ['end_date'],
                        'days': 90},
                       {'id': 'c531-nda-incomplete',
                        'label': 'Required NDAs not acknowledged',
                        'source': 'partnership_agreement',
                        'mode': 'conditions',
                        'conditions': [{'field': ['requires_nda'], 'op': 'truthy'},
                                       {'field': ['nda_acknowledged'], 'op': 'falsy'}]},
                       {'id': 'c531-managed',
                        'label': 'Managed partnership records',
                        'source': 'partnership_management',
                        'mode': 'all'},
                       {'id': 'c531-below-threshold',
                        'label': 'Managed partnerships below selection threshold',
                        'source': 'partnership_management',
                        'mode': 'lt',
                        'field': ['average_identification_and_selection_score'],
                        'value': 70},
                       {'id': 'c531-provider-ratings',
                        'label': 'Supplier Rating records',
                        'source': 'provider_rating',
                        'mode': 'all'},
                       {'id': 'c531-average-rating',
                        'label': 'Average Supplier Rating',
                        'source': 'provider_rating',
                        'mode': 'average_fields',
                        'fields': [['rating', 'rating_likert']],
                        'unit': 'rating'}]},
 '5.4': {'sources': ['survey_response', 'student_attendance'],
         'metrics': [{'id': 'c54-surveys', 'label': 'Survey responses', 'source': 'survey_response', 'mode': 'all'},
                     {'id': 'c54-module-surveys',
                      'label': 'End-of-Module survey records',
                      'source': 'survey_response',
                      'mode': 'conditions',
                      'conditions': [{'field': ['title'], 'op': 'contains', 'value': 'module'}]},
                     {'id': 'c54-course-surveys',
                      'label': 'End-of-Course survey records',
                      'source': 'survey_response',
                      'mode': 'conditions',
                      'conditions': [{'field': ['title'], 'op': 'contains', 'value': 'course'}]},
                     {'id': 'c54-average-score',
                      'label': 'Average survey score',
                      'source': 'survey_response',
                      'mode': 'average_fields',
                      'fields': [['rating', 'score']],
                      'unit': 'rating'},
                     {'id': 'c54-absent',
                      'label': 'Absent attendance records',
                      'source': 'student_attendance',
                      'mode': 'equals',
                      'field': ['status'],
                      'value': 'Absent'},
                     {'id': 'c54-late',
                      'label': 'Late attendance records',
                      'source': 'student_attendance',
                      'mode': 'equals',
                      'field': ['status'],
                      'value': 'Late'},
                     {'id': 'c54-response-children',
                      'label': 'Question-level survey analysis',
                      'source': 'survey_response',
                      'mode': 'unsupported',
                      'message': 'Survey Response.response is a child table and is not evaluated by the lightweight '
                                 'foundation API.'}]},
 '5.5': {'sources': ['assessment_plan', 'assessment_result'],
         'metrics': [{'id': 'c55-plans', 'label': 'Assessment plans', 'source': 'assessment_plan', 'mode': 'all'},
                     {'id': 'c55-examiner',
                      'label': 'Assessment plans with examiner',
                      'source': 'assessment_plan',
                      'mode': 'truthy',
                      'field': ['examiner']},
                     {'id': 'c55-supervisor',
                      'label': 'Assessment plans with supervisor',
                      'source': 'assessment_plan',
                      'mode': 'truthy',
                      'field': ['supervisor']},
                     {'id': 'c55-room',
                      'label': 'Assessment plans with room',
                      'source': 'assessment_plan',
                      'mode': 'truthy',
                      'field': ['room']},
                     {'id': 'c55-results', 'label': 'Assessment results', 'source': 'assessment_result', 'mode': 'all'},
                     {'id': 'c55-graded-results',
                      'label': 'Assessment results with grade',
                      'source': 'assessment_result',
                      'mode': 'truthy',
                      'field': ['grade']},
                     {'id': 'c55-average-score',
                      'label': 'Average assessment score',
                      'source': 'assessment_result',
                      'mode': 'average_fields',
                      'fields': [['total_score']],
                      'unit': 'score'},
                     {'id': 'c55-score-errors',
                      'label': 'Results above maximum score',
                      'source': 'assessment_result',
                      'mode': 'field_compare',
                      'fields': [['total_score'], ['maximum_score']],
                      'operator': 'gt'}]}}

QUESTION_REGISTRY = {'5.1.1': [{'id': 'q511-1',
            'question': 'How many course proposals are approved?',
            'metric_id': 'c511-approved-proposals'},
           {'id': 'q511-2', 'question': 'How many Modules have curriculum topics?', 'metric_id': 'c511-topics'},
           {'id': 'q511-3',
            'question': 'How many Modules have assessment criteria?',
            'metric_id': 'c511-assessment-criteria'},
           {'id': 'q511-4',
            'question': 'How many Assessment Plans are recorded?',
            'metric_id': 'c511-assessment-plans'}],
 '5.1.2': [{'id': 'q512-1',
            'question': 'How many Module Reviews are approved?',
            'metric_id': 'c512-approved-module-reviews'},
           {'id': 'q512-2',
            'question': 'How many Course Reviews are completed?',
            'metric_id': 'c512-completed-course-reviews'},
           {'id': 'q512-3', 'question': 'How many Course Reviews are overdue?', 'metric_id': 'c512-overdue-reviews'},
           {'id': 'q512-4',
            'question': 'How many recommendations remain unimplemented?',
            'metric_id': 'c512-pending-recommendations'}],
 '5.2.1': [{'id': 'q521-1', 'question': 'How many Intakes are recorded?', 'metric_id': 'c521-intakes'},
           {'id': 'q521-2',
            'question': 'How many Module Classes have a Teacher assigned?',
            'metric_id': 'c521-teachers-assigned'},
           {'id': 'q521-3',
            'question': 'How many scheduled sessions have a Teacher?',
            'metric_id': 'c521-session-teachers'},
           {'id': 'q521-4',
            'question': 'How many applicants have complete contract dates?',
            'metric_id': 'c521-contract-dates'}],
 '5.2.2': [{'id': 'q522-1', 'question': 'How many attendance records are available?', 'metric_id': 'c522-attendance'},
           {'id': 'q522-2', 'question': 'How many Absent records are recorded?', 'metric_id': 'c522-absent'},
           {'id': 'q522-3',
            'question': 'How many Classroom Observations are recorded?',
            'metric_id': 'c522-observations'},
           {'id': 'q522-4',
            'question': 'How many observations have both signatures?',
            'metric_id': 'c522-signed-observations'}],
 '5.3.1': [{'id': 'q531-1',
            'question': 'How many partnership agreements are recorded?',
            'metric_id': 'c531-agreements'},
           {'id': 'q531-2', 'question': 'How many agreements expire within 90 days?', 'metric_id': 'c531-expiring'},
           {'id': 'q531-3',
            'question': 'How many required NDAs remain unacknowledged?',
            'metric_id': 'c531-nda-incomplete'},
           {'id': 'q531-4', 'question': 'What is the average Supplier Rating?', 'metric_id': 'c531-average-rating'}],
 '5.4': [{'id': 'q54-1', 'question': 'How many survey responses are recorded?', 'metric_id': 'c54-surveys'},
         {'id': 'q54-2', 'question': 'How many End-of-Module surveys are recorded?', 'metric_id': 'c54-module-surveys'},
         {'id': 'q54-3', 'question': 'What is the average survey score?', 'metric_id': 'c54-average-score'},
         {'id': 'q54-4', 'question': 'How many attendance risk records are visible?', 'metric_id': 'c54-absent'}],
 '5.5': [{'id': 'q55-1', 'question': 'How many Assessment Plans are recorded?', 'metric_id': 'c55-plans'},
         {'id': 'q55-2', 'question': 'How many Assessment Plans have an examiner?', 'metric_id': 'c55-examiner'},
         {'id': 'q55-3', 'question': 'How many Assessment Results have a grade?', 'metric_id': 'c55-graded-results'},
         {'id': 'q55-4', 'question': 'How many results exceed the maximum score?', 'metric_id': 'c55-score-errors'}]}

EXCEPTION_METRIC_IDS = ['c511-course-mapping',
 'c512-overdue-reviews',
 'c512-pending-recommendations',
 'c512-action-plans',
 'c521-teachers-assigned',
 'c521-session-teachers',
 'c521-session-rooms',
 'c521-contract-dates',
 'c522-absent',
 'c522-late',
 'c522-observation-coverage',
 'c531-expired',
 'c531-expiring',
 'c531-nda-incomplete',
 'c531-below-threshold',
 'c54-absent',
 'c54-late',
 'c54-response-children',
 'c55-score-errors']

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
            # A permission-aware get_list is the runtime source probe. If a
            # candidate is stale or its table is unavailable, continue to the
            # next approved candidate instead of stopping the whole section.
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
                "count": len(rows),
                "truncated": len(rows) >= row_limit,
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
                    "count": 0,
                    "message": message,
                    "probe": "frappe.get_list",
                    "fallback_used": False,
                    "resolution_attempts": attempts
                }
            continue

    return {
        "key": alias,
        "doctype": None,
        "candidates": candidates,
        "status": "unavailable",
        "count": 0,
        "message": "No approved candidate DocType could be resolved. Open Source Mapping Report for the candidate-level errors.",
        "metadata_errors": attempts,
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

def resolve_field_groups(doctype, groups):
    resolved = []
    missing = []
    for candidates in groups or []:
        fieldname = resolve_field(doctype, candidates)
        if fieldname:
            resolved.append(fieldname)
        else:
            missing.append(candidates)
    return resolved, missing

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
    for fieldname in fields:
        if fieldname not in output and field_exists(meta, fieldname):
            output.append(fieldname)
    if "name" not in output:
        output.insert(0, "name")
    return output

def fetch_rows(source, requested_fields=None):
    doctype = source.get("doctype")
    alias = source.get("key")
    if source.get("status") != "available" or not doctype:
        return []
    if alias in ROW_CACHE:
        return ROW_CACHE.get(alias) or []
    fields_to_fetch = safe_fields(
        doctype,
        SAFE_FIELDS.get(alias) or ["name"]
    )
    try:
        rows = frappe.get_list(
            doctype,
            fields=fields_to_fetch,
            filters=applied_filters(doctype),
            limit_page_length=row_limit,
            order_by="modified desc"
        ) or []
        ROW_CACHE[alias] = rows
        source["count"] = len(rows)
        source["truncated"] = len(rows) >= row_limit
        return rows
    except Exception as error:
        source["status"] = "permission_denied" if is_permission_error(error) else "unavailable"
        source["message"] = clean_text(error)
        ROW_CACHE[alias] = []
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
            today = frappe.utils.getdate(frappe.utils.today())
            end_date = frappe.utils.getdate(
                frappe.utils.add_days(today, int(days or 0))
            )
            return date_value >= today and date_value <= end_date
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

def metric_required_fields(metric, doctype):
    fields = []
    missing = []

    if metric.get("field"):
        fieldname = resolve_field(doctype, metric.get("field"))
        if fieldname:
            fields.append(fieldname)
        else:
            missing.append(metric.get("field"))

    if metric.get("compare_field"):
        fieldname = resolve_field(doctype, metric.get("compare_field"))
        if fieldname:
            fields.append(fieldname)
        else:
            missing.append(metric.get("compare_field"))

    field_group_result = resolve_field_groups(
        doctype,
        metric.get("fields") or []
    )
    resolved_groups = field_group_result[0]
    missing_groups = field_group_result[1]
    fields.extend(resolved_groups)
    missing.extend(missing_groups)

    resolved_conditions = []
    for condition in metric.get("conditions") or []:
        fieldname = resolve_field(doctype, condition.get("field") or [])
        if not fieldname:
            missing.append(condition.get("field") or [])
            continue
        item = {}
        for key in condition:
            item[key] = condition.get(key)
        item["resolved_field"] = fieldname
        resolved_conditions.append(item)
        if fieldname not in fields:
            fields.append(fieldname)

    return fields, missing, resolved_conditions

def row_matches(row, metric, resolved_fields, resolved_conditions):
    mode = metric.get("mode")
    if mode == "all":
        return True
    if mode in ["truthy", "falsy", "equals", "in", "not_in", "date_next_days", "date_before_today", "gt", "gte", "lt", "lte"]:
        if not resolved_fields:
            return False
        return compare(
            row,
            resolved_fields[0],
            mode,
            expected=metric.get("value"),
            values=metric.get("values"),
            days=metric.get("days")
        )
    if mode == "all_required":
        for fieldname in resolved_fields:
            if not is_truthy(row.get(fieldname)):
                return False
        return True
    if mode == "conditions":
        for condition in resolved_conditions:
            if not compare(
                row,
                condition.get("resolved_field"),
                condition.get("op"),
                expected=condition.get("value"),
                values=condition.get("values"),
                days=condition.get("days")
            ):
                return False
        return True
    if mode == "field_compare":
        if len(resolved_fields) < 2:
            return False
        left = to_number(row.get(resolved_fields[0]))
        right = to_number(row.get(resolved_fields[1]))
        if left is None or right is None:
            return False
        operator = metric.get("operator") or "gte"
        if operator == "gt":
            return left > right
        if operator == "gte":
            return left >= right
        if operator == "lt":
            return left < right
        if operator == "lte":
            return left <= right
        return left == right
    if mode in ["average_fields", "sum"]:
        for condition in resolved_conditions:
            if not compare(
                row,
                condition.get("resolved_field"),
                condition.get("op"),
                expected=condition.get("value"),
                values=condition.get("values"),
                days=condition.get("days")
            ):
                return False
        if mode == "sum":
            return bool(resolved_fields and to_number(row.get(resolved_fields[0])) is not None)
        for fieldname in resolved_fields:
            if to_number(row.get(fieldname)) is not None:
                return True
        return False
    return False

if subcriterion not in CONFIG:
    frappe.throw("Unsupported Criterion 5 subcriterion.")

resolved_sources = {}
for alias in CONFIG[subcriterion]["sources"]:
    resolved_sources[alias] = resolve_source(alias)

ROW_CACHE = {}

def evaluate_metric(metric, include_rows=False):
    if metric.get("mode") == "unsupported":
        return {
            "id": metric.get("id"),
            "label": metric.get("label"),
            "source": metric.get("source"),
            "doctype": None,
            "value": None,
            "status": "unsupported",
            "message": metric.get("message"),
            "rows": []
        }

    source = resolved_sources.get(metric.get("source")) or {}
    if source.get("status") != "available":
        return {
            "id": metric.get("id"),
            "label": metric.get("label"),
            "source": metric.get("source"),
            "doctype": source.get("doctype"),
            "value": None,
            "status": source.get("status") or "unavailable",
            "message": source.get("message"),
            "rows": []
        }

    doctype = source.get("doctype")
    required_field_result = metric_required_fields(metric, doctype)
    resolved_fields = required_field_result[0]
    missing = required_field_result[1]
    resolved_conditions = required_field_result[2]

    if metric.get("mode") != "all" and missing:
        return {
            "id": metric.get("id"),
            "label": metric.get("label"),
            "source": metric.get("source"),
            "doctype": doctype,
            "value": None,
            "status": "unsupported_field",
            "message": "Required field is not installed.",
            "missing_field_candidates": missing,
            "rows": []
        }

    requested = list(resolved_fields)
    for fieldname in SAFE_FIELDS.get(metric.get("source"), []):
        if include_rows and fieldname not in requested:
            requested.append(fieldname)

    rows = fetch_rows(source, requested)
    matched = []
    for row in rows:
        if row_matches(row, metric, resolved_fields, resolved_conditions):
            matched.append(row)

    mode = metric.get("mode")
    value = len(matched)
    record_count = len(matched)

    if mode == "average_fields":
        numbers = []
        for row in matched:
            for fieldname in resolved_fields:
                number = to_number(row.get(fieldname))
                if number is not None:
                    numbers.append(number)
        value = round(sum(numbers) / len(numbers), 2) if numbers else 0
        record_count = len(matched)

    if mode == "sum":
        total = 0
        for row in matched:
            number = to_number(row.get(resolved_fields[0]))
            if number is not None:
                total = total + number
        value = round(total, 2)

    output_rows = []
    if include_rows:
        start = (page - 1) * page_size
        end = start + page_size
        safe_output_fields = safe_fields(
            doctype,
            SAFE_FIELDS.get(metric.get("source"), ["name"])
        )
        for row in matched[start:end]:
            item = {}
            for fieldname in safe_output_fields:
                item[fieldname] = row.get(fieldname)
            output_rows.append(item)

    return {
        "id": metric.get("id"),
        "label": metric.get("label"),
        "source": metric.get("source"),
        "doctype": doctype,
        "value": value,
        "unit": metric.get("unit") or "records",
        "record_count": record_count,
        "status": "available",
        "resolved_fields": resolved_fields,
        "rows": output_rows,
        "total": len(matched)
    }

metrics = []
for configured_metric in CONFIG[subcriterion]["metrics"]:
    metrics.append(evaluate_metric(configured_metric, False))

questions = []
for question in QUESTION_REGISTRY.get(subcriterion) or []:
    selected_metric = None
    for metric in metrics:
        if metric.get("id") == question.get("metric_id"):
            selected_metric = metric
            break

    if selected_metric and selected_metric.get("status") == "available":
        unit = selected_metric.get("unit") or "records"
        if unit == "rating":
            answer = (
                str(selected_metric.get("value"))
                + " is the live average rating from "
                + str(selected_metric.get("record_count") or 0)
                + " matching record(s)."
            )
        elif unit == "SGD":
            answer = "SGD " + str(selected_metric.get("value")) + " matches the current filters."
        elif unit == "percent":
            answer = str(selected_metric.get("value")) + "% matches the current filters."
        else:
            answer = str(selected_metric.get("value") or 0) + " record(s) match the current filters."
        status = "available"
        confidence = "Live"
    else:
        answer = "Unavailable: " + clean_text(
            (selected_metric or {}).get("message")
            or (selected_metric or {}).get("status")
            or "required source or field is unavailable"
        )
        status = (selected_metric or {}).get("status") or "unavailable"
        confidence = "Unavailable"

    questions.append({
        "id": question.get("id"),
        "criterion": subcriterion,
        "question": question.get("question"),
        "answer": answer,
        "metric_id": question.get("metric_id"),
        "status": status,
        "confidence": confidence,
        "doctype": (selected_metric or {}).get("doctype")
    })

sources = []
for alias in CONFIG[subcriterion]["sources"]:
    sources.append(resolved_sources.get(alias))

data_quality = []
for source in sources:
    if source.get("status") != "available":
        data_quality.append({
            "criterion": subcriterion,
            "check": "Source availability",
            "source": source.get("doctype") or " / ".join(source.get("candidates") or []),
            "status": source.get("status"),
            "detail": source.get("message") or "Source is unavailable."
        })

for metric in metrics:
    if metric.get("status") != "available":
        data_quality.append({
            "criterion": subcriterion,
            "check": metric.get("label"),
            "source": metric.get("doctype") or metric.get("source"),
            "status": metric.get("status"),
            "detail": metric.get("message") or "Metric is unavailable."
        })

exceptions = []
for metric in metrics:
    if metric.get("id") in EXCEPTION_METRIC_IDS:
        exceptions.append(metric)

available_sources = 0
for source in sources:
    if source.get("status") == "available":
        available_sources = available_sources + 1

available_metrics = 0
for metric in metrics:
    if metric.get("status") == "available":
        available_metrics = available_metrics + 1

result = {
    "ok": True,
    "meta": {
        "api_method": "ucc_analytics_criterion_5",
        "platform_version": "1.9.13",
        "status": "live_foundation",
        "generated_at": frappe.utils.now(),
        "action": action,
        "subcriterion": subcriterion,
        "row_limit": row_limit
    },
    "policy": POLICY_REGISTRY.get(subcriterion),
    "filters": filters,
    "sources": sources,
    "metrics": metrics,
    "questions": questions,
    "exceptions": exceptions,
    "data_quality": data_quality,
    "source_summary": {
        "total": len(sources),
        "available": available_sources,
        "issues": len(sources) - available_sources
    },
    "metric_summary": {
        "total": len(metrics),
        "available": available_metrics,
        "issues": len(metrics) - available_metrics
    },
    "data": {
        "sources": sources,
        "metrics": metrics,
        "questions": questions,
        "exceptions": exceptions,
        "data_quality": data_quality
    },
    "warnings": ['Criterion 5 spans course design, review, planning, delivery, partnerships, surveys and assessment sources.',
 'Custom DocTypes are resolved only from approved policy-referenced candidates.',
 'Cross-DocType coverage ratios and child-table-only controls remain unsupported until approved relationship rules are supplied.']
}

if action == "policy_registry":
    result["registry"] = POLICY_REGISTRY

if action == "drilldown":
    selected_config = None
    for configured_metric in CONFIG[subcriterion]["metrics"]:
        if configured_metric.get("id") == metric_id:
            selected_config = configured_metric
            break
    if not selected_config:
        frappe.throw("Unknown Criterion 5 metric.")
    result["drilldown"] = evaluate_metric(selected_config, True)

frappe.response["message"] = result
