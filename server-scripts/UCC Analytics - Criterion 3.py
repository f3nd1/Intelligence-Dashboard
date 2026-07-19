"""
UCC Intelligence Platform Server Script

Visible name:
    UCC Analytics - Criterion 3

Script type:
    API

API method:
    ucc_analytics_criterion_3

Purpose:
    Return permission-aware live foundations for EduTrust Criterion 3 using
    confirmed UCC recruitment-agent DocTypes and fields.

Current status:
    Live API foundation. The dashboard now uses this API. Source access is probed with permission-aware frappe.get_list calls. Metrics that require missing child-table metadata or unconfirmed
    business rules are returned as unsupported instead of being guessed.

Deployment:
    Allow Guest must remain disabled.
"""

payload_input = frappe.form_dict.get("payload") or {}
payload = json.loads(payload_input) if isinstance(payload_input, str) else payload_input
if not isinstance(payload, dict):
    payload = {}

action = payload.get("action") or "summary"
subcriterion = payload.get("subcriterion") or "3.1.1"
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

ALLOWED_ACTIONS = ["summary", "source_status", "policy_registry", "drilldown"]
if action not in ALLOWED_ACTIONS:
    frappe.throw("Unsupported Criterion 3 action.")

POLICY_REGISTRY = {
    "3.1.1": {
        "title": "Selection and Appointment of External Recruitment Agents",
        "policy": "PPD-SES-SL-3.1.1",
        "version": "1.2"
    },
    "3.2.1": {
        "title": "Management and Evaluation of Recruitment Agents",
        "policy": "PPD-SES-SL-3.2.1",
        "version": "1.2"
    }
}

SOURCE_CANDIDATES = {
    "agent": ["Agent"],
    "contract": ["Agent Contract"],
    "nda": ["Non Disclosure Agreement"],
    "onboarding": ["External Onboarding"],
    "offboarding": ["External Offboarding"],
    "provider_rating": ["Provider Rating", "Supplier Rating"],
    "annual_review": ["Agent Annual Performance Review"],
    "claim": ["Agent Claim Form"],
    "applicant": ["Student Applicant"]
}

SAFE_FIELDS = {
    "agent": [
        "name", "agent_or_company_name", "status", "custom_ra_application_form_date",
        "processed_date", "approved_date", "place_of_registration",
        "countries_of_recruitment", "average_identification_and_selection_score",
        "done_consent_and_onboarding_survey", "onboarding_survey_date",
        "contract", "nda", "agent_search_type", "identification_types", "modified"
    ],
    "contract": [
        "name", "ac_agent_link_agent_contract", "ac_name_of_agent", "posting_date",
        "start_date", "end_date", "contract_type", "requires_nda",
        "nda_acknowledged", "nda_signed_date", "signed_date", "ucc_signed_date",
        "docstatus", "modified"
    ],
    "nda": [
        "name", "status", "agent_contract", "posting_date", "start_date", "end_date",
        "signed_date", "ucc_signed_date", "docstatus", "modified"
    ],
    "onboarding": [
        "name", "document_type", "agent_id", "agent_name", "date_of_joining",
        "onboarding_begins_on", "signed_date", "signed_date_and_time", "modified"
    ],
    "offboarding": [
        "name", "document_type", "agent_id", "agent_name",
        "separation_begins_on", "signed_date", "modified"
    ],
    "provider_rating": [
        "name", "posting_date", "year", "status", "type", "document", "supplier",
        "evaluation_stage", "rating", "rating_likert", "assessment_template",
        "assessment", "note", "modified"
    ],
    "annual_review": [
        "name", "agent_name", "agent_full_name", "year", "date_of_review",
        "reviewed_by", "survey_training", "survey_comm", "survey_marketing",
        "survey_stakeholder", "survey_pdpa", "survey_isms", "survey_overall",
        "rating_recognition", "rating_pro_development", "rating_agent_recommend",
        "rating_policies_clarity", "rating_support_resources",
        "rating_communication", "modified"
    ],
    "claim": [
        "name", "year", "month", "agent", "full_name", "teaching_total",
        "extra_total", "grand_total", "docstatus", "modified"
    ],
    "applicant": [
        "name", "applicant_name", "student_name", "application_status", "status",
        "custom_agent", "agent", "recruitment_agent", "academic_year",
        "program", "modified"
    ]
}

CONFIG = {
    "3.1.1": {
        "sources": [
            "agent", "provider_rating", "contract", "nda", "onboarding", "applicant"
        ],
        "metrics": [
            {
                "id": "c311-agents", "label": "Recruitment agents in scope",
                "source": "agent", "mode": "all"
            },
            {
                "id": "c311-screening", "label": "Agents in screening or approval",
                "source": "agent", "mode": "in",
                "field": ["status"],
                "values": [
                    "Prospective", "Pending Verification", "For Approval",
                    "For Internal Use", "Under Review"
                ]
            },
            {
                "id": "c311-active", "label": "Active appointed agents",
                "source": "agent", "mode": "equals",
                "field": ["status"], "value": "Active"
            },
            {
                "id": "c311-selection-score", "label": "Selection score recorded",
                "source": "agent", "mode": "truthy",
                "field": ["average_identification_and_selection_score"]
            },
            {
                "id": "c311-selection-complete", "label": "Selection criteria completed",
                "source": "agent", "mode": "all_required",
                "fields": [
                    ["share_values_rating"], ["legal_rating"], ["partnership_rating"],
                    ["collaborative_rating"], ["financial_rating"],
                    ["communication_rating"], ["cultural_rating"],
                    ["support_rating"], ["sustainability_rating"]
                ]
            },
            {
                "id": "c311-screening-ratings", "label": "Identification and screening evaluations",
                "source": "provider_rating", "mode": "conditions",
                "conditions": [
                    {"field": ["type"], "op": "equals", "value": "Agent"},
                    {
                        "field": ["evaluation_stage"], "op": "equals",
                        "value": "Identification and Screening"
                    }
                ]
            },
            {
                "id": "c311-first-contracts", "label": "First-time agreements",
                "source": "contract", "mode": "equals",
                "field": ["contract_type"], "value": "First-time Agreement"
            },
            {
                "id": "c311-signed-contracts", "label": "Contracts signed by both parties",
                "source": "contract", "mode": "all_required",
                "fields": [["signed_date"], ["ucc_signed_date"]]
            },
            {
                "id": "c311-nda-required", "label": "Contracts requiring NDA",
                "source": "contract", "mode": "truthy",
                "field": ["requires_nda"]
            },
            {
                "id": "c311-nda-acknowledged", "label": "NDA acknowledgements completed",
                "source": "contract", "mode": "truthy",
                "field": ["nda_acknowledged"]
            },
            {
                "id": "c311-signed-nda", "label": "NDAs signed by both parties",
                "source": "nda", "mode": "all_required",
                "fields": [["signed_date"], ["ucc_signed_date"]]
            },
            {
                "id": "c311-onboardings", "label": "Agent onboarding records",
                "source": "onboarding", "mode": "conditions",
                "conditions": [
                    {"field": ["document_type"], "op": "equals", "value": "Agent"}
                ]
            },
            {
                "id": "c311-onboarding-signed", "label": "Signed agent onboarding records",
                "source": "onboarding", "mode": "conditions",
                "conditions": [
                    {"field": ["document_type"], "op": "equals", "value": "Agent"},
                    {
                        "field": ["signed_date", "signed_date_and_time"],
                        "op": "truthy"
                    }
                ]
            },
            {
                "id": "c311-linked-applicants", "label": "Applicants linked to an agent",
                "source": "applicant", "mode": "truthy",
                "field": ["custom_agent", "agent", "recruitment_agent"]
            },
            {
                "id": "c311-background-check", "label": "Background checks completed",
                "source": "agent", "mode": "unsupported",
                "message": "No confirmed dedicated background-check field or child DocType was supplied."
            }
        ]
    },
    "3.2.1": {
        "sources": [
            "agent", "provider_rating", "annual_review", "contract",
            "offboarding", "claim", "applicant"
        ],
        "metrics": [
            {
                "id": "c321-active", "label": "Active recruitment agents",
                "source": "agent", "mode": "equals",
                "field": ["status"], "value": "Active"
            },
            {
                "id": "c321-under-review", "label": "Agents under review",
                "source": "agent", "mode": "equals",
                "field": ["status"], "value": "Under Review"
            },
            {
                "id": "c321-suspended-terminated", "label": "Suspended or terminated agents",
                "source": "agent", "mode": "in",
                "field": ["status"], "values": ["Suspended", "Terminated"]
            },
            {
                "id": "c321-annual-reviews", "label": "Annual performance reviews",
                "source": "annual_review", "mode": "all"
            },
            {
                "id": "c321-survey-average", "label": "Average annual agent survey score",
                "source": "annual_review", "mode": "average_fields",
                "fields": [
                    ["survey_training"], ["survey_comm"], ["survey_marketing"],
                    ["survey_stakeholder"], ["survey_pdpa"], ["survey_isms"],
                    ["survey_overall"]
                ],
                "unit": "rating"
            },
            {
                "id": "c321-renewals", "label": "Renewal agreements",
                "source": "contract", "mode": "equals",
                "field": ["contract_type"], "value": "Renewal"
            },
            {
                "id": "c321-expiring-90", "label": "Contracts expiring within 90 days",
                "source": "contract", "mode": "date_next_days",
                "field": ["end_date"], "days": 90
            },
            {
                "id": "c321-regular-evaluations", "label": "Renewal and regular evaluations",
                "source": "provider_rating", "mode": "conditions",
                "conditions": [
                    {"field": ["type"], "op": "equals", "value": "Agent"},
                    {
                        "field": ["evaluation_stage"], "op": "equals",
                        "value": "Renewal and Regular Review"
                    }
                ]
            },
            {
                "id": "c321-continuation", "label": "Approved for continuation",
                "source": "provider_rating", "mode": "conditions",
                "conditions": [
                    {"field": ["type"], "op": "equals", "value": "Agent"},
                    {
                        "field": ["status"], "op": "equals",
                        "value": "Approved for Continuation"
                    }
                ]
            },
            {
                "id": "c321-offboardings", "label": "Agent offboarding records",
                "source": "offboarding", "mode": "conditions",
                "conditions": [
                    {"field": ["document_type"], "op": "equals", "value": "Agent"}
                ]
            },
            {
                "id": "c321-submitted-claims", "label": "Submitted agent claim forms",
                "source": "claim", "mode": "equals",
                "field": ["docstatus"], "value": 1
            },
            {
                "id": "c321-claim-total", "label": "Submitted claim amount",
                "source": "claim", "mode": "sum",
                "field": ["grand_total"],
                "conditions": [
                    {"field": ["docstatus"], "op": "equals", "value": 1}
                ],
                "unit": "SGD"
            },
            {
                "id": "c321-linked-applicants", "label": "Applicants linked to agents",
                "source": "applicant", "mode": "truthy",
                "field": ["custom_agent", "agent", "recruitment_agent"]
            },
            {
                "id": "c321-training-completion", "label": "Agent training completion",
                "source": "agent", "mode": "unsupported",
                "message": "The Agent Training and Review Log child-table field definitions were not supplied."
            },
            {
                "id": "c321-complaints", "label": "Complaints against agents",
                "source": "agent", "mode": "unsupported",
                "message": "No confirmed complaint or breach source was supplied."
            }
        ]
    }
}

QUESTION_REGISTRY = {
    "3.1.1": [
        {
            "id": "q311-1",
            "question": "How many recruitment agents are currently in the selection and appointment scope?",
            "metric_id": "c311-agents"
        },
        {
            "id": "q311-2",
            "question": "How many agents have complete selection criteria?",
            "metric_id": "c311-selection-complete"
        },
        {
            "id": "q311-3",
            "question": "How many first-time agreements are recorded?",
            "metric_id": "c311-first-contracts"
        },
        {
            "id": "q311-4",
            "question": "How many onboarding records are signed?",
            "metric_id": "c311-onboarding-signed"
        }
    ],
    "3.2.1": [
        {
            "id": "q321-1",
            "question": "How many recruitment agents are active?",
            "metric_id": "c321-active"
        },
        {
            "id": "q321-2",
            "question": "How many contracts expire within the next 90 days?",
            "metric_id": "c321-expiring-90"
        },
        {
            "id": "q321-3",
            "question": "What is the average annual agent survey score?",
            "metric_id": "c321-survey-average"
        },
        {
            "id": "q321-4",
            "question": "How many agents were approved for continuation?",
            "metric_id": "c321-continuation"
        }
    ]
}

EXCEPTION_METRIC_IDS = [
    "c311-screening",
    "c311-background-check",
    "c321-under-review",
    "c321-suspended-terminated",
    "c321-expiring-90",
    "c321-training-completion",
    "c321-complaints"
]

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
                limit_page_length=row_limit,
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

    requested_status = filters.get("status")
    if requested_status:
        for candidate in ["status", "review_status", "application_status"]:
            if field_exists(meta, candidate):
                output[candidate] = requested_status
                break

    requested_agent = filters.get("agent")
    if requested_agent:
        for candidate in [
            "agent_id", "agent_name", "ac_agent_link_agent_contract",
            "document", "custom_agent", "agent", "recruitment_agent"
        ]:
            if field_exists(meta, candidate):
                output[candidate] = requested_agent
                break

    requested_year = filters.get("year") or filters.get("academic_year")
    if requested_year:
        for candidate in ["year", "academic_year"]:
            if field_exists(meta, candidate):
                output[candidate] = requested_year
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
    if source.get("status") != "available" or not doctype:
        return []
    fields_to_fetch = safe_fields(
        doctype,
        ["name"] + (requested_fields or [])
    )
    try:
        return frappe.get_list(
            doctype,
            fields=fields_to_fetch,
            filters=applied_filters(doctype),
            limit_page_length=row_limit,
            order_by="modified desc"
        ) or []
    except Exception:
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
    if mode in ["truthy", "falsy", "equals", "in", "date_next_days"]:
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
    frappe.throw("Unsupported Criterion 3 subcriterion.")

resolved_sources = {}
for alias in CONFIG[subcriterion]["sources"]:
    resolved_sources[alias] = resolve_source(alias)

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
                + " matching review record(s)."
            )
        elif unit == "SGD":
            answer = "SGD " + str(selected_metric.get("value")) + " matches the current filters."
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
        "api_method": "ucc_analytics_criterion_3",
        "platform_version": "1.9.5",
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
    "warnings": [
        "Criterion 3 dashboard is connected to this permission-aware API foundation.",
        "Child-table metrics are marked unsupported where field metadata was not supplied."
    ]
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
        frappe.throw("Unknown Criterion 3 metric.")
    result["drilldown"] = evaluate_metric(selected_config, True)

frappe.response["message"] = result
