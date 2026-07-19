"""
UCC Intelligence Platform Server Script

Visible name:
    UCC Ask - Recruitment Agent

Script type:
    API

API method:
    ucc_ask_recruitment_agent

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
# API Method: ucc_ask_recruitment_agent
#
# Module: Recruitment Agent
#
# Purpose:
# Provides a guided view of agent contracts, ratings, recruited students, revenue, commission and renewal.
#
# Design principles:
# - ERPNext remains the factual source of truth.
# - Deterministic rules handle dates, status, counts and filters.
# - AI may assist with interpretation or drafting where enabled.
# - Missing data is reported clearly and is never guessed.

AGENT_VERSION = "1.1.0"
AGENT_BUILD = "UCC Ask - Recruitment Agent V1.1.0"


def clean_text(value):
    return " ".join(str(value or "").strip().split())


def normalise(value):
    text = clean_text(value).lower()

    for character in [
        ",", ".", "'", '"', "(", ")", "[", "]",
        "{", "}", "-", "_", "/", "?", "!", ":", ";"
    ]:
        text = text.replace(character, " ")

    return " ".join(text.split())


def format_date(value):
    text = clean_text(value)

    if not text:
        return "Not recorded"

    try:
        return frappe.utils.formatdate(text, "dd MMM yyyy")
    except Exception:
        return text


def iso_date(value):
    text = clean_text(value)

    if not text:
        return ""

    return text[:10]


def safe_db_list(doctype, filters=None, fields=None, order_by=None, limit=500):
    try:
        return frappe.db.get_list(
            doctype,
            filters=filters or {},
            fields=fields or ["name"],
            order_by=order_by,
            limit_page_length=limit
        ) or []
    except Exception:
        return []


def safe_get_doc(doctype, name):
    if not name:
        return None

    try:
        return frappe.get_doc(doctype, name)
    except Exception:
        return None


def first_value(record, fieldnames):
    for fieldname in fieldnames:
        try:
            value = record.get(fieldname)
        except Exception:
            value = None

        if value not in [None, ""]:
            return value

    return None



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
        "name": name
    }


def response_base(
    answer,
    visuals=None,
    sources=None,
    warnings=None,
    confidence="Confirmed"
):
    return {
        "status": "ok",
        "answer": answer,
        "visuals": visuals or [],
        "sources": sources or [],
        "warnings": warnings or [],
        "confidence": confidence,
        "ai_used": False,
        "agent_version": AGENT_VERSION
    }


def contract_name(contract):
    return clean_text(
        first_value(
            contract,
            ["party_name", "agent_name", "company_name", "supplier_name"]
        )
    ) or clean_text(contract.get("name"))


def detect_intent(question):
    q = normalise(question)

    if any(term in q for term in [
        "complete journey",
        "agent s complete journey",
        "agent complete journey",
        "how this agent s complete journey",
        "show this agent s journey"
    ]):
        return "journey"

    if any(term in q for term in [
        "latest contract",
        "show this agent s latest contract",
        "most recent contract"
    ]):
        return "latest_contract"

    if any(term in q for term in [
        "compliance issues",
        "compliance issue",
        "show this agent s compliance",
        "non compliance",
        "noncompliance"
    ]):
        return "compliance"

    if any(term in q for term in [
        "commission status",
        "show this agent s commission",
        "commission"
    ]):
        return "commission"

    if any(term in q for term in [
        "how many students",
        "students did this agent recruit",
        "students recruited",
        "recruitment list",
        "show students recruited"
    ]):
        return "students"

    if any(term in q for term in [
        "does this agent meet the minimum rating",
        "meet the minimum rating",
        "rating threshold",
        "minimum rating"
    ]):
        return "rating_threshold"

    if any(term in q for term in [
        "latest rating",
        "what is this agent s latest rating",
        "provider rating",
        "rating history"
    ]):
        return "rating"

    if any(term in q for term in [
        "how many recruitment agents",
        "how many active agents",
        "active agents",
        "active contracts"
    ]):
        return "active_count"

    if any(term in q for term in [
        "expiring soon",
        "which contracts are expiring"
    ]):
        return "expiring"

    if "revenue" in q:
        return "finance"

    if any(term in q for term in [
        "renewed", "renewal", "should this agent s contract be renewed",
        "risk summary"
    ]):
        return "renewal"

    if any(term in q for term in [
        "expire", "expiry", "contract dates", "contract status", "active"
    ]):
        return "contract"

    if "journey" in q:
        return "journey"

    if any(term in q for term in ["profile", "agent", "company"]):
        return "profile"

    return "unsupported"
def find_contract(selected_contract, question):
    if selected_contract:
        doc = safe_get_doc("Agent Contract", selected_contract)

        if doc:
            return {
                "status": "ok",
                "contract": doc
            }

    rows = safe_db_list(
        "Agent Contract",
        fields=["name", "party_name", "personal_id"],
        order_by="modified desc",
        limit=1000
    )

    q = normalise(question)
    matches = []

    for row in rows:
        searchable = normalise(
            clean_text(row.get("name"))
            + " "
            + clean_text(row.get("party_name"))
            + " "
            + clean_text(row.get("personal_id"))
        )

        if q and q in searchable:
            matches.append(row)
            continue

        tokens = q.split()
        if tokens and all(token in searchable for token in tokens):
            matches.append(row)

    if len(matches) == 1:
        doc = safe_get_doc("Agent Contract", matches[0].get("name"))
        return {
            "status": "ok",
            "contract": doc
        }

    if len(matches) > 1:
        return {
            "status": "choose",
            "candidates": matches[:20]
        }

    return {
        "status": "required"
    }


def contract_dates(contract):
    start_date = first_value(
        contract,
        [
            "commencement_date", "start_date", "contract_start_date",
            "posting_date", "effective_date"
        ]
    )
    end_date = first_value(
        contract,
        [
            "end_date", "expiry_date", "contract_end_date",
            "expiration_date", "valid_till"
        ]
    )

    return {
        "start": iso_date(start_date),
        "end": iso_date(end_date)
    }


def contract_status(contract):
    dates = contract_dates(contract)
    today = iso_date(frappe.utils.today())

    if dates.get("end") and dates.get("end") < today:
        return "Expired"

    if dates.get("start") and dates.get("start") > today:
        return "Not started"

    if dates.get("start") or dates.get("end"):
        return "Active"

    return clean_text(
        first_value(
            contract,
            ["status", "workflow_state", "contract_status"]
        )
    ) or "Not recorded"


def handle_profile(contract):
    name = contract_name(contract)
    dates = contract_dates(contract)

    items = [
        {"label": "Recruitment Agent", "value": name},
        {"label": "Agent Contract", "value": contract.get("name")},
        {
            "label": "Personal ID / UEN / Company ID",
            "value": first_value(
                contract,
                ["personal_id", "uen", "company_id", "registration_number"]
            ) or "Not recorded"
        },
        {"label": "Contract Status", "value": contract_status(contract)},
        {"label": "Commencement", "value": format_date(dates.get("start"))},
        {"label": "Expiry", "value": format_date(dates.get("end"))}
    ]

    return response_base(
        name + " has an Agent Contract record in ERPNext.",
        visuals=[
            {
                "type": "summary",
                "title": "Recruitment agent profile",
                "items": items
            }
        ],
        sources=[source("Agent Contract", "Agent Contract", contract.get("name"))]
    )


def handle_contract(contract):
    name = contract_name(contract)
    dates = contract_dates(contract)
    status = contract_status(contract)

    answer = (
        name
        + "'s contract status is "
        + status
        + ". Commencement: "
        + format_date(dates.get("start"))
        + ". Expiry: "
        + format_date(dates.get("end"))
        + "."
    )

    return response_base(
        answer,
        visuals=[
            {
                "type": "summary",
                "title": "Contract details",
                "items": [
                    {"label": "Agent", "value": name},
                    {"label": "Status", "value": status},
                    {"label": "Commencement", "value": format_date(dates.get("start"))},
                    {"label": "Expiry", "value": format_date(dates.get("end"))}
                ]
            }
        ],
        sources=[source("Agent Contract", "Agent Contract", contract.get("name"))]
    )


def all_contracts_for_agent(contract):
    identities = agent_identity_values(contract)
    rows = safe_db_list(
        "Agent Contract",
        fields=["name", "party_name", "personal_id", "modified"],
        order_by="modified desc",
        limit=1000
    )
    output = []

    for row in rows:
        searchable = normalise(
            clean_text(row.get("party_name"))
            + " "
            + clean_text(row.get("personal_id"))
            + " "
            + clean_text(row.get("name"))
        )

        matched = False

        for identity in identities:
            identity_text = normalise(identity)

            if identity_text and identity_text in searchable:
                matched = True
                break

        if matched:
            doc = safe_get_doc("Agent Contract", row.get("name"))
            if doc:
                output.append(doc)

    if not output:
        output.append(contract)

    return output


def latest_contract_for_agent(contract):
    contracts = all_contracts_for_agent(contract)

    if contracts:
        return contracts[0]

    return contract


def handle_latest_contract(contract):
    latest = latest_contract_for_agent(contract)
    dates = contract_dates(latest)

    return response_base(
        "The latest Agent Contract for "
        + contract_name(latest)
        + " is "
        + clean_text(latest.get("name"))
        + ". It is "
        + contract_status(latest)
        + ", from "
        + format_date(dates.get("start"))
        + " to "
        + format_date(dates.get("end"))
        + ".",
        visuals=[
            {
                "type": "summary",
                "title": "Latest agent contract",
                "items": [
                    {
                        "label": "Contract",
                        "value": link_cell(
                            latest.get("name"),
                            "Agent Contract",
                            latest.get("name")
                        )
                    },
                    {
                        "label": "Status",
                        "value": contract_status(latest)
                    },
                    {
                        "label": "Commencement",
                        "value": format_date(dates.get("start"))
                    },
                    {
                        "label": "Expiry",
                        "value": format_date(dates.get("end"))
                    }
                ]
            }
        ],
        sources=[
            source(
                "Agent Contract",
                "Agent Contract",
                latest.get("name")
            )
        ]
    )


def handle_journey(contract):
    contracts = all_contracts_for_agent(contract)
    ratings = rating_rows(contract)
    source_matches = student_recruitment_sources(contract)
    people = normalise_recruited_people(source_matches)
    direct_invoices = direct_invoice_matches(contract).get("rows") or []

    timeline_rows = []

    for item in contracts:
        dates = contract_dates(item)
        timeline_rows.append([
            "Contract",
            link_cell(
                item.get("name"),
                "Agent Contract",
                item.get("name")
            ),
            format_date(dates.get("start")),
            format_date(dates.get("end")),
            contract_status(item)
        ])

    for item in ratings:
        values = rating_values(item)
        timeline_rows.append([
            "Rating",
            link_cell(
                item.get("name"),
                "Supplier Rating",
                item.get("name")
            ),
            format_date(item.get("modified")),
            values.get("evaluation_stage") or "Not recorded",
            (
                "Rating "
                + clean_text(values.get("rating") or "Not recorded")
                + " / Likert "
                + clean_text(values.get("rating_likert") or "Not recorded")
            )
        ])

    warnings = []

    if not people:
        warnings.append(
            "No recruited-student link was found in the currently checked student and admission DocTypes."
        )

    if not direct_invoices:
        warnings.append(
            "No direct Sales Invoice agent link was found. Revenue may still require another DocType or report."
        )

    return response_base(
        "Complete recorded journey for "
        + contract_name(contract)
        + ": "
        + str(len(contracts))
        + " contract record(s), "
        + str(len(ratings))
        + " rating record(s), "
        + str(len(people))
        + " unique recruited-student record(s), and Agent master "
        + (
            agent_master_id(contract)
            if agent_master_id(contract)
            else "not resolved"
        )
        + ".",
        visuals=[
            {
                "type": "table",
                "title": "Agent journey timeline",
                "columns": [
                    "Record Type", "Record", "Date / Start",
                    "End / Stage", "Outcome"
                ],
                "rows": timeline_rows
            },
            {
                "type": "summary",
                "title": "Journey summary",
                "items": [
                    {
                        "label": "Current Contract Status",
                        "value": contract_status(
                            latest_contract_for_agent(contract)
                        )
                    },
                    {
                        "label": "Contracts Found",
                        "value": len(contracts)
                    },
                    {
                        "label": "Ratings Found",
                        "value": len(ratings)
                    },
                    {
                        "label": "Recruited Students Found",
                        "value": len(people)
                    },
                    {
                        "label": "Direct Agent-linked Invoices",
                        "value": len(direct_invoices)
                    }
                ]
            }
        ],
        sources=(
            (
                [
                    source(
                        "Agent",
                        "Agent",
                        agent_master_id(contract)
                    )
                ]
                if agent_master_id(contract)
                else []
            )
            + [
                source(
                    "Agent Contract",
                    "Agent Contract",
                    item.get("name")
                )
                for item in contracts
            ]
            + [
                source(
                    "Supplier Rating",
                    "Supplier Rating",
                    item.get("name")
                )
                for item in ratings
            ]
        ),
        warnings=warnings,
        confidence="Partial" if warnings else "Confirmed"
    )
def rating_rows(contract):
    agent_name = contract_name(contract)
    candidate_filters = [
        {"supplier_name": agent_name},
        {"supplier": agent_name},
        {"provider_name": agent_name},
        {"party_name": agent_name},
        {"agent_name": agent_name},
        {"agent": agent_name}
    ]

    records = []

    for filters in candidate_filters:
        rows = safe_db_list(
            "Supplier Rating",
            filters=filters,
            fields=["name", "modified"],
            order_by="modified desc",
            limit=50
        )

        if rows:
            for row in rows:
                doc = safe_get_doc("Supplier Rating", row.get("name"))
                if doc:
                    records.append(doc)
            break

    return records


def rating_values(rating_doc):
    return {
        "rating": first_value(
            rating_doc,
            [
                "rating",
                "total_rating",
                "overall_rating",
                "rating_score",
                "total_score"
            ]
        ),
        "rating_likert": first_value(
            rating_doc,
            [
                "rating_likert",
                "overall_likert",
                "likert_rating",
                "average_likert"
            ]
        ),
        "evaluation_stage": first_value(
            rating_doc,
            [
                "evaluation_stage",
                "custom_evaluation_stage",
                "stage"
            ]
        ),
        "status": first_value(
            rating_doc,
            [
                "status",
                "workflow_state",
                "recommendation"
            ]
        ),
        "modified": rating_doc.get("modified")
    }


def numeric_value(value):
    try:
        return float(value)
    except Exception:
        return None


def handle_rating(contract, threshold_check=False):
    records = rating_rows(contract)

    if not records:
        return response_base(
            "No linked Supplier Rating was found for "
            + contract_name(contract)
            + ".",
            warnings=[
                "Confirm the field linking Agent Contract to Supplier Rating."
            ],
            confidence="Missing data"
        )

    table_rows = []

    for rating_doc in records:
        values = rating_values(rating_doc)
        table_rows.append([
            link_cell(
                rating_doc.get("name"),
                "Supplier Rating",
                rating_doc.get("name")
            ),
            values.get("evaluation_stage") or "Not recorded",
            values.get("rating") if values.get("rating") not in [None, ""] else "Not recorded",
            values.get("rating_likert") if values.get("rating_likert") not in [None, ""] else "Not recorded",
            values.get("status") or "Not recorded",
            format_date(values.get("modified"))
        ])

    latest = records[0]
    latest_values = rating_values(latest)

    if threshold_check:
        minimum = 3.5
        likert = numeric_value(latest_values.get("rating_likert"))

        if likert is None:
            answer = (
                "The latest rating record for "
                + contract_name(contract)
                + " does not contain a usable rating_likert value, so the "
                + str(minimum)
                + " minimum threshold cannot be confirmed."
            )
            confidence = "Missing data"
        elif likert >= minimum:
            answer = (
                contract_name(contract)
                + " meets the minimum rating threshold. Latest rating_likert: "
                + str(latest_values.get("rating_likert"))
                + "; minimum required: "
                + str(minimum)
                + "."
            )
            confidence = "Confirmed"
        else:
            answer = (
                contract_name(contract)
                + " does not meet the minimum rating threshold. Latest rating_likert: "
                + str(latest_values.get("rating_likert"))
                + "; minimum required: "
                + str(minimum)
                + "."
            )
            confidence = "Confirmed"
    else:
        answer = (
            "The latest rating record for "
            + contract_name(contract)
            + " is "
            + clean_text(latest.get("name"))
            + ". Rating: "
            + clean_text(latest_values.get("rating") or "Not recorded")
            + "; rating_likert: "
            + clean_text(latest_values.get("rating_likert") or "Not recorded")
            + "; evaluation stage: "
            + clean_text(latest_values.get("evaluation_stage") or "Not recorded")
            + "."
        )
        confidence = "Confirmed"

    return response_base(
        answer,
        visuals=[
            {
                "type": "table",
                "title": "Linked rating records",
                "columns": [
                    "Rating Record",
                    "Evaluation Stage",
                    "Rating",
                    "Rating Likert",
                    "Status",
                    "Modified"
                ],
                "rows": table_rows
            }
        ],
        sources=[
            source("Supplier Rating", "Supplier Rating", doc.get("name"))
            for doc in records
        ],
        confidence=confidence
    )
def discover_agent_fields(doctype):
    output = []

    try:
        meta = frappe.get_meta(doctype)
    except Exception:
        return output

    for field in meta.fields or []:
        fieldname = clean_text(field.fieldname)
        label = normalise(field.label)
        options = normalise(field.options)
        combined = normalise(fieldname + " " + label + " " + options)

        if not fieldname:
            continue

        if any(term in combined for term in [
            "recruitment agent",
            "recruit agent",
            "agent contract",
            "education agent",
            "sales agent",
            "sales partner",
            "recruiter",
            "agent"
        ]):
            output.append(fieldname)

    return output



def resolve_agent_master(contract):
    agent_name = contract_name(contract)

    rows = safe_db_list(
        "Agent",
        filters={"agent_or_company_name": agent_name},
        fields=[
            "name",
            "agent_or_company_name",
            "status",
            "registration_no",
            "supplier",
            "contract",
            "fc_commission",
            "sc_commission",
            "modified"
        ],
        order_by="modified desc",
        limit=20
    )

    if rows:
        return safe_get_doc("Agent", rows[0].get("name"))

    # Fallback for punctuation or spacing differences.
    candidates = safe_db_list(
        "Agent",
        fields=["name", "agent_or_company_name", "modified"],
        order_by="modified desc",
        limit=5000
    )

    best = None
    best_score = 0

    for row in candidates:
        score = token_overlap_score(
            agent_name,
            row.get("agent_or_company_name")
        )

        if score > best_score:
            best_score = score
            best = row

    if best and best_score >= 2:
        return safe_get_doc("Agent", best.get("name"))

    return None


def agent_master_id(contract):
    agent_doc = resolve_agent_master(contract)

    if agent_doc:
        return clean_text(agent_doc.get("name"))

    return ""


def agent_identity_values(contract):
    values = []

    for value in [
        clean_text(contract.get("name")),
        contract_name(contract),
        clean_text(
            first_value(
                contract,
                ["personal_id", "uen", "company_id", "registration_number"]
            )
        )
    ]:
        if value and value not in values:
            values.append(value)

    return values



def field_definition(doctype, fieldname):
    try:
        meta = frappe.get_meta(doctype)
        return meta.get_field(fieldname)
    except Exception:
        return None


def linked_record_identity_values(link_doctype, contract):
    identities = agent_identity_values(contract)
    matches = []

    rows = safe_db_list(
        link_doctype,
        fields=["name"],
        order_by="modified desc",
        limit=5000
    )

    for row in rows:
        doc = safe_get_doc(link_doctype, row.get("name"))

        if not doc:
            continue

        searchable_parts = [
            doc.get("name"),
            first_value(
                doc,
                [
                    "agent_name", "party_name", "partner_name",
                    "supplier_name", "company_name", "customer_name",
                    "title", "personal_id", "uen",
                    "registration_number"
                ]
            )
        ]
        searchable = normalise(" ".join([
            clean_text(value) for value in searchable_parts if value
        ]))

        for identity in identities:
            identity_text = normalise(identity)

            if identity_text and (
                identity_text == searchable
                or identity_text in searchable
                or searchable in identity_text
            ):
                value = clean_text(doc.get("name"))

                if value and value not in matches:
                    matches.append(value)
                break

    return matches


def values_for_agent_field(doctype, fieldname, contract):
    values = agent_identity_values(contract)
    field = field_definition(doctype, fieldname)

    if field and clean_text(field.fieldtype) == "Link":
        link_doctype = clean_text(field.options)

        if link_doctype:
            for value in linked_record_identity_values(link_doctype, contract):
                if value not in values:
                    values.append(value)

    return values



def token_overlap_score(left, right):
    left_tokens = [token for token in normalise(left).split() if len(token) >= 3]
    right_tokens = [token for token in normalise(right).split() if len(token) >= 3]

    if not left_tokens or not right_tokens:
        return 0

    matched = 0

    for token in left_tokens:
        if token in right_tokens:
            matched = matched + 1

    return matched


def field_value_matches_agent(doctype, fieldname, raw_value, contract):
    value = clean_text(raw_value)

    if not value:
        return False

    identities = agent_identity_values(contract)
    value_norm = normalise(value)

    for identity in identities:
        identity_norm = normalise(identity)

        if not identity_norm:
            continue

        if (
            identity_norm == value_norm
            or identity_norm in value_norm
            or value_norm in identity_norm
            or token_overlap_score(identity_norm, value_norm) >= 2
        ):
            return True

    field = field_definition(doctype, fieldname)

    if field and clean_text(field.fieldtype) == "Link":
        linked_doc = safe_get_doc(clean_text(field.options), value)

        if linked_doc:
            searchable = " ".join([
                clean_text(linked_doc.get("name")),
                clean_text(first_value(
                    linked_doc,
                    [
                        "agent_name", "party_name", "partner_name",
                        "supplier_name", "company_name", "customer_name",
                        "title", "personal_id", "uen",
                        "registration_number"
                    ]
                ))
            ])

            for identity in identities:
                if (
                    normalise(identity) in normalise(searchable)
                    or normalise(searchable) in normalise(identity)
                    or token_overlap_score(identity, searchable) >= 2
                ):
                    return True

    return False


def scan_rows_for_agent(doctype, contract, fields, result_fields, limit=5000):
    rows = safe_db_list(
        doctype,
        fields=list(dict.fromkeys(["name"] + fields + result_fields)),
        order_by="modified desc",
        limit=limit
    )
    matched = []
    matched_field = ""
    matched_value = ""

    for row in rows:
        for fieldname in fields:
            value = row.get(fieldname)

            if field_value_matches_agent(
                doctype,
                fieldname,
                value,
                contract
            ):
                matched.append(row)
                matched_field = fieldname
                matched_value = clean_text(value)
                break

    return {
        "rows": matched,
        "doctype": doctype,
        "fieldname": matched_field,
        "value": matched_value
    }


def actual_field_values(doctype, fieldnames, limit=20):
    rows = safe_db_list(
        doctype,
        fields=list(dict.fromkeys(["name"] + fieldnames)),
        order_by="modified desc",
        limit=500
    )
    output = []

    for fieldname in fieldnames:
        seen = []

        for row in rows:
            value = clean_text(row.get(fieldname))

            if not value or value in seen:
                continue

            seen.append(value)
            output.append({
                "doctype": doctype,
                "fieldname": fieldname,
                "value": value,
                "record": row.get("name")
            })

            if len(seen) >= limit:
                break

    return output


def matching_rows_for_agent(doctype, contract, fields, limit=5000):
    candidate_fields = discover_agent_fields(doctype)

    for fieldname in candidate_fields:
        candidate_values = values_for_agent_field(
            doctype,
            fieldname,
            contract
        )

        for value in candidate_values:
            rows = safe_db_list(
                doctype,
                filters={fieldname: value},
                fields=fields,
                order_by="modified desc",
                limit=limit
            )

            if rows:
                return {
                    "rows": rows,
                    "doctype": doctype,
                    "fieldname": fieldname,
                    "value": value
                }

    # Fallback: inspect real stored values and match company/agent tokens.
    scanned = scan_rows_for_agent(
        doctype,
        contract,
        candidate_fields,
        fields,
        limit
    )

    if scanned.get("rows"):
        return scanned

    return {
        "rows": [],
        "doctype": doctype,
        "fieldname": "",
        "value": ""
    }
def applicant_full_name(row):
    return clean_text(
        clean_text(row.get("first_name"))
        + " "
        + clean_text(row.get("middle_name"))
        + " "
        + clean_text(row.get("last_name"))
    )


def student_recruitment_sources(contract):
    agent_id = agent_master_id(contract)
    matches = []

    if agent_id:
        direct_checks = [
            {
                "doctype": "Student Applicant",
                "fieldname": "agent",
                "fields": [
                    "name", "first_name", "middle_name",
                    "last_name", "program", "modified"
                ]
            },
            {
                "doctype": "Student Admission UCC",
                "fieldname": "agent",
                "fields": [
                    "name", "student_applicant", "student_name",
                    "program", "modified"
                ]
            },
            {
                "doctype": "Student",
                "fieldname": "custom_agent",
                "fields": [
                    "name", "student_name", "student_applicant",
                    "program", "modified"
                ]
            },
            {
                "doctype": "Student",
                "fieldname": "agent",
                "fields": [
                    "name", "student_name", "student_applicant",
                    "program", "modified"
                ]
            }
        ]

        for check in direct_checks:
            rows = safe_db_list(
                check.get("doctype"),
                filters={check.get("fieldname"): agent_id},
                fields=check.get("fields"),
                order_by="modified desc",
                limit=5000
            )

            if rows:
                matches.append({
                    "rows": rows,
                    "doctype": check.get("doctype"),
                    "fieldname": check.get("fieldname"),
                    "value": agent_id
                })

    # Keep generic fallback for any future custom source.
    if not matches:
        checks = [
            {
                "doctype": "Student Applicant",
                "fields": [
                    "name", "first_name", "middle_name",
                    "last_name", "program", "modified"
                ]
            },
            {
                "doctype": "Shortlisted Applicants",
                "fields": [
                    "name", "student_applicant", "applicant_name",
                    "program", "modified"
                ]
            },
            {
                "doctype": "Student Admission UCC",
                "fields": [
                    "name", "student_applicant", "student_name",
                    "program", "modified"
                ]
            },
            {
                "doctype": "Student",
                "fields": [
                    "name", "student_name", "student_applicant",
                    "program", "modified"
                ]
            }
        ]

        for check in checks:
            result = matching_rows_for_agent(
                check.get("doctype"),
                contract,
                check.get("fields"),
                5000
            )

            if result.get("rows"):
                matches.append(result)

    return matches
def normalise_recruited_people(source_matches):
    people = []
    seen = []

    for match in source_matches:
        doctype = match.get("doctype")

        for row in match.get("rows") or []:
            applicant_id = clean_text(
                row.get("student_applicant")
                or (
                    row.get("name")
                    if doctype == "Student Applicant"
                    else ""
                )
            )
            record_id = clean_text(row.get("name"))
            person_name = clean_text(
                applicant_full_name(row)
                or row.get("student_name")
                or row.get("applicant_name")
                or applicant_id
                or record_id
            )
            key = applicant_id or person_name or record_id

            if not key or key in seen:
                continue

            seen.append(key)
            people.append({
                "name": person_name,
                "applicant_id": applicant_id,
                "record_id": record_id,
                "doctype": doctype,
                "program": clean_text(row.get("program")) or "Not recorded",
                "link_field": match.get("fieldname"),
                "link_value": match.get("value")
            })

    return people


def handle_students(contract):
    source_matches = student_recruitment_sources(contract)
    people = normalise_recruited_people(source_matches)

    if not people:
        detected = []

        for doctype in [
            "Student Applicant",
            "Shortlisted Applicants",
            "Student Admission UCC",
            "Student"
        ]:
            fields = discover_agent_fields(doctype)
            if fields:
                detected.append(
                    doctype + ": " + ", ".join(fields)
                )

        diagnostic_rows = []

        for doctype in [
            "Student Applicant",
            "Shortlisted Applicants",
            "Student Admission UCC",
            "Student"
        ]:
            fields = discover_agent_fields(doctype)

            for item in actual_field_values(doctype, fields, 8):
                diagnostic_rows.append([
                    item.get("doctype"),
                    item.get("fieldname"),
                    item.get("value"),
                    link_cell(
                        item.get("record"),
                        item.get("doctype"),
                        item.get("record")
                    )
                ])

        return response_base(
            "No recruitment-linked student records were matched for "
            + contract_name(contract)
            + (
                " using Agent "
                + agent_master_id(contract)
                if agent_master_id(contract)
                else ""
            )
            + ".",
            visuals=[
                {
                    "type": "table",
                    "title": "Actual agent-field values found",
                    "columns": [
                        "DocType", "Field", "Stored Value", "Example Record"
                    ],
                    "rows": diagnostic_rows
                }
            ] if diagnostic_rows else [],
            warnings=[
                (
                    "Detected possible agent fields: "
                    + "; ".join(detected)
                    if detected
                    else "No agent-related fields were detected in the checked student and admission DocTypes."
                ),
                "Use the table above to identify the exact stored value used for this agent. One confirmed example is enough to finalise the mapping."
            ],
            confidence="Missing data"
        )

    rows = []

    for person in people:
        link_name = person.get("applicant_id") or person.get("record_id")
        link_doctype = (
            "Student Applicant"
            if person.get("applicant_id")
            else person.get("doctype")
        )

        rows.append([
            person.get("name"),
            link_cell(link_name, link_doctype, link_name),
            person.get("program"),
            person.get("doctype"),
            person.get("link_field")
        ])

    return response_base(
        str(len(people))
        + " unique recruited student record(s) were found for "
        + contract_name(contract)
        + " across "
        + str(len(source_matches))
        + " source DocType(s).",
        visuals=[
            {
                "type": "table",
                "title": "Students recruited",
                "columns": [
                    "Student", "Record", "Programme",
                    "Source DocType", "Agent Link Field"
                ],
                "rows": rows
            }
        ],
        sources=[
            source(
                person.get("doctype"),
                person.get("doctype"),
                person.get("record_id")
            )
            for person in people
            if person.get("record_id")
        ],
        warnings=[
            "Counts are deduplicated using Student Applicant ID first, then student name or source record ID."
        ]
    )


def direct_invoice_matches(contract):
    fields = [
        "name", "customer", "customer_name", "posting_date",
        "grand_total", "outstanding_amount", "currency",
        "status", "modified"
    ]

    result = matching_rows_for_agent(
        "Sales Invoice",
        contract,
        fields,
        5000
    )

    return result


def invoice_rows_for_recruited_people(people):
    customer_values = []

    for person in people:
        for value in [
            person.get("name"),
            person.get("applicant_id"),
            person.get("record_id")
        ]:
            value = clean_text(value)
            if value and value not in customer_values:
                customer_values.append(value)

    invoices = []

    for fieldname in ["customer", "customer_name"]:
        if not customer_values:
            continue

        rows = safe_db_list(
            "Sales Invoice",
            filters={
                "docstatus": 1,
                fieldname: ["in", customer_values]
            },
            fields=[
                "name", "customer", "customer_name", "posting_date",
                "grand_total", "outstanding_amount", "currency", "status"
            ],
            order_by="posting_date desc",
            limit=5000
        )

        for row in rows:
            if row.get("name") not in [
                invoice.get("name") for invoice in invoices
            ]:
                invoices.append(row)

    return invoices


def handle_finance(contract):
    direct = direct_invoice_matches(contract)
    invoices = direct.get("rows") or []
    method = ""

    if invoices:
        method = (
            "Direct Sales Invoice field "
            + direct.get("fieldname")
            + " = "
            + direct.get("value")
        )
    else:
        source_matches = student_recruitment_sources(contract)
        people = normalise_recruited_people(source_matches)
        invoices = invoice_rows_for_recruited_people(people)

        if invoices:
            method = (
                "Indirect match through "
                + str(len(people))
                + " recruited student record(s)"
            )

    if not invoices:
        detected_invoice_fields = discover_agent_fields("Sales Invoice")

        invoice_values = actual_field_values(
            "Sales Invoice",
            detected_invoice_fields,
            12
        )
        invoice_diagnostics = [
            [
                item.get("fieldname"),
                item.get("value"),
                link_cell(
                    item.get("record"),
                    "Sales Invoice",
                    item.get("record")
                )
            ]
            for item in invoice_values
        ]

        return response_base(
            "No submitted Sales Invoice records were matched automatically to "
            + contract_name(contract)
            + ".",
            visuals=[
                {
                    "type": "table",
                    "title": "Actual Sales Invoice agent-field values",
                    "columns": ["Field", "Stored Value", "Invoice"],
                    "rows": invoice_diagnostics
                }
            ] if invoice_diagnostics else [],
            warnings=[
                (
                    "Possible Sales Invoice agent fields detected: "
                    + ", ".join(detected_invoice_fields)
                    if detected_invoice_fields
                    else "No agent-related field was detected in Sales Invoice."
                ),
                "Use one confirmed invoice from the table to finalise the revenue mapping.",
                "Commission remains unavailable until its exact source is identified."
            ],
            confidence="Missing data"
        )

    total_invoiced = 0
    total_outstanding = 0

    for invoice in invoices:
        try:
            total_invoiced = total_invoiced + float(
                invoice.get("grand_total") or 0
            )
        except Exception:
            pass

        try:
            total_outstanding = total_outstanding + float(
                invoice.get("outstanding_amount") or 0
            )
        except Exception:
            pass

    currency = clean_text(invoices[0].get("currency")) or "SGD"

    return response_base(
        "Estimated revenue linked to "
        + contract_name(contract)
        + ": "
        + currency
        + " "
        + str(round(total_invoiced, 2))
        + " across "
        + str(len(invoices))
        + " submitted invoice(s). Outstanding: "
        + currency
        + " "
        + str(round(total_outstanding, 2))
        + ".",
        visuals=[
            {
                "type": "table",
                "title": "Agent-linked invoices",
                "columns": [
                    "Invoice", "Customer", "Posting Date",
                    "Total", "Outstanding", "Status"
                ],
                "rows": [
                    [
                        link_cell(
                            invoice.get("name"),
                            "Sales Invoice",
                            invoice.get("name")
                        ),
                        invoice.get("customer_name")
                        or invoice.get("customer")
                        or "Not recorded",
                        format_date(invoice.get("posting_date")),
                        invoice.get("grand_total") or 0,
                        invoice.get("outstanding_amount") or 0,
                        invoice.get("status") or "Not recorded"
                    ]
                    for invoice in invoices
                ]
            }
        ],
        sources=[
            source("Sales Invoice", "Sales Invoice", invoice.get("name"))
            for invoice in invoices
        ],
        warnings=[
            "Revenue matching method: " + method + ".",
            "Commission status remains unavailable until the exact commission field, child table or transaction DocType is mapped."
        ],
        confidence="Partial"
    )

def handle_commission(contract):
    agent_doc = resolve_agent_master(contract)

    if not agent_doc:
        return response_base(
            "No Agent master record could be resolved for "
            + contract_name(contract)
            + ".",
            warnings=[
                "Expected mapping: Agent Contract.party_name to Agent.agent_or_company_name."
            ],
            confidence="Missing data"
        )

    registration_rows = []

    for row in agent_doc.get("registration") or []:
        registration_rows.append([
            format_date(
                first_value(
                    row,
                    ["start_contract", "start_date", "from_date"]
                )
            ),
            format_date(
                first_value(
                    row,
                    ["end_contract", "end_date", "to_date"]
                )
            ),
            (
                "Yes"
                if int(first_value(row, ["active", "is_active"]) or 0) == 1
                else "No"
            ),
            first_value(
                row,
                [
                    "commission",
                    "commission_percentage",
                    "commission_percent",
                    "rate"
                ]
            ) or "Not recorded"
        ])

    full_course = clean_text(agent_doc.get("fc_commission"))
    short_course = clean_text(agent_doc.get("sc_commission"))

    active_rows = [
        row for row in registration_rows
        if row[2] == "Yes"
    ]

    if active_rows:
        answer = (
            "The active commission arrangement for "
            + contract_name(contract)
            + " is "
            + clean_text(active_rows[0][3])
            + "%, based on the Agent registration table."
        )
        confidence = "Confirmed"
    elif registration_rows:
        answer = (
            "Commission records exist for "
            + contract_name(contract)
            + ", but no row is marked active."
        )
        confidence = "Partial"
    elif full_course or short_course:
        answer = (
            "Commission fields are recorded on the Agent master for "
            + contract_name(contract)
            + "."
        )
        confidence = "Confirmed"
    else:
        answer = (
            "No commission rate was found on the Agent master for "
            + contract_name(contract)
            + "."
        )
        confidence = "Missing data"

    visuals = []

    if registration_rows:
        visuals.append({
            "type": "table",
            "title": "Commission history",
            "columns": [
                "Start Contract",
                "End Contract",
                "Active",
                "Commission (%)"
            ],
            "rows": registration_rows
        })

    visuals.append({
        "type": "summary",
        "title": "Agent commission fields",
        "items": [
            {
                "label": "Agent",
                "value": link_cell(
                    agent_doc.get("name"),
                    "Agent",
                    agent_doc.get("name")
                )
            },
            {
                "label": "Full Course Commission",
                "value": full_course or "Not recorded"
            },
            {
                "label": "Short Course Commission",
                "value": short_course or "Not recorded"
            }
        ]
    })

    return response_base(
        answer,
        visuals=visuals,
        sources=[
            source("Agent", "Agent", agent_doc.get("name"))
        ],
        warnings=[
            "Payment status is separate from the contractual commission rate and still depends on Payment Entry mapping."
        ],
        confidence=confidence
    )
def handle_compliance(contract):
    issues = []
    evidence_rows = []
    latest = latest_contract_for_agent(contract)
    dates = contract_dates(latest)
    status = contract_status(latest)
    ratings = rating_rows(contract)

    if status in ["Expired", "Not started"]:
        issues.append("Contract status is " + status + ".")

    if not dates.get("start"):
        issues.append("Contract commencement date is missing.")

    if not dates.get("end"):
        issues.append("Contract expiry date is missing.")

    if ratings:
        latest_rating = ratings[0]
        values = rating_values(latest_rating)
        likert = numeric_value(values.get("rating_likert"))
        rating_status = normalise(values.get("status"))

        evidence_rows.append([
            link_cell(
                latest_rating.get("name"),
                "Supplier Rating",
                latest_rating.get("name")
            ),
            values.get("evaluation_stage") or "Not recorded",
            values.get("rating") or "Not recorded",
            values.get("rating_likert") or "Not recorded",
            values.get("status") or "Not recorded"
        ])

        if likert is not None and likert < 3.5:
            issues.append(
                "Latest rating_likert is below the 3.5 minimum."
            )

        if any(term in rating_status for term in [
            "terminate", "reject", "suspend", "not approved",
            "corrective", "conditional"
        ]):
            issues.append(
                "Latest rating status requires attention: "
                + clean_text(values.get("status"))
                + "."
            )
    else:
        issues.append("No linked Supplier Rating was found.")

    if issues:
        answer = (
            str(len(issues))
            + " possible compliance issue(s) were identified for "
            + contract_name(contract)
            + "."
        )
        confidence = "Partial"
    else:
        answer = (
            "No compliance issue was identified from the Agent Contract and latest Supplier Rating currently checked for "
            + contract_name(contract)
            + "."
        )
        confidence = "Confirmed"

    return response_base(
        answer,
        visuals=[
            {
                "type": "table",
                "title": "Latest compliance evidence",
                "columns": [
                    "Rating Record", "Evaluation Stage",
                    "Rating", "Rating Likert", "Status"
                ],
                "rows": evidence_rows
            }
        ] if evidence_rows else [],
        warnings=issues + [
            "This check covers contract dates/status and the latest Supplier Rating. It does not replace a full compliance audit."
        ],
        sources=(
            [
                source(
                    "Agent Contract",
                    "Agent Contract",
                    latest.get("name")
                )
            ]
            + [
                source(
                    "Supplier Rating",
                    "Supplier Rating",
                    item.get("name")
                )
                for item in ratings[:1]
            ]
        ),
        confidence=confidence
    )


def handle_renewal(contract):
    latest = latest_contract_for_agent(contract)
    dates = contract_dates(latest)
    status = contract_status(latest)
    ratings = rating_rows(contract)
    latest_rating = ratings[0] if ratings else None
    rating_values_data = (
        rating_values(latest_rating)
        if latest_rating
        else {}
    )
    likert = numeric_value(
        rating_values_data.get("rating_likert")
    )
    warnings = []

    if status == "Expired":
        recommendation = "Do not renew automatically; complete a formal renewal review."
    elif status == "Not started":
        recommendation = "Renewal is not applicable because the latest contract has not started."
    elif not dates.get("end"):
        recommendation = "Hold the renewal decision until the expiry date is recorded."
        warnings.append("The contract expiry date is missing.")
    elif not latest_rating:
        recommendation = "Complete a current Supplier Rating before deciding on renewal."
        warnings.append("No linked Supplier Rating was found.")
    elif likert is None:
        recommendation = "Review manually because the latest rating_likert is missing."
        warnings.append("Latest rating_likert is not recorded.")
    elif likert < 3.5:
        recommendation = "Do not renew without corrective action and management approval."
        warnings.append("Latest rating_likert is below the 3.5 minimum.")
    else:
        recommendation = "Eligible for continuation, subject to management approval and completion of the formal renewal process."

    items = [
        {"label": "Contract Status", "value": status},
        {"label": "Expiry", "value": format_date(dates.get("end"))},
        {
            "label": "Latest Rating Record",
            "value": (
                link_cell(
                    latest_rating.get("name"),
                    "Supplier Rating",
                    latest_rating.get("name")
                )
                if latest_rating
                else "Not recorded"
            )
        },
        {
            "label": "Latest Rating Likert",
            "value": (
                rating_values_data.get("rating_likert")
                if rating_values_data.get("rating_likert") not in [None, ""]
                else "Not recorded"
            )
        },
        {"label": "Recommendation", "value": recommendation}
    ]

    return response_base(
        "Renewal assessment for "
        + contract_name(contract)
        + ": "
        + recommendation,
        visuals=[
            {
                "type": "summary",
                "title": "Renewal readiness",
                "items": items
            }
        ],
        warnings=warnings + [
            "Final renewal remains a management decision and should consider performance, compliance, recruitment outcomes and contractual requirements."
        ],
        sources=(
            [
                source(
                    "Agent Contract",
                    "Agent Contract",
                    latest.get("name")
                )
            ]
            + (
                [
                    source(
                        "Supplier Rating",
                        "Supplier Rating",
                        latest_rating.get("name")
                    )
                ]
                if latest_rating
                else []
            )
        ),
        confidence="Partial"
    )
def handle_active_count():
    rows = safe_db_list(
        "Agent Contract",
        fields=["name", "party_name", "posting_date", "end_date"],
        order_by="modified desc",
        limit=5000
    )
    active = []

    for row in rows:
        doc = safe_get_doc("Agent Contract", row.get("name"))
        if doc and contract_status(doc) == "Active":
            active.append(doc)

    return response_base(
        str(len(active)) + " recruitment agent contract(s) appear active.",
        visuals=[
            {
                "type": "table",
                "title": "Active recruitment agent contracts",
                "columns": ["Agent", "Contract", "Expiry"],
                "rows": [
                    [
                        contract_name(doc),
                        link_cell(
                            doc.get("name"),
                            "Agent Contract",
                            doc.get("name")
                        ),
                        format_date(contract_dates(doc).get("end"))
                    ]
                    for doc in active
                ]
            }
        ],
        sources=[
            source("Agent Contract", "Agent Contract", doc.get("name"))
            for doc in active
        ]
    )


question = clean_text(frappe.form_dict.get("question"))
selected_contract = clean_text(frappe.form_dict.get("agent_contract"))

if not question:
    frappe.response["message"] = response_base(
        "Please enter a question.",
        confidence="Not applicable"
    )
else:
    intent = detect_intent(question)

    if intent == "unsupported":
        frappe.response["message"] = response_base(
            "This question is outside the Recruitment Agent module. Ask about an agent profile, contract, expiry, recruitment performance, rating, compliance or renewal.",
            confidence="Not applicable"
        )
    elif intent == "active_count":
        frappe.response["message"] = handle_active_count()
    else:
        match = find_contract(selected_contract, question)

        if match.get("status") == "required":
            frappe.response["message"] = {
                "status": "student_required",
                "answer": "Please select a recruitment agent or include the agent or company name.",
                "visuals": [],
                "sources": [],
                "warnings": [],
                "ai_used": False
            }
        elif match.get("status") == "choose":
            frappe.response["message"] = {
                "status": "choose_student",
                "answer": "More than one recruitment agent matches. Select the correct agent.",
                "candidates": [
                    {
                        "student_applicant": row.get("name"),
                        "student_name": row.get("party_name") or row.get("name"),
                        "course": row.get("personal_id") or "Agent Contract"
                    }
                    for row in match.get("candidates") or []
                ],
                "visuals": [],
                "sources": [],
                "warnings": [],
                "ai_used": False
            }
        else:
            contract = match.get("contract")

            if intent == "profile":
                result = handle_profile(contract)
            elif intent == "contract":
                result = handle_contract(contract)
            elif intent == "journey":
                result = handle_journey(contract)
            elif intent == "latest_contract":
                result = handle_latest_contract(contract)
            elif intent == "rating":
                result = handle_rating(contract, False)
            elif intent == "rating_threshold":
                result = handle_rating(contract, True)
            elif intent == "students":
                result = handle_students(contract)
            elif intent == "finance":
                result = handle_finance(contract)
            elif intent == "commission":
                result = handle_commission(contract)
            elif intent == "compliance":
                result = handle_compliance(contract)
            elif intent == "renewal":
                result = handle_renewal(contract)
            else:
                result = handle_profile(contract)

            result["agent_contract"] = contract.get("name")
            result["agent_name"] = contract_name(contract)
            frappe.response["message"] = result
