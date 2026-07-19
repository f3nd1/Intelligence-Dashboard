"""
UCC Intelligence Platform Server Script

Visible name:
    UCC Analytics - Criterion 1

Script type:
    API

API method:
    ucc_analytics_criterion_1

Purpose:
    Return permission-aware live analytics foundations for EduTrust Criterion 1.

Current status:
    Live API foundation. The dashboard uses this API. Unsupported fields and
    unavailable sources are reported explicitly instead of being guessed.

Deployment:
    Allow Guest must remain disabled.
"""

payload_input = frappe.form_dict.get("payload") or {}
payload = json.loads(payload_input) if isinstance(payload_input, str) else payload_input
if not isinstance(payload, dict):
    payload = {}

action = payload.get("action") or "summary"
subcriterion = payload.get("subcriterion") or "1.1.1"
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
    frappe.throw("Unsupported Criterion 1 action.")

POLICY_REGISTRY = {'1.1.1': {'title': 'Leadership and Corporate Governance',
           'policy': 'PPD-SGL-CG-1.1.1',
           'version': '2.2'},
 '1.2.1': {'title': 'Strategic Planning', 'policy': 'PPD-SGL-SQ-1.2.1', 'version': '1.2'}}

SOURCE_CANDIDATES = {'oversight': ['Oversight Framework'],
 'stakeholder_registry': ['Stakeholder Registry'],
 'stakeholder_engagement': ['Stakeholder Engagement Strategy'],
 'policy_control': ['Policies and Standards Type', 'Quality Procedure'],
 'esg_strategy': ['ESG Strategy Insights'],
 'esg_tracker': ['ESG Impact Tracker'],
 'business_impact': ['Business Impact Analysis'],
 'risk_register': ['Risk Register and Mitigation Plans'],
 'quality_goal': ['Quality Goal'],
 'staff_goal': ['Goal'],
 'appraisal': ['Appraisal'],
 'management_review': ['Management Review'],
 'quality_action': ['Quality Action']}

SAFE_FIELDS = {'oversight': ['name',
               'title',
               'subject',
               'status',
               'review_status',
               'framework_type',
               'owner',
               'assigned_to',
               'review_date',
               'next_review_date',
               'approval_date',
               'modified'],
 'stakeholder_registry': ['name',
                          'stakeholder_name',
                          'stakeholder_type',
                          'category',
                          'status',
                          'department',
                          'owner',
                          'modified'],
 'stakeholder_engagement': ['name',
                            'stakeholder',
                            'stakeholder_group',
                            'engagement_type',
                            'communication_channel',
                            'frequency',
                            'status',
                            'engagement_date',
                            'next_engagement_date',
                            'modified'],
 'policy_control': ['name',
                     'title',
                     'policy_name',
                     'document_code',
                     'version',
                     'status',
                     'effective_date',
                     'review_date',
                     'next_review_date',
                     'owner',
                     'department',
                     'modified'],
 'esg_strategy': ['name',
                  'title',
                  'status',
                  'year',
                  'objective',
                  'target',
                  'actual',
                  'progress',
                  'owner',
                  'modified'],
 'esg_tracker': ['name',
                 'initiative',
                 'status',
                 'year',
                 'target',
                 'actual',
                 'progress',
                 'owner',
                 'modified'],
 'business_impact': ['name',
                     'title',
                     'department',
                     'status',
                     'risk_level',
                     'review_date',
                     'next_review_date',
                     'owner',
                     'modified'],
 'risk_register': ['name',
                   'risk',
                   'risk_title',
                   'status',
                   'risk_level',
                   'likelihood',
                   'severity',
                   'risk_score',
                   'residual_risk',
                   'owner',
                   'target_date',
                   'modified'],
 'quality_goal': ['name', 'goal', 'frequency', 'procedure', 'date', 'weekday', 'modified'],
 'staff_goal': ['name',
                'goal_name',
                'is_group',
                'parent_goal',
                'progress',
                'status',
                'custom_type',
                'employee',
                'employee_name',
                'company',
                'user',
                'start_date',
                'end_date',
                'custom_change_department',
                'custom_department',
                'appraisal_cycle',
                'kra',
                'description',
                'modified'],
 'appraisal': ['name',
               'employee',
               'employee_name',
               'status',
               'start_date',
               'end_date',
               'appraisal_cycle',
               'final_score',
               'modified'],
 'management_review': ['name',
                       'review_date',
                       'review_period',
                       'review_type',
                       'review_status',
                       'chairperson',
                       'next_review_date',
                       'modified'],
 'quality_action': ['name',
                    'goal',
                    'review',
                    'procedure',
                    'status',
                    'custom_status_updates',
                    'date',
                    'custom_proposed_date',
                    'custom_completed_date',
                    'custom_priority_score',
                    'modified']}

FILTER_FIELD_CANDIDATES = {'status': ['status', 'review_status', 'custom_status_updates'],
 'year': ['year', 'monitoring_year', 'review_year', 'academic_year'],
 'review_year': ['year', 'monitoring_year', 'review_year'],
 'department': ['department', 'custom_department', 'department_name'],
 'owner': ['owner', 'assigned_to', 'responsible']}

CONFIG = {'1.1.1': {'sources': ['oversight',
                       'stakeholder_registry',
                       'stakeholder_engagement',
                       'policy_control',
                       'esg_strategy',
                       'esg_tracker',
                       'business_impact',
                       'risk_register',
                       'management_review',
                       'quality_action'],
           'metrics': [{'id': 'c111-oversight',
                        'label': 'Oversight records in scope',
                        'source': 'oversight',
                        'mode': 'all'},
                       {'id': 'c111-active-oversight',
                        'label': 'Active or approved oversight records',
                        'source': 'oversight',
                        'mode': 'in',
                        'field': ['status', 'review_status'],
                        'values': ['Active', 'Approved', 'Completed']},
                       {'id': 'c111-stakeholders',
                        'label': 'Stakeholders in the registry',
                        'source': 'stakeholder_registry',
                        'mode': 'all'},
                       {'id': 'c111-engagements',
                        'label': 'Stakeholder engagement records',
                        'source': 'stakeholder_engagement',
                        'mode': 'all'},
                       {'id': 'c111-policies',
                        'label': 'Controlled policies and standards',
                        'source': 'policy_control',
                        'mode': 'all'},
                       {'id': 'c111-overdue-policy-review',
                        'label': 'Policies overdue for review',
                        'source': 'policy_control',
                        'mode': 'date_before_today',
                        'field': ['next_review_date', 'review_date']},
                       {'id': 'c111-esg-strategies',
                        'label': 'ESG strategy records',
                        'source': 'esg_strategy',
                        'mode': 'all'},
                       {'id': 'c111-esg-initiatives',
                        'label': 'ESG initiatives tracked',
                        'source': 'esg_tracker',
                        'mode': 'all'},
                       {'id': 'c111-business-impact',
                        'label': 'Business impact assessments',
                        'source': 'business_impact',
                        'mode': 'all'},
                       {'id': 'c111-risks',
                        'label': 'Governance risks in scope',
                        'source': 'risk_register',
                        'mode': 'all'},
                       {'id': 'c111-high-risks',
                        'label': 'High or critical governance risks',
                        'source': 'risk_register',
                        'mode': 'in',
                        'field': ['risk_level'],
                        'values': ['High', 'Critical', 'Very High']},
                       {'id': 'c111-management-reviews',
                        'label': 'Management reviews',
                        'source': 'management_review',
                        'mode': 'all'},
                       {'id': 'c111-quality-actions',
                        'label': 'Governance-related Quality Actions',
                        'source': 'quality_action',
                        'mode': 'all'},
                       {'id': 'c111-committee-composition',
                        'label': 'Governance committee composition coverage',
                        'source': 'oversight',
                        'mode': 'unsupported',
                        'message': 'Committee member child-table definitions were not supplied.'}]},
 '1.2.1': {'sources': ['quality_goal',
                       'staff_goal',
                       'appraisal',
                       'management_review',
                       'quality_action',
                       'risk_register',
                       'business_impact'],
           'metrics': [{'id': 'c121-quality-goals',
                        'label': 'Quality Goals in scope',
                        'source': 'quality_goal',
                        'mode': 'all'},
                       {'id': 'c121-goals-defined',
                        'label': 'Quality Goals with a defined goal',
                        'source': 'quality_goal',
                        'mode': 'truthy',
                        'field': ['goal']},
                       {'id': 'c121-staff-goals',
                        'label': 'Staff Goals in scope',
                        'source': 'staff_goal',
                        'mode': 'all'},
                       {'id': 'c121-staff-goals-on-track',
                        'label': 'Staff Goals in progress or completed',
                        'source': 'staff_goal',
                        'mode': 'in',
                        'field': ['status'],
                        'values': ['In Progress', 'Completed', 'Closed']},
                       {'id': 'c121-appraisals', 'label': 'Appraisal records', 'source': 'appraisal', 'mode': 'all'},
                       {'id': 'c121-management-reviews',
                        'label': 'Management Reviews',
                        'source': 'management_review',
                        'mode': 'all'},
                       {'id': 'c121-completed-reviews',
                        'label': 'Completed Management Reviews',
                        'source': 'management_review',
                        'mode': 'equals',
                        'field': ['review_status', 'status'],
                        'value': 'Completed'},
                       {'id': 'c121-quality-actions',
                        'label': 'Strategic Quality Actions',
                        'source': 'quality_action',
                        'mode': 'all'},
                       {'id': 'c121-overdue-actions',
                        'label': 'Overdue strategic Quality Actions',
                        'source': 'quality_action',
                        'mode': 'conditions',
                        'conditions': [{'field': ['custom_proposed_date', 'target_date'], 'op': 'date_before_today'},
                                       {'field': ['custom_status_updates', 'status'],
                                        'op': 'not_in',
                                        'values': ['Completed', 'Closed']}]},
                       {'id': 'c121-risks',
                        'label': 'Strategic risks and opportunities',
                        'source': 'risk_register',
                        'mode': 'all'},
                       {'id': 'c121-business-impact',
                        'label': 'Business impact assessments',
                        'source': 'business_impact',
                        'mode': 'all'},
                       {'id': 'c121-kpi-achievement',
                        'label': 'KPI and KRA achievement',
                        'source': 'quality_goal',
                        'mode': 'unsupported',
                        'message': 'Quality Goal-to-KRA aggregation and approved achievement thresholds were not supplied.'}]}}

QUESTION_REGISTRY = {'1.1.1': [{'id': 'q111-1',
            'question': 'How many governance oversight records are in scope?',
            'metric_id': 'c111-oversight'},
           {'id': 'q111-2',
            'question': 'How many controlled policies are overdue for review?',
            'metric_id': 'c111-overdue-policy-review'},
           {'id': 'q111-3', 'question': 'How many stakeholders are recorded?', 'metric_id': 'c111-stakeholders'},
           {'id': 'q111-4',
            'question': 'How many high or critical governance risks are open?',
            'metric_id': 'c111-high-risks'}],
 '1.2.1': [{'id': 'q121-1', 'question': 'How many Quality Goals are defined?', 'metric_id': 'c121-goals-defined'},
           {'id': 'q121-2',
            'question': 'How many Staff Goals are in progress or completed?',
            'metric_id': 'c121-staff-goals-on-track'},
           {'id': 'q121-3',
            'question': 'How many Management Reviews are completed?',
            'metric_id': 'c121-completed-reviews'},
           {'id': 'q121-4',
            'question': 'How many strategic Quality Actions are overdue?',
            'metric_id': 'c121-overdue-actions'}]}

EXCEPTION_METRIC_IDS = ['c111-overdue-policy-review',
 'c111-high-risks',
 'c111-committee-composition',
 'c121-overdue-actions',
 'c121-kpi-achievement']

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
    frappe.throw("Unsupported Criterion 1 subcriterion.")

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
        "api_method": "ucc_analytics_criterion_1",
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
    "warnings": ['Criterion 1 source availability depends on site-installed UCC custom DocTypes.',
 'Unsupported committee and KPI calculations remain explicit until child-table rules are supplied.']
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
        frappe.throw("Unknown Criterion 1 metric.")
    result["drilldown"] = evaluate_metric(selected_config, True)

frappe.response["message"] = result
