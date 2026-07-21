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
    "c522_analytics",
    "c531_analytics",
    "c511_hydrate",
    "c511_summary",
    "c511_proposals",
    "c511_modules",
    "c511_reviews",
    "c511_gaps",
    "c5_qa"
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

def numeric_rating(v):
    if v is None or v == "":
        n = 0.0
    elif v is True:
        n = 1.0
    elif v is False:
        n = 0.0
    else:
        try:
            n = float(v)
        except (TypeError, ValueError):
            n = float("nan")
    if n != n:
        return None
    return n * 5 if n <= 1 else n

RATING_FIELDS = {
    "Preparation": ["availability_of_learning_materials_likert", "lesson_aligned_likert", "lesson_plan_alignment_likert", "lesson_objective_likert"],
    "Delivery": ["relevance_likert", "mastery_likert", "transition_likert", "pacing_likert", "educational_tools_likert", "teaching_style_likert"],
    "Class dynamics": ["able_to_maintain_order_in_class_likert", "good_rapport_with_students_likert", "teacher_attentive_likert", "timely_likert"],
    "Communication": ["simple_language_likert", "teacher_confident_likert", "good_balance_likert", "vocal_likert", "teacher_encourage_likert", "non_verbal_likert"],
}
RATING_ORDER = ["Preparation", "Delivery", "Class dynamics", "Communication"]
FLAT_RATING_FIELDS = [f for g in RATING_ORDER for f in RATING_FIELDS[g]]

def compute_c522(d, today):
    obs = d.get("Classroom Observation") or []
    classes = d.get("Module Class Details") or []
    surveys = d.get("Survey Response") or []
    schedules = d.get("Course Schedule") or []
    attendance = d.get("Student Attendance") or []

    def ratings_of(o, fields):
        out = []
        for f in fields:
            r = numeric_rating(o.get(f))
            if r is not None:
                out.append(r)
        return out
    all_ratings = []
    for o in obs:
        all_ratings.extend(ratings_of(o, FLAT_RATING_FIELDS))
    observed_class_names = set(x.get("module_class_details") for x in obs if x.get("module_class_details"))
    observed_classes = [x for x in classes if x.get("name") in observed_class_names]
    unobserved_classes = [x for x in classes if x.get("name") not in observed_class_names]
    area_rows = []
    for label in RATING_ORDER:
        vals = []
        for o in obs:
            vals.extend(ratings_of(o, RATING_FIELDS[label]))
        area_rows.append({"label": label, "value": (sum(vals) / len(vals) if vals else 0), "records": obs, "doctype": "Classroom Observation"})

    category_map = {}
    for survey in surveys:
        for response in (survey.get("response") or []):
            label = response.get("category") or "Uncategorised"
            category_map.setdefault(label, {})[survey.get("name")] = survey
    survey_categories = []
    for label, m in category_map.items():
        val = 0
        for survey in m.values():
            val += len([row for row in (survey.get("response") or []) if (row.get("category") or "Uncategorised") == label])
        survey_categories.append({"label": label, "value": val, "records": list(m.values()), "doctype": "Survey Response"})
    survey_categories.sort(key=lambda x: -x["value"])

    both_signed = [x for x in obs if x.get("observers_signature") and x.get("teachers_signature")]
    observer_only = [x for x in obs if x.get("observers_signature") and not x.get("teachers_signature")]
    teacher_only = [x for x in obs if not x.get("observers_signature") and x.get("teachers_signature")]
    unsigned = [x for x in obs if not x.get("observers_signature") and not x.get("teachers_signature")]

    def strip_tags(v):
        s = str(v); out = []; i = 0; n = len(s)
        while i < n:
            if s[i] == "<":
                j = s.find(">", i + 1)
                if j != -1 and j > i + 1:
                    i = j + 1; continue
            out.append(s[i]); i += 1
        return "".join(out)
    concerns = [x for x in obs if strip_tags(x.get("areas_text") or "").strip()]
    concern_names = set(x.get("name") for x in concerns)
    no_concerns = [x for x in obs if x.get("name") not in concern_names]

    delivered_schedule_names = set(x.get("course_schedule") for x in attendance if x.get("course_schedule"))
    delivered_schedules = [x for x in schedules if x.get("name") in delivered_schedule_names]
    undelivered_schedules = [x for x in schedules if x.get("name") not in delivered_schedule_names]

    teachers = []
    seen_t = set()
    for x in classes:
        t = x.get("custom_instructor_full_name") or x.get("custom_instructor")
        if t and t not in seen_t:
            seen_t.add(t); teachers.append(t)
    observed_teachers = set(x.get("name_of_teacher") for x in obs if x.get("name_of_teacher"))

    def is_scheduled(x):
        t = str(x.get("type_of_observation") or "").lower()
        return ("scheduled" in t) or ("formal" in t) or bool(x.get("course_schedule"))
    scheduled_obs = [x for x in obs if is_scheduled(x)]
    scheduled_names = set(x.get("name") for x in scheduled_obs)
    adhoc_obs = [x for x in obs if x.get("name") not in scheduled_names]

    unsigned_obs = [x for x in obs if not (x.get("observers_signature") and x.get("teachers_signature"))]
    def age(x):
        if not x.get("date_of_observation"):
            return None
        return frappe.utils.date_diff(today, x.get("date_of_observation"))
    signoff_aging = [
        {"label": "0–7 days", "records": [x for x in unsigned_obs if age(x) is not None and age(x) <= 7]},
        {"label": "8–30 days", "records": [x for x in unsigned_obs if age(x) is not None and 7 < age(x) <= 30]},
        {"label": "31+ days", "records": [x for x in unsigned_obs if age(x) is not None and age(x) > 30]},
        {"label": "No observation date", "records": [x for x in unsigned_obs if not x.get("date_of_observation")]},
    ]
    observation_averages = []
    for record in obs:
        vals = ratings_of(record, FLAT_RATING_FIELDS)
        avg = (sum(vals) / len(vals)) if vals else None
        observation_averages.append((record, avg))
    band_45 = [r for r, a in observation_averages if a is not None and a >= 4]
    band_34 = [r for r, a in observation_averages if a is not None and a >= 3 and a < 4]
    band_below = [r for r, a in observation_averages if a is not None and a < 3]
    band_none = [r for r, a in observation_averages if a is None]

    def text_present(x, fields):
        return any(strip_tags(x.get(f) or "").strip() for f in fields)
    strength_fields = ["strengths", "strengths_text", "positive_observations", "good_practices"]
    improvement_fields = ["areas_text", "areas_for_improvement", "improvement_areas", "recommendations"]
    strength_rows = [x for x in obs if text_present(x, strength_fields)]
    strength_names = set(x.get("name") for x in strength_rows)
    improvement_rows = [x for x in obs if text_present(x, improvement_fields)]
    improvement_names = set(x.get("name") for x in improvement_rows)

    survey_months = {}
    for x in surveys:
        month = str(x.get("posting_date") or x.get("modified") or "No date")[:7]
        survey_months.setdefault(month, []).append(x)
    survey_volume = []
    for month in sorted(survey_months.keys()):
        recs = survey_months[month]
        survey_volume.append({"label": month, "value": sum(max(1, len(x.get("response") or [])) for x in recs), "records": recs, "doctype": "Survey Response"})

    def slim(rows):
        out = []
        for x in rows:
            e = {"label": x["label"], "value": x["value"], "records": [r.get("name") for r in x.get("records", [])]}
            if x.get("doctype") is not None: e["doctype"] = x["doctype"]
            out.append(e)
        return out
    return {
        "kpis": {"observations": len(obs), "observationScoreAvg": (sum(all_ratings) / len(all_ratings) if all_ratings else None), "surveys": len(surveys), "unobserved": len(unobserved_classes)},
        "coverage": slim([{"label": "Observed Module classes", "value": len(observed_classes), "records": observed_classes, "doctype": "Module Class Details"}, {"label": "Without observation", "value": len(unobserved_classes), "records": unobserved_classes, "doctype": "Module Class Details"}]),
        "observationType": slim(group_records(obs, "type_of_observation", "Classroom Observation")),
        "platform": slim(group_records(obs, "platform_delivery", "Classroom Observation")),
        "ratings": slim(area_rows),
        "surveyCategories": slim(survey_categories),
        "notice": slim(group_records(obs, "prior_notice", "Classroom Observation")),
        "signoff": slim([{"label": "Both signed", "value": len(both_signed), "records": both_signed, "doctype": "Classroom Observation"}, {"label": "Observer only", "value": len(observer_only), "records": observer_only, "doctype": "Classroom Observation"}, {"label": "Teacher only", "value": len(teacher_only), "records": teacher_only, "doctype": "Classroom Observation"}, {"label": "Unsigned", "value": len(unsigned), "records": unsigned, "doctype": "Classroom Observation"}]),
        "concerns": slim([{"label": "Areas for improvement recorded", "value": len(concerns), "records": concerns, "doctype": "Classroom Observation"}, {"label": "No areas recorded", "value": len(no_concerns), "records": no_concerns, "doctype": "Classroom Observation"}]),
        "plannedDelivered": slim([{"label": "Planned sessions", "value": len(schedules), "records": schedules, "doctype": "Course Schedule"}, {"label": "Delivered / attendance captured", "value": len(delivered_schedules), "records": delivered_schedules, "doctype": "Course Schedule"}, {"label": "No delivery evidence", "value": len(undelivered_schedules), "records": undelivered_schedules, "doctype": "Course Schedule"}]),
        "teacherCoverage": slim([{"label": "Teachers observed", "value": len([x for x in teachers if x in observed_teachers]), "records": [x for x in obs if x.get("name_of_teacher") in observed_teachers], "doctype": "Classroom Observation"}, {"label": "Teachers not observed", "value": len([x for x in teachers if x not in observed_teachers]), "records": [x for x in classes if (x.get("custom_instructor_full_name") or x.get("custom_instructor")) not in observed_teachers], "doctype": "Module Class Details"}]),
        "moduleCoverage": slim(group_records(obs, "module_name", "Classroom Observation")),
        "observationMode": slim([{"label": "Scheduled / formal", "value": len(scheduled_obs), "records": scheduled_obs, "doctype": "Classroom Observation"}, {"label": "Ad-hoc / other", "value": len(adhoc_obs), "records": adhoc_obs, "doctype": "Classroom Observation"}]),
        "signoffAging": slim([{"label": g["label"], "value": len(g["records"]), "records": g["records"], "doctype": "Classroom Observation"} for g in signoff_aging]),
        "ratingDistribution": slim([{"label": "4.0–5.0", "value": len(band_45), "records": band_45, "doctype": "Classroom Observation"}, {"label": "3.0–3.9", "value": len(band_34), "records": band_34, "doctype": "Classroom Observation"}, {"label": "Below 3.0", "value": len(band_below), "records": band_below, "doctype": "Classroom Observation"}, {"label": "Not rated", "value": len(band_none), "records": band_none, "doctype": "Classroom Observation"}]),
        "strengths": slim([{"label": "Strengths recorded", "value": len(strength_rows), "records": strength_rows, "doctype": "Classroom Observation"}, {"label": "No strengths recorded", "value": len(obs) - len(strength_rows), "records": [x for x in obs if x.get("name") not in strength_names], "doctype": "Classroom Observation"}]),
        "improvements": slim([{"label": "Improvement areas recorded", "value": len(improvement_rows), "records": improvement_rows, "doctype": "Classroom Observation"}, {"label": "No improvement area recorded", "value": len(obs) - len(improvement_rows), "records": [x for x in obs if x.get("name") not in improvement_names], "doctype": "Classroom Observation"}]),
        "surveyVolume": slim(survey_volume),
        "deliveryExceptions": slim([{"label": "Module classes without observation", "value": len(unobserved_classes), "records": unobserved_classes, "doctype": "Module Class Details"}, {"label": "Observations awaiting full sign-off", "value": len(unsigned_obs), "records": unsigned_obs, "doctype": "Classroom Observation"}, {"label": "Observations below rating threshold", "value": len(band_below), "records": band_below, "doctype": "Classroom Observation"}, {"label": "No delivery evidence", "value": len(undelivered_schedules), "records": undelivered_schedules, "doctype": "Course Schedule"}]),
        "obs": [x.get("name") for x in obs],
        "surveys": [x.get("name") for x in surveys],
    }

def compute_c531(d, today, in90):
    signed = d.get("Partnership Agreement") or []
    managed = d.get("Partnerships Agreement Management") or []
    ratings = d.get("Supplier Rating") or []

    def dstr(v):
        return str(v)[:10] if v else None
    monitoring = []
    for parent in managed:
        for row in (parent.get("monitoring_childtable") or []):
            rr = dict(row); rr["name"] = parent.get("name"); rr["_doctype"] = "Partnerships Agreement Management"; monitoring.append(rr)
    evaluations = []
    for parent in managed:
        for row in (parent.get("table_luoo") or []):
            rr = dict(row); rr["name"] = parent.get("name"); rr["_doctype"] = "Partnerships Agreement Management"; evaluations.append(rr)

    signed_status = []
    for x in signed:
        end = dstr(x.get("end_date")); start = dstr(x.get("start_date"))
        status = "Expired" if (end and end < today) else ("Upcoming" if (start and start > today) else "Active")
        xx = dict(x); xx["derived_status"] = status; signed_status.append(xx)

    expired = [x for x in signed if x.get("end_date") and dstr(x.get("end_date")) < today]
    expiring = [x for x in signed if x.get("end_date") and dstr(x.get("end_date")) >= today and dstr(x.get("end_date")) <= in90]
    later = [x for x in signed if x.get("end_date") and dstr(x.get("end_date")) > in90]
    no_end = [x for x in signed if not x.get("end_date")]
    nda_not_required = [x for x in signed if not x.get("requires_nda")]
    nda_complete = [x for x in signed if x.get("requires_nda") and x.get("nda_acknowledged")]
    nda_incomplete = [x for x in signed if x.get("requires_nda") and not x.get("nda_acknowledged")]

    score_rows = []
    for x in managed:
        if js_number(x.get("average_identification_and_selection_score")) > 0:
            score_rows.append({"label": x.get("agreement_title") or x.get("name"), "value": js_number(x.get("average_identification_and_selection_score")), "records": [x], "doctype": "Partnerships Agreement Management"})
    score_rows.sort(key=lambda r: -r["value"])
    passing = [x for x in managed if js_number(x.get("average_identification_and_selection_score")) >= 70]
    below = [x for x in managed if 0 < js_number(x.get("average_identification_and_selection_score")) < 70]
    not_scored = [x for x in managed if not js_number(x.get("average_identification_and_selection_score"))]

    def status_field(x):
        return str(x.get("status") or x.get("agreement_status") or x.get("workflow_state") or "")
    lifecycle = []
    for x in signed:
        explicit = status_field(x).lower()
        end = dstr(x.get("end_date")); start = dstr(x.get("start_date"))
        if "terminat" in explicit:
            derived = "Terminated"
        elif end and end < today:
            derived = "Expired"
        elif end and end <= in90:
            derived = "Expiring"
        elif start and start > today:
            derived = "Upcoming"
        else:
            derived = "Active"
        xx = dict(x); xx["derived_status_v110"] = derived; lifecycle.append(xx)

    party_signature_fields = ["party_signature", "partner_signature", "signed_by_partner", "partner_signed"]
    ucc_signature_fields = ["ucc_signature", "company_signature", "signed_by_ucc", "ucc_signed"]
    def has_field(x, fields):
        return any(f in x for f in fields)
    def has_value(x, fields):
        for f in fields:
            v = x.get(f)
            if v == 1 or v is True or str(v or "").strip() != "":
                return True
        return False
    signature_supported = any(has_field(x, party_signature_fields + ucc_signature_fields) for x in signed)
    both_signed = [x for x in signed if has_value(x, party_signature_fields) and has_value(x, ucc_signature_fields)] if signature_supported else []
    both_names = set(x.get("name") for x in both_signed)
    signature_incomplete = [x for x in signed if x.get("name") not in both_names] if signature_supported else []

    risk_fields = ["risk_level", "partnership_risk", "risk_rating", "average_identification_and_selection_score"]
    risk_supported = any(has_field(x, risk_fields) for x in managed)
    risk_rows = []
    if risk_supported:
        for x in managed:
            label = x.get("risk_level") or x.get("partnership_risk") or x.get("risk_rating")
            if not label and js_number(x.get("average_identification_and_selection_score")):
                label = "Low" if js_number(x.get("average_identification_and_selection_score")) >= 70 else "High"
            xx = dict(x); xx["_risk"] = label or "Not Set"; risk_rows.append(xx)

    latest_monitoring = {}
    for row in monitoring:
        key = row.get("name")
        dv = dstr(row.get("monitoring_date") or row.get("date") or row.get("modified")) or "1970-01-01"
        if key not in latest_monitoring or dv > latest_monitoring[key][0]:
            latest_monitoring[key] = (dv, row)
    recent_managed = []; stale_managed = []; no_monitoring = []
    for parent in managed:
        item = latest_monitoring.get(parent.get("name"))
        if not item:
            no_monitoring.append(parent); continue
        age = frappe.utils.date_diff(today, item[0])
        if age <= 180:
            recent_managed.append(parent)
        else:
            stale_managed.append(parent)

    decision_fields = ["decision", "continuation_decision", "evaluation_decision", "recommended_action"]
    decision_rows = []
    for x in evaluations:
        dec = None
        for f in decision_fields:
            if x.get(f):
                dec = x.get(f); break
        xx = dict(x); xx["_decision"] = dec or x.get("evaluation_outcome") or "Not Set"; decision_rows.append(xx)

    parents_with_monitoring = set(x.get("name") for x in monitoring)
    parents_with_evaluation = set(x.get("name") for x in evaluations)
    without_monitoring = [x for x in managed if x.get("name") not in parents_with_monitoring]
    without_evaluation = [x for x in managed if x.get("name") not in parents_with_evaluation]
    quality_complete = [x for x in managed if x.get("name") in parents_with_monitoring and x.get("name") in parents_with_evaluation and js_number(x.get("average_identification_and_selection_score")) > 0]
    quality_complete_names = set(x.get("name") for x in quality_complete)
    quality_incomplete = [x for x in managed if x.get("name") not in quality_complete_names]

    def slim(rows):
        out = []
        for x in rows:
            e = {"label": x["label"], "value": x["value"], "records": [r.get("name") for r in x.get("records", [])]}
            if x.get("doctype") is not None: e["doctype"] = x["doctype"]
            out.append(e)
        return out
    return {
        "kpis": {"partners": len(signed), "partnersActive": len([x for x in signed_status if x.get("derived_status") == "Active"]), "monitoring": len(monitoring), "evaluations": len(evaluations)},
        "status": slim(group_records(signed_status, "derived_status", "Partnership Agreement")),
        "type": slim(group_records(signed, "pa_agreement_type", "Partnership Agreement")),
        "expiry": slim([{"label": "Expired", "value": len(expired), "records": expired, "doctype": "Partnership Agreement"}, {"label": "Due within 90 days", "value": len(expiring), "records": expiring, "doctype": "Partnership Agreement"}, {"label": "More than 90 days", "value": len(later), "records": later, "doctype": "Partnership Agreement"}, {"label": "No end date", "value": len(no_end), "records": no_end, "doctype": "Partnership Agreement"}]),
        "nda": slim([{"label": "Not required", "value": len(nda_not_required), "records": nda_not_required, "doctype": "Partnership Agreement"}, {"label": "Required and acknowledged", "value": len(nda_complete), "records": nda_complete, "doctype": "Partnership Agreement"}, {"label": "Required but incomplete", "value": len(nda_incomplete), "records": nda_incomplete, "doctype": "Partnership Agreement"}]),
        "monitoring": slim(group_records(monitoring, "monitoring_details", None)),
        "monitoringType": slim(group_records(monitoring, "type_of_monitoring", None)),
        "evaluation": slim(group_records(evaluations, "evaluation_outcome", None)),
        "scores": slim(score_rows),
        "ratingStage": slim(group_records(ratings, "evaluation_stage", "Supplier Rating")),
        "threshold": slim([{"label": "Meets threshold", "value": len(passing), "records": passing, "doctype": "Partnerships Agreement Management"}, {"label": "Below threshold", "value": len(below), "records": below, "doctype": "Partnerships Agreement Management"}, {"label": "Not scored", "value": len(not_scored), "records": not_scored, "doctype": "Partnerships Agreement Management"}]),
        "lifecycle": slim(group_records(lifecycle, "derived_status_v110", "Partnership Agreement")),
        "signature": slim([{"label": ("Both parties signed" if signature_supported else "Signature fields unsupported"), "value": len(both_signed), "records": both_signed, "doctype": "Partnership Agreement"}, {"label": "Signature incomplete", "value": len(signature_incomplete), "records": signature_incomplete, "doctype": "Partnership Agreement"}]),
        "risk": (slim(group_records(risk_rows, "_risk", "Partnerships Agreement Management")) if risk_supported else slim([{"label": "Risk field unsupported", "value": 0, "records": [], "doctype": "Partnerships Agreement Management"}])),
        "monitoringRecency": slim([{"label": "Monitored within 180 days", "value": len(recent_managed), "records": recent_managed, "doctype": "Partnerships Agreement Management"}, {"label": "Monitoring older than 180 days", "value": len(stale_managed), "records": stale_managed, "doctype": "Partnerships Agreement Management"}, {"label": "No monitoring record", "value": len(no_monitoring), "records": no_monitoring, "doctype": "Partnerships Agreement Management"}]),
        "decisions": slim(group_records(decision_rows, "_decision", "Partnerships Agreement Management")),
        "missingControls": slim([{"label": "Without recent monitoring", "value": len(without_monitoring), "records": without_monitoring, "doctype": "Partnerships Agreement Management"}, {"label": "Without evaluation", "value": len(without_evaluation), "records": without_evaluation, "doctype": "Partnerships Agreement Management"}]),
        "qualityCompleteness": slim([{"label": "Core quality record complete", "value": len(quality_complete), "records": quality_complete, "doctype": "Partnerships Agreement Management"}, {"label": "Core quality record incomplete", "value": len(quality_incomplete), "records": quality_incomplete, "doctype": "Partnerships Agreement Management"}]),
        "signedStatus": [{"name": x.get("name"), "derived_status": x.get("derived_status")} for x in signed_status],
    }

def scoped_rows(data, active_filters):
    f = {"year": active_filters.get("year") or "", "student_group": active_filters.get("student_group") or "", "program": active_filters.get("program") or ""}
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
                prog = candidate; break
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
    return {"courses": courses, "schedules": schedules, "attendance": attendance, "plans": plans, "results": results, "enroll": enroll}

def survey_type(row, child):
    ch = child or {}
    text = (str(row.get("title") or "") + " " + str(ch.get("category") or "") + " " + str(ch.get("question") or "")).lower()
    nospace = "".join(text.split())
    if "graduate" in text or "graduation" in text or "alumni" in text:
        return "Graduate Survey"
    if "endofcourse" in nospace or "course survey" in text or "programme survey" in text or "program survey" in text:
        return "End of Course"
    if "endofmodule" in nospace or "module survey" in text or "module feedback" in text:
        return "End of Module"
    return "Other / Unclassified"

def parse_survey_score(value):
    raw = str(value if value is not None else "").strip()
    if not raw:
        return None
    numstr = raw.replace("%", "")
    if numstr == "":
        numeric = 0.0
    else:
        try:
            numeric = float(numstr)
        except (TypeError, ValueError):
            numeric = float("nan")
    if numeric == numeric:  # finite (not NaN)
        return numeric / 20 if "%" in raw else numeric
    key = raw.lower()
    likert = {
        "strongly disagree": 1, "disagree": 2, "neutral": 3, "neither agree nor disagree": 3,
        "agree": 4, "strongly agree": 5,
        "very dissatisfied": 1, "dissatisfied": 2, "satisfied": 4, "very satisfied": 5,
        "poor": 1, "fair": 2, "average": 3, "good": 4, "excellent": 5,
        "never": 1, "rarely": 2, "sometimes": 3, "often": 4, "always": 5,
    }
    return likert.get(key)

def js_round2(x):
    return int(x * 100 + 0.5) / 100

def build_survey_analytics(data, survey_filter):
    docs = data.get("Survey Response") or []
    fmod = survey_filter.get("module") or ""
    ftype = survey_filter.get("type") or ""
    scored = []; comments = []; type_counts = {}
    for doc in docs:
        if fmod and doc.get("course") != fmod:
            continue
        for child in (doc.get("response") if isinstance(doc.get("response"), list) else []):
            t = survey_type(doc, child)
            if ftype and t != ftype:
                continue
            type_counts[t] = type_counts.get(t, 0) + 1
            score = parse_survey_score(child.get("response"))
            base = {"survey_type": t, "module": doc.get("course") or "Not Set", "course": doc.get("program") or "Not Set",
                    "category": child.get("category") or "", "question": child.get("question") or "",
                    "response": child.get("response") or "", "posting_date": doc.get("posting_date") or "", "survey": doc.get("name")}
            if score is not None:
                b = dict(base); b["score"] = score; scored.append(b)
            elif str(child.get("response") or "").strip():
                comments.append(base)
    def avg_by(rows, key):
        m = {}
        for r in rows:
            k = r.get(key) or "Not Set"
            v = m.get(k) or {"sum": 0, "count": 0}
            v["sum"] = v["sum"] + r["score"]; v["count"] = v["count"] + 1; m[k] = v
        out = [{"label": label, "value": js_round2(v["sum"] / v["count"]), "count": v["count"]} for label, v in m.items()]
        out.sort(key=lambda x: -x["value"])
        return out
    docs_filtered = [dd for dd in docs if (not fmod or dd.get("course") == fmod)]
    return {"docs": docs_filtered, "scored": scored, "comments": comments,
            "typeCounts": [{"label": label, "value": value} for label, value in type_counts.items()],
            "moduleScores": avg_by(scored, "module"), "questionScores": avg_by(scored, "question")}

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

# ---- makeQA server port (compute_c5_qa) ----
# Faithful port of the client makeQA(); proven byte-identical to the JavaScript
# across main + partial-sources + filtered + survey-filter + empty fixtures.
# Answer text is gated on the client-supplied source availability so the
# rendered QA rows match the live client exactly regardless of load state.
def qa_group(rows, key):
    m = {}
    for r in (rows or []):
        k = (r.get(key) if r else None) or "Not Set"
        m[k] = m.get(k, 0) + 1
    out = [{"label": k, "value": v} for k, v in m.items()]
    out.sort(key=lambda x: -x["value"])
    return out

def group_join(rows, key):
    return ", ".join("{0}: {1}".format(g["label"], g["value"]) for g in qa_group(rows, key))

def dedup_names(*lists):
    seen = set(); out = []
    for lst in lists:
        for x in lst:
            n = x.get("name")
            if n not in seen:
                seen.add(n); out.append(n)
    return out

def name_list(lst):
    return [x.get("name") for x in lst]

def compute_c5_qa(data, filters, sources, survey_filter, nowdate, in90date):
    def ready(dt):
        return sources.get(dt) == "Available"
    s = scoped_rows(data, filters)
    metrics, quality = compute_c5_summary(data, filters)
    survey = build_survey_analytics(data, survey_filter)
    courses = s["courses"]
    topics = len([x for x in courses if x.get("topics")])
    criteria = len([x for x in courses if x.get("assessment_criteria")])
    d = data
    fmonth = filters.get("month") or ""

    missingTopics = [x for x in courses if not (x.get("topics") or [])]
    missingCriteria = [x for x in courses if not (x.get("assessment_criteria") or [])]
    mappedCourseNames = set()
    for p in (d.get("Program") or []):
        for x in (p.get("courses") or []):
            if x.get("course"):
                mappedCourseNames.add(x.get("course"))
    unmappedCourses = [x for x in courses if x.get("name") not in mappedCourseNames]
    coursesWithPlans = set(x.get("course") for x in s["plans"] if x.get("course"))
    coursesWithoutPlans = [x for x in courses if x.get("name") not in coursesWithPlans]
    schedules = s["schedules"] or []
    missingInstructor = [x for x in schedules if not x.get("instructor")]
    missingRoom = [x for x in schedules if not x.get("room")]
    schedNames = set(x.get("name") for x in schedules)
    attendedScheduleNames = set(x.get("course_schedule") for x in s["attendance"] if x.get("course_schedule") in schedNames)
    schedulesNoAttendance = [x for x in schedules if x.get("name") not in attendedScheduleNames]
    attendanceByStatus = qa_group(s["attendance"], "status")
    attendanceText = group_join(s["attendance"], "status") if attendanceByStatus else "No attendance records in the selected scope."
    absent = len([x for x in s["attendance"] if x.get("status") == "Absent"])
    late = len([x for x in s["attendance"] if x.get("status") == "Late"])
    plansMissingExaminer = [x for x in s["plans"] if not x.get("examiner")]
    plansMissingSupervisor = [x for x in s["plans"] if not x.get("supervisor")]
    plansMissingRoom = [x for x in s["plans"] if not x.get("room")]
    plansMissingDate = [x for x in s["plans"] if not x.get("schedule_date")]
    planNames = set(x.get("name") for x in s["plans"])
    resultPlanNames = set(x.get("assessment_plan") for x in s["results"] if x.get("assessment_plan") in planNames)
    plansWithoutResults = [x for x in s["plans"] if x.get("name") not in resultPlanNames]
    gradeDistribution = qa_group(s["results"], "grade")

    def is_result_check(c):
        cl = c.lower()
        return ("result" in cl) or ("score" in cl) or ("grade" in cl) or ("duplicate" in cl)
    resultErrors = sum(x["count"] for x in quality if is_result_check(x["check"]))

    mr = d.get("Module Review") or []
    cr = d.get("Course Review") or []
    overdueReviews = [x for x in cr if x.get("next_review_date") and x.get("next_review_date") <= nowdate]
    pendingRecommendations = [x for x in (mr + cr) if x.get("recommendation_implementation_status") == "Not Implemented"]
    actionRows = []
    for parent in cr:
        for action in (parent.get("actionplan_progress") or []):
            actionRows.append(action)
    mr_fields = ["rating_duration", "rating_pedagogy", "rating_assessment", "rating_learning_outcomes", "rating_lesson_plan", "rating_resource", "recommendation"]
    incompleteModuleReviews = [x for x in mr if any(not x.get(fld) for fld in mr_fields)]
    intakes = d.get("Student Intake No") or []
    classes = d.get("Module Class Details") or []
    admissions = d.get("Student Admission UCC") or []
    intakeGaps = [x for x in intakes if not x.get("program") or not x.get("course_start_date") or not x.get("course_end_date")]
    classesNoTeacher = [x for x in classes if not x.get("custom_instructor")]
    classesNoSchedule = [x for x in classes if not (x.get("schedules") or [])]
    incompleteContracts = [x for x in admissions if not x.get("contract_start") or not x.get("contract_end")]
    admissionsNoIntake = [x for x in admissions if not x.get("student_batch")]
    observations = d.get("Classroom Observation") or []
    observedClassNames = set(x.get("module_class_details") for x in observations if x.get("module_class_details"))
    classesNoObservation = [x for x in classes if x.get("name") not in observedClassNames]
    unsignedObservations = [x for x in observations if not x.get("observers_signature") or not x.get("teachers_signature")]
    concernObservations = [x for x in observations if strip_tags(x.get("areas_text") or "").strip()]
    observationTypes = group_join(observations, "type_of_observation")
    noticeTypes = group_join(observations, "prior_notice")
    agreements = d.get("Partnership Agreement") or []
    managed = d.get("Partnerships Agreement Management") or []
    supplierRatings = d.get("Supplier Rating") or []
    expiredAgreements = [x for x in agreements if x.get("end_date") and x.get("end_date") <= nowdate]
    expiringAgreements = [x for x in agreements if x.get("end_date") and x.get("end_date") > nowdate and x.get("end_date") <= in90date]
    ndaIncomplete = [x for x in agreements if x.get("requires_nda") and not x.get("nda_acknowledged")]
    monitoring = []
    for parent in managed:
        for r in (parent.get("monitoring_childtable") or []):
            monitoring.append(r)
    evaluations = []
    for parent in managed:
        for r in (parent.get("table_luoo") or []):
            evaluations.append(r)
    belowThreshold = [x for x in managed if js_number(x.get("average_identification_and_selection_score")) > 0 and js_number(x.get("average_identification_and_selection_score")) < 70]

    ELL = "…"
    ready_readiness = pct(topics + criteria, len(courses) * 2)

    # survey row helpers
    sc = survey["scored"]; cm = survey["comments"]
    mod_list = [x for x in survey["moduleScores"] if any(it["module"] == x["label"] and it["survey_type"] == "End of Module" for it in sc)]
    def fmt_avg(g):
        return "{0}: {1}".format(g["label"], num_fmt(g["value"]))
    q_low = sorted(survey["questionScores"], key=lambda g: g["value"])[:5]

    def types_line():
        parts = []
        for t in ["End of Module", "End of Course", "Graduate Survey"]:
            n = len([x for x in sc if x["survey_type"] == t]) + len([x for x in cm if x["survey_type"] == t])
            parts.append("{0}: {1}".format(t, n))
        return ", ".join(parts)

    def g_join_list(lst):
        return ", ".join(fmt_avg(g) for g in lst)

    rows = []
    def R(criterion, question, answer, source, doctypes, doctype=None, records=None, status="Good"):
        row = {"criterion": criterion, "question": question, "answer": answer, "source": source, "doctypes": doctypes, "status": status}
        if doctype is not None:
            row["doctype"] = doctype
            row["records"] = records if records is not None else []
        rows.append(row)

    # 5.1.1
    R("5.1.1", "Which Modules are missing curriculum topics?",
      ("{0} Module(s): {1}{2}".format(len(missingTopics), ", ".join((x.get("course_name") or x.get("name")) for x in missingTopics[:8]), ELL if len(missingTopics) > 8 else "") if missingTopics else "No scoped Modules are missing curriculum topics."),
      "Course.topics child table on scoped Module records.", ["Course"], "Course", name_list(missingTopics), "Risk" if missingTopics else "Good")
    R("5.1.1", "Which Modules are missing assessment criteria?",
      ("{0} Module(s) are missing assessment criteria.".format(len(missingCriteria)) if missingCriteria else "No scoped Modules are missing assessment criteria."),
      "Course.assessment_criteria child table.", ["Course"], "Course", name_list(missingCriteria), "Risk" if missingCriteria else "Good")
    R("5.1.1", "How complete is the Course-to-Module mapping?",
      "{0} unique Module(s) are mapped; {1} scoped Module(s) are not found in a readable Course mapping.".format(len(mappedCourseNames), len(unmappedCourses)),
      "Program.courses compared with scoped Course.name.", ["Program", "Course"], "Course", name_list(unmappedCourses), "Warning" if unmappedCourses else "Good")
    R("5.1.1", "Which Modules do not have an Assessment Plan?",
      ("{0} Module(s) have no Assessment Plan.".format(len(coursesWithoutPlans)) if coursesWithoutPlans else "Every scoped Module has at least one Assessment Plan."),
      "Course.name compared with Assessment Plan.course.", ["Course", "Assessment Plan"], "Course", name_list(coursesWithoutPlans), "Risk" if coursesWithoutPlans else "Good")
    R("5.1.1", "What is the overall Module-design readiness?",
      "{0}% across curriculum topics and assessment criteria for {1} scoped Module(s).".format(ready_readiness, len(courses)),
      "(Modules with topics + Modules with criteria) ÷ (Module count × 2).", ["Course"], "Course", dedup_names(missingTopics, missingCriteria),
      "Good" if ready_readiness >= 100 else ("Warning" if ready_readiness >= 90 else "Risk"))

    # 5.1.2
    R("5.1.2", "What is the Module Review approval status?",
      ((group_join(mr, "status") or "No Module Review records.") if ready("Module Review") else "Open 5.1.2 to load Module Review data."),
      "Module Review.status.", ["Module Review"], "Module Review", name_list(mr),
      "Warning" if not ready("Module Review") else ("Warning" if any(x.get("status") != "Approved" for x in mr) else "Good"))
    R("5.1.2", "Which Course Reviews are overdue?",
      ("{0} Course Review(s) have a next review date before today.".format(len(overdueReviews)) if ready("Course Review") else "Open 5.1.2 to load Course Review data."),
      "Course Review.next_review_date compared with today.", ["Course Review"], "Course Review", name_list(overdueReviews), "Risk" if overdueReviews else "Good")
    R("5.1.2", "Are scheduled and ad-hoc reviews identifiable?",
      (group_join([{"kind": (x.get("type_of_review") or "Not Set")} for x in mr] + [{"kind": (x.get("review_type") or "Not Set")} for x in cr], "kind") if (ready("Module Review") or ready("Course Review")) else "Open 5.1.2 to load review data."),
      "Module Review.type_of_review and Course Review.review_type.", ["Module Review", "Course Review"], None, None, "Good" if (mr or cr) else "Warning")
    R("5.1.2", "Which previous recommendations remain unimplemented?",
      ("{0} review record(s) are marked Not Implemented.".format(len(pendingRecommendations)) if (ready("Module Review") or ready("Course Review")) else "Open 5.1.2 to load review data."),
      "recommendation_implementation_status.", ["Module Review", "Course Review"], "Module Review", name_list(pendingRecommendations), "Risk" if pendingRecommendations else "Good")
    R("5.1.2", "What is the Course Review action-plan status?",
      ((group_join(actionRows, "status") or "No action-plan rows.") if ready("Course Review") else "Open 5.1.2 to load Course Review data."),
      "Course Review.actionplan_progress.status.", ["Course Review"], None, None, "Warning" if any(x.get("status") not in ("Completed", "In Effect") for x in actionRows) else "Good")
    R("5.1.2", "Which Module Reviews have incomplete core evidence?",
      ("{0} Module Review(s) have one or more core evidence fields empty.".format(len(incompleteModuleReviews)) if ready("Module Review") else "Open 5.1.2 to load Module Review data."),
      "Core rating and recommendation fields in Module Review.", ["Module Review"], "Module Review", name_list(incompleteModuleReviews), "Warning" if incompleteModuleReviews else "Good")

    # 5.2.1
    R("5.2.1", "How many scheduled Module sessions are in the selected period?",
      "{0} Module Schedule record(s) for {1}.".format(len(schedules), fmonth),
      "Course Schedule.schedule_date filtered by selected period and scope.", ["Course Schedule"], "Course Schedule", name_list(schedules), "Good" if schedules else "Warning")
    R("5.2.1", "Which scheduled sessions have no Teacher?",
      ("{0} session(s) lack a Teacher.".format(len(missingInstructor)) if missingInstructor else "All selected sessions have a Teacher."),
      "Course Schedule.instructor.", ["Course Schedule"], "Course Schedule", name_list(missingInstructor), "Risk" if missingInstructor else "Good")
    R("5.2.1", "Which scheduled sessions have no room or venue?",
      ("{0} session(s) lack a room.".format(len(missingRoom)) if missingRoom else "All selected sessions have a room."),
      "Course Schedule.room.", ["Course Schedule"], "Course Schedule", name_list(missingRoom), "Warning" if missingRoom else "Good")
    R("5.2.1", "Which Intakes are missing core planning dates or Course?",
      ("{0} Intake(s) have missing Course/start/end information.".format(len(intakeGaps)) if ready("Student Intake No") else "Open 5.2.1 to load Intake data."),
      "Student Intake No.program, course_start_date and course_end_date.", ["Student Intake No"], "Student Intake No", name_list(intakeGaps), "Risk" if intakeGaps else "Good")
    R("5.2.1", "Which Module Classes have no assigned Teacher or schedule?",
      ("{0} lack a Teacher; {1} have no schedule rows.".format(len(classesNoTeacher), len(classesNoSchedule)) if ready("Module Class Details") else "Open 5.2.1 to load Module Class Details."),
      "Module Class Details.custom_instructor and schedules.", ["Module Class Details"], "Module Class Details", dedup_names(classesNoTeacher, classesNoSchedule), "Risk" if (classesNoTeacher or classesNoSchedule) else "Good")
    R("5.2.1", "Which Shortlisted Applicants have incomplete Intake or contract dates?",
      ("{0} lack Intake No; {1} have incomplete contract dates.".format(len(admissionsNoIntake), len(incompleteContracts)) if ready("Student Admission UCC") else "Open 5.2.1 to load Shortlisted Applicants."),
      "Student Admission UCC.student_batch, contract_start and contract_end.", ["Student Admission UCC"], "Student Admission UCC", dedup_names(admissionsNoIntake, incompleteContracts), "Warning" if (admissionsNoIntake or incompleteContracts) else "Good")

    # 5.2.2
    cap = pct(len(attendedScheduleNames), len(schedNames))
    R("5.2.2", "What percentage of scheduled lessons have attendance captured?",
      "{0}% ({1} of {2} distinct schedules).".format(cap, len(attendedScheduleNames), len(schedNames)),
      "Distinct Student Attendance.course_schedule ÷ Course Schedule.name.", ["Student Attendance", "Course Schedule"], "Course Schedule", name_list(schedulesNoAttendance),
      "Good" if cap >= 100 else ("Warning" if cap >= 90 else "Risk"))
    R("5.2.2", "What is the attendance status distribution?",
      attendanceText, "Student Attendance.status.", ["Student Attendance"], None, None, "Good" if s["attendance"] else "Warning")
    R("5.2.2", "Which Module Classes have no Classroom Observation?",
      ("{0} Module Class(es) have no linked observation.".format(len(classesNoObservation)) if ready("Classroom Observation") else "Open 5.2.2 to load observation data."),
      "Module Class Details.name compared with Classroom Observation.module_class_details.", ["Module Class Details", "Classroom Observation"], "Module Class Details", name_list(classesNoObservation), "Warning" if classesNoObservation else "Good")
    R("5.2.2", "What observation types were conducted?",
      ((observationTypes or "No observations.") if ready("Classroom Observation") else "Open 5.2.2 to load observation data."),
      "Classroom Observation.type_of_observation.", ["Classroom Observation"], "Classroom Observation", name_list(observations), "Good" if observations else "Warning")
    R("5.2.2", "Which observations are missing Observer or Teacher sign-off?",
      ("{0} observation(s) have incomplete signatures.".format(len(unsignedObservations)) if ready("Classroom Observation") else "Open 5.2.2 to load observation data."),
      "Classroom Observation.observers_signature and teachers_signature.", ["Classroom Observation"], "Classroom Observation", name_list(unsignedObservations), "Warning" if unsignedObservations else "Good")
    R("5.2.2", "Which observations record areas for improvement?",
      ("{0} observation(s) contain areas for improvement.".format(len(concernObservations)) if ready("Classroom Observation") else "Open 5.2.2 to load observation data."),
      "Classroom Observation.areas_text.", ["Classroom Observation"], "Classroom Observation", name_list(concernObservations), "Warning" if concernObservations else "Good")
    R("5.2.2", "Were observations conducted with or without prior notice?",
      ((noticeTypes or "No observations.") if ready("Classroom Observation") else "Open 5.2.2 to load observation data."),
      "Classroom Observation.prior_notice.", ["Classroom Observation"], None, None, "Good" if observations else "Warning")

    # 5.3.1
    R("5.3.1", "How many signed partnership agreements are active, upcoming or expired?",
      ("{0} agreement(s); expired: {1}; expiring within 90 days: {2}.".format(len(agreements), len(expiredAgreements), len(expiringAgreements)) if ready("Partnership Agreement") else "Open 5.3.1 to load Partnership Agreement data."),
      "Partnership Agreement.start_date and end_date.", ["Partnership Agreement"], "Partnership Agreement", name_list(agreements), "Warning" if expiredAgreements else "Good")
    R("5.3.1", "Which agreements require an NDA that is not acknowledged?",
      ("{0} agreement(s) require NDA follow-up.".format(len(ndaIncomplete)) if ready("Partnership Agreement") else "Open 5.3.1 to load Partnership Agreement data."),
      "Partnership Agreement.requires_nda and nda_acknowledged.", ["Partnership Agreement", "Non Disclosure Agreement"], "Partnership Agreement", name_list(ndaIncomplete), "Risk" if ndaIncomplete else "Good")
    R("5.3.1", "How many partnership monitoring activities are recorded?",
      ("{0} monitoring row(s) across {1} managed partnership record(s).".format(len(monitoring), len(managed)) if ready("Partnerships Agreement Management") else "Open 5.3.1 to load management data."),
      "Partnerships Agreement Management.monitoring_childtable.", ["Partnerships Agreement Management"], "Partnerships Agreement Management", name_list([x for x in managed if (x.get("monitoring_childtable") or [])]), "Good" if monitoring else "Warning")
    R("5.3.1", "What monitoring methods are being used?",
      ((group_join(monitoring, "monitoring_details") or "No monitoring entries.") if ready("Partnerships Agreement Management") else "Open 5.3.1 to load management data."),
      "Partnerships Monitoring Childtable.monitoring_details.", ["Partnerships Agreement Management"], None, None, "Good" if monitoring else "Warning")
    R("5.3.1", "What decisions resulted from partnership evaluations?",
      ((group_join(evaluations, "evaluation_outcome") or "No evaluation entries.") if ready("Partnerships Agreement Management") else "Open 5.3.1 to load management data."),
      "Partnerships Evaluation Childtable.evaluation_outcome.", ["Partnerships Agreement Management"], None, None, "Good" if evaluations else "Warning")
    R("5.3.1", "Which managed partnerships are below the 70/100 selection threshold?",
      ("{0} managed partnership(s) are below threshold.".format(len(belowThreshold)) if ready("Partnerships Agreement Management") else "Open 5.3.1 to load management data."),
      "average_identification_and_selection_score compared with 70/100.", ["Partnerships Agreement Management"], "Partnerships Agreement Management", name_list(belowThreshold), "Risk" if belowThreshold else "Good")
    R("5.3.1", "What Provider Rating stages are recorded?",
      ((group_join(supplierRatings, "evaluation_stage") or "No Provider Rating records.") if ready("Supplier Rating") else "Open 5.3.1 to load Provider Rating data."),
      "Supplier Rating.evaluation_stage. Display term: Provider Rating.", ["Supplier Rating"], "Supplier Rating", name_list(supplierRatings), "Good" if supplierRatings else "Warning")

    # 5.4
    R("5.4", "What is the average End of Module Survey score for each Module?",
      (g_join_list(mod_list[:8]) if mod_list else "No scored End of Module Survey responses were classified in the selected scope."),
      "Survey Response.course plus scored child response rows.", ["Survey Response"], None, None, "Good" if survey["moduleScores"] else "Warning")
    R("5.4", "How many survey responses exist by survey type?",
      types_line(), "Survey type classified from title, category and question text.", ["Survey Response"], None, None, "Good" if (d.get("Survey Response") or []) else "Warning")
    R("5.4", "Which survey questions have the lowest scores?",
      (g_join_list(q_low) if q_low else "No scored survey questions were available."),
      "Average parsed score grouped by child question.", ["Survey Response"], None, None, "Warning")
    R("5.4", "What open-ended responses were submitted?",
      "{0} open-ended/non-numeric response(s) are available.".format(len(cm)),
      "Survey Response child rows not parsed as numeric/Likert scores.", ["Survey Response"], None, None, "Good" if cm else "Warning")
    R("5.4", "What attendance-risk indicators are visible alongside survey feedback?",
      "{0} Absent record(s) and {1} Late record(s) in the selected schedule scope.".format(absent, late),
      "Student Attendance.status linked to selected Module Schedule records.", ["Student Attendance"], None, None, "Warning" if (absent or late) else "Good")

    # 5.5
    R("5.5", "Which Assessment Plans are missing examiner or supervisor?",
      "{0} plan(s) lack examiner and {1} lack supervisor.".format(len(plansMissingExaminer), len(plansMissingSupervisor)),
      "Assessment Plan.examiner and supervisor.", ["Assessment Plan"], "Assessment Plan", dedup_names(plansMissingExaminer, plansMissingSupervisor), "Warning" if (plansMissingExaminer or plansMissingSupervisor) else "Good")
    R("5.5", "Which Assessment Plans have no linked results?",
      ("{0} plan(s) have no linked Assessment Result.".format(len(plansWithoutResults)) if plansWithoutResults else "Every selected Assessment Plan has at least one linked result."),
      "Assessment Plan.name compared with Assessment Result.assessment_plan.", ["Assessment Plan", "Assessment Result"], "Assessment Plan", name_list(plansWithoutResults), "Risk" if plansWithoutResults else "Good")
    R("5.5", "What is the grade distribution?",
      (group_join(s["results"], "grade") if gradeDistribution else "No graded Assessment Result records in the selected scope."),
      "Assessment Result.grade.", ["Assessment Result"], None, None, "Good" if gradeDistribution else "Warning")
    R("5.5", "How complete are assessment control fields?",
      "Missing room: {0}; missing schedule date: {1}; missing examiner: {2}; missing supervisor: {3}.".format(len(plansMissingRoom), len(plansMissingDate), len(plansMissingExaminer), len(plansMissingSupervisor)),
      "Assessment Plan control fields.", ["Assessment Plan"], None, None, "Warning" if (plansMissingRoom or plansMissingDate or plansMissingExaminer or plansMissingSupervisor) else "Good")
    R("5.5", "Are there assessment-result data errors requiring correction?",
      "{0} result-quality exception(s) across score-above-maximum, missing grade and duplicate-result checks.".format(resultErrors),
      "Assessment Result data-quality rules.", ["Assessment Result"], None, None, "Risk" if resultErrors else "Good")

    exceptions = []
    for x in metrics:
        if x["status"] != "Good":
            exceptions.append({"criterion": x["criterion"], "issue": x["question"], "value": "{0}%".format(x["current"]), "target": "{0}%".format(x["target"]), "status": x["status"]})
    for x in quality:
        if x["count"]:
            exceptions.append({"criterion": "Data Quality", "issue": x["check"], "value": x["count"], "target": 0, "status": "Risk"})
    for x in rows:
        if x["status"] == "Risk":
            exceptions.append({"criterion": x["criterion"], "issue": x["question"], "value": x["answer"], "target": "Follow-up required", "status": "Risk"})

    return {"rows": rows, "exceptions": exceptions}

def num_fmt(v):
    # JS number formatting: integers render without .0
    if isinstance(v, float) and v.is_integer():
        return int(v)
    return v

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
elif action == "c531_analytics":
    # Section 5.3.1 model, server-side. Faithful port of the client buildC531();
    # proven byte-identical to the JavaScript. Partnership Agreement (signature
    # fields) and Partnerships Agreement Management (monitoring_childtable /
    # table_luoo child tables) need full documents. The Provider/Supplier Rating
    # source is resolved with frappe.db.exists FIRST so a missing DocType never
    # raises (the permanent fix for the recurring "Provider Rating not found").
    data = {}
    sources = {}
    for doctype in ["Partnership Agreement", "Partnerships Agreement Management"]:
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

    rating_doctype = None
    for candidate in ["Provider Rating", "Supplier Rating"]:
        if frappe.db.exists("DocType", candidate):
            rating_doctype = candidate
            break
    if not rating_doctype:
        data["Supplier Rating"] = []
        sources["Supplier Rating"] = {"status": "Not installed", "count": 0, "attempted": ["Provider Rating", "Supplier Rating"]}
    else:
        try:
            data["Supplier Rating"] = frappe.get_list(rating_doctype, fields=["name", "evaluation_stage"], limit_page_length=500, order_by="modified desc") or []
        except Exception:
            try:
                data["Supplier Rating"] = frappe.get_list(rating_doctype, fields=["name", "modified"], limit_page_length=500, order_by="modified desc") or []
            except Exception as error:
                data["Supplier Rating"] = []
        sources["Supplier Rating"] = {"status": "Available", "count": len(data["Supplier Rating"]), "resolved": rating_doctype}

    today = frappe.utils.nowdate()
    in90 = frappe.utils.add_days(today, 90)
    model = compute_c531(data, today, in90)
    frappe.response["message"] = {
        "ok": True,
        "meta": {
            "api_method": "ucc_analytics_criterion_5",
            "dashboard": "criterion_5",
            "action": action,
            "section": "5.3.1",
            "as_of": today,
            "generated_at": frappe.utils.now()
        },
        "filters": filters,
        "model": model,
        "records": {
            "signed": data["Partnership Agreement"],
            "managed": data["Partnerships Agreement Management"],
            "ratings": data["Supplier Rating"]
        },
        "sources": sources
    }
elif action == "c522_analytics":
    # Section 5.2.2 model, server-side. Faithful port of the client buildC522();
    # proven byte-identical to the JavaScript. Classroom Observation (likert +
    # signature fields), Module Class Details and Survey Response (response child
    # table) need full documents; Survey Response is programme-filtered like the
    # client. The client's c522 branch does not load Course Schedule or Student
    # Attendance, so those are left empty to match the fresh-load client exactly.
    f5 = filters or {}
    program = f5.get("program")
    data = {}
    sources = {}
    for doctype in ["Classroom Observation", "Module Class Details"]:
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
    survey_filters = {}
    if program:
        survey_filters["program"] = program
    try:
        survey_names = frappe.get_list("Survey Response", filters=survey_filters, pluck="name", limit_page_length=500, order_by="modified desc") or []
        data["Survey Response"] = [frappe.get_doc("Survey Response", name).as_dict() for name in survey_names]
        sources["Survey Response"] = {"status": "Available", "count": len(data["Survey Response"])}
    except Exception as error:
        data["Survey Response"] = []
        sources["Survey Response"] = {"status": "Unavailable", "count": 0, "error": str(error)}
    data["Course Schedule"] = []
    data["Student Attendance"] = []

    today = frappe.utils.nowdate()
    model = compute_c522(data, today)
    frappe.response["message"] = {
        "ok": True,
        "meta": {
            "api_method": "ucc_analytics_criterion_5",
            "dashboard": "criterion_5",
            "action": action,
            "section": "5.2.2",
            "as_of": today,
            "generated_at": frappe.utils.now()
        },
        "filters": filters,
        "model": model,
        "records": {
            "obs": data["Classroom Observation"],
            "classes": data["Module Class Details"],
            "surveys": data["Survey Response"]
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
elif action == "c5_qa":
    # Full makeQA() model, server-side. Faithful port proven byte-identical to the
    # JavaScript across main + partial-sources + filtered + survey-filter + empty
    # fixtures. Child-table doctypes are fetched as full documents; flat doctypes
    # as field lists. Answer text is gated on the client-supplied source
    # availability (payload.sources) so the rendered rows match the live client
    # exactly regardless of which sections the user has opened. Permission-aware.
    survey_filter = payload.get("survey_filter") or {}
    client_sources = payload.get("sources") or {}
    data = {}
    fetch_status = {}
    full_doctypes = ["Program", "Course", "Course Review", "Module Class Details",
                     "Classroom Observation", "Survey Response",
                     "Partnerships Agreement Management", "Module Review"]
    list_fields = {
        "Student Group": ["name", "academic_year", "program", "course"],
        "Course Schedule": ["name", "student_group", "program", "course", "instructor", "room", "schedule_date"],
        "Student Attendance": ["name", "course_schedule", "status", "student"],
        "Assessment Plan": ["name", "course", "program", "academic_year", "student_group", "examiner", "supervisor", "room", "schedule_date"],
        "Assessment Result": ["name", "assessment_plan", "program", "academic_year", "student_group", "student", "grade", "total_score", "maximum_score"],
        "Course Enrollment": ["name", "program", "course"],
        "Student Intake No": ["name", "program", "course_start_date", "course_end_date"],
        "Student Admission UCC": ["name", "student_batch", "contract_start", "contract_end"],
        "Partnership Agreement": ["name", "start_date", "end_date", "requires_nda", "nda_acknowledged"],
    }
    for doctype in full_doctypes:
        try:
            row_names = frappe.get_list(doctype, pluck="name", limit_page_length=500, order_by="modified desc") or []
            data[doctype] = [frappe.get_doc(doctype, nm).as_dict() for nm in row_names]
            fetch_status[doctype] = {"status": "Available", "count": len(data[doctype])}
        except Exception as error:
            message = str(error)
            lowered = message.lower()
            status = "Not permitted" if ("permission" in lowered or "not permitted" in lowered or "not allowed" in lowered) else "Unavailable"
            data[doctype] = []
            fetch_status[doctype] = {"status": status, "count": 0, "error": message}
    for doctype in list_fields:
        try:
            data[doctype] = frappe.get_list(doctype, fields=list_fields[doctype], limit_page_length=500, order_by="modified desc") or []
            fetch_status[doctype] = {"status": "Available", "count": len(data[doctype])}
        except Exception as error:
            message = str(error)
            lowered = message.lower()
            status = "Not permitted" if ("permission" in lowered or "not permitted" in lowered or "not allowed" in lowered) else "Unavailable"
            data[doctype] = []
            fetch_status[doctype] = {"status": status, "count": 0, "error": message}
    # Provider/Supplier Rating resolved with frappe.db.exists FIRST (permanent fix).
    rating_doctype = None
    for candidate in ["Provider Rating", "Supplier Rating"]:
        if frappe.db.exists("DocType", candidate):
            rating_doctype = candidate
            break
    if not rating_doctype:
        data["Supplier Rating"] = []
        fetch_status["Supplier Rating"] = {"status": "Not installed", "count": 0, "attempted": ["Provider Rating", "Supplier Rating"]}
    else:
        try:
            data["Supplier Rating"] = frappe.get_list(rating_doctype, fields=["name", "evaluation_stage"], limit_page_length=500, order_by="modified desc") or []
        except Exception:
            try:
                data["Supplier Rating"] = frappe.get_list(rating_doctype, fields=["name", "modified"], limit_page_length=500, order_by="modified desc") or []
            except Exception:
                data["Supplier Rating"] = []
        fetch_status["Supplier Rating"] = {"status": "Available", "count": len(data["Supplier Rating"]), "resolved": rating_doctype}

    today = frappe.utils.nowdate()
    in90 = frappe.utils.add_days(today, 90)
    qa = compute_c5_qa(data, filters, client_sources, survey_filter, today, in90)
    # Record pools for client re-hydration (row.records carries name strings).
    pool_doctypes = ["Course", "Module Review", "Course Review", "Course Schedule",
                     "Student Intake No", "Module Class Details", "Student Admission UCC",
                     "Classroom Observation", "Partnership Agreement",
                     "Partnerships Agreement Management", "Supplier Rating", "Assessment Plan"]
    records_pool = {}
    for doctype in pool_doctypes:
        records_pool[doctype] = data.get(doctype) or []
    frappe.response["message"] = {
        "ok": True,
        "meta": {
            "api_method": "ucc_analytics_criterion_5",
            "dashboard": "criterion_5",
            "action": action,
            "section": "makeQA",
            "as_of": today,
            "generated_at": frappe.utils.now()
        },
        "filters": filters,
        "model": {"rows": qa["rows"], "exceptions": qa["exceptions"]},
        "records": records_pool,
        "sources": fetch_status
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
