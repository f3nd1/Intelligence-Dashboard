"""
UCC Intelligence Platform Server Script

Visible name:
    UCC Analytics - Criterion 4

Script type:
    API

API method:
    ucc_analytics_criterion_4

Purpose:
    Resolve Criterion 4 DocTypes and fields at runtime, return permission-aware
    metrics, source mappings, and drill-down rows.

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
subcriterion = payload.get("subcriterion") or "4.1.1"
filters = payload.get("filters") or {}
if not isinstance(filters, dict):
    filters = {}
metric_id = payload.get("metric_id")
try:
    page = max(int(payload.get("page") or 1), 1)
except Exception:
    page = 1
try:
    page_size = min(max(int(payload.get("page_size") or 50), 1), 200)
except Exception:
    page_size = 50

ALLOWED_ACTIONS = ["summary", "source_status", "policy_registry", "drilldown"]
if action not in ALLOWED_ACTIONS:
    frappe.throw("Unsupported Criterion 4 action.")

POLICY_REGISTRY = {
    "4.1.1": {"title": "Pre-Course Counselling, Selection and Admissions", "policy": "PPD-SSO-AD-4.1.1", "version": "2.2"},
    "4.2.1": {"title": "Student Contract", "policy": "PPD-SSO-AD-4.2.1", "version": "2.2"},
    "4.2.2": {"title": "Fee Collection and Fee Protection Scheme", "policy": "PPD-SSO-AD-4.2.2", "version": "2.3"},
    "4.3.1": {"title": "Course Transfer, Deferment and Withdrawal", "policy": "PPD-SSO-SS-4.3.1", "version": "2.2"},
    "4.4.1": {"title": "Refund", "policy": "PPD-SSO-SS-4.4.1", "version": "2.2"},
    "4.5.1": {"title": "Student Support Services", "policy": "PPD-SSO-SS-4.5.1", "version": "2.3"},
    "4.6.1": {"title": "Student Conduct and Attendance", "policy": "PPD-SSO-SS-4.6.1", "version": "2.2"}
}

CONFIG = {
    "4.1.1": {
        "sources": {
            "applicant": ["Student Applicant"],
            "admission": ["Student Admission UCC"],
            "counselling": ["Pre Course Counselling Declaration"],
            "adjustments": ["Student Log"]
        },
        "metrics": [
            {
                "id": "c411-counselling", "label": "Counselling declarations",
                "source": "counselling", "field": ["name"], "mode": "all"
            },
            {
                "id": "c411-acknowledged", "label": "Applicant acknowledgements",
                "source": "counselling", "field": ["declaration_check"], "mode": "truthy"
            },
            {
                "id": "c411-pdpa", "label": "PDPA consents",
                "source": "counselling", "field": ["pdpa_check"], "mode": "truthy"
            },
            {
                "id": "c411-staff-complete", "label": "Staff declarations completed",
                "source": "counselling", "field": ["name_of_staff"], "mode": "truthy",
                "requires": [
                    {"field": ["date"], "mode": "truthy"}
                ]
            },
            {
                "id": "c411-unacknowledged", "label": "Applicant acknowledgement missing",
                "source": "counselling", "field": ["declaration_check"], "mode": "falsy"
            },
            {
                "id": "c411-pdpa-missing", "label": "PDPA consent missing",
                "source": "counselling", "field": ["pdpa_check"], "mode": "falsy"
            },
            {
                "id": "c411-complete", "label": "Approved applications",
                "source": "applicant", "field": ["application_status"],
                "mode": "contains", "values": ["approved", "admitted", "enrolled"]
            },
            {
                "id": "c411-conditional", "label": "Conditional admissions",
                "source": "admission", "field": ["conditional"], "mode": "truthy"
            },
            {
                "id": "c411-late", "label": "Late-admission requests",
                "source": "adjustments",
                "child_doctype": "Course Adjustment Request Form",
                "child_table_field": "custom_course_adjustment",
                "field": ["type"], "mode": "equals", "values": ["Late Admission"]
            }
        ]
    },
    "4.2.1": {
        "sources": {
            "contract": ["Student Admission UCC"],
            "invoice": ["Sales Invoice"]
        },
        "metrics": [
            {
                "id": "c421-generated", "label": "Contracts generated",
                "source": "contract", "field": ["contract_url", "student_contract"],
                "mode": "truthy"
            },
            {
                "id": "c421-approved", "label": "Approved contracts",
                "source": "contract", "field": ["application_status"],
                "mode": "contains", "values": ["approved", "enrolled", "done"]
            },
            {
                "id": "c421-signed", "label": "Signed contracts",
                "source": "contract",
                "field": ["contract_signed_by_student_date", "student_signed_date"],
                "mode": "truthy"
            },
            {
                "id": "c421-pending", "label": "Sent but not signed",
                "source": "contract", "field": ["contract_sent_date"], "mode": "truthy",
                "requires": [
                    {
                        "field": ["contract_signed_by_student_date", "student_signed_date"],
                        "mode": "falsy"
                    }
                ]
            }
        ]
    },
    "4.2.2": {
        "sources": {
            "contract": ["Student Admission UCC"],
            "invoice": ["Sales Invoice"],
            "payment": ["Payment Entry"],
            "fps": ["FPS Record"]
        },
        "metrics": [
            {
                "id": "c422-invoiced", "label": "Students invoiced",
                "source": "contract", "field": ["sales_invoice"], "mode": "truthy"
            },
            {
                "id": "c422-paid", "label": "Submitted receipts",
                "source": "payment", "field": ["payment_type"],
                "mode": "contains", "values": ["receive"],
                "requires": [
                    {"field": ["docstatus"], "mode": "equals", "values": ["1"]}
                ]
            },
            {
                "id": "c422-fps", "label": "FPS declarations processed",
                "source": "fps", "field": ["fps_status"],
                "mode": "contains", "values": ["processed", "approved"]
            },
            {
                "id": "c422-late", "label": "Late-payment exceptions",
                "source": "invoice", "field": ["status"],
                "mode": "contains", "values": ["overdue"]
            }
        ]
    },
    "4.3.1": {
        "sources": {
            "adjustments": ["Student Log"],
            "contract": ["Student Admission UCC"],
            "fps": ["FPS Record"]
        },
        "metrics": [
            {
                "id": "c431-overdue", "label": "Open requests beyond 21 working days",
                "source": "adjustments",
                "child_doctype": "Course Adjustment Request Form",
                "child_table_field": "custom_course_adjustment",
                "field": ["posting_date"], "mode": "older_than_days", "days": 29,
                "requires": [
                    {
                        "field": ["type"], "mode": "contains",
                        "values": ["course transfer", "course deferment", "course withdrawal"]
                    },
                    {"field": ["approved_date"], "mode": "falsy"}
                ]
            },
            {
                "id": "c431-transfer", "label": "Transfer requests",
                "source": "adjustments",
                "child_doctype": "Course Adjustment Request Form",
                "child_table_field": "custom_course_adjustment",
                "field": ["type"], "mode": "equals", "values": ["Course Transfer"]
            },
            {
                "id": "c431-defer", "label": "Deferment requests",
                "source": "adjustments",
                "child_doctype": "Course Adjustment Request Form",
                "child_table_field": "custom_course_adjustment",
                "field": ["type"], "mode": "equals", "values": ["Course Deferment"]
            },
            {
                "id": "c431-withdraw", "label": "Withdrawal requests",
                "source": "adjustments",
                "child_doctype": "Course Adjustment Request Form",
                "child_table_field": "custom_course_adjustment",
                "field": ["type"], "mode": "equals", "values": ["Course Withdrawal"]
            }
        ]
    },
    "4.4.1": {
        "sources": {
            "adjustments": ["Student Log"],
            "payment": ["Payment Entry"],
            "contract": ["Student Admission UCC"]
        },
        "metrics": [
            {
                "id": "c441-open", "label": "Open refund requests",
                "source": "adjustments",
                "child_doctype": "Course Adjustment Request Form",
                "child_table_field": "custom_course_adjustment",
                "field": ["type"], "mode": "equals", "values": ["Refund"],
                "requires": [
                    {"field": ["approved_date"], "mode": "falsy"}
                ]
            },
            {
                "id": "c441-eligible", "label": "Approved refund requests",
                "source": "adjustments",
                "child_doctype": "Course Adjustment Request Form",
                "child_table_field": "custom_course_adjustment",
                "field": ["type"], "mode": "equals", "values": ["Refund"],
                "requires": [
                    {"field": ["approved_date"], "mode": "truthy"}
                ]
            },
            {
                "id": "c441-overdue", "label": "Open refunds beyond 7 days",
                "source": "adjustments",
                "child_doctype": "Course Adjustment Request Form",
                "child_table_field": "custom_course_adjustment",
                "field": ["posting_date"], "mode": "older_than_days", "days": 7,
                "requires": [
                    {"field": ["type"], "mode": "equals", "values": ["Refund"]},
                    {"field": ["approved_date"], "mode": "falsy"}
                ]
            },
            {
                "id": "c441-paid", "label": "Refund payments recorded",
                "source": "payment", "field": ["remarks"],
                "mode": "contains", "values": ["refund"],
                "requires": [
                    {"field": ["payment_type"], "mode": "contains", "values": ["pay"]},
                    {"field": ["docstatus"], "mode": "equals", "values": ["1"]}
                ]
            }
        ]
    },
    "4.5.1": {
        "sources": {
            "student_log": ["Student Log"],
            "academic_support": ["Intervention Issue Academic Support"],
            "wellness_support": ["Intervention Issue Wellness Services"],
            "integrity_support": ["Intervention Issue Academic Integrity"]
        },
        "metrics": [
            {
                "id": "c451-services", "label": "Student Logs",
                "source": "student_log", "field": ["name"], "mode": "all"
            },
            {
                "id": "c451-cases", "label": "Academic-support records",
                "source": "academic_support", "field": ["name"], "mode": "all"
            },
            {
                "id": "c451-followup", "label": "Wellness-support records",
                "source": "wellness_support", "field": ["name"], "mode": "all"
            },
            {
                "id": "c451-outcomes", "label": "Academic-integrity records",
                "source": "integrity_support", "field": ["name"], "mode": "all"
            }
        ]
    },
    "4.6.1": {
        "sources": {
            "attendance": ["Student Attendance"],
            "student_log": ["Student Log"],
            "warning": ["Dismissal Letters due to Attendance Requirements"],
            "leave": ["Student Leave Application"]
        },
        "metrics": [
            {
                "id": "c461-attendance", "label": "Attendance records",
                "source": "attendance", "field": ["name"], "mode": "all"
            },
            {
                "id": "c461-risk", "label": "Absent or late records",
                "source": "attendance", "field": ["status"],
                "mode": "contains", "values": ["absent", "late"]
            },
            {
                "id": "c461-warning", "label": "Attendance-dismissal records",
                "source": "warning", "field": ["name"], "mode": "all"
            },
            {
                "id": "c461-intervention", "label": "Student Logs",
                "source": "student_log", "field": ["name"], "mode": "all"
            }
        ]
    }
}

if subcriterion not in CONFIG:
    frappe.throw("Unsupported Criterion 4 subcriterion.")


SUBCRITERION_TAB = {
    "4.1.1": "c411",
    "4.2.1": "c421",
    "4.2.2": "c422",
    "4.3.1": "c431",
    "4.4.1": "c441",
    "4.5.1": "c451",
    "4.6.1": "c461"
}

C4_VISUAL_REGISTRY = {'c411': {'type': 'funnel',
          'title': 'Admissions control funnel',
          'stages': [{'label': 'Counselling declarations',
                      'metric': 'c411-counselling',
                      'source': 'Pre Course Counselling Declaration'},
                     {'label': 'Applicant acknowledgement',
                      'metric': 'c411-acknowledged',
                      'source': 'Pre Course Counselling Declaration'},
                     {'label': 'PDPA consent', 'metric': 'c411-pdpa', 'source': 'Pre Course Counselling Declaration'},
                     {'label': 'Staff declaration complete',
                      'metric': 'c411-staff-complete',
                      'source': 'Pre Course Counselling Declaration'},
                     {'label': 'Approved applications', 'metric': 'c411-complete', 'source': 'Student Applicant'}]},
 'c421': {'type': 'lifecycle',
          'title': 'Student contract lifecycle',
          'stages': [{'label': 'Admission approved', 'metric': 'c421-approved', 'source': 'Student Admission UCC'},
                     {'label': 'Contract generated', 'metric': 'c421-generated', 'source': 'Student Admission UCC'},
                     {'label': 'Sent, awaiting signature',
                      'metric': 'c421-pending',
                      'source': 'Student Admission UCC',
                      'exception': True},
                     {'label': 'Student signed', 'metric': 'c421-signed', 'source': 'Student Admission UCC'}]},
 'c422': {'type': 'reconciliation',
          'title': 'Fee and FPS reconciliation',
          'stages': [{'label': 'Sales invoice linked', 'metric': 'c422-invoiced', 'source': 'Student Admission UCC'},
                     {'label': 'Payment received', 'metric': 'c422-paid', 'source': 'Payment Entry'},
                     {'label': 'FPS processed / approved', 'metric': 'c422-fps', 'source': 'FPS Record'},
                     {'label': 'Overdue invoice',
                      'metric': 'c422-late',
                      'source': 'Sales Invoice',
                      'exception': True}]},
 'c431': {'type': 'decision',
          'title': 'Course adjustment decision tree',
          'stages': [{'label': 'All movement requests',
                      'aggregate': ['c431-transfer', 'c431-defer', 'c431-withdraw'],
                      'source': 'Student Log'},
                     {'label': 'Course transfer', 'metric': 'c431-transfer', 'source': 'Student Log'},
                     {'label': 'Course deferment', 'metric': 'c431-defer', 'source': 'Student Log'},
                     {'label': 'Course withdrawal', 'metric': 'c431-withdraw', 'source': 'Student Log'},
                     {'label': 'Beyond processing period',
                      'metric': 'c431-overdue',
                      'source': 'Student Log',
                      'exception': True}]},
 'c441': {'type': 'radial',
          'title': 'Refund decision and payment status',
          'stages': [{'label': 'Open requests', 'metric': 'c441-open', 'source': 'Student Log', 'exception': True},
                     {'label': 'Approved requests', 'metric': 'c441-eligible', 'source': 'Student Log'},
                     {'label': 'Refund payments', 'metric': 'c441-paid', 'source': 'Payment Entry'},
                     {'label': 'Overdue requests',
                      'metric': 'c441-overdue',
                      'source': 'Student Log',
                      'exception': True}]},
 'c451': {'type': 'network',
          'title': 'Student support pathway',
          'stages': [{'label': 'Student logs', 'metric': 'c451-services', 'source': 'Student Log'},
                     {'label': 'Academic support',
                      'metric': 'c451-cases',
                      'source': 'Intervention Issue Academic Support'},
                     {'label': 'Wellness support',
                      'metric': 'c451-followup',
                      'source': 'Intervention Issue Wellness Services'},
                     {'label': 'Academic integrity',
                      'metric': 'c451-outcomes',
                      'source': 'Intervention Issue Academic Integrity'}]},
 'c461': {'type': 'ladder',
          'title': 'Attendance intervention ladder',
          'stages': [{'label': 'Attendance records', 'metric': 'c461-attendance', 'source': 'Student Attendance'},
                     {'label': 'Attendance risk',
                      'metric': 'c461-risk',
                      'source': 'Student Attendance',
                      'exception': True},
                     {'label': 'Warning records',
                      'metric': 'c461-warning',
                      'source': 'Dismissal Letters due to Attendance Requirements'},
                     {'label': 'Open interventions',
                      'metric': 'c461-intervention',
                      'source': 'Student Log',
                      'exception': True}]},
 'c4-overview-flow': {'panel': 'overview',
                      'type': 'network',
                      'title': 'Student protection control flow',
                      'stages': [{'label': 'Approved applications',
                                  'metric': 'c411-complete',
                                  'source': 'Student Applicant'},
                                 {'label': 'Signed contracts',
                                  'metric': 'c421-signed',
                                  'source': 'Student Admission UCC'},
                                 {'label': 'Payments received', 'metric': 'c422-paid', 'source': 'Payment Entry'},
                                 {'label': 'Support cases', 'metric': 'c451-services', 'source': 'Student Log'},
                                 {'label': 'Attendance records',
                                  'metric': 'c461-attendance',
                                  'source': 'Student Attendance'}]},
 'c4-overview-exceptions': {'panel': 'overview',
                            'type': 'radial',
                            'title': 'Open exception profile',
                            'stages': [{'label': 'Late admissions',
                                        'metric': 'c411-late',
                                        'source': 'Student Applicant',
                                        'exception': True},
                                       {'label': 'Unsigned contracts',
                                        'metric': 'c421-pending',
                                        'source': 'Student Admission UCC',
                                        'exception': True},
                                       {'label': 'Overdue invoices',
                                        'metric': 'c422-late',
                                        'source': 'Sales Invoice',
                                        'exception': True},
                                       {'label': 'Movement overdue',
                                        'metric': 'c431-overdue',
                                        'source': 'Student Log',
                                        'exception': True},
                                       {'label': 'Refund overdue',
                                        'metric': 'c441-overdue',
                                        'source': 'Student Log',
                                        'exception': True},
                                       {'label': 'Attendance risk',
                                        'metric': 'c461-risk',
                                        'source': 'Student Attendance',
                                        'exception': True}]},
 'c4-overview-readiness': {'panel': 'overview',
                           'type': 'ladder',
                           'title': 'Student control readiness',
                           'stages': [{'label': 'Counselling complete',
                                       'metric': 'c411-counselling',
                                       'source': 'Pre Course Counselling Declaration'},
                                      {'label': 'Contract generated',
                                       'metric': 'c421-generated',
                                       'source': 'Student Admission UCC'},
                                      {'label': 'Fee invoiced', 'metric': 'c422-invoiced', 'source': 'Sales Invoice'},
                                      {'label': 'Refund requests', 'metric': 'c441-open', 'source': 'Student Log'},
                                      {'label': 'Support pathways', 'metric': 'c451-cases', 'source': 'Student Log'},
                                      {'label': 'Interventions',
                                       'metric': 'c461-intervention',
                                       'source': 'Student Log'}]},
 'c411-coverage': {'panel': 'c411',
                   'type': 'radial',
                   'title': 'Counselling and admission control coverage',
                   'stages': [{'label': 'Counselling',
                               'metric': 'c411-counselling',
                               'source': 'Pre Course Counselling Declaration'},
                              {'label': 'Acknowledged',
                               'metric': 'c411-acknowledged',
                               'source': 'Pre Course Counselling Declaration'},
                              {'label': 'PDPA consent',
                               'metric': 'c411-pdpa',
                               'source': 'Pre Course Counselling Declaration'},
                              {'label': 'Staff complete',
                               'metric': 'c411-staff-complete',
                               'source': 'Pre Course Counselling Declaration'},
                              {'label': 'Approved', 'metric': 'c411-complete', 'source': 'Student Applicant'}]},
 'c411-exceptions': {'panel': 'c411',
                     'type': 'ladder',
                     'title': 'Admissions exception escalation',
                     'stages': [{'label': 'Acknowledgement missing',
                                 'metric': 'c411-unacknowledged',
                                 'source': 'Pre Course Counselling Declaration',
                                 'exception': True},
                                {'label': 'PDPA missing',
                                 'metric': 'c411-pdpa-missing',
                                 'source': 'Pre Course Counselling Declaration',
                                 'exception': True},
                                {'label': 'Conditional open',
                                 'metric': 'c411-conditional',
                                 'source': 'Student Admission UCC',
                                 'exception': True},
                                {'label': 'Late admission',
                                 'metric': 'c411-late',
                                 'source': 'Student Applicant',
                                 'exception': True}]},
 'c421-readiness': {'panel': 'c421',
                    'type': 'radial',
                    'title': 'Student contract readiness',
                    'stages': [{'label': 'Admission approved',
                                'metric': 'c421-approved',
                                'source': 'Student Admission UCC'},
                               {'label': 'Contract generated',
                                'metric': 'c421-generated',
                                'source': 'Student Admission UCC'},
                               {'label': 'Contract sent', 'metric': 'c421-pending', 'source': 'Student Admission UCC'},
                               {'label': 'Contract signed',
                                'metric': 'c421-signed',
                                'source': 'Student Admission UCC'}]},
 'c421-aging': {'panel': 'c421',
                'type': 'ladder',
                'title': 'Contract follow-up ladder',
                'stages': [{'label': 'Generated', 'metric': 'c421-generated', 'source': 'Student Admission UCC'},
                           {'label': 'Approved', 'metric': 'c421-approved', 'source': 'Student Admission UCC'},
                           {'label': 'Awaiting signature',
                            'metric': 'c421-pending',
                            'source': 'Student Admission UCC',
                            'exception': True},
                           {'label': 'Signed', 'metric': 'c421-signed', 'source': 'Student Admission UCC'}]},
 'c422-flow': {'panel': 'c422',
               'type': 'lifecycle',
               'title': 'Fee and FPS processing flow',
               'stages': [{'label': 'Invoice linked', 'metric': 'c422-invoiced', 'source': 'Sales Invoice'},
                          {'label': 'Payment received', 'metric': 'c422-paid', 'source': 'Payment Entry'},
                          {'label': 'FPS processed', 'metric': 'c422-fps', 'source': 'FPS Record'},
                          {'label': 'Overdue', 'metric': 'c422-late', 'source': 'Sales Invoice', 'exception': True}]},
 'c422-exceptions': {'panel': 'c422',
                     'type': 'radial',
                     'title': 'Fee-control exception profile',
                     'stages': [{'label': 'Not invoiced',
                                 'metric': 'c422-invoiced',
                                 'source': 'Sales Invoice',
                                 'exception': True},
                                {'label': 'Payment pending',
                                 'metric': 'c422-paid',
                                 'source': 'Payment Entry',
                                 'exception': True},
                                {'label': 'FPS pending',
                                 'metric': 'c422-fps',
                                 'source': 'FPS Record',
                                 'exception': True},
                                {'label': 'Invoice overdue',
                                 'metric': 'c422-late',
                                 'source': 'Sales Invoice',
                                 'exception': True}]},
 'c431-mix': {'panel': 'c431',
              'type': 'radial',
              'title': 'Course movement request mix',
              'stages': [{'label': 'Transfer', 'metric': 'c431-transfer', 'source': 'Student Log'},
                         {'label': 'Deferment', 'metric': 'c431-defer', 'source': 'Student Log'},
                         {'label': 'Withdrawal', 'metric': 'c431-withdraw', 'source': 'Student Log'}]},
 'c431-timing': {'panel': 'c431',
                 'type': 'ladder',
                 'title': 'Movement processing timeliness',
                 'stages': [{'label': 'Transfer', 'metric': 'c431-transfer', 'source': 'Student Log'},
                            {'label': 'Deferment', 'metric': 'c431-defer', 'source': 'Student Log'},
                            {'label': 'Withdrawal', 'metric': 'c431-withdraw', 'source': 'Student Log'},
                            {'label': 'Beyond period',
                             'metric': 'c431-overdue',
                             'source': 'Student Log',
                             'exception': True}]},
 'c441-outcomes': {'panel': 'c441',
                   'type': 'reconciliation',
                   'title': 'Refund request outcomes',
                   'stages': [{'label': 'Open requests',
                               'metric': 'c441-open',
                               'source': 'Student Log',
                               'exception': True},
                              {'label': 'Eligible / approved', 'metric': 'c441-eligible', 'source': 'Student Log'},
                              {'label': 'Payments completed', 'metric': 'c441-paid', 'source': 'Payment Entry'},
                              {'label': 'Overdue',
                               'metric': 'c441-overdue',
                               'source': 'Student Log',
                               'exception': True}]},
 'c441-aging': {'panel': 'c441',
                'type': 'ladder',
                'title': 'Refund follow-up ladder',
                'stages': [{'label': 'Request logged', 'metric': 'c441-open', 'source': 'Student Log'},
                           {'label': 'Eligibility confirmed', 'metric': 'c441-eligible', 'source': 'Student Log'},
                           {'label': 'Payment issued', 'metric': 'c441-paid', 'source': 'Payment Entry'},
                           {'label': 'Overdue follow-up',
                            'metric': 'c441-overdue',
                            'source': 'Student Log',
                            'exception': True}]},
 'c451-channels': {'panel': 'c451',
                   'type': 'radial',
                   'title': 'Student support channel mix',
                   'stages': [{'label': 'Student logs', 'metric': 'c451-services', 'source': 'Student Log'},
                              {'label': 'Academic support',
                               'metric': 'c451-cases',
                               'source': 'Intervention Issue Academic Support'},
                              {'label': 'Wellness',
                               'metric': 'c451-followup',
                               'source': 'Intervention Issue Wellness Services'},
                              {'label': 'Academic integrity',
                               'metric': 'c451-outcomes',
                               'source': 'Intervention Issue Academic Integrity'}]},
 'c451-followup': {'panel': 'c451',
                   'type': 'lifecycle',
                   'title': 'Student support follow-up flow',
                   'stages': [{'label': 'Service request', 'metric': 'c451-services', 'source': 'Student Log'},
                              {'label': 'Case opened',
                               'metric': 'c451-cases',
                               'source': 'Intervention Issue Academic Support'},
                              {'label': 'Follow-up required',
                               'metric': 'c451-followup',
                               'source': 'Intervention Issue Wellness Services',
                               'exception': True},
                              {'label': 'Outcome recorded', 'metric': 'c451-outcomes', 'source': 'Student Log'}]},
 'c461-risk': {'panel': 'c461',
               'type': 'radial',
               'title': 'Attendance risk profile',
               'stages': [{'label': 'Attendance records', 'metric': 'c461-attendance', 'source': 'Student Attendance'},
                          {'label': 'At risk',
                           'metric': 'c461-risk',
                           'source': 'Student Attendance',
                           'exception': True},
                          {'label': 'Warning issued',
                           'metric': 'c461-warning',
                           'source': 'Dismissal Letters due to Attendance Requirements'},
                          {'label': 'Intervention open',
                           'metric': 'c461-intervention',
                           'source': 'Student Log',
                           'exception': True}]},
 'c461-response': {'panel': 'c461',
                   'type': 'lifecycle',
                   'title': 'Attendance intervention response',
                   'stages': [{'label': 'Attendance captured',
                               'metric': 'c461-attendance',
                               'source': 'Student Attendance'},
                              {'label': 'Risk identified',
                               'metric': 'c461-risk',
                               'source': 'Student Attendance',
                               'exception': True},
                              {'label': 'Warning issued',
                               'metric': 'c461-warning',
                               'source': 'Dismissal Letters due to Attendance Requirements'},
                              {'label': 'Intervention opened',
                               'metric': 'c461-intervention',
                               'source': 'Student Log'}]}}

def visual_registry_for(code):
    tab = SUBCRITERION_TAB.get(code)
    output = {}
    for key in C4_VISUAL_REGISTRY:
        item = C4_VISUAL_REGISTRY.get(key) or {}
        if key == tab or item.get("panel") == tab or item.get("panel") == "overview":
            output[key] = item
    return output

QUESTION_REGISTRY = {
    "4.1.1": [
        {"id": "q411-1", "metric_id": "c411-counselling", "question": "How many pre-course counselling declarations are recorded?", "logic": "Count Pre Course Counselling Declaration records in the current filter scope."},
        {"id": "q411-2", "metric_id": "c411-acknowledged", "question": "How many applicants acknowledged that the pre-course information was communicated?", "logic": "Count Pre Course Counselling Declaration.declaration_check values that are enabled."},
        {"id": "q411-3", "metric_id": "c411-pdpa", "question": "How many applicants provided PDPA consent?", "logic": "Count Pre Course Counselling Declaration.pdpa_check values that are enabled."},
        {"id": "q411-4", "metric_id": "c411-staff-complete", "question": "How many counselling declarations contain both the staff representative and declaration date?", "logic": "Count records with name_of_staff and date populated."},
        {"id": "q411-5", "metric_id": "c411-complete", "question": "How many applications are approved or admitted?", "logic": "Count Student Applicant records with approved, admitted or enrolled status."},
        {"id": "q411-6", "metric_id": "c411-conditional", "question": "How many admissions remain conditional?", "logic": "Count Student Admission UCC records where conditional is enabled."},
        {"id": "q411-7", "metric_id": "c411-late", "question": "How many late-admission requests require monitoring?", "logic": "Count Late Admission rows in Student Log course adjustments."},
        {"id": "q411-8", "metric_id": "c411-unacknowledged", "question": "How many counselling declarations are missing applicant acknowledgement?", "logic": "Count Pre Course Counselling Declaration records where declaration_check is not enabled."},
        {"id": "q411-9", "metric_id": "c411-pdpa-missing", "question": "How many counselling declarations are missing PDPA consent?", "logic": "Count Pre Course Counselling Declaration records where pdpa_check is not enabled."}
    ],
    "4.2.1": [
        {"id": "q421-1", "metric_id": "c421-generated", "question": "How many student contracts have been generated?", "logic": "Count Student Admission UCC records with a contract URL or contract content."},
        {"id": "q421-2", "metric_id": "c421-approved", "question": "How many contracts have an approved admission status?", "logic": "Count approved, enrolled or completed admission records."},
        {"id": "q421-3", "metric_id": "c421-signed", "question": "How many contracts have been signed by the student?", "logic": "Count records with a student contract signed date."},
        {"id": "q421-4", "metric_id": "c421-pending", "question": "How many sent contracts are still unsigned?", "logic": "Count records with contract sent date and no student signed date."}
    ],
    "4.2.2": [
        {"id": "q422-1", "metric_id": "c422-invoiced", "question": "How many admissions have a linked sales invoice?", "logic": "Count Student Admission UCC records with sales_invoice populated."},
        {"id": "q422-2", "metric_id": "c422-paid", "question": "How many submitted incoming payment records are available?", "logic": "Count submitted Payment Entry records with Receive payment type."},
        {"id": "q422-3", "metric_id": "c422-fps", "question": "How many FPS declarations are processed or approved?", "logic": "Count FPS Record rows with Processed or Approved status."},
        {"id": "q422-4", "metric_id": "c422-late", "question": "How many invoices are overdue?", "logic": "Count Sales Invoice records with Overdue status."}
    ],
    "4.3.1": [
        {"id": "q431-1", "metric_id": "c431-transfer", "question": "How many course transfer requests are recorded?", "logic": "Count Course Transfer child rows under Student Log."},
        {"id": "q431-2", "metric_id": "c431-defer", "question": "How many course deferment requests are recorded?", "logic": "Count Course Deferment child rows under Student Log."},
        {"id": "q431-3", "metric_id": "c431-withdraw", "question": "How many course withdrawal requests are recorded?", "logic": "Count Course Withdrawal child rows under Student Log."},
        {"id": "q431-4", "metric_id": "c431-overdue", "question": "How many movement requests exceed the processing threshold?", "logic": "Count applicable requests older than the configured working-day approximation."}
    ],
    "4.4.1": [
        {"id": "q441-1", "metric_id": "c441-open", "question": "How many refund requests are recorded?", "logic": "Count Refund rows in Student Log course adjustments."},
        {"id": "q441-2", "metric_id": "c441-eligible", "question": "How many refund requests have an approval date?", "logic": "Count refund rows with approved_date populated."},
        {"id": "q441-3", "metric_id": "c441-paid", "question": "How many refund cases are marked complete by the available workflow evidence?", "logic": "Count refund rows matching the confirmed completion rule."},
        {"id": "q441-4", "metric_id": "c441-overdue", "question": "How many refund requests exceed seven working days?", "logic": "Count refund requests older than the configured calendar-day approximation."}
    ],
    "4.5.1": [
        {"id": "q451-1", "metric_id": "c451-services", "question": "How many student support service records are available?", "logic": "Count readable intervention or counselling records."},
        {"id": "q451-2", "metric_id": "c451-cases", "question": "How many student support cases are recorded?", "logic": "Count Student Log rows containing support, intervention, counselling, wellness or academic terms."},
        {"id": "q451-3", "metric_id": "c451-followup", "question": "How many support cases require follow-up?", "logic": "Count Student Log rows containing follow-up, action-plan, pending or review terms."},
        {"id": "q451-4", "metric_id": "c451-outcomes", "question": "How many support cases contain an outcome?", "logic": "Count Student Log rows containing resolved, completed, closed, outcome or effective terms."}
    ],
    "4.6.1": [
        {"id": "q461-1", "metric_id": "c461-attendance", "question": "How many attendance records are available?", "logic": "Count readable Student Attendance records."},
        {"id": "q461-2", "metric_id": "c461-risk", "question": "How many attendance records indicate absence or lateness?", "logic": "Count Student Attendance rows with Absent or Late status."},
        {"id": "q461-3", "metric_id": "c461-warning", "question": "How many attendance warning or dismissal records are available?", "logic": "Count readable warning or dismissal records."},
        {"id": "q461-4", "metric_id": "c461-intervention", "question": "How many conduct or attendance interventions are open in Student Log evidence?", "logic": "Count Student Log rows containing intervention, warning, dismissal, attendance or counselling terms."}
    ]
}

EXCEPTION_METRIC_IDS = [
    "c411-unacknowledged", "c411-pdpa-missing", "c411-conditional", "c411-late",
    "c421-pending",
    "c422-late",
    "c431-overdue",
    "c441-open", "c441-overdue",
    "c451-followup",
    "c461-risk", "c461-intervention"
]

def resolve_doctype(candidates):
    errors = []

    for name in candidates:
        # Frappe Server Script safe-exec does not expose every normal
        # module helper, so source access is tested through get_list.
        try:
            frappe.get_meta(name)
        except Exception as error:
            errors.append({"doctype": name, "stage": "metadata", "message": str(error)})
            continue

        try:
            # Permission-aware existence probe. A successful empty result is
            # still valid and means the DocType exists and is readable.
            frappe.get_list(
                name,
                fields=["name"],
                limit_start=0,
                limit_page_length=1
            )
            return {
                "doctype": name,
                "status": "available",
                "probe": "frappe.get_list"
            }
        except Exception as error:
            message = str(error)
            lowered = message.lower()

            if (
                "permission" in lowered
                or "not permitted" in lowered
                or "not allowed" in lowered
            ):
                return {
                    "doctype": name,
                    "status": "permission_denied",
                    "message": message
                }

            # Metadata exists, so do not incorrectly report "unavailable".
            return {
                "doctype": name,
                "status": "error",
                "message": message
            }

    return {
        "doctype": None,
        "status": "unavailable",
        "candidates": candidates,
        "errors": errors
    }

def resolve_field(doctype, candidates):
    if not doctype:
        return None
    try:
        meta = frappe.get_meta(doctype)
        names = []
        for meta_field in meta.fields:
            field_name = meta_field.fieldname
            if field_name and field_name not in names:
                names.append(field_name)
        for standard_name in ["name", "creation", "modified", "owner", "docstatus"]:
            if standard_name not in names:
                names.append(standard_name)
        for fieldname in candidates:
            if fieldname in names:
                return fieldname
    except Exception:
        return None
    return None

def effective_metric(metric, doctype):
    output = {}
    for key in metric:
        output[key] = metric.get(key)
    rule = (metric.get("doctype_rules") or {}).get(doctype)
    if rule:
        for key in rule:
            output[key] = rule.get(key)
    return output

def resolve_requirements(doctype, metric):
    resolved = []
    missing = []
    requirements = metric.get("requires") or []
    for requirement in requirements:
        fieldname = resolve_field(doctype, requirement.get("field") or [])
        if not fieldname:
            missing.append(requirement.get("field") or [])
            continue
        item = {}
        for key in requirement:
            item[key] = requirement.get(key)
        item["resolved_field"] = fieldname
        resolved.append(item)
    return {
        "resolved": resolved,
        "missing": missing
    }

def user_filters(doctype):
    output = []
    try:
        meta = frappe.get_meta(doctype)
        fieldnames = []
        for meta_field in meta.fields:
            field_name = meta_field.fieldname
            if field_name and field_name not in fieldnames:
                fieldnames.append(field_name)

        mapping = {
            "academic_year": ["academic_year"],
            "program": ["program", "course", "course_applying_for", "course_type"],
            "intake": ["intake", "student_admission", "academic_term", "intake_applying"],
            "status": ["status", "workflow_state"]
        }

        for key in mapping:
            candidates = mapping.get(key) or []
            value = filters.get(key)
            if not value:
                continue
            for fieldname in candidates:
                if fieldname in fieldnames:
                    output.append([fieldname, "=", value])
                    break
    except Exception:
        pass
    return output

def fetch_rows(doctype, fields, extra_filters=None, limit=None, start=0):
    requested = []
    for fieldname in ["name", "creation", "modified"] + fields:
        if fieldname and fieldname not in requested:
            requested.append(fieldname)
    return frappe.get_list(
        doctype,
        fields=requested,
        filters=(user_filters(doctype) + (extra_filters or [])),
        limit_start=start,
        limit_page_length=limit or 500,
        order_by="modified desc"
    )

def matches(row, fieldname, metric):
    mode = metric.get("mode")
    if mode == "all":
        return True

    value = row.get(fieldname)
    text_value = str(value or "").strip().lower()
    values = []
    raw_values = metric.get("values") or []
    for raw_value in raw_values:
        values.append(str(raw_value).lower())

    if mode == "truthy":
        return bool(value) and text_value not in ["0", "no", "false", "none"]
    if mode == "falsy":
        return (not value) or text_value in ["0", "no", "false", "none"]
    if mode == "equals":
        return text_value in values
    if mode == "contains":
        for item in values:
            if item in text_value:
                return True
        return False
    if mode == "not_contains":
        for item in values:
            if item in text_value:
                return False
        return True
    if mode == "positive":
        try:
            return float(value or 0) > 0
        except Exception:
            return False
    if mode == "older_than_days":
        if not value:
            return False
        try:
            return frappe.utils.date_diff(
                frappe.utils.nowdate(),
                value
            ) > int(metric.get("days") or 0)
        except Exception:
            return False
    return False

def child_user_filter(row):
    academic_year = filters.get("academic_year")
    program = filters.get("program")
    status = filters.get("status")

    if academic_year and str(row.get("academic_year") or "") != str(academic_year):
        return False
    if program and str(row.get("program") or "") != str(program):
        return False

    if status:
        approved = bool(row.get("approved_date"))
        status_text = str(status).strip().lower()
        if status_text in ["approved", "completed"] and not approved:
            return False
        if status_text in ["open", "pending"] and approved:
            return False

    return True

def is_permission_error(error):
    message = str(error or "").lower()
    return (
        "permission" in message
        or "not permitted" in message
        or "not allowed" in message
    )

def fetch_child_rows(parent_doctype, table_field, child_doctype, requested_fields):
    table_meta_field = None
    try:
        parent_meta = frappe.get_meta(parent_doctype)
        table_meta_field = parent_meta.get_field(table_field)
    except Exception:
        table_meta_field = None

    if not table_meta_field or table_meta_field.fieldtype != "Table":
        return {"status": "unsupported_field", "rows": [], "message": "Child table field is unavailable."}

    if table_meta_field.options != child_doctype:
        return {
            "status": "unsupported_field", "rows": [],
            "message": "Child table field does not point to the expected DocType."
        }

    try:
        parent_rows = frappe.get_list(
            parent_doctype,
            fields=["name", "student", "academic_year", "program"],
            filters=user_filters(parent_doctype),
            limit_page_length=500,
            order_by="modified desc"
        )
    except Exception as error:
        if is_permission_error(error):
            return {"status": "permission_denied", "rows": [], "message": str(error)}
        return {"status": "error", "rows": [], "message": str(error)}

    output = []
    for parent_row in parent_rows:
        if len(output) >= 2000:
            break
        try:
            parent_doc = frappe.get_doc(parent_doctype, parent_row.get("name"))
        except Exception:
            continue

        children = parent_doc.get(table_field) or []
        for child in children:
            row = {
                "name": child.get("name"),
                "parent": parent_doc.name,
                "parenttype": parent_doctype,
                "parentfield": table_field,
                "student": parent_doc.get("student"),
                "parent_academic_year": parent_doc.get("academic_year"),
                "parent_program": parent_doc.get("program")
            }

            for fieldname in requested_fields:
                row[fieldname] = child.get(fieldname)

            if not row.get("academic_year"):
                row["academic_year"] = parent_doc.get("academic_year")
            if not row.get("program"):
                row["program"] = parent_doc.get("program")

            if child_user_filter(row):
                output.append(row)

    return {"status": "available", "rows": output}

def evaluate_child_metric(metric, source, include_rows=False):
    parent_doctype = source.get("doctype")
    child_doctype = metric.get("child_doctype")
    table_field = metric.get("child_table_field")

    if not child_doctype or not table_field:
        return {
            "id": metric["id"], "label": metric["label"], "value": None,
            "status": "unsupported_field", "doctype": parent_doctype,
            "field": table_field, "rows": []
        }

    fieldname = resolve_field(child_doctype, metric.get("field") or ["name"])
    if not fieldname:
        return {
            "id": metric["id"], "label": metric["label"], "value": None,
            "status": "unsupported_field", "doctype": child_doctype,
            "field": None, "field_candidates": metric.get("field"), "rows": []
        }

    requirement_result = resolve_requirements(child_doctype, metric)
    requirements = requirement_result.get("resolved") or []
    missing_requirements = requirement_result.get("missing") or []
    if missing_requirements:
        return {
            "id": metric["id"], "label": metric["label"], "value": None,
            "status": "unsupported_field", "doctype": child_doctype,
            "field": fieldname, "field_candidates": missing_requirements, "rows": []
        }

    requested_fields = [
        "type", "approved_date", "student_id", "student_name", "program",
        "posting_date", "academic_year", "reasons_for_request",
        "parent_consent", "attach_parent", "attach_docs", "withdrawal_type",
        "transferring_to", "start_date_of_deferral", "end_date_of_deferral",
        "expected_date_of_return", "courses_to_be_deferred"
    ]

    if fieldname not in requested_fields:
        requested_fields.append(fieldname)
    for requirement in requirements:
        requested = requirement.get("resolved_field")
        if requested and requested not in requested_fields:
            requested_fields.append(requested)

    fetched = fetch_child_rows(parent_doctype, table_field, child_doctype, requested_fields)
    if fetched.get("status") != "available":
        return {
            "id": metric["id"], "label": metric["label"], "value": None,
            "status": fetched.get("status"), "doctype": child_doctype,
            "field": fieldname, "message": fetched.get("message"), "rows": []
        }

    matched = []
    for row in fetched.get("rows") or []:
        if not matches(row, fieldname, metric):
            continue

        accepted = True
        for requirement in requirements:
            if not matches(row, requirement.get("resolved_field"), requirement):
                accepted = False
                break

        if accepted:
            matched.append(row)

    output_rows = matched[(page - 1) * page_size: page * page_size] if include_rows else []
    return {
        "id": metric["id"], "label": metric["label"], "value": len(matched),
        "status": "available", "doctype": child_doctype, "parent_doctype": parent_doctype,
        "field": fieldname, "rows": output_rows, "total": len(matched)
    }

resolved_sources = {}
source_output = []
source_config = CONFIG[subcriterion]["sources"]
for key in source_config:
    candidates = source_config.get(key) or []
    source = resolve_doctype(candidates)
    resolved_sources[key] = source

    source_item = {
        "key": key,
        "candidates": candidates
    }
    for source_key in source:
        source_item[source_key] = source.get(source_key)
    source_output.append(source_item)

def evaluate_metric(metric, include_rows=False):
    source = resolved_sources.get(metric["source"]) or {}
    if source.get("status") != "available":
        return {
            "id": metric["id"], "label": metric["label"], "value": None,
            "status": source.get("status") or "unavailable",
            "doctype": source.get("doctype"), "field": None, "rows": []
        }

    if metric.get("child_table_field"):
        return evaluate_child_metric(metric, source, include_rows)

    doctype = source["doctype"]
    configured = effective_metric(metric, doctype)
    fieldname = resolve_field(doctype, configured.get("field") or ["name"])
    if not fieldname:
        return {
            "id": metric["id"], "label": metric["label"], "value": None,
            "status": "unsupported_field", "doctype": doctype, "field": None,
            "field_candidates": configured.get("field"), "rows": []
        }

    requirement_result = resolve_requirements(doctype, configured)
    requirements = requirement_result.get("resolved") or []
    missing_requirements = requirement_result.get("missing") or []
    if missing_requirements:
        return {
            "id": metric["id"], "label": metric["label"], "value": None,
            "status": "unsupported_field", "doctype": doctype, "field": fieldname,
            "field_candidates": missing_requirements, "rows": []
        }

    try:
        requested_fields = [fieldname]
        for requirement in requirements:
            requested_fields.append(requirement.get("resolved_field"))

        rows = fetch_rows(doctype, requested_fields, limit=1000)
        matched = []

        for row in rows:
            if not matches(row, fieldname, configured):
                continue

            requirement_match = True
            for requirement in requirements:
                if not matches(row, requirement.get("resolved_field"), requirement):
                    requirement_match = False
                    break

            if requirement_match:
                matched.append(row)

        output_rows = matched[(page - 1) * page_size: page * page_size] if include_rows else []
        return {
            "id": metric["id"], "label": metric["label"], "value": len(matched),
            "status": "available", "doctype": doctype, "field": fieldname,
            "rows": output_rows, "total": len(matched)
        }
    except Exception as error:
        if is_permission_error(error):
            return {
                "id": metric["id"], "label": metric["label"], "value": None,
                "status": "permission_denied", "doctype": doctype,
                "field": fieldname, "message": str(error), "rows": []
            }
        return {
            "id": metric["id"], "label": metric["label"], "value": None,
            "status": "error", "doctype": doctype, "field": fieldname,
            "message": str(error), "rows": []
        }

metrics = []
configured_metrics = CONFIG[subcriterion]["metrics"]
for metric in configured_metrics:
    metrics.append(evaluate_metric(metric, False))


questions = []
question_config = QUESTION_REGISTRY.get(subcriterion) or []
for question in question_config:
    matched_metric = None
    for metric in metrics:
        if metric.get("id") == question.get("metric_id"):
            matched_metric = metric
            break

    answer = "No live answer is available."
    source_logic = question.get("logic") or ""
    confidence = "Unavailable"
    question_status = "unavailable"
    record_count = 0
    question_doctype = None
    question_field = None

    if matched_metric:
        question_status = matched_metric.get("status") or "unavailable"
        if question_status == "available":
            answer = str(matched_metric.get("value") or 0) + " record(s) match the current filters."
            source_parts = []
            if matched_metric.get("doctype"):
                source_parts.append(str(matched_metric.get("doctype")))
            if matched_metric.get("field"):
                source_parts.append(str(matched_metric.get("field")))
            if source_parts:
                source_logic = " · ".join(source_parts) + " — " + source_logic
            confidence = "Live"
            record_count = int(matched_metric.get("value") or 0)
            question_doctype = matched_metric.get("doctype")
            question_field = matched_metric.get("field")
        else:
            answer = "Unavailable: " + str(matched_metric.get("message") or matched_metric.get("status") or "source or field is unavailable.")
            confidence = "Unavailable"

    questions.append({
        "id": question.get("id"),
        "criterion": subcriterion,
        "question": question.get("question"),
        "answer": answer,
        "source_logic": source_logic,
        "confidence": confidence,
        "status": question_status,
        "metric_id": question.get("metric_id"),
        "record_count": record_count,
        "doctype": question_doctype,
        "field": question_field
    })

data_quality = []
for source in source_output:
    if source.get("status") != "available":
        data_quality.append({
            "criterion": subcriterion,
            "check": "Source availability",
            "source": source.get("doctype") or " / ".join(source.get("candidates") or []),
            "status": source.get("status") or "unavailable",
            "detail": source.get("message") or "Source could not be resolved or read."
        })

for metric in metrics:
    if metric.get("status") != "available":
        data_quality.append({
            "criterion": subcriterion,
            "check": metric.get("label"),
            "source": metric.get("doctype") or "",
            "status": metric.get("status") or "unavailable",
            "detail": metric.get("message") or "Required source or field is not available."
        })

exceptions = []
for metric in metrics:
    if metric.get("id") in EXCEPTION_METRIC_IDS:
        exceptions.append(metric)

available_source_count = 0
for source in source_output:
    if source.get("status") == "available":
        available_source_count = available_source_count + (1)

available_metric_count = 0
for metric in metrics:
    if metric.get("status") == "available":
        available_metric_count = available_metric_count + (1)

answered_question_count = 0
for question in questions:
    if question.get("status") == "available":
        answered_question_count = answered_question_count + (1)

source_summary = {
    "total": len(source_output),
    "available": available_source_count,
    "issues": len(source_output) - available_source_count
}

metric_summary = {
    "total": len(metrics),
    "available": available_metric_count,
    "issues": len(metrics) - available_metric_count
}

result = {
    "ok": True,
    "meta": {
        "api_method": "ucc_analytics_criterion_4",
        "platform_version": "1.9.8",
        "mapping_basis": "canonical_doctype_names_plus_user_confirmed_fields",
        "translation_note": "Student Admission UCC and Student Applicant may both display as Shortlisted Applicants",
        "generated_at": frappe.utils.now(),
        "subcriterion": subcriterion,
        "action": action
    },
    "filters": filters,
    "policy": POLICY_REGISTRY.get(subcriterion),
    "sources": source_output,
    "metrics": metrics,
    "questions": questions,
    "exceptions": exceptions,
    "data_quality": data_quality,
    "source_summary": source_summary,
    "metric_summary": metric_summary,
    "data": {
        "metrics": metrics,
        "sources": source_output,
        "questions": questions,
        "exceptions": exceptions,
        "data_quality": data_quality
    },
    "visual_registry": visual_registry_for(subcriterion),
    "warnings": []
}

if action == "policy_registry":
    result["registry"] = POLICY_REGISTRY
elif action == "drilldown":
    selected = None
    for metric in CONFIG[subcriterion]["metrics"]:
        if metric["id"] == metric_id:
            selected = metric
            break
    if not selected:
        frappe.throw("Unknown Criterion 4 metric.")
    result["drilldown"] = evaluate_metric(selected, True)

frappe.response["message"] = result
