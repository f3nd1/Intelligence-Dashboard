"""
UCC Intelligence Platform Server Script

Visible name:
    UCC Analytics - Bootstrap

Script type:
    API

API method:
    ucc_analytics_bootstrap

Purpose:
    Return common filter options for the signed-in user.

Deployment:
    Allow Guest must remain disabled.
"""


def safe_list(doctype, fields, order_by=None, page_length=500):
    """Return records allowed for the current user, or an empty list."""
    try:
        return frappe.db.get_list(
            doctype,
            fields=fields,
            order_by=order_by or "modified desc",
            page_length=page_length
        ) or []
    except Exception:
        return []


current_user = frappe.session.user
roles = ["Guest"] if current_user == "Guest" else ["All"]

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
        "platform_version": "1.9.15",
        "safe_exec_hotfix": "2"
    },
    "user": {
        "name": current_user,
        "roles": roles
    },
    "dashboards": [
        {"id": "criterion_1", "status": "live_foundation", "api_method": "ucc_analytics_criterion_1"},
        {"id": "criterion_2", "status": "live_foundation", "api_method": "ucc_analytics_criterion_2"},
        {"id": "criterion_3", "status": "live_foundation", "api_method": "ucc_analytics_criterion_3"},
        {"id": "criterion_4", "status": "live", "api_method": "ucc_analytics_criterion_4"},
        {"id": "criterion_5", "status": "live_frontend", "api_method": "ucc_analytics_criterion_5"},
        {"id": "criterion_6", "status": "live_foundation", "api_method": "ucc_analytics_criterion_6"},
        {"id": "criterion_7", "status": "live_foundation", "api_method": "ucc_analytics_criterion_7"}
    ],
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
