"""
UCC Intelligence Platform Server Script

Visible name:
    UCC Ask - Quality Action

Script type:
    API

API method:
    ucc_ask_quality_action

Deployment:
    Paste this entire file into one Frappe Server Script.
    Allow Guest must remain disabled.

Source:
    Part of UCC Intelligence Platform v1.1.0.

Important:
    This script is self-contained because Frappe Server Scripts are not treated
    as a normal importable Python package.
"""

# Frappe Server Script
# Script Type: API
# API Method: ucc_ask_quality_action
#
# Module: Quality Action
#
# Purpose:
# Provides a guided view of Quality Actions, resolution rows, ownership, due dates, actions and closure.
#
# Design principles:
# - ERPNext remains the factual source of truth.
# - Deterministic rules handle dates, status, counts and filters.
# - AI may assist with interpretation or drafting where enabled.
# - Missing data is reported clearly and is never guessed.

AGENT_VERSION = "1.1.0"
AGENT_BUILD = "UCC Ask - Quality Action V1.1.0"


def clean_text(value):
    if value is None:
        return ""

    return str(value).replace("\n", " ").replace("\r", " ").strip()


def normalise(value):
    return " ".join(
        clean_text(value)
        .lower()
        .replace("’", "'")
        .replace("‘", "'")
        .replace("'", " ")
        .replace("-", " ")
        .replace("_", " ")
        .split()
    )


def strip_html(value):
    text = clean_text(value)

    for token in [
        "<p>", "</p>", "<div>", "</div>", "<br>", "<br/>", "<br />",
        "<ul>", "</ul>", "<ol>", "</ol>", "<li>", "</li>",
        "<strong>", "</strong>", "<b>", "</b>", "<em>", "</em>",
        "<i>", "</i>", "&nbsp;"
    ]:
        text = text.replace(token, " ")

    while "<" in text and ">" in text:
        start = text.find("<")
        end = text.find(">", start)

        if start < 0 or end < 0:
            break

        text = text[:start] + " " + text[end + 1:]

    return " ".join(text.split())


def safe_db_list(doctype, filters=None, fields=None, order_by=None, limit=5000):
    try:
        return frappe.db.get_list(
            doctype,
            filters=filters or {},
            fields=fields or ["name"],
            order_by=order_by or "modified desc",
            limit_page_length=limit
        ) or []
    except Exception:
        return []


def safe_get_doc(doctype, name):
    try:
        return frappe.get_doc(doctype, name)
    except Exception:
        return None


def first_value(doc, fields):
    for fieldname in fields:
        try:
            value = doc.get(fieldname)
        except Exception:
            value = None

        if value not in [None, ""]:
            return value

    return None


def format_date(value):
    if not value:
        return "Not recorded"

    try:
        return frappe.utils.formatdate(value, "dd MMM yyyy")
    except Exception:
        return clean_text(value)


def iso_date(value):
    if not value:
        return ""

    try:
        return clean_text(frappe.utils.getdate(value))
    except Exception:
        return clean_text(value)[:10]


def link_cell(text, doctype, name):
    return {
        "text": clean_text(text) or clean_text(name),
        "doctype": doctype,
        "name": clean_text(name)
    }


def source(label, doctype, name):
    return {
        "label": label,
        "doctype": doctype,
        "name": clean_text(name)
    }


def response_base(answer, visuals=None, warnings=None, sources=None, confidence="Confirmed"):
    return {
        "status": "ok",
        "answer": answer,
        "visuals": visuals or [],
        "warnings": warnings or [],
        "sources": sources or [],
        "confidence": confidence,
        "ai_used": False,
        "version": AGENT_VERSION,
        "build": AGENT_BUILD
    }


def quality_action_title(doc):
    return clean_text(
        first_value(
            doc,
            [
                "custom_subject", "subject", "title",
                "action_name", "quality_action_name"
            ]
        )
    ) or clean_text(doc.get("name"))


def find_resolution_field():
    try:
        meta = frappe.get_meta("Quality Action")
    except Exception:
        return ""

    for field in meta.fields or []:
        if (
            clean_text(field.fieldtype) == "Table"
            and clean_text(field.options) == "Quality Action Resolution"
        ):
            return clean_text(field.fieldname)

    return ""


def resolution_rows(doc):
    fieldname = find_resolution_field()

    if fieldname:
        try:
            return doc.get(fieldname) or []
        except Exception:
            pass

    # Safe fallbacks for likely fieldnames.
    for candidate in [
        "resolutions", "resolution", "quality_action_resolution",
        "quality_action_resolutions", "action_resolution"
    ]:
        try:
            rows = doc.get(candidate) or []
        except Exception:
            rows = []

        if rows:
            return rows

    return []


def row_status(row):
    return clean_text(row.get("status")) or "Not recorded"


def row_is_completed(row):
    return (
        normalise(row_status(row)) == "completed"
        or bool(row.get("completion_by"))
    )


def row_is_overdue(row):
    target = iso_date(row.get("target_date"))

    if not target or row_is_completed(row):
        return False

    today = iso_date(frappe.utils.today())
    return bool(today and target < today)


def row_owner(row):
    return clean_text(row.get("full_name") or row.get("responsible")) or "Not assigned"


def resolution_summary_rows(doc):
    output = []

    for index, row in enumerate(resolution_rows(doc), 1):
        output.append([
            index,
            clean_text(row.get("finding_type")) or "Not recorded",
            row_status(row),
            row_owner(row),
            format_date(row.get("target_date")),
            format_date(row.get("completion_by")),
            "Yes" if row_is_overdue(row) else "No",
            strip_html(row.get("problem")) or "Not recorded"
        ])

    return output


def detect_intent(question):
    q = normalise(question)

    if any(term in q for term in [
        "all open quality actions", "show open quality actions",
        "open quality actions", "all open actions"
    ]):
        return "global_open"

    if any(term in q for term in [
        "all overdue quality actions", "show overdue quality actions",
        "overdue quality actions", "overdue actions"
    ]):
        return "global_overdue"

    if any(term in q for term in [
        "show nc findings", "all nc findings", "nonconformity findings",
        "non conformity findings"
    ]):
        return "global_nc"

    if any(term in q for term in [
        "show ofi findings", "all ofi findings",
        "opportunities for improvement"
    ]):
        return "global_ofi"

    if any(term in q for term in [
        "ready for closure", "closure readiness",
        "can this be closed", "should this be closed"
    ]):
        return "closure"

    if any(term in q for term in [
        "ai review", "review the quality", "review root cause",
        "assess root cause", "assess action", "quality review"
    ]):
        return "review"

    if any(term in q for term in [
        "root cause", "resolution plan", "root cause and resolution"
    ]):
        return "resolution"

    if any(term in q for term in [
        "action taken", "what action", "progress made"
    ]):
        return "action_taken"

    if any(term in q for term in [
        "who is assigned", "assigned to", "responsible"
    ]):
        return "assigned"

    if any(term in q for term in [
        "is it overdue", "due date", "when is it due", "target completion"
    ]):
        return "due"

    if any(term in q for term in [
        "current status", "what is the status", "status"
    ]):
        return "status"

    if any(term in q for term in [
        "what is the problem", "show the problem", "finding summary",
        "what happened"
    ]):
        return "problem"

    if any(term in q for term in [
        "show this quality action", "quality action details",
        "complete quality action", "full quality action"
    ]):
        return "profile"

    return "profile"


def find_quality_action(selected_name, question):
    if selected_name:
        doc = safe_get_doc("Quality Action", selected_name)

        if doc:
            return {"status": "ok", "doc": doc}

    rows = safe_db_list(
        "Quality Action",
        fields=["name", "custom_subject", "modified"],
        order_by="modified desc",
        limit=2000
    )
    q = normalise(question)
    matches = []

    for row in rows:
        searchable = normalise(
            clean_text(row.get("name"))
            + " "
            + clean_text(row.get("custom_subject"))
        )

        if q and q in searchable:
            matches.append(row)
            continue

        tokens = [token for token in q.split() if len(token) >= 3]

        if tokens and all(token in searchable for token in tokens):
            matches.append(row)

    if len(matches) == 1:
        return {
            "status": "ok",
            "doc": safe_get_doc("Quality Action", matches[0].get("name"))
        }

    if len(matches) > 1:
        return {"status": "choose", "candidates": matches[:20]}

    return {"status": "required"}


def all_quality_actions():
    rows = safe_db_list(
        "Quality Action",
        fields=["name", "custom_subject", "modified"],
        order_by="modified desc",
        limit=5000
    )
    output = []

    for row in rows:
        doc = safe_get_doc("Quality Action", row.get("name"))

        if doc:
            output.append(doc)

    return output


def global_rows(mode):
    rows = []

    for doc in all_quality_actions():
        for index, item in enumerate(resolution_rows(doc), 1):
            finding_type = clean_text(item.get("finding_type"))
            status = row_status(item)
            include = False

            if mode == "global_open":
                include = not row_is_completed(item)
            elif mode == "global_overdue":
                include = row_is_overdue(item)
            elif mode == "global_nc":
                include = normalise(finding_type) in [
                    "nc", "min nc", "maj nc"
                ]
            elif mode == "global_ofi":
                include = normalise(finding_type) == "ofi"

            if include:
                rows.append([
                    link_cell(doc.get("name"), "Quality Action", doc.get("name")),
                    quality_action_title(doc),
                    index,
                    finding_type or "Not recorded",
                    status,
                    row_owner(item),
                    format_date(item.get("target_date")),
                    "Yes" if row_is_overdue(item) else "No",
                    strip_html(item.get("problem")) or "Not recorded"
                ])

    return rows


def handle_global(mode):
    rows = global_rows(mode)
    labels = {
        "global_open": "open",
        "global_overdue": "overdue",
        "global_nc": "NC",
        "global_ofi": "OFI"
    }
    label = labels.get(mode, "matching")

    return response_base(
        str(len(rows)) + " " + label + " Quality Action resolution row(s) found.",
        visuals=[
            {
                "type": "table",
                "title": label.title() + " Quality Actions",
                "columns": [
                    "Quality Action", "Subject", "Row", "Finding Type",
                    "Status", "Assigned To", "Target Date", "Overdue",
                    "Problem"
                ],
                "rows": rows
            }
        ],
        sources=[],
        confidence="Confirmed"
    )


def handle_profile(doc):
    rows = resolution_summary_rows(doc)
    open_count = 0
    completed_count = 0
    overdue_count = 0

    for item in resolution_rows(doc):
        if row_is_completed(item):
            completed_count = completed_count + 1
        else:
            open_count = open_count + 1

        if row_is_overdue(item):
            overdue_count = overdue_count + 1

    return response_base(
        quality_action_title(doc)
        + " contains "
        + str(len(rows))
        + " resolution row(s): "
        + str(open_count)
        + " open, "
        + str(completed_count)
        + " completed and "
        + str(overdue_count)
        + " overdue.",
        visuals=[
            {
                "type": "summary",
                "title": "Quality Action overview",
                "items": [
                    {
                        "label": "Quality Action",
                        "value": link_cell(
                            doc.get("name"),
                            "Quality Action",
                            doc.get("name")
                        )
                    },
                    {
                        "label": "Subject",
                        "value": quality_action_title(doc)
                    },
                    {"label": "Resolution Rows", "value": len(rows)},
                    {"label": "Open", "value": open_count},
                    {"label": "Completed", "value": completed_count},
                    {"label": "Overdue", "value": overdue_count}
                ]
            },
            {
                "type": "table",
                "title": "Resolution rows",
                "columns": [
                    "Row", "Finding Type", "Status", "Assigned To",
                    "Target Date", "Completed On", "Overdue", "Problem"
                ],
                "rows": rows
            }
        ],
        sources=[
            source("Quality Action", "Quality Action", doc.get("name"))
        ]
    )


def detail_rows(doc, fieldname, title):
    rows = []

    for index, row in enumerate(resolution_rows(doc), 1):
        rows.append([
            index,
            clean_text(row.get("finding_type")) or "Not recorded",
            row_status(row),
            row_owner(row),
            strip_html(row.get(fieldname)) or "Not recorded"
        ])

    return response_base(
        title + " for " + quality_action_title(doc) + ".",
        visuals=[
            {
                "type": "table",
                "title": title,
                "columns": [
                    "Row", "Finding Type", "Status", "Assigned To", title
                ],
                "rows": rows
            }
        ],
        sources=[
            source("Quality Action", "Quality Action", doc.get("name"))
        ]
    )


def handle_status(doc):
    rows = []

    for index, row in enumerate(resolution_rows(doc), 1):
        rows.append([
            index,
            clean_text(row.get("finding_type")) or "Not recorded",
            row_status(row),
            row_owner(row),
            format_date(row.get("target_date")),
            format_date(row.get("completion_by")),
            "Yes" if row_is_overdue(row) else "No"
        ])

    return response_base(
        "Current status for " + quality_action_title(doc) + ".",
        visuals=[
            {
                "type": "table",
                "title": "Resolution status",
                "columns": [
                    "Row", "Finding Type", "Status", "Assigned To",
                    "Target Date", "Completed On", "Overdue"
                ],
                "rows": rows
            }
        ],
        sources=[
            source("Quality Action", "Quality Action", doc.get("name"))
        ]
    )


def handle_assigned(doc):
    rows = []

    for index, row in enumerate(resolution_rows(doc), 1):
        rows.append([
            index,
            row_owner(row),
            row_status(row),
            clean_text(row.get("finding_type")) or "Not recorded",
            format_date(row.get("target_date")),
            strip_html(row.get("problem")) or "Not recorded"
        ])

    return response_base(
        "Assignment details for " + quality_action_title(doc) + ".",
        visuals=[
            {
                "type": "table",
                "title": "Assigned resolutions",
                "columns": [
                    "Row", "Assigned To", "Status", "Finding Type",
                    "Target Date", "Problem"
                ],
                "rows": rows
            }
        ],
        sources=[
            source("Quality Action", "Quality Action", doc.get("name"))
        ]
    )


def handle_due(doc):
    rows = []

    for index, row in enumerate(resolution_rows(doc), 1):
        rows.append([
            index,
            row_status(row),
            row_owner(row),
            format_date(row.get("target_date")),
            format_date(row.get("completion_by")),
            "Yes" if row_is_overdue(row) else "No"
        ])

    overdue = len([row for row in resolution_rows(doc) if row_is_overdue(row)])

    return response_base(
        str(overdue)
        + " resolution row(s) are overdue for "
        + quality_action_title(doc)
        + ".",
        visuals=[
            {
                "type": "table",
                "title": "Due dates",
                "columns": [
                    "Row", "Status", "Assigned To", "Target Date",
                    "Completed On", "Overdue"
                ],
                "rows": rows
            }
        ],
        sources=[
            source("Quality Action", "Quality Action", doc.get("name"))
        ]
    )


def root_cause_review(text):
    value = strip_html(text)
    q = normalise(value)
    issues = []

    if not value:
        issues.append("Root cause and resolution are missing.")
        return issues

    if len(value) < 80:
        issues.append("Root cause and resolution are very brief.")

    causal_terms = [
        "because", "due to", "caused by", "root cause",
        "lack of", "failure to", "insufficient", "inadequate"
    ]

    if not any(term in q for term in causal_terms):
        issues.append(
            "The text does not clearly distinguish the underlying cause from the symptom."
        )

    action_terms = [
        "implement", "update", "revise", "train", "monitor",
        "review", "create", "configure", "approve", "verify"
    ]

    if not any(term in q for term in action_terms):
        issues.append("The resolution plan does not contain a clear corrective step.")

    recurrence_terms = [
        "prevent recurrence", "recurrence", "ongoing monitoring",
        "periodic review", "control", "verification"
    ]

    if not any(term in q for term in recurrence_terms):
        issues.append("Recurrence-prevention or ongoing control is not explicit.")

    return issues


def action_review(text):
    value = strip_html(text)
    q = normalise(value)
    issues = []

    if not value:
        issues.append("Action taken is missing.")
        return issues

    if len(value) < 50:
        issues.append("Action taken is too brief to demonstrate implementation.")

    evidence_terms = [
        "attached", "evidence", "record", "screenshot", "approved",
        "completed", "updated", "implemented", "verified"
    ]

    if not any(term in q for term in evidence_terms):
        issues.append("Implementation evidence or an identifiable record is not mentioned.")

    return issues


def closure_assessment(doc):
    rows = []
    ready_count = 0

    for index, row in enumerate(resolution_rows(doc), 1):
        reasons = []

        if not row_is_completed(row):
            reasons.append("Status is not completed.")

        if not row.get("completion_by"):
            reasons.append("Completed On is missing.")

        reasons.extend(root_cause_review(row.get("resolution")))
        reasons.extend(action_review(row.get("action_taken")))

        ready = len(reasons) == 0

        if ready:
            ready_count = ready_count + 1

        rows.append([
            index,
            clean_text(row.get("finding_type")) or "Not recorded",
            row_status(row),
            "Ready" if ready else "Not ready",
            "; ".join(reasons) if reasons else "No rule-based gap identified"
        ])

    total = len(rows)

    return response_base(
        str(ready_count)
        + " of "
        + str(total)
        + " resolution row(s) appear ready for closure based on recorded status, completion date, root cause and action taken.",
        visuals=[
            {
                "type": "table",
                "title": "Closure readiness review",
                "columns": [
                    "Row", "Finding Type", "Status",
                    "Closure Readiness", "Reason"
                ],
                "rows": rows
            }
        ],
        warnings=[
            "This is a rule-based readiness check. Formal closure still requires authorised verification and supporting evidence."
        ],
        sources=[
            source("Quality Action", "Quality Action", doc.get("name"))
        ],
        confidence="Partial"
    )


def quality_review(doc):
    rows = []

    for index, row in enumerate(resolution_rows(doc), 1):
        root_issues = root_cause_review(row.get("resolution"))
        action_issues = action_review(row.get("action_taken"))
        issues = root_issues + action_issues

        rows.append([
            index,
            clean_text(row.get("finding_type")) or "Not recorded",
            row_status(row),
            "Adequate" if not issues else "Needs improvement",
            "; ".join(issues) if issues else "No rule-based wording gap identified"
        ])

    return response_base(
        "Rule-based quality review completed for "
        + quality_action_title(doc)
        + ".",
        visuals=[
            {
                "type": "table",
                "title": "Root cause and action adequacy",
                "columns": [
                    "Row", "Finding Type", "Status",
                    "Review Result", "Review Notes"
                ],
                "rows": rows
            }
        ],
        warnings=[
            "This review analyses completeness and wording patterns. It does not replace management judgement or evidence verification."
        ],
        sources=[
            source("Quality Action", "Quality Action", doc.get("name"))
        ],
        confidence="Partial"
    )


question = clean_text(frappe.form_dict.get("question"))
selected_quality_action = clean_text(
    frappe.form_dict.get("quality_action")
)

if not question:
    frappe.response["message"] = response_base(
        "Please enter a question.",
        confidence="Not applicable"
    )
else:
    intent = detect_intent(question)

    if intent in [
        "global_open", "global_overdue",
        "global_nc", "global_ofi"
    ]:
        frappe.response["message"] = handle_global(intent)
    else:
        match = find_quality_action(
            selected_quality_action,
            question
        )

        if match.get("status") == "required":
            frappe.response["message"] = {
                "status": "student_required",
                "answer": "Please select a Quality Action or include its record ID or subject.",
                "visuals": [],
                "sources": [],
                "warnings": [],
                "ai_used": False
            }
        elif match.get("status") == "choose":
            frappe.response["message"] = {
                "status": "choose_student",
                "answer": "More than one Quality Action matches. Select the correct record.",
                "candidates": [
                    {
                        "student_applicant": row.get("name"),
                        "student_name": row.get("custom_subject") or row.get("name"),
                        "course": "Quality Action"
                    }
                    for row in match.get("candidates") or []
                ],
                "visuals": [],
                "sources": [],
                "warnings": [],
                "ai_used": False
            }
        else:
            doc = match.get("doc")

            if intent == "problem":
                result = detail_rows(doc, "problem", "Problem")
            elif intent == "resolution":
                result = detail_rows(
                    doc,
                    "resolution",
                    "Root Cause & Resolution"
                )
            elif intent == "action_taken":
                result = detail_rows(
                    doc,
                    "action_taken",
                    "Action Taken"
                )
            elif intent == "assigned":
                result = handle_assigned(doc)
            elif intent == "due":
                result = handle_due(doc)
            elif intent == "status":
                result = handle_status(doc)
            elif intent == "closure":
                result = closure_assessment(doc)
            elif intent == "review":
                result = quality_review(doc)
            else:
                result = handle_profile(doc)

            frappe.response["message"] = result
