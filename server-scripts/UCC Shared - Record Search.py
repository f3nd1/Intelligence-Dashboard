"""
UCC Intelligence Platform Server Script

Visible name:
    UCC Shared - Record Search

Script type:
    API

API method:
    ucc_shared_record_search

Purpose:
    Search only approved record types for Ask UCC and future shared selectors.
"""

payload_input = frappe.form_dict.get("payload") or {}
payload = json.loads(payload_input) if isinstance(payload_input, str) else payload_input
if not isinstance(payload, dict):
    payload = {}
entity = payload.get("entity") or ""
query = str(payload.get("query") or "").strip()
limit = payload.get("limit") or 20

try:
    limit = max(1, min(int(limit), 50))
except Exception:
    limit = 20

ENTITY_CONFIG = {
    "student": {
        "doctype": "Student Applicant",
        "search_fields": ["name", "student_name", "first_name"],
        "field_attempts": [
            ["name", "student_name", "program", "application_status"],
            ["name", "first_name", "program", "status"],
            ["name"]
        ]
    },
    "recruitment_agent": {
        "doctype": "Agent Contract",
        "search_fields": ["name", "party_name", "personal_id"],
        "field_attempts": [
            ["name", "party_name", "personal_id", "contract_start", "contract_end"],
            ["name", "party_name", "personal_id"],
            ["name"]
        ]
    },
    "quality_action": {
        "doctype": "Quality Action",
        "search_fields": ["name", "custom_subject"],
        "field_attempts": [
            ["name", "custom_subject", "status", "modified"],
            ["name", "status", "modified"],
            ["name"]
        ]
    }
}

config = ENTITY_CONFIG.get(entity)

def query_records(doctype, fields, search_fields):
    filters = []

    if query:
        or_filters = []
        for fieldname in search_fields:
            or_filters.append([doctype, fieldname, "like", "%" + query + "%"])
    else:
        or_filters = []

    return frappe.get_list(
        doctype,
        fields=fields,
        or_filters=or_filters,
        order_by="modified desc",
        limit_page_length=limit
    ) or []

if not config:
    frappe.response["message"] = {
        "ok": False,
        "error_code": "UNSUPPORTED_ENTITY",
        "message": "Unsupported record-search entity.",
        "allowed_entities": sorted(ENTITY_CONFIG.keys())
    }
elif not frappe.has_permission(config["doctype"], "read"):
    frappe.response["message"] = {
        "ok": False,
        "error_code": "NOT_PERMITTED",
        "message": "You do not have permission to search this record type."
    }
else:
    records = []
    last_error = ""

    for fields in config["field_attempts"]:
        try:
            records = query_records(
                config["doctype"],
                fields,
                config["search_fields"]
            )
            last_error = ""
            break
        except Exception as error:
            last_error = str(error)

    if last_error:
        frappe.response["message"] = {
            "ok": False,
            "error_code": "SEARCH_FAILED",
            "message": last_error
        }
    else:
        frappe.response["message"] = {
            "ok": True,
            "meta": {
                "entity": entity,
                "doctype": config["doctype"],
                "returned": len(records),
                "generated_at": frappe.utils.now()
            },
            "records": records
        }
