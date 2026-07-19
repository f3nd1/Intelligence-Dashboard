"""
UCC Intelligence Platform Server Script

Visible name:
    UCC Analytics - Drilldown

Script type:
    API

API method:
    ucc_analytics_drilldown

Purpose:
    Return paginated, permission-aware records for approved analytics datasets.
"""

payload_input = frappe.form_dict.get("payload") or {}
payload = json.loads(payload_input) if isinstance(payload_input, str) else payload_input
if not isinstance(payload, dict):
    payload = {}
dataset = payload.get("dataset") or ""
page = payload.get("page") or 1
page_size = payload.get("page_size") or 50
requested_filters = payload.get("filters") or {}

try:
    page = max(1, int(page))
except Exception:
    page = 1

try:
    page_size = max(1, min(int(page_size), 100))
except Exception:
    page_size = 50

DATASETS = {
    "course_proposals": {
        "doctype": "Course Proposal",
        "fields": ["name", "course_title", "approval_status", "proposed_date", "decision_date", "modified"],
        "filter_fields": ["name", "approval_status", "proposed_date", "decision_date"]
    },
    "modules": {
        "doctype": "Course",
        "fields": ["name", "course_name", "department", "modified"],
        "filter_fields": ["name", "department"]
    },
    "courses": {
        "doctype": "Program",
        "fields": ["name", "program_name", "department", "modified"],
        "filter_fields": ["name", "department"]
    },
    "course_reviews": {
        "doctype": "Course Review",
        "fields": ["name", "course", "review_date", "review_status", "next_review_date", "modified"],
        "filter_fields": ["name", "course", "review_status", "review_date", "next_review_date"]
    },
    "assessment_plans": {
        "doctype": "Assessment Plan",
        "fields": ["name", "assessment_name", "student_group", "course", "program", "academic_year", "schedule_date"],
        "filter_fields": ["name", "student_group", "course", "program", "academic_year", "schedule_date"]
    },
    "assessment_results": {
        "doctype": "Assessment Result",
        "fields": ["name", "assessment_plan", "student", "student_name", "student_group", "course", "program", "academic_year", "total_score", "grade"],
        "filter_fields": ["name", "assessment_plan", "student", "student_group", "course", "program", "academic_year", "grade"]
    },
    "quality_actions": {
        "doctype": "Quality Action",
        "fields": ["name", "custom_subject", "status", "modified"],
        "filter_fields": ["name", "status"]
    }
}

config = DATASETS.get(dataset)

if not config:
    frappe.response["message"] = {
        "ok": False,
        "error_code": "UNSUPPORTED_DATASET",
        "message": "The requested drill-down dataset is not approved.",
        "allowed_datasets": sorted(DATASETS.keys())
    }
else:
    doctype = config["doctype"]

    if not frappe.has_permission(doctype, "read"):
        frappe.response["message"] = {
            "ok": False,
            "error_code": "NOT_PERMITTED",
            "message": "You do not have permission to read this dataset."
        }
    else:
        clean_filters = {}

        for fieldname in config["filter_fields"]:
            if fieldname in requested_filters:
                clean_filters[fieldname] = requested_filters.get(fieldname)

        start = (page - 1) * page_size

        try:
            records = frappe.get_list(
                doctype,
                fields=config["fields"],
                filters=clean_filters,
                order_by="modified desc",
                start=start,
                page_length=page_size
            ) or []

            frappe.response["message"] = {
                "ok": True,
                "meta": {
                    "dataset": dataset,
                    "doctype": doctype,
                    "page": page,
                    "page_size": page_size,
                    "returned": len(records),
                    "generated_at": frappe.utils.now()
                },
                "records": records
            }
        except Exception as error:
            frappe.response["message"] = {
                "ok": False,
                "error_code": "QUERY_FAILED",
                "message": str(error)
            }
