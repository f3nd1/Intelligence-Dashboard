"""
UCC Intelligence Platform Server Script

Visible name:
    UCC Analytics - Criterion 6

Script type:
    API

API method:
    ucc_analytics_criterion_6

Purpose:
    Return permission-aware live foundations for EduTrust Criterion 6 using
    confirmed UCC quality, management-review, provider-rating and operational
    outcome sources.

Current status:
    Partial live foundation. The API returns confirmed source and metric
    readiness. Metrics requiring missing audit, HIRA, provider-accreditation or
    child-table metadata are returned as unsupported instead of being guessed.

Deployment:
    Allow Guest must remain disabled.
"""

payload_input = frappe.form_dict.get("payload") or {}
payload = json.loads(payload_input) if isinstance(payload_input, str) else payload_input
if not isinstance(payload, dict):
    payload = {}

action = payload.get("action") or "summary"
subcriterion = payload.get("subcriterion") or "6.1.1"
filters = payload.get("filters") or {}
metric_id = payload.get("metric_id")
page = payload.get("page") or 1
page_size = payload.get("page_size") or 50
row_limit = payload.get("limit") or 1000

try:
    page = max(1, int(page))
except Exception:
    page = 1

try:
    page_size = max(1, min(int(page_size), 200))
except Exception:
    page_size = 50

try:
    row_limit = max(1, min(int(row_limit), 3000))
except Exception:
    row_limit = 1000

ALLOWED_ACTIONS = ["summary", "source_status", "policy_registry", "drilldown"]
if action not in ALLOWED_ACTIONS:
    frappe.throw("Unsupported Criterion 6 action.")

POLICY_REGISTRY = {
    "6.1.1": {
        "title": "Internal Assessment and Quality Audits",
        "policy": "PPD-SGL-SQ-6.1.1",
        "version": "1.2"
    },
    "6.2.1": {
        "title": "Management Review",
        "policy": "PPD-SGL-SQ-6.2.1",
        "version": "1.3"
    },
    "6.3.1": {
        "title": "Innovation and Continual Improvement",
        "policy": "PPD-SGL-SQ-6.3.1",
        "version": "1.2"
    },
    "6.4.1": {
        "title": "Provider's Accreditation and Evaluation",
        "policy": "PPD-OE-FN-6.4.1",
        "version": "1.2"
    },
    "6.5.3": {
        "title": "Hazard Identification and Risk Assessment",
        "policy": "PPD-SGL-SQ-6.5.3",
        "version": "1.2"
    }
}

SOURCE_CANDIDATES = {
    "quality_action": ["Quality Action"],
    "management_review": ["Management Review"],
    "operational_outcomes": ["Operational Outcomes Cost Time Saving"],
    "provider_rating": ["Provider Rating", "Supplier Rating"]
}

SAFE_FIELDS = {
    "quality_action": [
        "name", "naming_series", "custom_subject", "custom_status_updates",
        "status", "corrective_preventive", "date", "custom_proposed_date",
        "custom_completed_date", "custom_type_of_innovation",
        "custom_innovation_category", "custom_innovation",
        "custom_continuous_improvement",
        "custom_aggregated_performance_index_api",
        "custom_timeadjusted_cost_efficiency_index_tacei",
        "custom_cost_efficiency_index_cei", "custom_implementation_duration",
        "custom_cost_saving_data", "custom_annual_people_savings_ctei",
        "custom_priority_score", "custom_total_budget_fee",
        "custom_total_actual_spending", "custom_spending_difference",
        "goal", "review", "procedure", "feedback", "custom_quality_meeting",
        "modified"
    ],
    "management_review": [
        "name", "review_date", "review_period", "review_type", "review_status",
        "chairperson", "chairperson_full_name", "minutes_of_meeting",
        "next_review_date", "modified"
    ],
    "operational_outcomes": [
        "name", "monitoring_year", "period_start", "period_end",
        "benchmark_type", "benchmark_value", "variance_to_benchmark",
        "total_people_saving", "total_technology_saving",
        "total_physical_saving", "total_gross_saving",
        "total_implementation_cost", "total_maintenance_cost",
        "total_net_saving", "modified"
    ],
    "provider_rating": [
        "name", "posting_date", "year", "status", "type", "document", "supplier",
        "evaluation_stage", "rating", "rating_likert", "assessment_template",
        "assessment", "note", "modified"
    ]
}

CHILD_SAFE_FIELDS = {
    "Quality Action Resolution": [
        "idx", "finding_type", "status", "responsible", "full_name",
        "target_date", "completion_by"
    ],
    "Strategic Planning Audit Results": ["idx"],
    "Strategic Planning Nonconformities and Corrective Actions": ["idx"],
    "Management Review Strategic Planning Innovation Childtable": ["idx"],
    "Strategic Planning Performance of External Providers": ["idx"],
    "Strategic Planning Risk and Opportunities": ["idx"],
    "Quality Action Performance Indicators Childtable": ["idx"]
}

CONFIG = {
    "6.1.1": {
        "sources": ["quality_action", "management_review"],
        "metrics": [
            {
                "id": "c611-actions", "label": "Quality Actions in scope",
                "source": "quality_action", "mode": "all"
            },
            {
                "id": "c611-open-actions", "label": "Open or active Quality Actions",
                "source": "quality_action", "mode": "in",
                "field": ["custom_status_updates", "status"],
                "values": ["Open", "Planned", "In Progress"]
            },
            {
                "id": "c611-completed-actions", "label": "Completed Quality Actions",
                "source": "quality_action", "mode": "equals",
                "field": ["custom_status_updates", "status"], "value": "Completed"
            },
            {
                "id": "c611-resolutions", "label": "Quality Action resolution rows",
                "source": "quality_action", "mode": "child_count",
                "table_field": ["resolutions"],
                "child_doctype": "Quality Action Resolution"
            },
            {
                "id": "c611-open-resolutions", "label": "Open Quality Action resolutions",
                "source": "quality_action", "mode": "child_count",
                "table_field": ["resolutions"],
                "child_doctype": "Quality Action Resolution",
                "conditions": [
                    {
                        "field": ["status"], "op": "not_in",
                        "values": ["Completed"]
                    }
                ]
            },
            {
                "id": "c611-overdue-resolutions", "label": "Overdue Quality Action resolutions",
                "source": "quality_action", "mode": "child_count",
                "table_field": ["resolutions"],
                "child_doctype": "Quality Action Resolution",
                "conditions": [
                    {"field": ["target_date"], "op": "date_before_today"},
                    {
                        "field": ["status"], "op": "not_in",
                        "values": ["Completed"]
                    }
                ]
            },
            {
                "id": "c611-nonconformities", "label": "Nonconformity resolution rows",
                "source": "quality_action", "mode": "child_count",
                "table_field": ["resolutions"],
                "child_doctype": "Quality Action Resolution",
                "conditions": [
                    {
                        "field": ["finding_type"], "op": "in",
                        "values": ["NC", "Min. NC", "Maj. NC"]
                    }
                ]
            },
            {
                "id": "c611-review-audit-evidence", "label": "Management Reviews with audit results",
                "source": "management_review", "mode": "child_parent_count",
                "table_field": ["table_efwt"],
                "child_doctype": "Strategic Planning Audit Results"
            },
            {
                "id": "c611-review-nc-evidence", "label": "Management Reviews with nonconformity actions",
                "source": "management_review", "mode": "child_parent_count",
                "table_field": ["nonconformities_corrective_actions"],
                "child_doctype": "Strategic Planning Nonconformities and Corrective Actions"
            },
            {
                "id": "c611-audit-schedule", "label": "Annual audit schedule coverage",
                "source": "quality_action", "mode": "unsupported",
                "message": "Oversight Framework and audit schedule field definitions were not supplied."
            }
        ]
    },
    "6.2.1": {
        "sources": ["management_review", "quality_action"],
        "metrics": [
            {
                "id": "c621-reviews", "label": "Management Reviews in scope",
                "source": "management_review", "mode": "all"
            },
            {
                "id": "c621-scheduled", "label": "Scheduled Management Reviews",
                "source": "management_review", "mode": "equals",
                "field": ["review_status"], "value": "Scheduled"
            },
            {
                "id": "c621-in-progress", "label": "Management Reviews in progress",
                "source": "management_review", "mode": "equals",
                "field": ["review_status"], "value": "In Progress"
            },
            {
                "id": "c621-completed", "label": "Completed Management Reviews",
                "source": "management_review", "mode": "equals",
                "field": ["review_status"], "value": "Completed"
            },
            {
                "id": "c621-postponed", "label": "Postponed Management Reviews",
                "source": "management_review", "mode": "equals",
                "field": ["review_status"], "value": "Postponed"
            },
            {
                "id": "c621-overdue-next-review", "label": "Overdue next-review dates",
                "source": "management_review", "mode": "conditions",
                "conditions": [
                    {"field": ["next_review_date"], "op": "date_before_today"},
                    {
                        "field": ["review_status"], "op": "not_in",
                        "values": ["Completed"]
                    }
                ]
            },
            {
                "id": "c621-minutes", "label": "Management Reviews with minutes",
                "source": "management_review", "mode": "truthy",
                "field": ["minutes_of_meeting"]
            },
            {
                "id": "c621-quality-actions", "label": "Management Review Quality Action rows",
                "source": "management_review", "mode": "child_count",
                "table_field": ["table_qzdd"],
                "child_doctype": "Management Review Strategic Planning Innovation Childtable"
            },
            {
                "id": "c621-thesis-complete", "label": "Management Reviews with THESIS evidence",
                "source": "management_review", "mode": "all_required",
                "fields": [
                    ["leaderhip_note", "essential_information"],
                    ["resource_note", "table_bhwb"],
                    ["process_performance_note", "process_performace_conformity"],
                    ["risk_note", "risk_opportunities"],
                    ["bcp__note", "business_continuity"],
                    ["opportunities_note", "table_qzdd"]
                ]
            }
        ]
    },
    "6.3.1": {
        "sources": ["quality_action", "operational_outcomes"],
        "metrics": [
            {
                "id": "c631-innovation-actions", "label": "Innovation Quality Actions",
                "source": "quality_action", "mode": "truthy",
                "field": ["custom_innovation"]
            },
            {
                "id": "c631-improvement-actions", "label": "Continual-improvement Quality Actions",
                "source": "quality_action", "mode": "truthy",
                "field": ["custom_continuous_improvement"]
            },
            {
                "id": "c631-completed", "label": "Completed Quality Actions",
                "source": "quality_action", "mode": "equals",
                "field": ["custom_status_updates", "status"],
                "value": "Completed"
            },
            {
                "id": "c631-innovation-type", "label": "Actions with innovation type recorded",
                "source": "quality_action", "mode": "truthy",
                "field": ["custom_type_of_innovation"]
            },
            {
                "id": "c631-innovation-category", "label": "Actions with innovation category recorded",
                "source": "quality_action", "mode": "truthy",
                "field": ["custom_innovation_category"]
            },
            {
                "id": "c631-qipi", "label": "Average QIPI",
                "source": "quality_action", "mode": "average",
                "field": ["custom_aggregated_performance_index_api"],
                "unit": "index"
            },
            {
                "id": "c631-tacei", "label": "Average TACEI",
                "source": "quality_action", "mode": "average",
                "field": ["custom_timeadjusted_cost_efficiency_index_tacei"],
                "unit": "index"
            },
            {
                "id": "c631-cei", "label": "Average CEI",
                "source": "quality_action", "mode": "average",
                "field": ["custom_cost_efficiency_index_cei"],
                "unit": "index"
            },
            {
                "id": "c631-recorded-savings", "label": "Recorded Quality Action savings",
                "source": "quality_action", "mode": "sum",
                "field": [
                    "custom_cost_saving_data",
                    "custom_annual_people_savings_ctei",
                    "custom_ctei_savings"
                ],
                "unit": "SGD"
            },
            {
                "id": "c631-performance-evidence", "label": "Actions with performance indicators",
                "source": "quality_action", "mode": "child_parent_count",
                "table_field": ["custom_performance"],
                "child_doctype": "Quality Action Performance Indicators Childtable"
            },
            {
                "id": "c631-outcome-years", "label": "Operational outcome monitoring records",
                "source": "operational_outcomes", "mode": "all"
            },
            {
                "id": "c631-net-saving", "label": "Total net operational saving",
                "source": "operational_outcomes", "mode": "sum",
                "field": ["total_net_saving"], "unit": "SGD"
            },
            {
                "id": "c631-benchmark-variance", "label": "Total variance to benchmark",
                "source": "operational_outcomes", "mode": "sum",
                "field": ["variance_to_benchmark"], "unit": "SGD"
            }
        ]
    },
    "6.4.1": {
        "sources": ["provider_rating", "management_review"],
        "metrics": [
            {
                "id": "c641-ratings", "label": "Provider Rating records",
                "source": "provider_rating", "mode": "all"
            },
            {
                "id": "c641-screening", "label": "Provider identification and screening evaluations",
                "source": "provider_rating", "mode": "equals",
                "field": ["evaluation_stage"],
                "value": "Identification and Screening"
            },
            {
                "id": "c641-regular-review", "label": "Provider renewal and regular evaluations",
                "source": "provider_rating", "mode": "equals",
                "field": ["evaluation_stage"],
                "value": "Renewal and Regular Review"
            },
            {
                "id": "c641-continuation", "label": "Providers approved for continuation",
                "source": "provider_rating", "mode": "equals",
                "field": ["status"], "value": "Approved for Continuation"
            },
            {
                "id": "c641-terminated", "label": "Provider evaluations resulting in termination",
                "source": "provider_rating", "mode": "equals",
                "field": ["status"], "value": "Terminated"
            },
            {
                "id": "c641-review-evidence", "label": "Management Reviews with provider evidence",
                "source": "management_review", "mode": "child_parent_count",
                "table_field": ["table_kenc"],
                "child_doctype": "Strategic Planning Performance of External Providers"
            },
            {
                "id": "c641-accreditation", "label": "Provider accreditation completion",
                "source": "provider_rating", "mode": "unsupported",
                "message": "Provider master, accreditation and tier field definitions were not supplied."
            }
        ]
    },
    "6.5.3": {
        "sources": ["quality_action", "management_review"],
        "metrics": [
            {
                "id": "c653-risk-assessments", "label": "Quality Actions with risk assessments",
                "source": "quality_action", "mode": "child_parent_count",
                "table_field": ["custom_risk_identification_table"],
                "child_doctype": "Risk Identification Childtable"
            },
            {
                "id": "c653-risk-mitigation", "label": "Quality Actions with mitigation plans",
                "source": "quality_action", "mode": "child_parent_count",
                "table_field": ["custom_risk_mitigation"],
                "child_doctype": "Risk Justification Childtable"
            },
            {
                "id": "c653-risk-notes", "label": "Quality Actions with risk notes",
                "source": "quality_action", "mode": "truthy",
                "field": ["custom_risk_and_opportunities_identified"]
            },
            {
                "id": "c653-priority", "label": "Quality Actions with priority score",
                "source": "quality_action", "mode": "truthy",
                "field": ["custom_priority_score"]
            },
            {
                "id": "c653-review-risk-evidence", "label": "Management Reviews with risk and opportunity rows",
                "source": "management_review", "mode": "child_parent_count",
                "table_field": ["risk_opportunities"],
                "child_doctype": "Strategic Planning Risk and Opportunities"
            },
            {
                "id": "c653-risk-matrix", "label": "5×5 risk-matrix coverage",
                "source": "quality_action", "mode": "unsupported",
                "message": "Risk Register and Mitigation Plans fields were not supplied."
            },
            {
                "id": "c653-hazard-reports", "label": "Hazard reports",
                "source": "quality_action", "mode": "unsupported",
                "message": "The Helpdesk-Ticket hazard classification fields were not supplied."
            }
        ]
    }
}

QUESTION_REGISTRY = {
    "6.1.1": [
        {
            "id": "q611-1",
            "question": "How many Quality Action resolution rows are open?",
            "metric_id": "c611-open-resolutions"
        },
        {
            "id": "q611-2",
            "question": "How many resolution rows are overdue?",
            "metric_id": "c611-overdue-resolutions"
        },
        {
            "id": "q611-3",
            "question": "How many nonconformity rows are recorded?",
            "metric_id": "c611-nonconformities"
        }
    ],
    "6.2.1": [
        {
            "id": "q621-1",
            "question": "How many Management Reviews are completed?",
            "metric_id": "c621-completed"
        },
        {
            "id": "q621-2",
            "question": "How many Management Reviews are postponed?",
            "metric_id": "c621-postponed"
        },
        {
            "id": "q621-3",
            "question": "How many Management Reviews include THESIS evidence?",
            "metric_id": "c621-thesis-complete"
        }
    ],
    "6.3.1": [
        {
            "id": "q631-1",
            "question": "How many innovation Quality Actions are recorded?",
            "metric_id": "c631-innovation-actions"
        },
        {
            "id": "q631-2",
            "question": "What is the average QIPI?",
            "metric_id": "c631-qipi"
        },
        {
            "id": "q631-3",
            "question": "What is the total net operational saving?",
            "metric_id": "c631-net-saving"
        }
    ],
    "6.4.1": [
        {
            "id": "q641-1",
            "question": "How many provider evaluations are approved for continuation?",
            "metric_id": "c641-continuation"
        },
        {
            "id": "q641-2",
            "question": "How many provider evaluations resulted in termination?",
            "metric_id": "c641-terminated"
        }
    ],
    "6.5.3": [
        {
            "id": "q653-1",
            "question": "How many Quality Actions include a risk assessment?",
            "metric_id": "c653-risk-assessments"
        },
        {
            "id": "q653-2",
            "question": "How many Quality Actions include a mitigation plan?",
            "metric_id": "c653-risk-mitigation"
        }
    ]
}

EXCEPTION_METRIC_IDS = [
    "c611-open-actions",
    "c611-open-resolutions",
    "c611-overdue-resolutions",
    "c611-nonconformities",
    "c611-audit-schedule",
    "c621-postponed",
    "c621-overdue-next-review",
    "c641-terminated",
    "c641-accreditation",
    "c653-risk-matrix",
    "c653-hazard-reports"
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
        text = clean_text(value).replace(",", "").replace("SGD", "").replace("$", "")
        return float(text)
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
        for candidate in ["custom_status_updates", "status", "review_status"]:
            if field_exists(meta, candidate):
                output[candidate] = requested_status
                break

    requested_year = filters.get("year") or filters.get("monitoring_year")
    if requested_year:
        for candidate in ["monitoring_year", "year"]:
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

def compare(row, fieldname, op, expected=None, values=None):
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
    if op == "date_before_today":
        if not value:
            return False
        try:
            return frappe.utils.getdate(value) < frappe.utils.getdate(frappe.utils.today())
        except Exception:
            return False
    return False

def resolve_conditions(doctype, conditions):
    resolved = []
    missing = []
    for condition in conditions or []:
        fieldname = resolve_field(doctype, condition.get("field") or [])
        if not fieldname:
            missing.append(condition.get("field") or [])
            continue
        item = {}
        for key in condition:
            item[key] = condition.get(key)
        item["resolved_field"] = fieldname
        resolved.append(item)
    return resolved, missing

def conditions_match(row, conditions):
    for condition in conditions:
        if not compare(
            row,
            condition.get("resolved_field"),
            condition.get("op"),
            expected=condition.get("value"),
            values=condition.get("values")
        ):
            return False
    return True

if subcriterion not in CONFIG:
    frappe.throw("Unsupported Criterion 6 subcriterion.")

resolved_sources = {}
for alias in CONFIG[subcriterion]["sources"]:
    resolved_sources[alias] = resolve_source(alias)

def evaluate_parent_metric(metric, source, include_rows):
    doctype = source.get("doctype")
    mode = metric.get("mode")
    fields = []
    missing = []

    if metric.get("field"):
        fieldname = resolve_field(doctype, metric.get("field"))
        if fieldname:
            fields.append(fieldname)
        else:
            missing.append(metric.get("field"))

    field_group_result = resolve_field_groups(
        doctype, metric.get("fields") or []
    )
    resolved_groups = field_group_result[0]
    missing_groups = field_group_result[1]
    fields.extend(resolved_groups)
    missing.extend(missing_groups)

    condition_result = resolve_conditions(
        doctype, metric.get("conditions") or []
    )
    resolved_conditions = condition_result[0]
    missing_conditions = condition_result[1]
    missing.extend(missing_conditions)
    for condition in resolved_conditions:
        if condition.get("resolved_field") not in fields:
            fields.append(condition.get("resolved_field"))

    if mode != "all" and missing:
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

    requested = list(fields)
    if include_rows:
        for fieldname in SAFE_FIELDS.get(metric.get("source"), []):
            if fieldname not in requested:
                requested.append(fieldname)

    rows = fetch_rows(source, requested)
    matched = []

    for row in rows:
        accepted = True
        if mode == "all":
            accepted = True
        elif mode in ["truthy", "equals", "in"]:
            accepted = compare(
                row,
                fields[0] if fields else "",
                mode,
                expected=metric.get("value"),
                values=metric.get("values")
            )
        elif mode == "conditions":
            accepted = conditions_match(row, resolved_conditions)
        elif mode == "all_required":
            for fieldname in fields:
                if not is_truthy(row.get(fieldname)):
                    accepted = False
                    break
        elif mode in ["average", "sum"]:
            accepted = conditions_match(row, resolved_conditions)
            if accepted:
                accepted = bool(fields and to_number(row.get(fields[0])) is not None)
        else:
            accepted = False

        if accepted:
            matched.append(row)

    value = len(matched)
    if mode == "average":
        numbers = []
        for row in matched:
            number = to_number(row.get(fields[0]))
            if number is not None:
                numbers.append(number)
        value = round(sum(numbers) / len(numbers), 2) if numbers else 0

    if mode == "sum":
        total = 0
        for row in matched:
            number = to_number(row.get(fields[0]))
            if number is not None:
                total = total + number
        value = round(total, 2)

    output_rows = []
    if include_rows:
        start = (page - 1) * page_size
        end = start + page_size
        allowed = safe_fields(
            doctype,
            SAFE_FIELDS.get(metric.get("source"), ["name"])
        )
        for row in matched[start:end]:
            item = {}
            for fieldname in allowed:
                item[fieldname] = row.get(fieldname)
            output_rows.append(item)

    return {
        "id": metric.get("id"),
        "label": metric.get("label"),
        "source": metric.get("source"),
        "doctype": doctype,
        "value": value,
        "unit": metric.get("unit") or "records",
        "record_count": len(matched),
        "status": "available",
        "resolved_fields": fields,
        "rows": output_rows,
        "total": len(matched)
    }

def evaluate_child_metric(metric, source, include_rows):
    parent_doctype = source.get("doctype")
    table_field = resolve_field(
        parent_doctype,
        metric.get("table_field") or []
    )
    if not table_field:
        return {
            "id": metric.get("id"),
            "label": metric.get("label"),
            "source": metric.get("source"),
            "doctype": parent_doctype,
            "value": None,
            "status": "unsupported_field",
            "message": "Required child-table field is not installed.",
            "missing_field_candidates": [metric.get("table_field") or []],
            "rows": []
        }

    parent_meta = get_meta(parent_doctype)
    child_doctype = metric.get("child_doctype")
    try:
        table_meta = parent_meta.get_field(table_field)
        if table_meta and table_meta.options:
            child_doctype = table_meta.options
    except Exception:
        pass

    child_meta = get_meta(child_doctype)
    if not child_meta:
        return {
            "id": metric.get("id"),
            "label": metric.get("label"),
            "source": metric.get("source"),
            "doctype": child_doctype,
            "parent_doctype": parent_doctype,
            "value": None,
            "status": "unavailable",
            "message": "Required child DocType is not installed.",
            "rows": []
        }

    child_condition_result = resolve_conditions(
        child_doctype,
        metric.get("conditions") or []
    )
    resolved_conditions = child_condition_result[0]
    missing = child_condition_result[1]
    if missing:
        return {
            "id": metric.get("id"),
            "label": metric.get("label"),
            "source": metric.get("source"),
            "doctype": child_doctype,
            "parent_doctype": parent_doctype,
            "value": None,
            "status": "unsupported_field",
            "message": "Required child field is not installed.",
            "missing_field_candidates": missing,
            "rows": []
        }

    parent_rows = fetch_rows(source, [])
    matched_rows = []
    matched_parents = []

    for parent in parent_rows:
        try:
            doc = frappe.get_doc(parent_doctype, parent.get("name"))
        except Exception:
            continue

        try:
            child_rows = doc.get(table_field) or []
        except Exception:
            child_rows = []

        parent_has_match = False
        for child in child_rows:
            if conditions_match(child, resolved_conditions):
                parent_has_match = True
                matched_rows.append({
                    "parent": parent.get("name"),
                    "child": child
                })

        if parent_has_match:
            matched_parents.append(parent.get("name"))

    count_mode = "parents" if metric.get("mode") == "child_parent_count" else "rows"
    value = len(matched_parents) if count_mode == "parents" else len(matched_rows)

    output_rows = []
    if include_rows:
        start = (page - 1) * page_size
        end = start + page_size
        selected_rows = matched_rows[start:end]
        allowed = safe_fields(
            child_doctype,
            CHILD_SAFE_FIELDS.get(child_doctype, ["idx"])
        )
        for entry in selected_rows:
            item = {
                "parent_doctype": parent_doctype,
                "parent": entry.get("parent"),
                "child_doctype": child_doctype
            }
            child = entry.get("child")
            for fieldname in allowed:
                try:
                    item[fieldname] = child.get(fieldname)
                except Exception:
                    item[fieldname] = None
            output_rows.append(item)

    return {
        "id": metric.get("id"),
        "label": metric.get("label"),
        "source": metric.get("source"),
        "doctype": child_doctype,
        "parent_doctype": parent_doctype,
        "table_field": table_field,
        "value": value,
        "unit": "parents" if count_mode == "parents" else "rows",
        "record_count": value,
        "status": "available",
        "rows": output_rows,
        "total": value
    }

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

    if metric.get("mode") in ["child_count", "child_parent_count"]:
        return evaluate_child_metric(metric, source, include_rows)

    return evaluate_parent_metric(metric, source, include_rows)

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
        if unit == "SGD":
            answer = "SGD " + str(selected_metric.get("value")) + " matches the current filters."
        elif unit == "index":
            answer = str(selected_metric.get("value")) + " is the live calculated average."
        else:
            answer = str(selected_metric.get("value") or 0) + " " + unit + " match the current filters."
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
        "api_method": "ucc_analytics_criterion_6",
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
        "Criterion 6 dashboard is connected to this permission-aware API foundation.",
        "Audit schedule, HIRA and provider-accreditation metrics remain unsupported where metadata was not supplied.",
        "Operational Outcomes Cost Time Saving is treated as a cross-criterion source pending ownership confirmation."
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
        frappe.throw("Unknown Criterion 6 metric.")
    result["drilldown"] = evaluate_metric(selected_config, True)

frappe.response["message"] = result
