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
    "summary",
    "c511_analytics",
    "c512_analytics",
    "c521_analytics",
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

def js_round(x):
    # equals JavaScript Math.round for x >= 0 (all percentages here are >= 0)
    return int(x + 0.5)

def pct(n, d):
    return js_round(n / d * 100) if d else 0

def js_number(v):
    # mirror JavaScript Number(): "" / None -> 0; non-numeric -> NaN
    if v is None or v == "":
        return 0.0
    try:
        return float(v)
    except (TypeError, ValueError):
        return float("nan")

C511_GROUPS = {
    "overview": ["course_title", "mode_of_delivery", "academic_level", "course_language", "programme_structure", "proposed_date"],
    "strategy": ["overall_achievement", "industry_relevance", "skills_development", "target_headcount", "competitors"],
    "learner": ["target_audience_industry", "minimum_age", "industry_experience", "cognitive_level", "prior_knowledge", "learning_style", "cognitive_development_focus", "motivation_level", "emotional_state", "stress_resilience", "social_engagement_level", "peer_learning_engagement", "teamwork_and_collaboration_skills", "special_educational_needs", "inclusivity_measures", "learning_environment_support", "learner_profile_characteristic", "mer_academic", "mer_language"],
    "pedagogy": ["table_teqa", "teaching_technique_offline", "teacher_student_ratio_offline", "teaching_technique_online", "teacher_student_ratio_online", "total_duration_ft", "total_duration_pt", "days_per_week_ft", "hour_per_day_ft", "days_per_week_pt", "hour_per_day_pt", "ft_contact_hour_total", "pt_contact_hour_total"],
    "curriculum": ["learning_outcomes", "module_list", "sequencing_and_rationale", "course_developer", "industrial_attachment_needead", "industrial_attachment_details", "articulation_pathway", "pathway_programme_details", "accrediation_y_n", "accrediation_details", "association_y_n", "association_details"],
    "assessment": ["assessment_criteria", "assessmnet_descriptions"],
    "risk": ["table_ornh", "budget_management", "total_budget_fee", "total_actual_spending", "resource_childable", "risk_table", "risk_mitigation_childtable", "table_odgh", "stakeholder_note", "documentation_table"],
    "approval": ["approval_status", "decision_date", "quality_meeting", "ssg_approval_date", "decision_summary"],
}
C511_GROUP_ORDER = ["overview", "strategy", "learner", "pedagogy", "curriculum", "assessment", "risk", "approval"]
NORM_ALLOWED = "abcdefghijklmnopqrstuvwxyz0123456789"

def has_evidence(v):
    if isinstance(v, (list, tuple)):
        return len(v) > 0
    if isinstance(v, dict):
        return len(v) > 0
    return v is not None and str(v).strip() != "" and v != 0

def norm_value(s):
    return "".join(ch for ch in str(s).lower() if ch in NORM_ALLOWED)

def find_evidence_field(record, candidates):
    for field in candidates:
        if field in record and has_evidence(record[field]):
            return field
    keys = list((record or {}).keys())
    for candidate in candidates:
        n = norm_value(candidate)
        for k in keys:
            nk = norm_value(k)
            if (nk == n or n in nk or nk in n) and has_evidence(record[k]):
                return k
    return None

def c511_group(record, group):
    fields = []
    for field in C511_GROUPS[group]:
        hit = find_evidence_field(record, [field])
        if hit is not None and hit not in fields:
            fields.append(hit)
    return {"ok": len(fields) > 0, "fields": fields}

def child_len(record, primary, fallback=None):
    # mirror JS (record[primary] || record[fallback] || []).length where [] is truthy in JS
    v = record.get(primary)
    if v is None and fallback is not None:
        v = record.get(fallback)
    if v is None:
        v = []
    return len(v) if isinstance(v, (list, tuple)) else 0

def compute_c511(data, today):
    proposals = data.get("Course Proposal") or []
    reviews = data.get("Course Review") or []
    courses = data.get("Course") or []

    checks = []
    for record in proposals:
        groups = {}
        for g in C511_GROUP_ORDER:
            groups[g] = c511_group(record, g)
        complete = len([1 for g in C511_GROUP_ORDER if groups[g]["ok"]])
        checks.append({"record": record.get("name"),
                       "groups": {g: {"ok": groups[g]["ok"], "fields": groups[g]["fields"]} for g in C511_GROUP_ORDER},
                       "rate": pct(complete, len(C511_GROUP_ORDER)),
                       "status": record.get("approval_status") or "Not set"})

    topics = len([c for c in courses if (c.get("topics") or [])])
    criteria = len([c for c in courses if (c.get("assessment_criteria") or [])])
    approved_words = ("approved", "accepted", "endorsed", "submitted")
    proposals_by_name = {}
    for p in proposals:
        proposals_by_name[p.get("name")] = p
    approved = 0
    for x in checks:
        status_l = str(x["status"]).lower()
        if any(w in status_l for w in approved_words) or proposals_by_name.get(x["record"], {}).get("docstatus") == 1:
            approved += 1

    readiness = []
    for g in C511_GROUP_ORDER:
        readiness.append({"label": g[0].upper() + g[1:],
                          "value": pct(len([x for x in checks if x["groups"][g]["ok"]]), len(checks))})

    gaps = []
    for x in checks:
        for g in C511_GROUP_ORDER:
            if not x["groups"][g]["ok"]:
                gaps.append({"doctype": "Course Proposal", "record": x["record"], "area": g,
                             "issue": "No populated {0} evidence detected".format(g), "severity": "Risk"})

    module_rows = []
    for record in courses:
        lo = child_len(record, "custom_list_of_learning_objective", "topics")
        lessons = child_len(record, "custom_lesson_plans")
        teaching = child_len(record, "custom_teaching_approach")
        assessment = child_len(record, "assessment_criteria")
        resources = child_len(record, "custom_resource")
        areas = [lo, lessons, teaching, assessment, resources]
        module_rows.append({"record": record.get("name"), "lo": lo, "lessons": lessons, "teaching": teaching,
                            "assessment": assessment, "resources": resources,
                            "coverage": pct(len([v for v in areas if v > 0]), 5),
                            "zero": all(v == 0 for v in areas), "complete": all(v > 0 for v in areas)})
    for x in module_rows:
        for area, value in [("learning outcomes", x["lo"]), ("lesson plans", x["lessons"]),
                            ("teaching approach", x["teaching"]), ("assessment criteria", x["assessment"]),
                            ("resources", x["resources"])]:
            if not value:
                gaps.append({"doctype": "Course", "record": x["record"], "area": area,
                             "issue": "Missing {0}".format(area), "severity": "Risk"})

    if not reviews:
        gaps.append({"doctype": "Course Review", "record": "—", "area": "validation",
                     "issue": "No readable Course Review records", "severity": "Risk"})
    else:
        for review in reviews:
            rec_text = review.get("recommendations") or review.get("module_recommendation_summary")
            if not has_evidence(rec_text):
                gaps.append({"doctype": "Course Review", "record": review.get("name"), "area": "recommendations",
                             "issue": "Missing recommendations", "severity": "Warning"})
            if not (review.get("actionplan_progress") or []):
                gaps.append({"doctype": "Course Review", "record": review.get("name"), "area": "action plan",
                             "issue": "No action plan rows", "severity": "Risk"})
            nrd = review.get("next_review_date")
            if nrd and str(nrd)[:10] <= today:
                gaps.append({"doctype": "Course Review", "record": review.get("name"), "area": "review cycle",
                             "issue": "Next review date is overdue", "severity": "Risk"})

    proposal_approved = len([x for x in proposals if x.get("approval_status") == "Approved"])
    review_approved = len([x for x in reviews if x.get("review_status") == "Approved"])
    ssg_count = len([x for x in proposals if x.get("ssg_approval_date")])
    overdue = len([x for x in reviews if x.get("next_review_date") and str(x.get("next_review_date"))[:10] <= today])
    decision_vals = []
    for x in proposals:
        pd = x.get("proposed_date")
        dd = x.get("decision_date")
        if pd and dd:
            days = frappe.utils.date_diff(dd, pd)
            if days >= 0:
                decision_vals.append(days)
    avg_decision_days = js_round(sum(decision_vals) / len(decision_vals)) if decision_vals else None
    action_counts = [len(x.get("actionplan_progress") or []) for x in reviews]
    avg_actions = (js_round(sum(action_counts) / len(action_counts) * 10) / 10) if action_counts else 0

    return {"topics": topics, "criteria": criteria, "approved": approved, "readiness": readiness, "gaps": gaps,
            "moduleRows": module_rows, "checks": checks, "proposalApproved": proposal_approved,
            "reviewApproved": review_approved, "ssgCount": ssg_count, "overdue": overdue,
            "avgDecisionDays": avg_decision_days, "avgActions": avg_actions}

# Server form of compute_c512: no imports, no leading-underscore identifiers,
# no id(), frappe.utils for dates. String date keys "_doctype"/"_parent"/"_age"
# are data (allowed); only NAMES avoid leading underscores.
def group_records(rows, key, doctype):
    m = {}
    for r in (rows or []):
        label = (r.get(key) if r else None) or "Not Set"
        m.setdefault(label, []).append(r)
    out = [{"label": l, "value": len(recs), "records": recs, "doctype": doctype} for l, recs in m.items()]
    out.sort(key=lambda x: -x["value"])
    return out

def strip_tags(v):
    s = str(v); out = []; i = 0; n = len(s)
    while i < n:
        if s[i] == "<":
            j = s.find(">", i + 1)
            if j != -1 and j > i + 1:
                i = j + 1
                continue
        out.append(s[i]); i += 1
    return "".join(out)

def compute_c512(data, today):
    def attach(rows, dt):
        res = []
        for r in (rows or []):
            rr = dict(r); rr["_doctype"] = dt; res.append(rr)
        return res
    mr = data.get("Module Review") or []
    cr = data.get("Course Review") or []
    review_records = attach(mr, "Module Review") + attach(cr, "Course Review")
    overdue = [x for x in cr if x.get("next_review_date") and str(x.get("next_review_date"))[:10] < today]
    upcoming = [x for x in cr if x.get("next_review_date") and str(x.get("next_review_date"))[:10] >= today]
    no_next = [x for x in cr if not x.get("next_review_date")]

    review_type_groups = {}
    for r in review_records:
        label = (r.get("type_of_review") or "Not Set") if r.get("_doctype") == "Module Review" else (r.get("review_type") or "Not Set")
        review_type_groups.setdefault(label, []).append(r)
    action_groups = {}
    for parent in cr:
        for action in (parent.get("actionplan_progress") or []):
            label = action.get("status") or "Not Set"
            action_groups.setdefault(label, {})[parent.get("name")] = parent
    rec_groups = {}
    for r in review_records:
        label = r.get("recommendation_implementation_status") or "Not Set"
        rec_groups.setdefault(label, []).append(r)
    evidence_fields = ["rating_duration","rating_pedagogy","rating_assessment","rating_learning_outcomes","rating_lesson_plan","rating_resource","risk_question","existing_attendance","existing_assessment_result","existing_classroom_observation","student_intervention_plan","admission_requirement_effectiveness","survey_results","rating_value_quality","recommendation"]
    complete = [r for r in mr if all(r.get(f) is not None and r.get(f) != "" for f in evidence_fields)]
    complete_names = set(r.get("name") for r in complete)
    incomplete = [r for r in mr if r.get("name") not in complete_names]
    completed_reviews = [x for x in cr if "complet" in str(x.get("review_status") or "").lower()]
    today_plus_30 = frappe.utils.add_days(today, 30)
    due_reviews = [x for x in cr if x.get("next_review_date") and str(x.get("next_review_date"))[:10] >= today and str(x.get("next_review_date"))[:10] <= today_plus_30]
    future_reviews = [x for x in cr if x.get("next_review_date") and str(x.get("next_review_date"))[:10] > today_plus_30]
    reviewed_courses = set(x.get("course") for x in cr if x.get("course"))
    reviewed_modules = set((x.get("course") or x.get("module")) for x in mr if (x.get("course") or x.get("module")))
    covered = [x for x in mr if x.get("course") in reviewed_courses]
    uncovered = [x for x in mr if x.get("course") not in reviewed_courses]
    all_actions = []
    for parent in cr:
        for action in (parent.get("actionplan_progress") or []):
            a = dict(action); a["_parent"] = parent; all_actions.append(a)
    def action_record_set(items):
        seen = {}
        for x in items:
            seen[x.get("_parent").get("name")] = x.get("_parent")
        return list(seen.values())
    def is_done(s):
        s = str(s or "").lower()
        return ("complete" in s) or ("closed" in s) or ("done" in s) or ("implemented" in s)
    completed_actions = []
    pending_actions = []
    for x in all_actions:
        if is_done(x.get("status")):
            completed_actions.append(x)
        else:
            pending_actions.append(x)
    def action_date(x):
        return x.get("due_date") or x.get("target_date") or x.get("completion_date") or x.get("date") or x.get("modified")
    aged = []
    for x in pending_actions:
        ad = action_date(x)
        xx = dict(x); xx["_age"] = (max(0, frappe.utils.date_diff(today, ad)) if ad else None); aged.append(xx)
    aging = [
        ("0–30 days", [x for x in aged if x.get("_age") is not None and x.get("_age") <= 30]),
        ("31–60 days", [x for x in aged if x.get("_age") is not None and 30 < x.get("_age") <= 60]),
        ("61–90 days", [x for x in aged if x.get("_age") is not None and 60 < x.get("_age") <= 90]),
        ("More than 90 days", [x for x in aged if x.get("_age") is not None and x.get("_age") > 90]),
        ("No action date", [x for x in aged if x.get("_age") is None]),
    ]
    stakeholder_fields = ["stakeholder_feedback","feedback_from_stakeholders","stakeholder_comments","stakeholder_input"]
    benchmark_fields = ["benchmarking_evidence","benchmarking","benchmark_data","industry_benchmark"]
    stakeholder_supported = any(any(name in x for name in stakeholder_fields) for x in cr)
    benchmark_supported = any(any(name in x for name in benchmark_fields) for x in cr)
    def has_value(rec, names):
        return any(rec.get(nm) is not None and strip_tags(rec.get(nm)).strip() != "" for nm in names)
    missing_stakeholder = [x for x in cr if not has_value(x, stakeholder_fields)] if stakeholder_supported else []
    missing_benchmark = [x for x in cr if not has_value(x, benchmark_fields)] if benchmark_supported else []
    followup_groups = {}
    for r in review_records:
        raw = r.get("review_date") or r.get("date_of_review") or r.get("modified")
        month = str(raw)[:7] if raw else "No date"
        followup_groups.setdefault(month, []).append(r)

    def slim(rows):
        out = []
        for x in rows:
            e = {"label": x["label"], "value": x["value"], "records": [r.get("name") for r in x.get("records", [])]}
            if x.get("doctype") is not None:
                e["doctype"] = x["doctype"]
            out.append(e)
        return out

    review_type = sorted([{"label": l, "value": len(recs), "records": recs} for l, recs in review_type_groups.items()], key=lambda x: -x["value"])
    actions_ds = sorted([{"label": l, "value": sum(len([a for a in (p.get("actionplan_progress") or []) if (a.get("status") or "Not Set") == l]) for p in m.values()), "records": list(m.values()), "doctype": "Course Review"} for l, m in action_groups.items()], key=lambda x: -x["value"])
    rec_status = sorted([{"label": l, "value": len(recs), "records": recs} for l, recs in rec_groups.items()], key=lambda x: -x["value"])
    followup = sorted([{"label": l, "value": len([x for x in recs if is_done(x.get("recommendation_implementation_status") or x.get("review_status") or x.get("status"))]), "records": recs} for l, recs in followup_groups.items()], key=lambda x: x["label"])

    return {
        "kpis": {"mrTotal": len(mr), "mrApproved": len([x for x in mr if x.get("status") == "Approved"]), "crTotal": len(cr), "crOverdue": len(overdue)},
        "reviewLevel": slim([{"label": "Module Review", "value": len(mr), "records": mr, "doctype": "Module Review"}, {"label": "Course Review", "value": len(cr), "records": cr, "doctype": "Course Review"}]),
        "schedule": slim([{"label": "Overdue", "value": len(overdue), "records": overdue, "doctype": "Course Review"}, {"label": "Upcoming / current", "value": len(upcoming), "records": upcoming, "doctype": "Course Review"}, {"label": "No next review date", "value": len(no_next), "records": no_next, "doctype": "Course Review"}]),
        "moduleStatus": slim(group_records(mr, "status", "Module Review")),
        "courseStatus": slim(group_records(cr, "review_status", "Course Review")),
        "reviewType": slim(review_type),
        "actions": slim(actions_ds),
        "recommendationStatus": slim(rec_status),
        "evidence": slim([{"label": "Core evidence complete", "value": len(complete), "records": complete, "doctype": "Module Review"}, {"label": "Core evidence incomplete", "value": len(incomplete), "records": incomplete, "doctype": "Module Review"}]),
        "cycle": slim([{"label": "Completed", "value": len(completed_reviews), "records": completed_reviews, "doctype": "Course Review"}, {"label": "Due within 30 days", "value": len(due_reviews), "records": due_reviews, "doctype": "Course Review"}, {"label": "Upcoming", "value": len(future_reviews), "records": future_reviews, "doctype": "Course Review"}, {"label": "Overdue", "value": len(overdue), "records": overdue, "doctype": "Course Review"}, {"label": "No next review date", "value": len(no_next), "records": no_next, "doctype": "Course Review"}]),
        "coverage": slim([{"label": "Module Reviews linked to a Course Review", "value": len(covered), "records": covered, "doctype": "Module Review"}, {"label": "Module Reviews without matching Course Review", "value": len(uncovered), "records": uncovered, "doctype": "Module Review"}, {"label": "Distinct reviewed modules", "value": len(reviewed_modules), "records": mr, "doctype": "Module Review"}]),
        "actionsCompletion": slim([{"label": "Completed actions", "value": len(completed_actions), "records": action_record_set(completed_actions), "doctype": "Course Review"}, {"label": "Pending actions", "value": len(pending_actions), "records": action_record_set(pending_actions), "doctype": "Course Review"}]),
        "actionAging": slim([{"label": l, "value": len(items), "records": action_record_set(items), "doctype": "Course Review"} for l, items in aging]),
        "missingEvidence": slim([{"label": "Missing next review date", "value": len(no_next), "records": no_next, "doctype": "Course Review"}, {"label": ("Missing stakeholder feedback" if stakeholder_supported else "Stakeholder feedback field unsupported"), "value": (len(missing_stakeholder) if stakeholder_supported else 0), "records": missing_stakeholder, "doctype": "Course Review"}, {"label": ("Missing benchmarking evidence" if benchmark_supported else "Benchmarking field unsupported"), "value": (len(missing_benchmark) if benchmark_supported else 0), "records": missing_benchmark, "doctype": "Course Review"}]),
        "followup": slim(followup),
        "mr": [x.get("name") for x in mr],
        "cr": [x.get("name") for x in cr],
    }

def compute_c521(d):
    intakes = d.get("Student Intake No") or []
    classes = d.get("Module Class Details") or []
    schedules = d.get("Course Schedule") or []
    apps = d.get("Student Admission UCC") or []

    ready = [x for x in intakes if x.get("program") and x.get("course_start_date") and x.get("course_end_date")]
    ready_names = set(x.get("name") for x in ready)
    not_ready = [x for x in intakes if x.get("name") not in ready_names]
    assigned = [x for x in classes if x.get("custom_instructor")]
    unassigned = [x for x in classes if not x.get("custom_instructor")]
    session_ready = [x for x in schedules if x.get("instructor") and x.get("room") and x.get("from_time") and x.get("to_time")]
    missing_teacher = [x for x in schedules if not x.get("instructor")]
    missing_room = [x for x in schedules if not x.get("room")]
    missing_timing = [x for x in schedules if not x.get("from_time") or not x.get("to_time")]
    complete_contracts = [x for x in apps if x.get("contract_start") and x.get("contract_end")]
    incomplete_contracts = [x for x in apps if not x.get("contract_start") or not x.get("contract_end")]
    schedule_class_names = set((x.get("student_group") or x.get("module_class_details")) for x in schedules if (x.get("student_group") or x.get("module_class_details")))
    unscheduled_classes = [x for x in classes if x.get("name") not in schedule_class_names]
    scheduled_classes = [x for x in classes if x.get("name") in schedule_class_names]

    def to_minutes(value):
        if value is None or value == "":
            return None
        parts = str(value).split(":")
        def num(s):
            try: return float(s)
            except (TypeError, ValueError): return None
        p0 = num(parts[0])
        if p0 is None:
            return None
        p1 = num(parts[1]) if len(parts) > 1 else None
        p1v = p1 if (p1 is not None and p1 != 0) else 0
        return p0 * 60 + p1v
    def overlap(a, b):
        if str(a.get("schedule_date") or "") != str(b.get("schedule_date") or ""):
            return False
        af = to_minutes(a.get("from_time")); at = to_minutes(a.get("to_time"))
        bf = to_minutes(b.get("from_time")); bt = to_minutes(b.get("to_time"))
        return af is not None and at is not None and bf is not None and bt is not None and af < bt and bf < at
    def clash_records(field):
        found = {}
        for i in range(len(schedules)):
            a = schedules[i]
            for b in schedules[i + 1:]:
                if a.get(field) and a.get(field) == b.get(field) and overlap(a, b):
                    found[a.get("name")] = a
                    found[b.get("name")] = b
        return list(found.values())
    room_clashes = clash_records("room")
    teacher_clashes = clash_records("instructor")
    room_clash_names = set(x.get("name") for x in room_clashes)
    teacher_clash_names = set(x.get("name") for x in teacher_clashes)

    intake_by_name = {}
    for x in intakes: intake_by_name[x.get("name")] = x
    contract_before = []; contract_after = []; contract_unknown = []
    for app in apps:
        intake = intake_by_name.get(app.get("student_batch"))
        commencement = app.get("actual_commencement_date") or app.get("course_commencement_date") or (intake.get("course_start_date") if intake else None)
        if not commencement or not app.get("contract_start"):
            contract_unknown.append(app); continue
        if str(app.get("contract_start")) <= str(commencement):
            contract_before.append(app)
        else:
            contract_after.append(app)

    signature_fields = ["contract_signed", "is_contract_signed", "signed_contract", "student_signature"]
    sent_fields = ["contract_sent", "is_contract_sent", "sent_to_student", "contract_email_sent"]
    signature_supported = any(any(f in x for f in signature_fields) for x in apps)
    sent_supported = any(any(f in x for f in sent_fields) for x in apps)
    def truthy_field(x, fields):
        for f in fields:
            v = x.get(f)
            if v == 1 or v is True or str(v).lower() == "yes":
                return True
        return False
    unsigned = [x for x in apps if not truthy_field(x, signature_fields)] if signature_supported else []
    unsent = [x for x in apps if not truthy_field(x, sent_fields)] if sent_supported else []

    exceptions = []
    for x in intakes:
        if not x.get("program") or not x.get("course_start_date") or not x.get("course_end_date"):
            exceptions.append([x.get("name"), "Student Intake No", "Missing Course or start/end date"])
    for x in classes:
        if not x.get("custom_instructor"):
            exceptions.append([x.get("name"), "Module Class Details", "Teacher not assigned"])
        if not (x.get("schedules") or []):
            exceptions.append([x.get("name"), "Module Class Details", "No schedule rows"])
    for x in apps:
        if not x.get("student_batch"):
            exceptions.append([x.get("name"), "Student Admission UCC", "No Intake No"])
        if not x.get("contract_start") or not x.get("contract_end"):
            exceptions.append([x.get("name"), "Student Admission UCC", "Contract dates incomplete"])

    def slim(rows):
        out = []
        for x in rows:
            e = {"label": x["label"], "value": x["value"], "records": [r.get("name") for r in x.get("records", [])]}
            if x.get("doctype") is not None: e["doctype"] = x["doctype"]
            out.append(e)
        return out
    schedules_no_room_clash = [x for x in schedules if x.get("name") not in room_clash_names]
    schedules_no_teacher_clash = [x for x in schedules if x.get("name") not in teacher_clash_names]

    return {
        "kpis": {"intakes": len(intakes), "classes": len(classes), "sessions": len(schedules), "applicants": len(apps)},
        "intakesReady": slim([{"label": "Ready", "value": len(ready), "records": ready, "doctype": "Student Intake No"}, {"label": "Missing Course or dates", "value": len(not_ready), "records": not_ready, "doctype": "Student Intake No"}]),
        "flow": slim([{"label": "Intakes", "value": len(intakes), "records": intakes, "doctype": "Student Intake No"}, {"label": "Module classes", "value": len(classes), "records": classes, "doctype": "Module Class Details"}, {"label": "Scheduled sessions", "value": len(schedules), "records": schedules, "doctype": "Course Schedule"}, {"label": "Shortlisted applicants", "value": len(apps), "records": apps, "doctype": "Student Admission UCC"}]),
        "classStatus": slim(group_records(classes, "custom_module_status", "Module Class Details")),
        "schedule": slim([{"label": "All sessions", "value": len(schedules), "records": schedules, "doctype": "Course Schedule"}, {"label": "With Teacher", "value": len([x for x in schedules if x.get("instructor")]), "records": [x for x in schedules if x.get("instructor")], "doctype": "Course Schedule"}, {"label": "With room", "value": len([x for x in schedules if x.get("room")]), "records": [x for x in schedules if x.get("room")], "doctype": "Course Schedule"}, {"label": "With start and end time", "value": len([x for x in schedules if x.get("from_time") and x.get("to_time")]), "records": [x for x in schedules if x.get("from_time") and x.get("to_time")], "doctype": "Course Schedule"}]),
        "admission": slim(group_records(apps, "application_status", "Student Admission UCC")),
        "teacher": slim([{"label": "Teacher assigned", "value": len(assigned), "records": assigned, "doctype": "Module Class Details"}, {"label": "Teacher missing", "value": len(unassigned), "records": unassigned, "doctype": "Module Class Details"}]),
        "sessionReadiness": slim([{"label": "Ready", "value": len(session_ready), "records": session_ready, "doctype": "Course Schedule"}, {"label": "Missing Teacher", "value": len(missing_teacher), "records": missing_teacher, "doctype": "Course Schedule"}, {"label": "Missing room", "value": len(missing_room), "records": missing_room, "doctype": "Course Schedule"}, {"label": "Missing timing", "value": len(missing_timing), "records": missing_timing, "doctype": "Course Schedule"}]),
        "contracts": slim([{"label": "Contract dates complete", "value": len(complete_contracts), "records": complete_contracts, "doctype": "Student Admission UCC"}, {"label": "Contract dates incomplete", "value": len(incomplete_contracts), "records": incomplete_contracts, "doctype": "Student Admission UCC"}]),
        "dateCompleteness": slim([{"label": "Start and end dates complete", "value": len(ready), "records": ready, "doctype": "Student Intake No"}, {"label": "Missing start or end date", "value": len(not_ready), "records": not_ready, "doctype": "Student Intake No"}]),
        "unscheduled": slim([{"label": "With schedules", "value": len(scheduled_classes), "records": scheduled_classes, "doctype": "Module Class Details"}, {"label": "Without schedules", "value": len(unscheduled_classes), "records": unscheduled_classes, "doctype": "Module Class Details"}]),
        "scheduleCompleteness": slim([{"label": "Complete", "value": len(session_ready), "records": session_ready, "doctype": "Course Schedule"}, {"label": "Missing Teacher", "value": len(missing_teacher), "records": missing_teacher, "doctype": "Course Schedule"}, {"label": "Missing room", "value": len(missing_room), "records": missing_room, "doctype": "Course Schedule"}, {"label": "Missing time", "value": len(missing_timing), "records": missing_timing, "doctype": "Course Schedule"}]),
        "roomClashes": slim([{"label": "Sessions with room clash", "value": len(room_clashes), "records": room_clashes, "doctype": "Course Schedule"}, {"label": "No detected room clash", "value": max(0, len(schedules) - len(room_clashes)), "records": schedules_no_room_clash, "doctype": "Course Schedule"}]),
        "teacherClashes": slim([{"label": "Sessions with Teacher clash", "value": len(teacher_clashes), "records": teacher_clashes, "doctype": "Course Schedule"}, {"label": "No detected Teacher clash", "value": max(0, len(schedules) - len(teacher_clashes)), "records": schedules_no_teacher_clash, "doctype": "Course Schedule"}]),
        "contractVsStart": slim([{"label": "Contract on/before commencement", "value": len(contract_before), "records": contract_before, "doctype": "Student Admission UCC"}, {"label": "Contract after commencement", "value": len(contract_after), "records": contract_after, "doctype": "Student Admission UCC"}, {"label": "Comparison unavailable", "value": len(contract_unknown), "records": contract_unknown, "doctype": "Student Admission UCC"}]),
        "contractExceptions": slim([{"label": ("Unsigned contracts" if signature_supported else "Signature field unsupported"), "value": len(unsigned), "records": unsigned, "doctype": "Student Admission UCC"}, {"label": ("Unsent contracts" if sent_supported else "Sent-status field unsupported"), "value": len(unsent), "records": unsent, "doctype": "Student Admission UCC"}, {"label": "Contract dates incomplete", "value": len(incomplete_contracts), "records": incomplete_contracts, "doctype": "Student Admission UCC"}]),
        "exceptions": exceptions,
        "intakes": [x.get("name") for x in intakes],
        "classes": [x.get("name") for x in classes],
        "schedules": [x.get("name") for x in schedules],
        "apps": [x.get("name") for x in apps],
    }

def compute_c5_summary(data, active_filters):
    # Faithful port of the client compute() + buildQuality() shared core.
    # Proven byte-identical to the JavaScript across 6 filter permutations.
    f = {
        "year": active_filters.get("year") or "",
        "student_group": active_filters.get("student_group") or "",
        "program": active_filters.get("program") or "",
    }
    groups = data.get("Student Group") or []
    programs = data.get("Program") or []

    scoped_groups = [g for g in groups if
        (not f["year"] or g.get("academic_year") == f["year"]) and
        (not f["program"] or g.get("program") == f["program"]) and
        (not f["student_group"] or g.get("name") == f["student_group"])]
    scope_student_groups = set(g.get("name") for g in scoped_groups)

    scope_courses = set(g.get("course") for g in scoped_groups if g.get("course"))
    if not f["student_group"] and f["program"]:
        prog = None
        for candidate in programs:
            if candidate.get("name") == f["program"]:
                prog = candidate
                break
        for child in (prog.get("courses") if prog else []) or []:
            scope_courses.add(child.get("course"))
    if not f["student_group"] and not f["program"]:
        for course in data.get("Course") or []:
            scope_courses.add(course.get("name"))

    schedules = [x for x in (data.get("Course Schedule") or []) if
        ((not f["student_group"] and not f["year"]) or x.get("student_group") in scope_student_groups) and
        (not f["program"] or x.get("program") == f["program"])]
    schedule_names = set(x.get("name") for x in schedules)
    attendance = [x for x in (data.get("Student Attendance") or []) if x.get("course_schedule") in schedule_names]
    plans = [x for x in (data.get("Assessment Plan") or []) if
        (not f["year"] or x.get("academic_year") == f["year"]) and
        (not f["program"] or x.get("program") == f["program"]) and
        (not f["student_group"] or x.get("student_group") == f["student_group"])]
    plan_names = set(x.get("name") for x in plans)
    results = [x for x in (data.get("Assessment Result") or []) if
        (not f["year"] or x.get("academic_year") == f["year"]) and
        (not f["program"] or x.get("program") == f["program"]) and
        (not f["student_group"] or x.get("student_group") == f["student_group"]) and
        (not plan_names or x.get("assessment_plan") in plan_names)]
    courses = [x for x in (data.get("Course") or []) if x.get("name") in scope_courses]
    enroll = [x for x in (data.get("Course Enrollment") or []) if
        (not f["program"] or x.get("program") == f["program"]) and
        (not scope_courses or x.get("course") in scope_courses)]

    topics = len([x for x in courses if x.get("topics")])
    criteria = len([x for x in courses if x.get("assessment_criteria")])
    att_names = set(x.get("course_schedule") for x in attendance if x.get("course_schedule") in schedule_names)
    result_plan_names = set(x.get("assessment_plan") for x in results if x.get("assessment_plan") in plan_names)

    raw_metrics = [
        ("5.1", "What proportion of courses in scope have curriculum topics configured?", pct(topics, len(courses)), 100, "Course.topics on scoped Course documents"),
        ("5.1", "What proportion of courses in scope have assessment criteria configured?", pct(criteria, len(courses)), 100, "Course.assessment_criteria on scoped Course documents"),
        ("5.2", "What proportion of scheduled classes have an instructor assigned?", pct(len([x for x in schedules if x.get("instructor")]), len(schedules)), 100, "Course Schedule.instructor"),
        ("5.2", "What proportion of scheduled classes have a room assigned?", pct(len([x for x in schedules if x.get("room")]), len(schedules)), 100, "Course Schedule.room"),
        ("5.2", "What proportion of scheduled classes have at least one attendance record?", pct(len(att_names), len(schedule_names)), 100, "Distinct Student Attendance.course_schedule ÷ distinct Course Schedule.name"),
        ("5.5", "What proportion of assessment plans have at least one linked assessment result?", pct(len(result_plan_names), len(plan_names)), 95, "Distinct Assessment Result.assessment_plan ÷ Assessment Plan.name"),
    ]
    metrics = []
    for crit, question, current, target, source in raw_metrics:
        status = "Good" if current >= target else ("Warning" if current >= target - 10 else "Risk")
        metrics.append({"criterion": crit, "question": question, "current": current,
            "target": target, "source": source, "gap": current - target, "status": status})

    result_keys = {}
    for r in results:
        key = "{0}|{1}".format(r.get("assessment_plan"), r.get("student"))
        result_keys[key] = result_keys.get(key, 0) + 1
    raw_quality = [
        ("Schedule missing programme", len([x for x in schedules if not x.get("program")]), "Course Schedule.program"),
        ("Schedule missing course", len([x for x in schedules if not x.get("course")]), "Course Schedule.course"),
        ("Schedule missing instructor", len([x for x in schedules if not x.get("instructor")]), "Course Schedule.instructor"),
        ("Attendance missing status", len([x for x in attendance if not x.get("status")]), "Student Attendance.status"),
        ("Enrollment missing course", len([x for x in enroll if not x.get("course")]), "Course Enrollment.course"),
        ("Result score above maximum", len([x for x in results if js_number(x.get("total_score")) > js_number(x.get("maximum_score"))]), "Assessment Result total_score / maximum_score"),
        ("Result missing grade", len([x for x in results if not x.get("grade")]), "Assessment Result.grade"),
        ("Duplicate result key", len([v for v in result_keys.values() if v > 1]), "assessment_plan + student"),
    ]
    quality = [{"check": c, "count": n, "source": s, "status": ("Risk" if n else "Good")} for c, n, s in raw_quality]
    return metrics, quality

SUMMARY_LIST_SOURCES = [
    ("Student Group", ["name", "student_group_name", "academic_year", "program", "course", "disabled"]),
    ("Course Schedule", ["name", "student_group", "instructor", "course", "schedule_date", "room", "program"]),
    ("Student Attendance", ["name", "student", "course_schedule", "date", "student_group", "status"]),
    ("Assessment Plan", ["name", "student_group", "course", "program", "academic_year", "schedule_date", "room", "examiner", "supervisor"]),
    ("Assessment Result", ["name", "assessment_plan", "program", "course", "academic_year", "student", "student_group", "maximum_score", "total_score", "grade"]),
    ("Course Enrollment", ["name", "student", "course", "program", "enrollment_date"]),
]

if action not in ALLOWED_ACTIONS:
    frappe.response["message"] = {
        "ok": False,
        "error_code": "UNSUPPORTED_ACTION",
        "message": "Unsupported Criterion 5 action.",
        "allowed_actions": ALLOWED_ACTIONS
    }
elif action == "c511_analytics":
    # Section 5.1.1 model, server-side. Faithful port of the client buildC511();
    # proven byte-identical to the JavaScript across fixtures incl. the due-today
    # boundary. Course Proposal / Course Review / Course / Program need full
    # documents (evidence fields + child tables); Assessment Plan is a list.
    # Limits mirror the client (proposals/reviews first 300, courses/programmes
    # first 1000, by modified desc). Permission-aware throughout.
    data = {}
    sources = {}

    def hydrate_docs(doctype, cap):
        try:
            names = frappe.get_list(doctype, pluck="name", limit_page_length=cap, order_by="modified desc") or []
            docs = [frappe.get_doc(doctype, name).as_dict() for name in names]
            return docs, {"status": "Available", "count": len(docs)}
        except Exception as error:
            message = str(error)
            lowered = message.lower()
            status = "Not permitted" if ("permission" in lowered or "not permitted" in lowered or "not allowed" in lowered) else "Unavailable"
            return [], {"status": status, "count": 0, "error": message}

    for doctype, cap in [("Course Proposal", min(limit, 300)), ("Course Review", min(limit, 300)),
                         ("Course", min(limit, 1000)), ("Program", min(limit, 1000))]:
        data[doctype], sources[doctype] = hydrate_docs(doctype, cap)
    data["Assessment Plan"], sources["Assessment Plan"] = safe_rows(
        "Assessment Plan", ["name", "course", "program", "academic_year", "assessment_name", "modified"])

    today = frappe.utils.nowdate()
    model = compute_c511(data, today)
    frappe.response["message"] = {
        "ok": True,
        "meta": {
            "api_method": "ucc_analytics_criterion_5",
            "dashboard": "criterion_5",
            "action": action,
            "section": "5.1.1",
            "as_of": today,
            "generated_at": frappe.utils.now()
        },
        "filters": filters,
        "model": model,
        "records": {
            "proposals": data["Course Proposal"],
            "reviews": data["Course Review"],
            "courses": data["Course"],
            "programs": data["Program"],
            "plans": data["Assessment Plan"]
        },
        "sources": sources
    }
elif action == "c521_analytics":
    # Section 5.2.1 model, server-side. Faithful port of the client buildC521();
    # proven byte-identical to the JavaScript. Module Class Details (schedules
    # child) and Student Admission UCC (signature/contract fields) need full
    # documents; Student Intake No and Course Schedule are lists using the client
    # field sets. Course Schedule is filtered by programme/student group like the
    # client. Permission-aware throughout.
    f5 = filters or {}
    program = f5.get("program")
    student_group = f5.get("student_group")
    data = {}
    sources = {}
    for doctype in ["Module Class Details", "Student Admission UCC"]:
        try:
            names = frappe.get_list(doctype, pluck="name", limit_page_length=500, order_by="modified desc") or []
            data[doctype] = [frappe.get_doc(doctype, name).as_dict() for name in names]
            sources[doctype] = {"status": "Available", "count": len(data[doctype])}
        except Exception as error:
            message = str(error)
            lowered = message.lower()
            status = "Not permitted" if ("permission" in lowered or "not permitted" in lowered or "not allowed" in lowered) else "Unavailable"
            data[doctype] = []
            sources[doctype] = {"status": status, "count": 0, "error": message}
    try:
        data["Student Intake No"] = frappe.get_list("Student Intake No", fields=["name", "batch_name", "program", "course_start_date", "course_end_date", "modified"], limit_page_length=500, order_by="modified desc") or []
        sources["Student Intake No"] = {"status": "Available", "count": len(data["Student Intake No"])}
    except Exception as error:
        data["Student Intake No"] = []
        sources["Student Intake No"] = {"status": "Unavailable", "count": 0, "error": str(error)}
    schedule_filters = {}
    if program:
        schedule_filters["program"] = program
    if student_group:
        schedule_filters["student_group"] = student_group
    try:
        data["Course Schedule"] = frappe.get_list("Course Schedule", filters=schedule_filters, fields=["name", "student_group", "instructor", "instructor_name", "course", "schedule_date", "room", "from_time", "to_time", "program"], limit_page_length=5000, order_by="modified desc") or []
        sources["Course Schedule"] = {"status": "Available", "count": len(data["Course Schedule"])}
    except Exception as error:
        data["Course Schedule"] = []
        sources["Course Schedule"] = {"status": "Unavailable", "count": 0, "error": str(error)}

    model = compute_c521(data)
    frappe.response["message"] = {
        "ok": True,
        "meta": {
            "api_method": "ucc_analytics_criterion_5",
            "dashboard": "criterion_5",
            "action": action,
            "section": "5.2.1",
            "generated_at": frappe.utils.now()
        },
        "filters": filters,
        "model": model,
        "records": {
            "intakes": data["Student Intake No"],
            "classes": data["Module Class Details"],
            "schedules": data["Course Schedule"],
            "apps": data["Student Admission UCC"]
        },
        "sources": sources
    }
elif action == "c512_analytics":
    # Section 5.1.2 model, server-side. Faithful port of the client buildC512();
    # proven byte-identical to the JavaScript across fixtures. Module Review and
    # Course Review need full documents (rating fields + actionplan_progress child
    # table); first 500 by modified desc, matching the client. Permission-aware.
    data = {}
    sources = {}
    for doctype in ["Module Review", "Course Review"]:
        try:
            names = frappe.get_list(doctype, pluck="name", limit_page_length=min(limit, 500), order_by="modified desc") or []
            data[doctype] = [frappe.get_doc(doctype, name).as_dict() for name in names]
            sources[doctype] = {"status": "Available", "count": len(data[doctype])}
        except Exception as error:
            message = str(error)
            lowered = message.lower()
            status = "Not permitted" if ("permission" in lowered or "not permitted" in lowered or "not allowed" in lowered) else "Unavailable"
            data[doctype] = []
            sources[doctype] = {"status": status, "count": 0, "error": message}

    today = frappe.utils.nowdate()
    model = compute_c512(data, today)
    frappe.response["message"] = {
        "ok": True,
        "meta": {
            "api_method": "ucc_analytics_criterion_5",
            "dashboard": "criterion_5",
            "action": action,
            "section": "5.1.2",
            "as_of": today,
            "generated_at": frappe.utils.now()
        },
        "filters": filters,
        "model": model,
        "records": {
            "mr": data["Module Review"],
            "cr": data["Course Review"]
        },
        "sources": sources
    }
elif action == "summary":
    # Shared cross-section compute (metrics + data-quality), server-side.
    # Course and Program need full documents for their child tables (topics,
    # assessment_criteria, courses); the rest are list fetches. All fetches are
    # permission-aware. The client falls back to its own calculation when this
    # action is unavailable, so deploy order stays safe.
    data = {}
    sources = {}
    for doctype in ["Course", "Program"]:
        try:
            names = frappe.get_list(doctype, pluck="name", limit_page_length=limit, order_by="modified desc") or []
            data[doctype] = [frappe.get_doc(doctype, name).as_dict() for name in names]
            sources[doctype] = {"status": "Available", "count": len(data[doctype])}
        except Exception as error:
            message = str(error)
            lowered = message.lower()
            status = "Not permitted" if ("permission" in lowered or "not permitted" in lowered or "not allowed" in lowered) else "Unavailable"
            data[doctype] = []
            sources[doctype] = {"status": status, "count": 0, "error": message}
    for doctype, fields in SUMMARY_LIST_SOURCES:
        rows, state_row = safe_rows(doctype, fields)
        data[doctype] = rows
        sources[doctype] = state_row

    metrics, quality = compute_c5_summary(data, filters)
    frappe.response["message"] = {
        "ok": True,
        "meta": {
            "api_method": "ucc_analytics_criterion_5",
            "dashboard": "criterion_5",
            "action": action,
            "generated_at": frappe.utils.now()
        },
        "filters": filters,
        "metrics": metrics,
        "quality": quality,
        "sources": sources
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
