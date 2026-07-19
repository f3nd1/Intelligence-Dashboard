"""
UCC Intelligence Platform Server Script

Visible name:
    UCC Analytics - Bootstrap

Script type:
    API

API method:
    ucc_analytics_bootstrap

Purpose:
    Return the signed-in user's capabilities and common filter options.

Deployment:
    Allow Guest must remain disabled.
"""

def safe_list(doctype, fields, order_by=None, limit=500):
    try:
        if not frappe.has_permission(doctype, "read"):
            return []
        return frappe.get_list(
            doctype,
            fields=fields,
            order_by=order_by or "modified desc",
            limit_page_length=limit
        ) or []
    except Exception:
        return []

roles = frappe.get_roles(frappe.session.user) or []

academic_years = safe_list(
    "Academic Year",
    ["name", "academic_year_name", "year_start_date", "year_end_date"],
    "year_start_date desc",
    100
)

programs = safe_list(
    "Program",
    ["name", "program_name"],
    "program_name asc",
    500
)

student_groups = safe_list(
    "Student Group",
    ["name", "student_group_name", "academic_year", "program", "course", "disabled"],
    "modified desc",
    1000
)

frappe.response["message"] = {
    "ok": True,
    "meta": {
        "api_method": "ucc_analytics_bootstrap",
        "generated_at": frappe.utils.now(),
        "platform_version": "1.9.5"
    },
    "user": {
        "name": frappe.session.user,
        "roles": roles
    },
    "dashboards": [{'id': 'criterion_1', 'status': 'live_foundation', 'api_method': 'ucc_analytics_criterion_1'},
 {'id': 'criterion_2', 'status': 'live_foundation', 'api_method': 'ucc_analytics_criterion_2'},
 {'id': 'criterion_3', 'status': 'live_foundation', 'api_method': 'ucc_analytics_criterion_3'},
 {'id': 'criterion_4', 'status': 'live', 'api_method': 'ucc_analytics_criterion_4'},
 {'id': 'criterion_5', 'status': 'live_frontend', 'api_method': 'ucc_analytics_criterion_5'},
 {'id': 'criterion_6', 'status': 'live_foundation', 'api_method': 'ucc_analytics_criterion_6'},
 {'id': 'criterion_7', 'status': 'live_foundation', 'api_method': 'ucc_analytics_criterion_7'}],
    "ask_modules": [
        {"id": "student_journey", "status": "active"},
        {"id": "recruitment_agent", "status": "active"},
        {"id": "quality_action", "status": "active"},
        {"id": "hr", "status": "planned"}
    ],
    "filters": {
        "academic_years": academic_years,
        "programs": programs,
        "student_groups": student_groups
    }
}
