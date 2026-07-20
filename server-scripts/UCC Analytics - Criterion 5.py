"""
UCC Intelligence Platform Server Script

Visible name:
    UCC Analytics - Criterion 5

Script type:
    API

API method:
    ucc_analytics_criterion_5

Purpose:
    Permission-aware migration API for Criterion 5 analytics.

Current status:
    Migration foundation plus the first migrated capability: c511_hydrate
    returns full Course and Program documents (child tables included) in one
    call, replacing the frontend's per-record frappe.client.get hydration loop
    for section 5.1.1. The client falls back to per-record hydration when this
    action is unavailable, so deploying this script is safe either way.
    Move remaining sections one at a time and compare values before deleting
    the matching JavaScript calculation.

Deployment:
    Allow Guest must remain disabled.
"""

payload_input = frappe.form_dict.get("payload") or {}
payload = json.loads(payload_input) if isinstance(payload_input, str) else payload_input
if not isinstance(payload, dict):
    payload = {}
action = payload.get("action") or frappe.form_dict.get("section") or "c511_summary"
filters = payload.get("filters") or {}
limit = payload.get("limit") or frappe.form_dict.get("limit") or 500

try:
    limit = int(limit)
except Exception:
    limit = 500

limit = max(1, min(limit, 1000))

ALLOWED_ACTIONS = [
    "base",
    "overview",
    "c511_hydrate",
    "c511_summary",
    "c511_proposals",
    "c511_modules",
    "c511_reviews",
    "c511_gaps"
]

SOURCE_MAP = {
    "base": [
        ("Academic Year", ["name", "academic_year_name", "year_start_date", "year_end_date"]),
        ("Student Group", ["name", "student_group_name", "academic_year", "program", "course", "disabled"]),
        ("Course", ["name", "course_name", "department", "modified"]),
        ("Program", ["name", "program_name", "department", "modified"])
    ],
    "overview": [
        ("Academic Year", ["name", "academic_year_name", "year_start_date", "year_end_date"]),
        ("Student Group", ["name", "student_group_name", "academic_year", "program", "course", "disabled"]),
        ("Course", ["name", "course_name", "department", "modified"]),
        ("Program", ["name", "program_name", "department", "modified"])
    ],
    "c511_summary": [
        ("Course Proposal", ["name", "course_title", "approval_status", "proposed_date", "decision_date", "ssg_approval_date", "modified"]),
        ("Course", ["name", "course_name", "department", "modified"]),
        ("Program", ["name", "program_name", "department", "modified"]),
        ("Course Review", ["name", "course", "review_date", "review_status", "next_review_date", "modified"]),
        ("Assessment Plan", ["name", "course", "program", "academic_year", "assessment_name", "modified"])
    ],
    "c511_proposals": [
        ("Course Proposal", ["name", "course_title", "approval_status", "proposed_date", "decision_date", "ssg_approval_date", "modified"])
    ],
    "c511_modules": [
        ("Course", ["name", "course_name", "department", "modified"]),
        ("Program", ["name", "program_name", "department", "modified"]),
        ("Assessment Plan", ["name", "course", "program", "academic_year", "assessment_name", "modified"])
    ],
    "c511_reviews": [
        ("Course Review", ["name", "course", "review_date", "review_status", "next_review_date", "modified"])
    ],
    "c511_gaps": [
        ("Course Proposal", ["name", "course_title", "approval_status", "proposed_date", "decision_date", "ssg_approval_date", "modified"]),
        ("Course", ["name", "course_name", "department", "modified"]),
        ("Course Review", ["name", "course", "review_date", "review_status", "next_review_date", "modified"])
    ]
}

def safe_rows(doctype, fields):
    try:
        rows = frappe.get_list(
            doctype,
            fields=fields,
            limit_page_length=limit,
            order_by="modified desc"
        ) or []
        return rows, {
            "status": "Available",
            "count": len(rows)
        }
    except Exception as error:
        message = str(error)
        lowered = message.lower()
        status = "Not permitted" if (
            "permission" in lowered
            or "not permitted" in lowered
            or "not allowed" in lowered
        ) else "Unavailable"
        return [], {
            "status": status,
            "count": 0,
            "error": message
        }

if action not in ALLOWED_ACTIONS:
    frappe.response["message"] = {
        "ok": False,
        "error_code": "UNSUPPORTED_ACTION",
        "message": "Unsupported Criterion 5 action.",
        "allowed_actions": ALLOWED_ACTIONS
    }
elif action == "c511_hydrate":
    # Full documents (child tables included) for the 5.1.1 evidence checks,
    # replacing up to 2 x limit per-record frappe.client.get round-trips with
    # this single call. Permission-aware: get_list and get_doc both enforce
    # the caller's read permissions.
    data = {}
    sources = {}
    for doctype in ["Course", "Program"]:
        try:
            names = frappe.get_list(
                doctype,
                pluck="name",
                limit_page_length=limit,
                order_by="modified desc"
            ) or []
            documents = []
            for name in names:
                documents.append(frappe.get_doc(doctype, name).as_dict())
            data[doctype] = documents
            sources[doctype] = {"status": "Available", "count": len(documents)}
        except Exception as error:
            message = str(error)
            lowered = message.lower()
            status = "Not permitted" if (
                "permission" in lowered
                or "not permitted" in lowered
                or "not allowed" in lowered
            ) else "Unavailable"
            data[doctype] = []
            sources[doctype] = {"status": status, "count": 0, "error": message}

    frappe.response["message"] = {
        "ok": True,
        "meta": {
            "api_method": "ucc_analytics_criterion_5",
            "dashboard": "criterion_5",
            "action": action,
            "generated_at": frappe.utils.now()
        },
        "data": data,
        "sources": sources
    }
else:
    data = {}
    sources = {}

    for source_item in SOURCE_MAP.get(action, []):
        doctype = source_item[0]
        fields = source_item[1]
        source_result = safe_rows(doctype, fields)
        rows = source_result[0]
        source_state = source_result[1]
        data[doctype] = rows
        sources[doctype] = source_state

    frappe.response["message"] = {
        "ok": True,
        "meta": {
            "api_method": "ucc_analytics_criterion_5",
            "dashboard": "criterion_5",
            "action": action,
            "generated_at": frappe.utils.now(),
            "status": "migration_foundation"
        },
        "filters": filters,
        "data": data,
        "sources": sources,
        "warnings": [
            "This API is a migration foundation. The v1.0.0 Analytics Hub still uses the validated v5.6.1 frontend calculation path."
        ]
    }
