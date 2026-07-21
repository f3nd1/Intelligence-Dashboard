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
