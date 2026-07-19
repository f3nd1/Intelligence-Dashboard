"""
UCC Intelligence Platform Server Script

Visible name:
    UCC Ask - Student Journey

Script type:
    API

API method:
    ucc_ask_student_journey

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
# API Method: ucc_ask_student_journey
#
# Module: Student Journey
#
# Purpose:
# Provides a guided view of student lifecycle, study progress, attendance, finance, completion and graduation.
#
# Design principles:
# - ERPNext remains the factual source of truth.
# - Deterministic rules handle dates, status, counts and filters.
# - AI may assist with interpretation or drafting where enabled.
# - Missing data is reported clearly and is never guessed.

AGENT_VERSION = "1.1.0"
AGENT_BUILD = "UCC Ask - Student Journey V1.1.0"

V15_CONFIG = {
    "attendance_warning_threshold": 90,
    "attendance_critical_threshold": 75,
    "outstanding_fee_warning": 0,
    "missing_result_warning": 1,
    "long_leave_days": 14,
    "max_recent_sources": 20,
    "finance_customer_fields": ["customer", "customer_name"],
    "sensitive_fields": [
        "passport_number", "fin", "nric", "mobile_number",
        "personal_email", "bank_account"
    ],
    "role_categories": {
        "finance": ["Accounts User", "Accounts Manager", "System Manager"],
        "academic": ["Education Manager", "Academic", "System Manager"],
        "attendance": ["Education Manager", "Student Support", "System Manager"],
        "admin": ["System Manager"]
    }
}


def clean_text(value):
    return " ".join(str(value or "").strip().split())


def normalise(value):
    text = clean_text(value).lower()

    for character in [
        ",", ".", "'", '"', "(", ")", "[", "]",
        "{", "}", "-", "_", "/", "?", "!", ":", ";"
    ]:
        text = text.replace(character, " ")

    corrections = {
        "jingynag": "jinyang",
        "jingyang": "jinyang",
        "studnet": "student",
        "studnets": "students",
        "htey": "they",
        "tehy": "they",
        "lifecyl": "lifecycle",
        "lifecyle": "lifecycle",
        "lifecyclee": "lifecycle"
    }

    output = []

    for word in text.split():
        output.append(corrections.get(word) or word)

    return " ".join(output)


def iso_date(value):
    text = clean_text(value)
    return text[:10] if text else ""


def format_date(value):
    text = iso_date(value)

    if len(text) != 10:
        return text or "Not recorded"

    months = [
        "", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    try:
        year = text[0:4]
        month = int(text[5:7])
        day = int(text[8:10])
        return str(day).zfill(2) + " " + months[month] + " " + year
    except Exception:
        return text


def full_applicant_name(applicant):
    parts = []

    for fieldname in ["first_name", "middle_name", "last_name"]:
        value = clean_text(applicant.get(fieldname))

        if value and value not in parts:
            parts.append(value)

    return " ".join(parts) or clean_text(applicant.get("name"))


def candidate_output(applicant):
    return {
        "student_applicant": applicant.get("name") or "",
        "student_name": full_applicant_name(applicant),
        "student_type": applicant.get("student_type") or "",
        "program": applicant.get("program") or ""
    }


def link_cell(text, doctype, name):
    return {
        "text": clean_text(text) or clean_text(name),
        "doctype": doctype,
        "name": clean_text(name)
    }


def source(label, doctype, name, short_label=""):
    if not doctype or not name:
        return None

    return {
        "label": label or name,
        "short_label": short_label or label or name,
        "doctype": doctype,
        "name": name
    }


def unique_sources(items):
    output = []
    seen = []

    for item in items or []:
        if not item:
            continue

        key = clean_text(item.get("doctype")) + "::" + clean_text(item.get("name"))

        if not key or key in seen:
            continue

        seen.append(key)
        output.append(item)

    return output


def safe_db_list(doctype, filters=None, fields=None, order_by="modified desc", limit=1000):
    try:
        return frappe.db.get_list(
            doctype,
            filters=filters or {},
            fields=fields or ["name"],
            order_by=order_by,
            limit_page_length=limit
        )
    except Exception as error:
        try:
            frappe.log_error(
                message=str(error),
                title="Admission Journey Query: " + doctype
            )
        except Exception:
            pass
        return []


def get_doc_safe(doctype, name):
    if not doctype or not name:
        return None

    try:
        return frappe.get_doc(doctype, name)
    except Exception:
        return None


def edit_distance(left, right):
    left = clean_text(left)
    right = clean_text(right)

    if left == right:
        return 0

    if not left:
        return len(right)

    if not right:
        return len(left)

    previous = list(range(len(right) + 1))

    for left_index in range(1, len(left) + 1):
        current = [left_index]

        for right_index in range(1, len(right) + 1):
            insert_cost = current[right_index - 1] + 1
            delete_cost = previous[right_index] + 1
            replace_cost = previous[right_index - 1]

            if left[left_index - 1] != right[right_index - 1]:
                replace_cost = replace_cost + 1

            current.append(min(insert_cost, delete_cost, replace_cost))

        previous = current

    return previous[-1]


def token_match(question_token, name_token):
    if question_token == name_token:
        return True

    if len(question_token) < 4 or len(name_token) < 4:
        return False

    allowed = 1

    if len(name_token) >= 8:
        allowed = 2

    return edit_distance(question_token, name_token) <= allowed


def question_contains_explicit_student_reference(applicants, question):
    q = normalise(question)
    padded = " " + q + " "
    q_tokens = q.split()

    follow_up_words = [
        "he", "his", "him", "she", "her", "hers", "they", "their",
        "this", "student", "profile", "journey", "attendance", "result",
        "results", "grade", "grades", "leave", "course", "module",
        "modules", "class", "group", "start", "started", "completion",
        "complete", "graduated", "nationality", "fees", "payment",
        "payments", "risk", "readiness", "documents", "fps"
    ]

    meaningful_tokens = []

    for token in q_tokens:
        if len(token) >= 3 and token not in follow_up_words:
            meaningful_tokens.append(token)

    for applicant in applicants:
        applicant_id = normalise(applicant.get("name"))
        complete_name = normalise(full_applicant_name(applicant))
        name_tokens = [
            token for token in complete_name.split()
            if len(token) >= 3
        ]

        if applicant_id and (
            applicant_id == q
            or " " + applicant_id + " " in padded
        ):
            return True

        if complete_name and " " + complete_name + " " in padded:
            return True

        matched = 0

        for name_token in name_tokens:
            for question_token in meaningful_tokens:
                if token_match(question_token, name_token):
                    matched = matched + 1
                    break

        if matched >= 2:
            return True

        # A short standalone query such as "jabbar" is treated as a new
        # name search rather than a follow-up about the selected student.
        if len(meaningful_tokens) == 1 and matched == 1:
            return True

    return False
def find_applicant(applicants, question, selected_applicant):
    q = normalise(question)
    padded = " " + q + " "
    q_tokens = q.split()

    pinned_followup_phrases = [
        "this student",
        "this student's",
        "this students",
        "his ",
        "her ",
        "their ",
        "he ",
        "she ",
        "they ",
        "and how much",
        "how much",
        "what about attendance",
        "what about leave",
        "what about results",
        "show all results",
        "show all this student"
    ]

    if selected_applicant:
        explicit_id_or_full_name = False

        for applicant in applicants:
            applicant_id = normalise(applicant.get("name"))
            complete_name = normalise(full_applicant_name(applicant))

            if applicant_id and (
                applicant_id == q
                or " " + applicant_id + " " in padded
            ):
                explicit_id_or_full_name = True
                break

            if complete_name and " " + complete_name + " " in padded:
                explicit_id_or_full_name = True
                break

        pinned_followup = False

        for phrase in pinned_followup_phrases:
            if phrase in q:
                pinned_followup = True
                break

        if pinned_followup and not explicit_id_or_full_name:
            for applicant in applicants:
                if applicant.get("name") == selected_applicant:
                    return {"status": "found", "applicant": applicant}

    # Follow-up questions stay on the selected student unless a new student
    # is explicitly named.
    if selected_applicant and not question_contains_explicit_student_reference(
        applicants,
        question
    ):
        for applicant in applicants:
            if applicant.get("name") == selected_applicant:
                return {"status": "found", "applicant": applicant}

    exact = []

    for applicant in applicants:
        applicant_id = normalise(applicant.get("name"))
        complete_name = normalise(full_applicant_name(applicant))

        id_match = (
            applicant_id
            and (
                applicant_id == q
                or " " + applicant_id + " " in padded
            )
        )

        name_match = (
            complete_name
            and " " + complete_name + " " in padded
        )

        if id_match or name_match:
            exact.append(applicant)

    if len(exact) == 1:
        return {"status": "found", "applicant": exact[0]}

    if len(exact) > 1:
        return {"status": "choose_student", "candidates": exact[:20]}

    scored = []

    for applicant in applicants:
        complete_name = normalise(full_applicant_name(applicant))
        name_tokens = [token for token in complete_name.split() if len(token) >= 3]
        matched_tokens = []
        total_distance = 0

        for name_token in name_tokens:
            best_distance = None

            for question_token in q_tokens:
                if token_match(question_token, name_token):
                    distance = edit_distance(question_token, name_token)

                    if best_distance is None or distance < best_distance:
                        best_distance = distance

            if best_distance is not None:
                matched_tokens.append(name_token)
                total_distance = total_distance + best_distance

        if matched_tokens:
            scored.append({
                "matched": len(matched_tokens),
                "distance": total_distance,
                "applicant": applicant
            })

    if not scored:
        return {"status": "student_required"}

    scored = sorted(
        scored,
        key=lambda item: (
            -item.get("matched"),
            item.get("distance"),
            full_applicant_name(item.get("applicant") or {})
        )
    )

    best_matched = scored[0].get("matched")
    best_distance = scored[0].get("distance")

    best = [
        item.get("applicant")
        for item in scored
        if (
            item.get("matched") == best_matched
            and item.get("distance") == best_distance
        )
    ]

    # One-token queries such as "jabbar" or "redha" are ambiguous by nature.
    # Return a short candidate list rather than guessing or rejecting.
    if best_matched == 1:
        return {
            "status": "choose_student",
            "candidates": best[:20]
        }

    if len(best) == 1:
        return {"status": "found", "applicant": best[0]}

    return {"status": "choose_student", "candidates": best[:20]}
def report_value(row, names):
    for name in names:
        value = row.get(name)

        if value is not None and value != "":
            return value

    return ""


def normalise_student_roll_row(row):
    return {
        "student_applicant": report_value(row, ["student_applicant", "Student Applicant"]),
        "student_admission": report_value(row, ["student_admission_ucc_id", "student_admission", "Student Admission"]),
        "student": report_value(row, ["student", "Student"]),
        "student_name": report_value(row, ["student_name", "Student Name"]),
        "student_type": report_value(row, ["student_type", "full_part_time", "Full/Part Time"]),
        "course": report_value(row, ["course", "program", "Course"]),
        "module_code": report_value(row, ["module_code", "Module Code"]),
        "module": report_value(row, ["module", "module_name", "Module"]),
        "start_date": iso_date(report_value(row, ["module_start_date", "start_date", "Start Date"])),
        "end_date": iso_date(report_value(row, ["module_end_date", "end_date", "End Date"])),
        "mark": report_value(row, ["mark", "total_score", "Mark"]),
        "grade": report_value(row, ["grade", "Grade"]),
        "course_commencement_date": iso_date(report_value(row, ["course_commencement_date", "commencement_date", "Course Commencement Date"])),
        "actual_commencement_date": iso_date(report_value(row, ["actual_commencement_date", "date_of_commencement", "Date of Commencement"])),
        "course_completion_date": iso_date(report_value(row, ["course_completion_date", "completion_date", "Course Completion Date"])),
        "assessment_date": iso_date(report_value(row, ["assessment_date", "Assessment Date"])),
        "assessment_result": report_value(row, ["assessment_result_id", "assessment_result", "Assessment Result"]),
        "student_group": report_value(row, ["module_class_details_id", "student_group", "Student Group"])
    }


def report_rows_for_student(rows, applicant, student_name):
    output = []
    applicant_id = normalise(applicant.get("name"))
    target_name = normalise(student_name)

    for row in rows or []:
        report_applicant = normalise(row.get("student_applicant"))
        report_name = normalise(row.get("student_name"))

        if applicant_id and report_applicant == applicant_id:
            output.append(row)
            continue

        if target_name and report_name == target_name:
            output.append(row)

    return output


def approved_workflow(value):
    state = normalise(value)

    if state in ["draft", "rejected", "cancelled", "canceled", "withdrawn"]:
        return False

    return True


def days_in_month(year, month):
    values = {
        1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
        7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }

    leap = (
        year % 400 == 0
        or (year % 4 == 0 and year % 100 != 0)
    )

    if month == 2 and leap:
        return 29

    return values.get(month, 28)


def shift_month(year, month, difference):
    total = year * 12 + month - 1 + difference
    return total // 12, total % 12 + 1


def month_range_from_question(question):
    q = normalise(question)
    tokens = q.split()
    today = str(frappe.utils.today())[:10]
    current_year = int(today[0:4])
    current_month = int(today[5:7])
    target_year = current_year
    target_month = current_month

    month_names = {
        "january": 1, "jan": 1,
        "february": 2, "feb": 2,
        "march": 3, "mar": 3,
        "april": 4, "apr": 4,
        "may": 5,
        "june": 6, "jun": 6,
        "july": 7, "jul": 7,
        "august": 8, "aug": 8,
        "september": 9, "sep": 9, "sept": 9,
        "october": 10, "oct": 10,
        "november": 11, "nov": 11,
        "december": 12, "dec": 12
    }

    number_words = {
        "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8,
        "nine": 9, "ten": 10, "eleven": 11, "twelve": 12
    }

    months_ago = None

    for index, token in enumerate(tokens):
        if token in ["month", "months"] and index + 1 < len(tokens) and tokens[index + 1] == "ago":
            if index > 0:
                previous = tokens[index - 1]

                if previous.isdigit():
                    months_ago = int(previous)
                elif previous in number_words:
                    months_ago = number_words.get(previous)

    if months_ago is not None:
        shifted_month = shift_month(current_year, current_month, -months_ago)
        target_year = shifted_month[0]
        target_month = shifted_month[1]

    elif "last month" in q:
        shifted_month = shift_month(current_year, current_month, -1)
        target_year = shifted_month[0]
        target_month = shifted_month[1]

    else:
        for token in tokens:
            if token in month_names:
                target_month = month_names.get(token)
                break

        for token in tokens:
            if token.isdigit() and len(token) == 4:
                target_year = int(token)
                break

    start_date = str(target_year).zfill(4) + "-" + str(target_month).zfill(2) + "-01"
    end_date = (
        str(target_year).zfill(4)
        + "-"
        + str(target_month).zfill(2)
        + "-"
        + str(days_in_month(target_year, target_month)).zfill(2)
    )

    month_labels = [
        "", "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    return {
        "start_date": start_date,
        "end_date": end_date,
        "label": month_labels[target_month] + " " + str(target_year)
    }


def date_range_from_question(question):
    q = normalise(question)
    tokens = q.split()
    today = str(frappe.utils.today())[:10]
    current_year = int(today[0:4])

    month_names = {
        "january": 1, "jan": 1,
        "february": 2, "feb": 2,
        "march": 3, "mar": 3,
        "april": 4, "apr": 4,
        "may": 5,
        "june": 6, "jun": 6,
        "july": 7, "jul": 7,
        "august": 8, "aug": 8,
        "september": 9, "sep": 9, "sept": 9,
        "october": 10, "oct": 10,
        "november": 11, "nov": 11,
        "december": 12, "dec": 12
    }

    month = None
    year = current_year
    numbers = []

    for token in tokens:
        if token in month_names:
            month = month_names.get(token)

        if token.isdigit():
            number = int(token)

            if len(token) == 4 and number >= 2000:
                year = number
            elif 1 <= number <= 31:
                numbers.append(number)

    if month and len(numbers) >= 2:
        first_day = numbers[0]
        last_day = numbers[1]
        maximum = days_in_month(year, month)
        first_day = min(max(first_day, 1), maximum)
        last_day = min(max(last_day, first_day), maximum)

        start_date = str(year).zfill(4) + "-" + str(month).zfill(2) + "-" + str(first_day).zfill(2)
        end_date = str(year).zfill(4) + "-" + str(month).zfill(2) + "-" + str(last_day).zfill(2)

        return {
            "start_date": start_date,
            "end_date": end_date,
            "label": format_date(start_date) + " to " + format_date(end_date)
        }

    month_period = month_range_from_question(question)
    return {
        "start_date": month_period.get("start_date"),
        "end_date": month_period.get("end_date"),
        "label": month_period.get("label")
    }


def active_in_range(admission, start_date, end_date):
    status = normalise(admission.get("application_status"))

    if status in ["rejected", "cancelled", "canceled", "withdrawn", "terminated"]:
        return False

    commencement = iso_date(admission.get("date_of_commencement") or admission.get("commencement_date"))
    completion = iso_date(admission.get("completion_date"))

    if not commencement:
        return False

    if commencement > end_date:
        return False

    if completion and completion < start_date:
        return False

    return True


def programme_matches(programme, keyword):
    return normalise(keyword) in normalise(programme)


def get_applicant_map(applicant_ids):
    applicant_ids = [value for value in applicant_ids if value]

    if not applicant_ids:
        return {}

    rows = safe_db_list(
        "Student Applicant",
        filters={"name": ["in", applicant_ids]},
        fields=["name", "first_name", "middle_name", "last_name", "student_type", "program"],
        order_by="modified desc",
        limit=5000
    )

    output = {}

    for row in rows:
        output[row.get("name")] = row

    return output


def get_student_map(student_ids):
    student_ids = [value for value in student_ids if value]

    if not student_ids:
        return {}

    try:
        rows = safe_db_list(
            "Student",
            filters={"name": ["in", student_ids]},
            fields=["name", "student_name", "custom_academic_status", "enabled"],
            order_by="student_name asc",
            limit=5000
        )
    except Exception:
        rows = []

    output = {}

    for row in rows:
        output[row.get("name")] = row

    return output


def group_members(group_name):
    output = []
    group_doc = get_doc_safe("Student Group", group_name)

    if not group_doc:
        return output

    rows = (
        group_doc.get("students")
        or group_doc.get("student_group_students")
        or []
    )

    for row in rows:
        output.append({
            "parent": group_name,
            "student": row.get("student") or "",
            "student_name": row.get("student_name") or "",
            "group_roll_number": row.get("group_roll_number") or "",
            "active": row.get("active")
        })

    return output
def build_individual_context(applicant, student_roll_rows):
    applicant_doc = get_doc_safe("Student Applicant", applicant.get("name"))

    if applicant_doc:
        applicant = applicant_doc

    applicant_name = full_applicant_name(applicant)

    admissions = safe_db_list(
        "Student Admission UCC",
        filters={
            "student_applicant": applicant.get("name"),
            "docstatus": ["<", 2]
        },
        fields=[
            "name", "student_applicant", "student", "student_name", "program",
            "commencement_date", "date_of_commencement", "completion_date",
            "conferment_date", "application_status", "modified"
        ],
        order_by="commencement_date desc, modified desc",
        limit=20
    )

    admission = admissions[0] if admissions else {}
    student_id = admission.get("student") or ""
    student_doc = get_doc_safe("Student", student_id) if student_id else None

    modules = []

    for admission_row in admissions:
        admission_doc = get_doc_safe("Student Admission UCC", admission_row.get("name"))

        if not admission_doc:
            continue

        for module in admission_doc.get("modules") or []:
            modules.append({
                "admission": admission_row.get("name") or "",
                "module_row": module.get("name") or "",
                "program": admission_row.get("program") or "",
                "module_code": module.get("module_code") or "",
                "module_name": module.get("module_name") or "",
                "abbreviation": module.get("abbreviation") or "",
                "start_date": iso_date(module.get("start_date")),
                "end_date": iso_date(module.get("end_date")),
                "score": None,
                "maximum_score": None,
                "grade": "",
                "assessment_result": "",
                "assessment_date": "",
                "student_group": "",
                "source_kind": "admission"
            })

    assessment_results = []

    if student_id:
        assessment_results = safe_db_list(
            "Assessment Result",
            filters={
                "student": student_id,
                "docstatus": ["<", 2]
            },
            fields=[
                "name", "docstatus", "student", "student_name", "program", "course",
                "assessment_name", "assessment_date", "custom_issued_date", "total_score",
                "maximum_score", "grade", "custom_retake", "student_group", "modified"
            ],
            order_by="assessment_date asc, custom_issued_date asc, modified asc",
            limit=1000
        )

        if not assessment_results:
            assessment_results = safe_db_list(
                "Assessment Result",
                filters={
                    "student": student_id,
                    "docstatus": ["<", 2]
                },
                fields=[
                    "name", "docstatus", "student", "student_name", "program", "course",
                    "assessment_name", "custom_issued_date", "total_score",
                    "maximum_score", "grade", "custom_retake", "student_group", "modified"
                ],
                order_by="custom_issued_date asc, modified asc",
                limit=1000
            )

            for result in assessment_results:
                result["assessment_date"] = result.get("custom_issued_date") or result.get("modified")

    def result_matches_module(result, module):
        result_values = [
            normalise(result.get("course")),
            normalise(result.get("assessment_name"))
        ]
        module_values = [
            normalise(module.get("module_code")),
            normalise(module.get("module_name")),
            normalise(module.get("abbreviation"))
        ]

        for result_value in result_values:
            if not result_value:
                continue

            for module_value in module_values:
                if not module_value:
                    continue

                if result_value == module_value:
                    return True

                if len(result_value) >= 4 and result_value in module_value:
                    return True

                if len(module_value) >= 4 and module_value in result_value:
                    return True

        return False

    for module in modules:
        matched = None

        for result in assessment_results:
            if int(result.get("docstatus") or 0) != 1:
                continue

            if result_matches_module(result, module):
                matched = result

        if matched:
            module["score"] = matched.get("total_score")
            module["maximum_score"] = matched.get("maximum_score")
            module["grade"] = matched.get("grade") or ""
            module["assessment_result"] = matched.get("name") or ""
            module["assessment_date"] = iso_date(
                matched.get("assessment_date")
                or matched.get("custom_issued_date")
                or matched.get("modified")
            )
            module["student_group"] = matched.get("student_group") or ""

    matching_report_rows = report_rows_for_student(
        student_roll_rows,
        applicant,
        applicant_name
    )

    if matching_report_rows:
        for report_row in matching_report_rows:
            module_code = clean_text(report_row.get("module_code") or report_row.get("module"))
            start_date = iso_date(report_row.get("start_date"))
            end_date = iso_date(report_row.get("end_date"))
            existing = None

            for module in modules:
                if (
                    normalise(module.get("module_code") or module.get("module_name"))
                    == normalise(module_code)
                    and (not start_date or module.get("start_date") == start_date)
                    and (not end_date or module.get("end_date") == end_date)
                ):
                    existing = module
                    break

            if not existing:
                existing = {
                    "admission": report_row.get("student_admission") or admission.get("name") or "",
                    "module_row": "",
                    "program": report_row.get("course") or admission.get("program") or "",
                    "module_code": report_row.get("module_code") or "",
                    "module_name": report_row.get("module") or report_row.get("module_code") or "",
                    "abbreviation": "",
                    "start_date": start_date,
                    "end_date": end_date,
                    "score": None,
                    "maximum_score": None,
                    "grade": "",
                    "assessment_result": "",
                    "assessment_date": "",
                    "student_group": report_row.get("student_group") or "",
                    "source_kind": "report"
                }
                modules.append(existing)

            if report_row.get("mark") is not None and report_row.get("mark") != "":
                existing["score"] = report_row.get("mark")

            if report_row.get("grade"):
                existing["grade"] = report_row.get("grade")

            if report_row.get("assessment_result"):
                existing["assessment_result"] = report_row.get("assessment_result")

            if report_row.get("assessment_date"):
                existing["assessment_date"] = report_row.get("assessment_date")

            if report_row.get("student_group"):
                existing["student_group"] = report_row.get("student_group")

            existing["source_kind"] = "report"

    leaves = []

    if student_id:
        leaves = safe_db_list(
            "Student Leave Application",
            filters={
                "student": student_id,
                "docstatus": ["<", 2]
            },
            fields=[
                "name", "student", "student_name", "workflow_state", "from_date", "to_date",
                "total_leave_days", "reason", "custom_approval_date", "modified"
            ],
            order_by="from_date asc",
            limit=1000
        )

    group_names = []

    for module in modules:
        group_name = clean_text(module.get("student_group"))

        if group_name and group_name not in group_names:
            group_names.append(group_name)

    for result in assessment_results:
        group_name = clean_text(result.get("student_group"))

        if group_name and group_name not in group_names:
            group_names.append(group_name)

    groups = []

    for group_name in group_names:
        group_doc = get_doc_safe("Student Group", group_name)

        if group_doc:
            groups.append({
                "name": group_doc.name,
                "student_group_name": group_doc.get("student_group_name") or "",
                "program": group_doc.get("program") or "",
                "course": group_doc.get("course") or group_doc.get("custom_course_name") or "",
                "start_date": iso_date(group_doc.get("course_date_start")),
                "end_date": iso_date(group_doc.get("course_date_end")),
                "instructor": group_doc.get("custom_instructor_full_name") or group_doc.get("custom_instructor") or ""
            })

    modules = deduplicate_modules(modules)
    attendance = load_attendance_for_student(student_id)
    groups = load_groups_for_student(student_id, modules, assessment_results)

    sources = [
        source("Student Applicant", "Student Applicant", applicant.get("name"), "Applicant")
    ]

    if admission.get("name"):
        sources.append(source("Admission", "Student Admission UCC", admission.get("name"), "Admission"))

    if student_id:
        sources.append(source("Student", "Student", student_id, "Student"))

    return {
        "current_date": str(frappe.utils.today())[:10],
        "applicant": applicant,
        "student_name": applicant_name,
        "student_id": student_id,
        "student_doc": student_doc,
        "admissions": admissions,
        "admission": admission,
        "modules": modules,
        "assessment_results": assessment_results,
        "leaves": leaves,
        "groups": groups,
        "attendance": attendance,
        "sources": sources
    }



def canonical_module_key(module):
    values = [
        clean_text(module.get("module_code")),
        clean_text(module.get("module_name")),
        clean_text(module.get("abbreviation"))
    ]

    for value in values:
        if not value:
            continue

        compact = value.upper().replace(" ", "")
        code = ""

        for character in compact:
            if character.isalnum():
                code = code + character
            else:
                break

        if code:
            return code

    return normalise(module_label(module))


def deduplicate_modules(modules):
    grouped = {}

    for module in modules or []:
        key = canonical_module_key(module)

        if not key:
            continue

        existing = grouped.get(key)

        if not existing:
            grouped[key] = module
            continue

        existing_priority = 0
        current_priority = 0

        if existing.get("source_kind") == "report":
            existing_priority = existing_priority + 100

        if module.get("source_kind") == "report":
            current_priority = current_priority + 100

        if existing.get("assessment_result"):
            existing_priority = existing_priority + 20

        if module.get("assessment_result"):
            current_priority = current_priority + 20

        if existing.get("student_group"):
            existing_priority = existing_priority + 10

        if module.get("student_group"):
            current_priority = current_priority + 10

        if current_priority > existing_priority:
            preferred = module
            secondary = existing
        else:
            preferred = existing
            secondary = module

        for fieldname in [
            "score", "maximum_score", "grade", "assessment_result",
            "assessment_date", "student_group", "module_name",
            "module_code", "abbreviation"
        ]:
            if preferred.get(fieldname) is None or preferred.get(fieldname) == "":
                preferred[fieldname] = secondary.get(fieldname)

        grouped[key] = preferred

    output = list(grouped.values())
    output = sorted(
        output,
        key=lambda item: (
            iso_date(item.get("start_date")) or "9999-12-31",
            canonical_module_key(item)
        )
    )
    return output

def load_attendance_for_student(student_id):
    if not student_id:
        return {
            "records": [],
            "summary": {
                "present": 0,
                "absent": 0,
                "late": 0,
                "other": 0,
                "total": 0,
                "rate": None
            }
        }

    rows = safe_db_list(
        "Student Attendance",
        filters={
            "student": student_id,
            "docstatus": ["<", 2]
        },
        fields=[
            "name",
            "student",
            "student_group",
            "course_schedule",
            "date",
            "status",
            "leave_application",
            "custom_type",
            "custom_attendance_percentage",
            "custom_minutes_late",
            "modified"
        ],
        order_by="date asc, modified asc",
        limit=5000
    )

    present = 0
    absent = 0
    late = 0
    other = 0

    for row in rows:
        status = normalise(row.get("status"))

        if status == "present":
            present = present + 1
        elif status == "absent":
            absent = absent + 1
        elif status == "late":
            late = late + 1
        else:
            other = other + 1

    total = present + absent + late + other
    rate = None

    if total:
        rate = ((present + late) / total) * 100

    return {
        "records": rows,
        "summary": {
            "present": present,
            "absent": absent,
            "late": late,
            "other": other,
            "total": total,
            "rate": rate
        }
    }


def load_groups_for_student(student_id, modules, assessment_results):
    group_names = []

    for module in modules or []:
        group_name = clean_text(module.get("student_group"))

        if group_name and group_name not in group_names:
            group_names.append(group_name)

    for result in assessment_results or []:
        group_name = clean_text(result.get("student_group"))

        if group_name and group_name not in group_names:
            group_names.append(group_name)

    groups = []

    for group_name in group_names:
        group_doc = get_doc_safe("Student Group", group_name)

        if not group_doc:
            continue

        groups.append({
            "name": group_doc.name,
            "student_group_name": group_doc.get("student_group_name") or "",
            "program": group_doc.get("program") or "",
            "course": group_doc.get("course") or group_doc.get("custom_course_name") or "",
            "start_date": iso_date(group_doc.get("course_date_start")),
            "end_date": iso_date(group_doc.get("course_date_end")),
            "instructor": group_doc.get("custom_instructor_full_name") or group_doc.get("custom_instructor") or ""
        })

    return groups
def module_label(module):
    code = clean_text(module.get("module_code"))
    name = clean_text(module.get("module_name"))

    if code and name and normalise(code) != normalise(name):
        return code + " - " + name

    return code or name or "Module"


def find_requested_module(modules, question):
    q = normalise(question)
    best = None
    best_score = 0

    for module in modules:
        values = [
            normalise(module.get("module_code")),
            normalise(module.get("module_name")),
            normalise(module.get("abbreviation"))
        ]
        score = 0

        for value in values:
            if not value:
                continue

            if value in q:
                score = score + 20 + len(value.split())
                continue

            for token in value.split():
                if len(token) >= 4 and token in q.split():
                    score = score + 1

        if score > best_score:
            best = module
            best_score = score

    return best


def detect_intent(question):
    q = normalise(question)


    if any(term in q for term in [
        "show this student's profile",
        "show this student profile",
        "show this student s profile",
        "this student s profile",
        "student profile",
        "show his profile",
        "show her profile",
        "show their profile",
        "profile of this student"
    ]):
        return "profile"

    if any(term in q for term in ["diagnostic", "diagnostics", "debug details", "admin details"]):
        return "diagnostics"

    # Global questions must be checked before individual "class" or
    # selected-student follow-up rules.
    if "how many" in q and "leave" in q:
        return "leave_count"

    if any(term in q for term in ["cohort dashboard", "student dashboard", "cohort overview"]):
        return "cohort_dashboard"

    if any(term in q for term in [
        "who graduated", "students who graduated",
        "graduated months ago", "graduated 6 months ago"
    ]):
        return "graduated_list"

    if any(term in q for term in [
        "graduating this month", "students graduating",
        "who is graduating", "who are graduating",
        "students completing this month"
    ]):
        return "graduation_list"

    if any(term in q for term in [
        "students in class today", "students in the class today",
        "who are the students in class today",
        "who is in class today", "class today"
    ]):
        return "class_today"

    if "ielts" in q and any(term in q for term in [
        "full time", "part time", "short course"
    ]):
        return "cohort_types"

    if "ielts" in q and any(term in q for term in [
        "how many", "did we have", "students in may"
    ]):
        return "cohort_count"

    if any(term in q for term in ["payment timeline", "invoice timeline", "payment history"]):
        return "payment_timeline"

    if any(term in q for term in [
        "fee status", "fees", "payment status", "outstanding",
        "unpaid", "invoice", "invoices", "paid amount"
    ]):
        return "finance"

    if any(term in q for term in [
        "graduation readiness", "ready to graduate",
        "can graduate", "eligible to graduate"
    ]):
        return "graduation_readiness"

    if any(term in q for term in [
        "risk summary", "student risk", "risk level",
        "what are the risks", "follow up actions"
    ]):
        return "risk_summary"

    if any(term in q for term in [
        "missing documents", "documents missing",
        "admission documents", "attached documents"
    ]):
        return "documents"

    if any(term in q for term in [
        "fps status", "fee protection", "fee protection scheme"
    ]):
        return "fps"

    if "mock" in q and any(term in q for term in [
        "when", "date", "take", "took"
    ]):
        return "assessment_date"

    if any(term in q for term in ["leave history", "leave records", "previous leave", "upcoming leave"]):
        return "leave_history"

    if "leave" in q and any(term in q for term in [
        "now", "currently", "today", "on leave"
    ]):
        return "leave_status"

    if any(term in q for term in ["academic progress", "study progress", "module progress"]):
        return "academic_progress"

    if any(term in q for term in ["grade analytics", "average mark", "highest mark", "lowest mark"]):
        return "grade_analytics"

    if any(term in q for term in [
        "all results", "all his results", "all her results",
        "all their results", "show results", "module results",
        "his result", "her result", "their result",
        "wats his result", "what is his result",
        "what are his results", "grades", "all grades",
        "his grades", "her grades", "show grades"
    ]):
        return "all_results"

    if any(term in q for term in [
        "nationality", "citizenship", "country"
    ]):
        return "nationality"

    if any(term in q for term in ["attendance trend", "monthly attendance", "attendance by month"]):
        return "attendance_trend"

    if any(term in q for term in [
        "attendance", "attendance rate", "absent", "present", "late"
    ]):
        return "attendance"

    if any(term in q for term in [
        "student group", "which class", "group details",
        "teacher", "instructor", "class and group"
    ]):
        return "student_group"

    if any(term in q for term in [
        "lifecycle", "life cycle", "journey", "student journey",
        "full journey", "complete journey", "admission journey"
    ]):
        return "full_journey"

    if any(term in q for term in [
        "finished all", "finish all", "completed all modules",
        "all his modules", "all her modules"
    ]):
        return "module_completion_status"

    if any(term in q for term in [
        "which module", "current module", "module is", "right now"
    ]):
        return "current_module"

    if any(term in q for term in [
        "when did", "when was", "start", "started", "commencement"
    ]):
        return "commencement"

    if any(term in q for term in [
        "when is", "completing", "completion date",
        "ending his course", "ending her course",
        "end his course", "end her course"
    ]):
        return "completion"

    if any(term in q for term in [
        "what course", "which course", "programme", "program"
    ]):
        return "course"

    if any(term in q for term in [
        "has graduated", "graduated", "graduation status"
    ]):
        return "graduation_status"

    if any(term in q for term in [
        "mark", "grade", "score", "result"
    ]):
        return "module_result"
    q_tokens = q.split()

    # Allow short direct student-name or Applicant-ID searches.
    if len(q_tokens) <= 3:
        return "profile"

    return "unsupported"

OPENAI_API_KEY = ""

def ai_route(question, conversation, selected_applicant):
    fallback = {
        "intent": detect_intent(question),
        "canonical_question": question,
        "scope": "individual" if selected_applicant else "unknown",
        "ai_used": False
    }

    key = clean_text(OPENAI_API_KEY)

    if not key or key == "PASTE_NEW_OPENAI_API_KEY_HERE":
        return fallback

    instruction = """
You are the routing layer for United Ceres College's Admission Journey Assistant.
Return one structured route. Do not answer and do not invent data.

Intent options:
current_module
commencement
completion
course
graduation_status
graduation_readiness
module_completion_status
module_result
all_results
nationality
attendance
student_group
assessment_date
class_today
cohort_types
cohort_count
graduation_list
graduated_list
leave_status
leave_count
finance
documents
fps
risk_summary
full_journey
profile

Rules:
- Correct obvious spelling mistakes silently.
- Preserve names, programme names, module names and date phrases.
- A short name can identify a different student from the selected student.
- Pronouns and follow-up wording refer to the selected student.
- Questions asking who or how many students are global.
- "Who are the students in class today?" is class_today.
- "Who graduated 6 months ago?" is graduated_list.
- "Who is graduating this month?" is graduation_list.
- Questions about invoices, outstanding fees or payment status are finance.
- Questions asking whether a student is ready to graduate are graduation_readiness.
- Questions asking for risks or follow-up actions are risk_summary.
- Return a complete canonical question.
"""

    recent = conversation or []
    messages = [{"role": "developer", "content": instruction}]

    for message in recent[-10:]:
        role = message.get("role")
        content = clean_text(message.get("content"))

        if role in ["user", "assistant"] and content:
            messages.append({"role": role, "content": content[:1200]})

    messages.append({
        "role": "user",
        "content": (
            "CURRENT QUESTION:\n" + question
            + "\n\nSELECTED APPLICANT:\n" + (selected_applicant or "None")
            + "\n\nCURRENT DATE:\n" + str(frappe.utils.today())
        )
    })

    schema = {
        "type": "object",
        "properties": {
            "intent": {
                "type": "string",
                "enum": [
                    "current_module", "commencement", "completion", "course",
                    "graduation_status", "graduation_readiness",
                    "module_completion_status", "module_result", "all_results",
                    "nationality", "attendance", "student_group",
                    "assessment_date", "class_today", "cohort_types",
                    "cohort_count", "graduation_list", "graduated_list",
                    "leave_status", "leave_count", "finance", "documents",
                    "fps", "risk_summary", "full_journey", "profile"
                ]
            },
            "canonical_question": {"type": "string"},
            "scope": {
                "type": "string",
                "enum": ["individual", "global", "unknown"]
            }
        },
        "required": ["intent", "canonical_question", "scope"],
        "additionalProperties": False
    }

    payload = {
        "model": OPENAI_MODEL,
        "store": False,
        "input": messages,
        "max_output_tokens": 350,
        "text": {
            "format": {
                "type": "json_schema",
                "name": "admission_journey_route",
                "strict": True,
                "schema": schema
            }
        }
    }

    try:
        response = frappe.make_post_request(
            "https://api.openai.com/v1/responses",
            headers={
                "Authorization": "Bearer " + key,
                "Content-Type": "application/json"
            },
            data=json.dumps(payload)
        )

        output_text = response.get("output_text") or ""

        if not output_text:
            for output_item in response.get("output") or []:
                if output_item.get("type") != "message":
                    continue

                for content_item in output_item.get("content") or []:
                    if content_item.get("type") == "output_text":
                        output_text = content_item.get("text") or ""
                        break

                if output_text:
                    break

        if not output_text:
            return fallback

        route = json.loads(output_text)
        route["ai_used"] = True

        if not clean_text(route.get("canonical_question")):
            route["canonical_question"] = question

        return route

    except Exception as error:
        try:
            frappe.log_error(
                message=str(error),
                title="Admission Journey AI Router"
            )
        except Exception:
            pass
        return fallback


def source_groups(sources):
    groups = {
        "Admission": [],
        "Academic": [],
        "Attendance and Leave": [],
        "Finance": [],
        "Documents": [],
        "Other": []
    }

    for item in unique_sources(sources or []):
        doctype = clean_text(item.get("doctype"))
        group = "Other"

        if doctype in ["Student Applicant", "Student Admission UCC", "Student"]:
            group = "Admission"
        elif doctype in ["Assessment Result", "Student Group", "Course Schedule"]:
            group = "Academic"
        elif doctype in ["Student Attendance", "Student Leave Application"]:
            group = "Attendance and Leave"
        elif doctype in ["Sales Invoice", "Payment Entry"]:
            group = "Finance"
        elif doctype == "File":
            group = "Documents"

        groups[group].append(item)

    return groups


def response_base(
    answer,
    visuals=None,
    sources=None,
    warnings=None,
    ai_used=False,
    confidence="Confirmed",
    diagnostics=None,
    actions=None
):
    source_list = unique_sources(sources or [])

    return {
        "status": "success",
        "answer": answer,
        "visuals": visuals or [],
        "sources": source_list,
        "source_groups": source_groups(source_list),
        "warnings": warnings or [],
        "ai_used": bool(ai_used),
        "agent_version": AGENT_VERSION,
        "agent_build": AGENT_BUILD,
        "confidence": confidence,
        "diagnostics": diagnostics or {},
        "actions": actions or []
    }

def numeric_grade_passed(grade):
    value = normalise(grade)

    if not value:
        return None

    if value in ["f", "fail", "failed", "unsatisfactory"]:
        return False

    if value in ["a", "b", "c", "d", "pass", "passed", "satisfactory"]:
        return True

    try:
        numeric = float(value)
        return numeric > 0
    except Exception:
        return None


def academic_analytics(context):
    modules = deduplicate_modules(context.get("modules") or [])
    submitted = []
    not_graded = []
    passed = []
    failed = []
    scores = []

    for module in modules:
        if module.get("assessment_result"):
            submitted.append(module)

            if module.get("score") is not None:
                try:
                    scores.append(float(module.get("score")))
                except Exception:
                    pass

            pass_state = numeric_grade_passed(module.get("grade"))

            if pass_state is True:
                passed.append(module)
            elif pass_state is False:
                failed.append(module)
        else:
            not_graded.append(module)

    total = len(modules)
    completion_percentage = 0

    if total:
        completion_percentage = round((len(submitted) / total) * 100, 1)

    average = None
    highest = None
    lowest = None

    if scores:
        average = round(sum(scores) / len(scores), 2)
        highest = max(scores)
        lowest = min(scores)

    return {
        "modules": modules,
        "total": total,
        "submitted": submitted,
        "not_graded": not_graded,
        "passed": passed,
        "failed": failed,
        "completion_percentage": completion_percentage,
        "average": average,
        "highest": highest,
        "lowest": lowest
    }


def handle_academic_progress(context, ai_used):
    data = academic_analytics(context)

    answer = (
        context.get("student_name")
        + " has "
        + str(len(data.get("submitted") or []))
        + " submitted result(s) across "
        + str(data.get("total") or 0)
        + " unique module(s). Academic result completion is "
        + str(data.get("completion_percentage") or 0)
        + "%."
    )

    visuals = [{
        "type": "summary",
        "title": "Academic progress",
        "items": [
            {"label": "Unique Modules", "value": data.get("total")},
            {"label": "Submitted Results", "value": len(data.get("submitted") or [])},
            {"label": "Not Graded", "value": len(data.get("not_graded") or [])},
            {"label": "Passed", "value": len(data.get("passed") or [])},
            {"label": "Failed", "value": len(data.get("failed") or [])},
            {"label": "Result Completion", "value": str(data.get("completion_percentage")) + "%"}
        ]
    }]

    return response_base(
        answer,
        visuals=visuals,
        sources=context.get("sources"),
        ai_used=ai_used,
        confidence="Confirmed"
    )


def handle_grade_analytics(context, ai_used):
    data = academic_analytics(context)
    answer = (
        "Grade analytics for "
        + context.get("student_name")
        + "."
    )

    visuals = [{
        "type": "summary",
        "title": "Grade analytics",
        "items": [
            {"label": "Average Mark", "value": data.get("average") if data.get("average") is not None else "Not recorded"},
            {"label": "Highest Mark", "value": data.get("highest") if data.get("highest") is not None else "Not recorded"},
            {"label": "Lowest Mark", "value": data.get("lowest") if data.get("lowest") is not None else "Not recorded"},
            {"label": "Passed", "value": len(data.get("passed") or [])},
            {"label": "Failed", "value": len(data.get("failed") or [])},
            {"label": "Not Graded", "value": len(data.get("not_graded") or [])}
        ]
    }]

    return response_base(
        answer,
        visuals=visuals,
        sources=context.get("sources"),
        ai_used=ai_used,
        confidence="Confirmed"
    )


def attendance_month_key(value):
    date_value = iso_date(value)

    if not date_value:
        return ""

    return date_value[:7]


def handle_attendance_trend(context, ai_used):
    records = ((context.get("attendance") or {}).get("records") or [])
    monthly = {}

    for row in records:
        key = attendance_month_key(row.get("date"))

        if not key:
            continue

        if key not in monthly:
            monthly[key] = {
                "present": 0,
                "absent": 0,
                "late": 0,
                "other": 0
            }

        status = normalise(row.get("status"))

        if status == "present":
            monthly[key]["present"] = monthly[key]["present"] + 1
        elif status == "absent":
            monthly[key]["absent"] = monthly[key]["absent"] + 1
        elif status == "late":
            monthly[key]["late"] = monthly[key]["late"] + 1
        else:
            monthly[key]["other"] = monthly[key]["other"] + 1

    rows = []

    for key in sorted(monthly.keys()):
        item = monthly[key]
        total = (
            item.get("present")
            + item.get("absent")
            + item.get("late")
            + item.get("other")
        )
        rate = None

        if total:
            rate = round(
                ((item.get("present") + item.get("late")) / total) * 100,
                1
            )

        rows.append([
            key,
            item.get("present"),
            item.get("late"),
            item.get("absent"),
            total,
            str(rate) + "%" if rate is not None else "Not recorded"
        ])

    answer = (
        str(len(rows))
        + " attendance month(s) were found for "
        + context.get("student_name")
        + "."
    )

    return response_base(
        answer,
        visuals=[{
            "type": "table",
            "title": "Monthly attendance trend",
            "columns": ["Month", "Present", "Late", "Absent", "Total", "Rate"],
            "rows": rows
        }],
        sources=context.get("sources"),
        ai_used=ai_used,
        confidence="Confirmed" if rows else "Missing data"
    )


def handle_leave_history(context, ai_used):
    leaves = context.get("leaves") or []
    rows = []

    for leave in leaves:
        start_date = iso_date(leave.get("from_date"))
        end_date = iso_date(leave.get("to_date"))
        total_days = ""

        if start_date and end_date:
            try:
                total_days = frappe.utils.date_diff(end_date, start_date) + 1
            except Exception:
                total_days = ""

        rows.append([
            format_date(start_date),
            format_date(end_date),
            total_days if total_days != "" else "Not recorded",
            leave.get("workflow_state") or leave.get("status") or "Not recorded",
            leave.get("reason") or leave.get("leave_reason") or "Not recorded"
        ])

    return response_base(
        (
            str(len(rows))
            + " leave record(s) were found for "
            + context.get("student_name")
            + "."
        ),
        visuals=[{
            "type": "table",
            "title": "Leave history",
            "columns": ["From", "To", "Days", "Status", "Reason"],
            "rows": rows
        }],
        sources=context.get("sources"),
        ai_used=ai_used,
        confidence="Confirmed" if rows else "Missing data"
    )


def handle_payment_timeline(context, ai_used):
    summary = finance_summary(context)
    invoices = summary.get("invoices") or []
    rows = []

    for invoice in invoices:
        rows.append([
            format_date(invoice.get("posting_date")),
            "Invoice issued",
            invoice.get("name") or "",
            str(invoice.get("grand_total") or 0),
            invoice.get("status") or ""
        ])

        if float(invoice.get("outstanding_amount") or 0) == 0:
            rows.append([
                format_date(invoice.get("due_date") or invoice.get("posting_date")),
                "Invoice settled",
                invoice.get("name") or "",
                str(invoice.get("grand_total") or 0),
                "Paid"
            ])

    rows = sorted(rows, key=lambda row: row[0] or "")

    return response_base(
        "Payment timeline for " + context.get("student_name") + ".",
        visuals=[{
            "type": "timeline_table",
            "title": "Payment timeline",
            "columns": ["Date", "Event", "Reference", "Amount", "Status"],
            "rows": rows
        }],
        sources=context.get("sources"),
        warnings=[
            "Payment events are inferred from submitted Sales Invoice status. "
            "Map Payment Entry references for exact receipt dates."
        ],
        ai_used=ai_used,
        confidence="Partial" if rows else "Missing data"
    )


def permission_snapshot():
    roles = []

    try:
        roles = frappe.get_roles()
    except Exception:
        roles = []

    return {
        "roles": roles,
        "can_view_finance": any(
            role in roles
            for role in V15_CONFIG.get("role_categories").get("finance")
        ),
        "can_view_admin": any(
            role in roles
            for role in V15_CONFIG.get("role_categories").get("admin")
        )
    }


def handle_diagnostics(context, intent, ai_used):
    attendance_records = (
        (context.get("attendance") or {}).get("records") or []
    )
    finance = finance_summary(context)

    diagnostics = {
        "intent": intent,
        "student_applicant": (context.get("applicant") or {}).get("name"),
        "student": context.get("student_id"),
        "admission": (context.get("admission") or {}).get("name"),
        "unique_modules": len(deduplicate_modules(context.get("modules") or [])),
        "assessment_results": len(context.get("assessment_results") or []),
        "attendance_records": len(attendance_records),
        "leave_records": len(context.get("leaves") or []),
        "invoice_records": len(finance.get("invoices") or []),
        "ai_used": bool(ai_used),
        "permissions": permission_snapshot()
    }

    return response_base(
        "Diagnostic information for " + context.get("student_name") + ".",
        visuals=[{
            "type": "diagnostics",
            "title": "Admin diagnostics",
            "items": diagnostics
        }],
        sources=context.get("sources"),
        ai_used=ai_used,
        confidence="Confirmed",
        diagnostics=diagnostics
    )


def handle_cohort_dashboard(student_roll_rows, ai_used):
    unique_students = {}
    current_date = iso_date(frappe.utils.today())
    report_rows = student_roll_rows or []

    if not report_rows:
        return response_base(
            "The Student Roll report returned no rows, so the cohort dashboard could not be generated.",
            warnings=[
                "Check that the Student Roll report is accessible and returns data for the current user."
            ],
            ai_used=ai_used,
            confidence="Missing data"
        )

    for row in report_rows:
        applicant_id = clean_text(row.get("student_applicant_id"))

        if not applicant_id:
            continue

        if applicant_id not in unique_students:
            unique_students[applicant_id] = {
                "student_name": row.get("student_name") or "",
                "course": row.get("course") or "",
                "completion": iso_date(row.get("course_completion_date")),
                "active_modules": 0,
                "missing_results": 0
            }

        start_date = iso_date(row.get("module_start_date"))
        end_date = iso_date(row.get("module_end_date"))

        if start_date and end_date and start_date <= current_date <= end_date:
            unique_students[applicant_id]["active_modules"] = (
                unique_students[applicant_id].get("active_modules") + 1
            )

        if not row.get("assessment_result_id"):
            unique_students[applicant_id]["missing_results"] = (
                unique_students[applicant_id].get("missing_results") + 1
            )

    active_count = len([
        item for item in unique_students.values()
        if item.get("active_modules")
    ])
    at_risk = len([
        item for item in unique_students.values()
        if item.get("missing_results")
    ])

    return response_base(
        "Cohort dashboard generated from the Student Roll report.",
        visuals=[
            {
                "type": "summary",
                "title": "Cohort overview",
                "items": [
                    {"label": "Unique Students", "value": len(unique_students)},
                    {"label": "Students with Active Modules", "value": active_count},
                    {"label": "Students with Missing Results", "value": at_risk}
                ]
            },
            {
                "type": "table",
                "title": "Cohort details",
                "columns": [
                    "Student", "Course", "Completion",
                    "Active Modules", "Missing Results"
                ],
                "rows": [[
                    item.get("student_name"),
                    item.get("course"),
                    format_date(item.get("completion")),
                    item.get("active_modules"),
                    item.get("missing_results")
                ] for item in unique_students.values()]
            }
        ],
        ai_used=ai_used,
        confidence="Confirmed"
    )
def handle_current_module(context, ai_used):
    today = context.get("current_date")
    current = []

    for module in context.get("modules") or []:
        start = iso_date(module.get("start_date"))
        end = iso_date(module.get("end_date"))

        if start and end and start <= today <= end:
            current.append(module)

    if current:
        labels = [module_label(module) for module in current]
        answer = context.get("student_name") + " is currently in " + ", ".join(labels) + "."
        sources = list(context.get("sources") or [])

        for module in current:
            sources.append(source("Module schedule", "Student Admission UCC", module.get("admission"), "Module"))

        return response_base(answer, sources=sources, ai_used=ai_used)

    future = [
        module for module in context.get("modules") or []
        if iso_date(module.get("start_date")) > today
    ]
    future = sorted(future, key=lambda item: iso_date(item.get("start_date")))

    if future:
        answer = (
            context.get("student_name")
            + " has no module active today. The next module is "
            + module_label(future[0])
            + ", starting on "
            + format_date(future[0].get("start_date"))
            + "."
        )
    else:
        answer = context.get("student_name") + " has no module active today."

    return response_base(answer, sources=context.get("sources"), ai_used=ai_used)


def handle_commencement(context, ai_used):
    admission = context.get("admission") or {}
    date = admission.get("date_of_commencement") or admission.get("commencement_date")

    answer = (
        context.get("student_name")
        + " started on "
        + format_date(date)
        + "."
    )

    return response_base(answer, sources=context.get("sources"), ai_used=ai_used)


def handle_completion(context, ai_used):
    admission = context.get("admission") or {}
    date = admission.get("completion_date")

    answer = (
        context.get("student_name")
        + " is scheduled to complete the course on "
        + format_date(date)
        + "."
    )

    return response_base(answer, sources=context.get("sources"), ai_used=ai_used)


def handle_course(context, ai_used):
    admission = context.get("admission") or {}
    programme = clean_text(admission.get("program") or context.get("applicant", {}).get("program"))

    answer = context.get("student_name") + " is enrolled in " + (programme or "a course that is not recorded") + "."
    return response_base(answer, sources=context.get("sources"), ai_used=ai_used)


def handle_graduation_status(context, ai_used):
    student_doc = context.get("student_doc")
    status = clean_text(student_doc.get("custom_academic_status") if student_doc else "")
    completion = clean_text((context.get("admission") or {}).get("completion_date"))

    if normalise(status) == "graduated":
        answer = context.get("student_name") + " is marked Graduated."

        if completion:
            answer = answer + " The recorded course completion date is " + format_date(completion) + "."
    else:
        answer = context.get("student_name") + " is not marked Graduated in the Student record."

        if completion:
            answer = answer + " The scheduled completion date is " + format_date(completion) + "."

    return response_base(answer, sources=context.get("sources"), ai_used=ai_used)


def handle_module_completion(context, ai_used):
    modules = context.get("modules") or []
    today = context.get("current_date")

    if not modules:
        return response_base(
            "No admission modules were found for " + context.get("student_name") + ".",
            sources=context.get("sources"),
            ai_used=ai_used
        )

    not_ended = []
    missing_results = []

    for module in modules:
        end = iso_date(module.get("end_date"))

        if not end or end >= today:
            not_ended.append(module)

        if not module.get("assessment_result"):
            missing_results.append(module)

    if not_ended:
        answer = (
            "No. " + context.get("student_name")
            + " still has " + str(len(not_ended))
            + " module(s) that have not ended."
        )
    else:
        answer = (
            "Yes. All " + str(len(modules))
            + " scheduled module periods have ended for "
            + context.get("student_name") + "."
        )

    if missing_results:
        answer = answer + " " + str(len(missing_results)) + " module(s) do not have a submitted result recorded."

    visuals = []

    if not_ended:
        visuals = [{
            "type": "table",
            "title": "Modules not yet ended",
            "columns": ["Module", "Start Date", "End Date"],
            "rows": [[
                module_label(module),
                format_date(module.get("start_date")),
                format_date(module.get("end_date"))
            ] for module in not_ended]
        }]

    return response_base(answer, visuals=visuals, sources=context.get("sources"), ai_used=ai_used)


def handle_module_result(context, question, ai_used):
    module = find_requested_module(context.get("modules") or [], question)

    if not module:
        return response_base(
            "I could not identify the requested module for " + context.get("student_name") + ".",
            sources=context.get("sources"),
            ai_used=ai_used
        )

    label = module_label(module)
    sources = list(context.get("sources") or [])

    if module.get("assessment_result"):
        score = module.get("score")
        maximum = module.get("maximum_score")
        score_text = "Not recorded"

        if score is not None and score != "":
            score_text = str(score)

            if maximum is not None and maximum != "":
                score_text = score_text + "/" + str(maximum)

        answer = (
            context.get("student_name")
            + " received " + score_text
            + " with grade " + clean_text(module.get("grade") or "Not recorded")
            + " for " + label + "."
        )
        sources.append(source("Assessment Result", "Assessment Result", module.get("assessment_result"), "Result"))
    else:
        answer = (
            "No submitted Assessment Result is recorded for "
            + context.get("student_name")
            + " in " + label + "."
        )

    return response_base(answer, sources=sources, ai_used=ai_used)



def handle_all_results(context, ai_used):
    modules = context.get("modules") or []
    results = context.get("assessment_results") or []
    rows = []
    seen_results = []
    sources = list(context.get("sources") or [])

    for module in modules:
        result_status = "Submitted" if module.get("assessment_result") else "Not graded"
        score = module.get("score")
        maximum = module.get("maximum_score")
        score_text = "Not recorded"

        if score is not None and score != "":
            score_text = str(score)

            if maximum is not None and maximum != "":
                score_text = score_text + "/" + str(maximum)

        rows.append([
            module_label(module),
            format_date(module.get("assessment_date")),
            score_text,
            clean_text(module.get("grade") or "Not recorded"),
            result_status
        ])

        if module.get("assessment_result"):
            seen_results.append(module.get("assessment_result"))
            sources.append(source(
                "Assessment Result",
                "Assessment Result",
                module.get("assessment_result"),
                "Result"
            ))

    for result in results:
        if int(result.get("docstatus") or 0) != 1:
            continue

        if result.get("name") in seen_results:
            continue

        score = result.get("total_score")
        maximum = result.get("maximum_score")
        score_text = "Not recorded"

        if score is not None and score != "":
            score_text = str(score)

            if maximum is not None and maximum != "":
                score_text = score_text + "/" + str(maximum)

        rows.append([
            clean_text(result.get("course") or result.get("assessment_name") or "Assessment"),
            format_date(result.get("assessment_date") or result.get("custom_issued_date") or result.get("modified")),
            score_text,
            clean_text(result.get("grade") or "Not recorded"),
            "Submitted"
        ])
        sources.append(source(
            "Assessment Result",
            "Assessment Result",
            result.get("name"),
            "Result"
        ))

    submitted_count = len([
        row for row in rows
        if row[4] == "Submitted"
    ])

    answer = (
        context.get("student_name")
        + " has " + str(submitted_count)
        + " submitted result(s). All recorded module results are shown below."
    )

    visuals = [{
        "type": "table",
        "title": "All module results",
        "columns": ["Module / Assessment", "Assessment Date", "Mark", "Grade", "Status"],
        "rows": rows
    }] if rows else []

    if not rows:
        answer = "No module or assessment results were found for " + context.get("student_name") + "."

    return response_base(answer, visuals=visuals, sources=sources, ai_used=ai_used)


def handle_nationality(context, ai_used):
    applicant = context.get("applicant") or {}
    nationality = clean_text(
        applicant.get("nationality")
        or applicant.get("custom_nationality")
        or applicant.get("citizenship")
        or applicant.get("country")
    )

    if nationality:
        answer = context.get("student_name") + "'s nationality is recorded as " + nationality + "."
    else:
        answer = "Nationality is not recorded for " + context.get("student_name") + "."

    return response_base(answer, sources=context.get("sources"), ai_used=ai_used)


def handle_lifecycle(context, ai_used):
    admission = context.get("admission") or {}
    student_doc = context.get("student_doc")
    academic_status = clean_text(student_doc.get("custom_academic_status") if student_doc else "")
    modules = context.get("modules") or []
    submitted = len([module for module in modules if module.get("assessment_result")])
    current_date = context.get("current_date")
    current_modules = []

    for module in modules:
        start = iso_date(module.get("start_date"))
        end = iso_date(module.get("end_date"))

        if start and end and start <= current_date <= end:
            current_modules.append(module_label(module))

    visuals = [{
        "type": "summary",
        "title": "Student lifecycle",
        "items": [
            {"label": "Student", "value": context.get("student_name")},
            {"label": "Programme", "value": admission.get("program") or "Not recorded"},
            {"label": "Commencement", "value": format_date(admission.get("date_of_commencement") or admission.get("commencement_date"))},
            {"label": "Current Module", "value": ", ".join(current_modules) if current_modules else "No active module today"},
            {"label": "Modules", "value": str(len(modules))},
            {"label": "Submitted Results", "value": str(submitted)},
            {"label": "Completion", "value": format_date(admission.get("completion_date"))},
            {"label": "Academic Status", "value": academic_status or "Not recorded"}
        ]
    }]

    answer = (
        context.get("student_name")
        + " started on "
        + format_date(admission.get("date_of_commencement") or admission.get("commencement_date"))
        + ", has " + str(len(modules)) + " scheduled module(s), "
        + str(submitted) + " submitted result(s), and is scheduled to complete on "
        + format_date(admission.get("completion_date")) + "."
    )

    return response_base(answer, visuals=visuals, sources=context.get("sources"), ai_used=ai_used)

def ordinal_from_question(question):
    q = normalise(question)

    values = {
        "1st": 1, "first": 1,
        "2nd": 2, "second": 2,
        "3rd": 3, "third": 3,
        "4th": 4, "fourth": 4
    }

    for token in q.split():
        if token in values:
            return values.get(token)

    return 1


def handle_assessment_date(context, question, ai_used):
    q = normalise(question)
    matches = []

    for result in context.get("assessment_results") or []:
        combined = normalise(
            clean_text(result.get("assessment_name"))
            + " " + clean_text(result.get("course"))
            + " " + clean_text(result.get("program"))
        )

        if "mock" in q and "mock" not in combined:
            continue

        if "ielts" in q and "ielts" not in combined:
            continue

        date = iso_date(
            result.get("assessment_date")
            or result.get("custom_issued_date")
            or result.get("modified")
        )

        if date:
            result["resolved_date"] = date
            matches.append(result)

    matches = sorted(matches, key=lambda item: item.get("resolved_date") or "")
    ordinal = ordinal_from_question(question)

    if len(matches) < ordinal:
        return response_base(
            "Only " + str(len(matches)) + " matching IELTS mock test record(s) were found for " + context.get("student_name") + ".",
            sources=context.get("sources"),
            ai_used=ai_used
        )

    selected = matches[ordinal - 1]
    answer = (
        context.get("student_name")
        + " took the " + str(ordinal)
        + " IELTS mock test on " + format_date(selected.get("resolved_date")) + "."
    )

    sources = list(context.get("sources") or [])
    sources.append(source("Assessment Result", "Assessment Result", selected.get("name"), "Mock test"))
    return response_base(answer, sources=sources, ai_used=ai_used)


def handle_leave_status(context, ai_used):
    today = context.get("current_date")
    active = []

    for leave in context.get("leaves") or []:
        start = iso_date(leave.get("from_date"))
        end = iso_date(leave.get("to_date"))

        if approved_workflow(leave.get("workflow_state")) and start and end and start <= today <= end:
            active.append(leave)

    if active:
        leave = active[0]
        answer = (
            "Yes. " + context.get("student_name")
            + " is on leave from " + format_date(leave.get("from_date"))
            + " to " + format_date(leave.get("to_date")) + "."
        )
        sources = list(context.get("sources") or [])
        sources.append(source("Leave Application", "Student Leave Application", leave.get("name"), "Leave"))
    else:
        answer = "No current approved leave was found for " + context.get("student_name") + "."
        sources = context.get("sources")

    return response_base(answer, sources=sources, ai_used=ai_used)



def handle_all_results(context, ai_used):
    modules = context.get("modules") or []

    graded_count = len([
        module for module in modules
        if module.get("assessment_result")
    ])
    answer = (
        str(len(modules))
        + " module record(s) were found for "
        + context.get("student_name")
        + ". "
        + str(graded_count)
        + " have submitted results."
    )

    visuals = [{
        "type": "table",
        "title": "All module results",
        "columns": [
            "Module",
            "Start Date",
            "End Date",
            "Mark",
            "Grade",
            "Status"
        ],
        "rows": [[
            module_label(module),
            format_date(module.get("start_date")),
            format_date(module.get("end_date")),
            str(module.get("score"))
                if module.get("score") is not None
                else "Not recorded",
            module.get("grade") or "Not recorded",
            "Submitted"
                if module.get("assessment_result")
                else "Not graded"
        ] for module in modules]
    }]

    sources = list(context.get("sources") or [])

    for module in modules:
        if module.get("assessment_result"):
            sources.append(
                source(
                    "Assessment Result",
                    "Assessment Result",
                    module.get("assessment_result"),
                    "Result"
                )
            )

    return response_base(
        answer,
        visuals=visuals,
        sources=sources,
        ai_used=ai_used
    )


def handle_nationality(context, ai_used):
    applicant = context.get("applicant") or {}

    nationality = clean_text(
        applicant.get("nationality")
        or applicant.get("country")
        or applicant.get("citizenship")
    )

    if not nationality:
        applicant_doc = get_doc_safe(
            "Student Applicant",
            applicant.get("name")
        )

        if applicant_doc:
            nationality = clean_text(
                applicant_doc.get("nationality")
                or applicant_doc.get("country")
                or applicant_doc.get("citizenship")
            )

    if nationality:
        answer = (
            context.get("student_name")
            + "'s recorded nationality is "
            + nationality
            + "."
        )
    else:
        answer = (
            "Nationality is not recorded for "
            + context.get("student_name")
            + "."
        )

    return response_base(
        answer,
        sources=context.get("sources"),
        ai_used=ai_used
    )

def handle_attendance(context, ai_used):
    attendance = context.get("attendance") or {}
    summary = attendance.get("summary") or {}
    records = attendance.get("records") or []

    if not records:
        return response_base(
            "No attendance records were found for " + context.get("student_name") + ".",
            sources=context.get("sources"),
            ai_used=ai_used
        )

    rate = summary.get("rate")
    rate_text = "Not recorded"

    if rate is not None:
        rate_text = str(round(rate, 1)) + "%"

    answer = (
        context.get("student_name")
        + " has "
        + str(summary.get("present") or 0)
        + " present, "
        + str(summary.get("late") or 0)
        + " late, and "
        + str(summary.get("absent") or 0)
        + " absent attendance record(s). Attendance rate: "
        + rate_text
        + "."
    )

    visuals = [{
        "type": "summary",
        "title": "Attendance summary",
        "items": [
            {"label": "Present", "value": summary.get("present") or 0},
            {"label": "Late", "value": summary.get("late") or 0},
            {"label": "Absent", "value": summary.get("absent") or 0},
            {"label": "Other", "value": summary.get("other") or 0},
            {"label": "Total Records", "value": summary.get("total") or 0},
            {"label": "Attendance Rate", "value": rate_text}
        ]
    }]

    sources = list(context.get("sources") or [])

    for row in records[-10:]:
        sources.append(
            source(
                "Attendance",
                "Student Attendance",
                row.get("name"),
                "Attendance"
            )
        )

    return response_base(
        answer,
        visuals=visuals,
        sources=sources,
        ai_used=ai_used
    )


def handle_student_group(context, ai_used):
    groups = context.get("groups") or []

    if not groups:
        return response_base(
            "No Student Group could be confirmed for " + context.get("student_name") + ".",
            sources=context.get("sources"),
            ai_used=ai_used
        )

    answer = (
        str(len(groups))
        + " Student Group record(s) were found for "
        + context.get("student_name")
        + "."
    )

    visuals = [{
        "type": "table",
        "title": "Student groups",
        "columns": [
            "Student Group",
            "Group Name",
            "Programme",
            "Module",
            "Start Date",
            "End Date",
            "Instructor"
        ],
        "rows": [[
            group.get("name") or "",
            group.get("student_group_name") or "",
            group.get("program") or "",
            group.get("course") or "",
            format_date(group.get("start_date")),
            format_date(group.get("end_date")),
            group.get("instructor") or "Not recorded"
        ] for group in groups]
    }]

    sources = list(context.get("sources") or [])

    for group in groups:
        sources.append(
            source(
                "Student Group",
                "Student Group",
                group.get("name"),
                "Class"
            )
        )

    return response_base(
        answer,
        visuals=visuals,
        sources=sources,
        ai_used=ai_used
    )
def handle_full_journey(context, ai_used):
    admission = context.get("admission") or {}
    applicant = context.get("applicant") or {}
    student_doc = context.get("student_doc")
    academic_status = clean_text(
        student_doc.get("custom_academic_status")
        if student_doc
        else ""
    )
    modules = deduplicate_modules(context.get("modules") or [])
    leaves = context.get("leaves") or []
    timeline_items = []

    commencement = (
        admission.get("date_of_commencement")
        or admission.get("commencement_date")
    )

    if commencement:
        timeline_items.append({
            "sort_date": iso_date(commencement),
            "date": format_date(commencement),
            "title": "Course commenced",
            "description": admission.get("program") or ""
        })

    for module in modules:
        timeline_items.append({
            "sort_date": iso_date(module.get("start_date")),
            "date": format_date(module.get("start_date")),
            "title": "Module started",
            "description": module_label(module)
        })

        if module.get("assessment_result"):
            result_description = module_label(module)

            if module.get("score") is not None:
                result_description = result_description + " | Mark " + str(module.get("score"))

            result_description = result_description + " | Grade " + clean_text(
                module.get("grade") or "Not recorded"
            )

            result_date = module.get("assessment_date") or module.get("end_date")
            timeline_items.append({
                "sort_date": iso_date(result_date),
                "date": format_date(result_date),
                "title": "Result recorded",
                "description": result_description
            })

    for leave in leaves:
        timeline_items.append({
            "sort_date": iso_date(leave.get("from_date")),
            "date": format_date(leave.get("from_date")),
            "title": "Leave",
            "description": (
                format_date(leave.get("from_date"))
                + " to "
                + format_date(leave.get("to_date"))
            )
        })

    completion = admission.get("completion_date")

    if completion:
        timeline_items.append({
            "sort_date": iso_date(completion),
            "date": format_date(completion),
            "title": "Scheduled course completion",
            "description": "Scheduled completion does not confirm graduation."
        })

    timeline_items = sorted(
        timeline_items,
        key=lambda item: item.get("sort_date") or "9999-12-31"
    )

    for item in timeline_items:
        if "sort_date" in item:
            del item["sort_date"]

    submitted_count = len([
        module for module in modules
        if module.get("assessment_result")
    ])

    visuals = [
        {
            "type": "summary",
            "title": "Journey summary",
            "items": [
                {"label": "Student", "value": context.get("student_name")},
                {"label": "Programme", "value": admission.get("program") or ""},
                {"label": "Study Type", "value": applicant.get("student_type") or "Not recorded"},
                {"label": "Commencement", "value": format_date(commencement)},
                {"label": "Completion", "value": format_date(completion)},
                {"label": "Academic Status", "value": academic_status or "Not recorded"},
                {"label": "Unique Modules", "value": str(len(modules))},
                {"label": "Submitted Results", "value": str(submitted_count)}
            ]
        },
        {
            "type": "timeline",
            "title": "Student journey timeline",
            "items": timeline_items
        },
        {
            "type": "table",
            "title": "Modules and results",
            "columns": [
                "Module", "Start Date", "End Date",
                "Mark", "Grade", "Result Status"
            ],
            "rows": [[
                module_label(module),
                format_date(module.get("start_date")),
                format_date(module.get("end_date")),
                str(module.get("score")) if module.get("score") is not None else "Not recorded",
                module.get("grade") or "Not recorded",
                "Submitted" if module.get("assessment_result") else "Not graded"
            ] for module in modules]
        }
    ]

    answer = "Student journey for " + context.get("student_name") + "."
    return response_base(
        answer,
        visuals=visuals,
        sources=context.get("sources"),
        ai_used=ai_used
    )

def find_student_invoices(context):
    student_id = normalise(context.get("student_id"))
    student_name = normalise(context.get("student_name"))
    applicant_id = normalise((context.get("applicant") or {}).get("name"))

    rows = safe_db_list(
        "Sales Invoice",
        filters={"docstatus": 1},
        fields=[
            "name", "posting_date", "due_date", "customer",
            "customer_name", "currency", "grand_total",
            "outstanding_amount", "status"
        ],
        order_by="posting_date asc, modified asc",
        limit=5000
    )

    matched = []

    for row in rows:
        searchable = normalise(
            clean_text(row.get("customer"))
            + " "
            + clean_text(row.get("customer_name"))
        )

        is_match = False

        if student_id and student_id in searchable:
            is_match = True

        if applicant_id and applicant_id in searchable:
            is_match = True

        if student_name and student_name in searchable:
            is_match = True

        if is_match:
            matched.append(row)

    return matched


def finance_summary(context):
    invoices = find_student_invoices(context)
    invoiced = 0.0
    outstanding = 0.0

    for invoice in invoices:
        try:
            invoiced = invoiced + float(invoice.get("grand_total") or 0)
        except Exception:
            pass

        try:
            outstanding = outstanding + float(
                invoice.get("outstanding_amount") or 0
            )
        except Exception:
            pass

    paid = invoiced - outstanding

    return {
        "invoices": invoices,
        "invoiced": invoiced,
        "paid": paid,
        "outstanding": outstanding
    }


def handle_finance(context, ai_used):
    summary = finance_summary(context)
    invoices = summary.get("invoices") or []

    if not invoices:
        return response_base(
            "No submitted Sales Invoice could be matched to "
            + context.get("student_name")
            + ".",
            sources=context.get("sources"),
            warnings=[
                "This answer uses Sales Invoice customer matching. "
                "A custom student billing link may require field mapping."
            ],
            ai_used=ai_used
        )

    currency = clean_text(invoices[0].get("currency")) or ""
    prefix = currency + " " if currency else ""

    answer = (
        context.get("student_name")
        + " has "
        + str(len(invoices))
        + " submitted invoice(s). Total invoiced: "
        + prefix
        + str(round(summary.get("invoiced") or 0, 2))
        + ". Estimated paid: "
        + prefix
        + str(round(summary.get("paid") or 0, 2))
        + ". Outstanding: "
        + prefix
        + str(round(summary.get("outstanding") or 0, 2))
        + "."
    )

    visuals = [{
        "type": "table",
        "title": "Invoices and payment status",
        "columns": [
            "Invoice", "Posting Date", "Due Date",
            "Total", "Outstanding", "Status"
        ],
        "rows": [[
            link_cell(
                invoice.get("name"),
                "Sales Invoice",
                invoice.get("name")
            ),
            format_date(invoice.get("posting_date")),
            format_date(invoice.get("due_date")),
            str(invoice.get("grand_total") or 0),
            str(invoice.get("outstanding_amount") or 0),
            invoice.get("status") or ""
        ] for invoice in invoices]
    }]

    sources = list(context.get("sources") or [])

    for invoice in invoices:
        sources.append(
            source(
                "Sales Invoice",
                "Sales Invoice",
                invoice.get("name"),
                "Invoice"
            )
        )

    return response_base(
        answer,
        visuals=visuals,
        sources=sources,
        ai_used=ai_used
    )


def handle_documents(context, ai_used):
    applicant = context.get("applicant") or {}
    applicant_id = applicant.get("name") or ""

    files = safe_db_list(
        "File",
        filters={
            "attached_to_doctype": "Student Applicant",
            "attached_to_name": applicant_id
        },
        fields=[
            "name", "file_name", "file_url",
            "is_private", "creation"
        ],
        order_by="creation asc",
        limit=500
    )

    answer = (
        str(len(files))
        + " file attachment(s) were found on the Student Applicant record for "
        + context.get("student_name")
        + "."
    )

    warnings = [
        "Attachment count does not confirm that every required admission "
        "document has been submitted. A formal checklist field is needed "
        "for a definitive missing-document verdict."
    ]

    visuals = []

    if files:
        visuals = [{
            "type": "table",
            "title": "Applicant attachments",
            "columns": ["File", "Uploaded On", "Private"],
            "rows": [[
                item.get("file_name") or item.get("name") or "",
                format_date(item.get("creation")),
                "Yes" if int(item.get("is_private") or 0) == 1 else "No"
            ] for item in files]
        }]

    sources = list(context.get("sources") or [])

    for item in files:
        sources.append(
            source(
                "File",
                "File",
                item.get("name"),
                "Document"
            )
        )

    return response_base(
        answer,
        visuals=visuals,
        sources=sources,
        warnings=warnings,
        ai_used=ai_used
    )


def handle_fps(context, ai_used):
    admission = context.get("admission") or {}
    applicant = context.get("applicant") or {}
    fps_value = ""

    fps_fields = [
        "fps_status", "custom_fps_status",
        "fee_protection_status", "custom_fee_protection_status",
        "fps_reference", "custom_fps_reference"
    ]

    admission_doc = get_doc_safe(
        "Student Admission UCC",
        admission.get("name")
    )

    for fieldname in fps_fields:
        if admission_doc and clean_text(admission_doc.get(fieldname)):
            fps_value = clean_text(admission_doc.get(fieldname))
            break

    if not fps_value:
        applicant_doc = get_doc_safe(
            "Student Applicant",
            applicant.get("name")
        )

        for fieldname in fps_fields:
            if applicant_doc and clean_text(applicant_doc.get(fieldname)):
                fps_value = clean_text(applicant_doc.get(fieldname))
                break

    if fps_value:
        answer = (
            "The recorded FPS information for "
            + context.get("student_name")
            + " is "
            + fps_value
            + "."
        )
        warnings = []
    else:
        answer = (
            "No FPS status or reference was found in the recognised "
            "Student Applicant or Student Admission fields for "
            + context.get("student_name")
            + "."
        )
        warnings = [
            "Your FPS field may use a different custom fieldname. "
            "Map that fieldname before treating this as a final verdict."
        ]

    return response_base(
        answer,
        sources=context.get("sources"),
        warnings=warnings,
        ai_used=ai_used
    )


def graduation_readiness_data(context):
    today = context.get("current_date")
    modules = context.get("modules") or []
    not_ended = []
    missing_results = []

    for module in modules:
        end_date = iso_date(module.get("end_date"))

        if not end_date or end_date >= today:
            not_ended.append(module)

        if not module.get("assessment_result"):
            missing_results.append(module)

    finance = finance_summary(context)
    outstanding = finance.get("outstanding") or 0
    student_doc = context.get("student_doc")
    academic_status = normalise(
        student_doc.get("custom_academic_status")
        if student_doc
        else ""
    )

    blockers = []

    if not modules:
        blockers.append("No module schedule was found")

    if not_ended:
        blockers.append(
            str(len(not_ended))
            + " module period(s) have not ended"
        )

    if missing_results:
        blockers.append(
            str(len(missing_results))
            + " module result(s) are not submitted"
        )

    if outstanding > 0:
        blockers.append(
            "Outstanding invoiced amount: "
            + str(round(outstanding, 2))
        )

    return {
        "blockers": blockers,
        "not_ended": not_ended,
        "missing_results": missing_results,
        "finance": finance,
        "academic_status": academic_status
    }


def handle_graduation_readiness(context, ai_used):
    readiness = graduation_readiness_data(context)
    blockers = readiness.get("blockers") or []

    if blockers:
        answer = (
            context.get("student_name")
            + " is not yet clear for graduation based on the available "
            "ERPNext records. "
            + "; ".join(blockers)
            + "."
        )
    else:
        answer = (
            "No module, result or outstanding-invoice blocker was found for "
            + context.get("student_name")
            + ". Final graduation still requires authorised academic approval."
        )

    visuals = [{
        "type": "summary",
        "title": "Graduation readiness",
        "items": [
            {
                "label": "Module Periods Not Ended",
                "value": len(readiness.get("not_ended") or [])
            },
            {
                "label": "Missing Submitted Results",
                "value": len(readiness.get("missing_results") or [])
            },
            {
                "label": "Outstanding Amount",
                "value": round(
                    (readiness.get("finance") or {}).get("outstanding") or 0,
                    2
                )
            },
            {
                "label": "Academic Status",
                "value": readiness.get("academic_status") or "Not recorded"
            },
            {
                "label": "Readiness",
                "value": "Blocked" if blockers else "No detected blocker"
            }
        ]
    }]

    sources = list(context.get("sources") or [])

    for invoice in (readiness.get("finance") or {}).get("invoices") or []:
        sources.append(
            source(
                "Sales Invoice",
                "Sales Invoice",
                invoice.get("name"),
                "Invoice"
            )
        )

    return response_base(
        answer,
        visuals=visuals,
        sources=sources,
        warnings=[
            "This is an operational readiness check, not an official "
            "graduation decision."
        ],
        ai_used=ai_used
    )


def handle_risk_summary(context, ai_used):
    readiness = graduation_readiness_data(context)
    attendance = context.get("attendance") or {}
    attendance_summary = attendance.get("summary") or {}
    attendance_rate = attendance_summary.get("rate")
    leaves = context.get("leaves") or []
    today = context.get("current_date")
    active_leave = 0
    risks = []
    actions = []

    if attendance_rate is not None and attendance_rate < 90:
        risks.append(
            "Attendance is below 90% at "
            + str(round(attendance_rate, 1))
            + "%"
        )
        actions.append("Review attendance and intervention records")

    missing_results = readiness.get("missing_results") or []

    if missing_results:
        risks.append(
            str(len(missing_results))
            + " module result(s) are not submitted"
        )
        actions.append("Confirm assessment completion and result submission")

    outstanding = (
        readiness.get("finance") or {}
    ).get("outstanding") or 0

    if outstanding > 0:
        risks.append(
            "Outstanding invoiced amount is "
            + str(round(outstanding, 2))
        )
        actions.append("Review payment status with Finance")

    for leave in leaves:
        start_date = iso_date(leave.get("from_date"))
        end_date = iso_date(leave.get("to_date"))

        if (
            approved_workflow(leave.get("workflow_state"))
            and start_date
            and end_date
            and start_date <= today <= end_date
        ):
            active_leave = active_leave + 1

    if active_leave:
        risks.append("The student is currently on approved leave")
        actions.append("Check whether the leave affects attendance or completion")

    if risks:
        risk_level = "High" if len(risks) >= 3 else "Medium"
        answer = (
            risk_level
            + " operational risk detected for "
            + context.get("student_name")
            + ": "
            + "; ".join(risks)
            + "."
        )
    else:
        risk_level = "Low"
        answer = (
            "No major attendance, result, leave or outstanding-invoice risk "
            "was detected for "
            + context.get("student_name")
            + "."
        )

    visuals = [
        {
            "type": "summary",
            "title": "Risk overview",
            "items": [
                {"label": "Risk Level", "value": risk_level},
                {
                    "label": "Attendance Rate",
                    "value": (
                        str(round(attendance_rate, 1)) + "%"
                        if attendance_rate is not None
                        else "Not recorded"
                    )
                },
                {
                    "label": "Missing Results",
                    "value": len(missing_results)
                },
                {
                    "label": "Outstanding Amount",
                    "value": round(outstanding, 2)
                },
                {
                    "label": "Current Leave",
                    "value": "Yes" if active_leave else "No"
                }
            ]
        }
    ]

    if actions:
        visuals.append({
            "type": "table",
            "title": "Recommended follow-up",
            "columns": ["No.", "Action"],
            "rows": [
                [str(index + 1), action]
                for index, action in enumerate(actions)
            ]
        })

    return response_base(
        answer,
        visuals=visuals,
        sources=context.get("sources"),
        warnings=[
            "Risk level is rule-based and must be reviewed by authorised staff."
        ],
        ai_used=ai_used
    )
def handle_profile(context, ai_used):
    admission = context.get("admission") or {}
    applicant = context.get("applicant") or {}
    student_doc = context.get("student_doc")
    academic_status = clean_text(
        student_doc.get("custom_academic_status")
        if student_doc
        else ""
    )

    nationality = clean_text(
        applicant.get("nationality")
        or applicant.get("country")
        or applicant.get("citizenship")
    )

    answer = (
        context.get("student_name")
        + " is enrolled in "
        + clean_text(
            admission.get("program")
            or applicant.get("program")
            or "a programme that is not recorded"
        )
        + "."
    )

    visuals = [{
        "type": "summary",
        "title": "Student profile",
        "items": [
            {"label": "Student", "value": context.get("student_name")},
            {"label": "Applicant ID", "value": applicant.get("name") or ""},
            {"label": "Student ID", "value": context.get("student_id") or "Not recorded"},
            {"label": "Programme", "value": admission.get("program") or applicant.get("program") or ""},
            {"label": "Study Type", "value": applicant.get("student_type") or "Not recorded"},
            {"label": "Nationality", "value": nationality or "Not recorded"},
            {"label": "Academic Status", "value": academic_status or "Not recorded"},
            {"label": "Commencement", "value": format_date(admission.get("date_of_commencement") or admission.get("commencement_date"))},
            {"label": "Completion", "value": format_date(admission.get("completion_date"))}
        ]
    }]

    return response_base(
        answer,
        visuals=visuals,
        sources=context.get("sources"),
        ai_used=ai_used
    )
def all_admissions():
    return safe_db_list(
        "Student Admission UCC",
        filters={"docstatus": ["<", 2]},
        fields=[
            "name", "student_applicant", "student", "student_name", "program",
            "commencement_date", "date_of_commencement", "completion_date",
            "application_status", "modified"
        ],
        order_by="student_name asc, modified desc",
        limit=10000
    )


def cohort_rows(keyword, start_date, end_date):
    admissions = all_admissions()
    selected = []
    seen = []

    for admission in admissions:
        if keyword and not programme_matches(admission.get("program"), keyword):
            continue

        if not active_in_range(admission, start_date, end_date):
            continue

        key = admission.get("student") or admission.get("student_applicant") or admission.get("name")

        if key in seen:
            continue

        seen.append(key)
        selected.append(admission)

    return selected


def handle_cohort_count(question, ai_used):
    period = month_range_from_question(question)
    rows = cohort_rows("ielts", period.get("start_date"), period.get("end_date"))

    answer = str(len(rows)) + " IELTS student(s) were active in " + period.get("label") + "."
    sources = [source("Admission", "Student Admission UCC", row.get("name"), "Admission") for row in rows[:50]]
    return response_base(answer, sources=sources, ai_used=ai_used)


def handle_cohort_types(question, ai_used):
    today = str(frappe.utils.today())[:10]
    rows = cohort_rows("ielts", today, today)
    applicant_map = get_applicant_map([row.get("student_applicant") for row in rows])
    output_rows = []
    counts = {"full time": 0, "part time": 0, "short course": 0, "other": 0}

    for row in rows:
        applicant = applicant_map.get(row.get("student_applicant")) or {}
        student_type = clean_text(applicant.get("student_type") or "Not recorded")
        normalised_type = normalise(student_type)

        if "full" in normalised_type:
            counts["full time"] = counts.get("full time") + 1
        elif "part" in normalised_type:
            counts["part time"] = counts.get("part time") + 1
        elif "short" in normalised_type:
            counts["short course"] = counts.get("short course") + 1
        else:
            counts["other"] = counts.get("other") + 1

        output_rows.append([
            row.get("student_name") or full_applicant_name(applicant) or row.get("student_applicant") or "",
            student_type,
            row.get("program") or "",
            format_date(row.get("date_of_commencement") or row.get("commencement_date")),
            format_date(row.get("completion_date"))
        ])

    answer = (
        "Current IELTS students: "
        + str(counts.get("full time")) + " full time, "
        + str(counts.get("part time")) + " part time, "
        + str(counts.get("short course")) + " short course"
    )

    if counts.get("other"):
        answer = answer + ", " + str(counts.get("other")) + " other or not recorded"

    answer = answer + "."

    visuals = [{
        "type": "table",
        "title": "Current IELTS students by study type",
        "columns": ["Student", "Study Type", "Programme", "Commencement", "Completion"],
        "rows": output_rows
    }]
    sources = [source("Admission", "Student Admission UCC", row.get("name"), "Admission") for row in rows[:50]]
    return response_base(answer, visuals=visuals, sources=sources, ai_used=ai_used)


def group_is_ielts(group_doc):
    combined = normalise(
        clean_text(group_doc.get("name"))
        + " " + clean_text(group_doc.get("student_group_name"))
        + " " + clean_text(group_doc.get("program"))
        + " " + clean_text(group_doc.get("course"))
        + " " + clean_text(group_doc.get("custom_course_name"))
    )
    return "ielts" in combined


def handle_class_today(ai_used, student_roll_rows):
    today = str(frappe.utils.today())[:10]

    schedules = safe_db_list(
        "Course Schedule",
        filters={"schedule_date": today},
        fields=[
            "name", "student_group", "course",
            "schedule_date", "from_time", "to_time"
        ],
        order_by="from_time asc",
        limit=2000
    )

    scheduled_groups = []
    schedule_course_map = {}

    for schedule in schedules:
        group_name = clean_text(schedule.get("student_group"))

        if not group_name:
            continue

        if group_name not in scheduled_groups:
            scheduled_groups.append(group_name)

        if group_name not in schedule_course_map:
            schedule_course_map[group_name] = clean_text(
                schedule.get("course")
            )

    normalised_rows = []

    for raw_row in student_roll_rows or []:
        row = normalise_student_roll_row(raw_row)
        group_name = clean_text(
            raw_row.get("module_class_details_id")
            or raw_row.get("student_group")
            or row.get("student_group")
        )

        normalised_rows.append({
            "raw": raw_row,
            "row": row,
            "group": group_name,
            "start_date": iso_date(
                raw_row.get("module_start_date")
                or row.get("start_date")
            ),
            "end_date": iso_date(
                raw_row.get("module_end_date")
                or row.get("end_date")
            )
        })

    represented_scheduled_groups = []

    for item in normalised_rows:
        if item.get("group") in scheduled_groups:
            represented_scheduled_groups.append(item.get("group"))

    rows = []
    seen = []
    sources = []

    for item in normalised_rows:
        raw_row = item.get("raw") or {}
        row = item.get("row") or {}
        group_name = item.get("group")
        start_date = item.get("start_date")
        end_date = item.get("end_date")

        include_row = False

        if group_name in scheduled_groups:
            include_row = True
        elif (
            group_name
            and group_name not in represented_scheduled_groups
            and start_date
            and end_date
            and start_date <= today <= end_date
        ):
            # Some Course Schedule rows use a different or incomplete
            # Student Group link. Include active Student Roll groups so
            # Diploma and other classes are not omitted.
            include_row = True

        if not include_row:
            continue

        student_name = clean_text(
            raw_row.get("student_name")
            or row.get("student_name")
        )
        applicant_id = clean_text(
            raw_row.get("student_applicant_id")
            or row.get("student_applicant")
        )
        student_id = clean_text(
            raw_row.get("student")
            or raw_row.get("student_id")
            or applicant_id
        )
        study_type = clean_text(
            raw_row.get("student_type")
            or row.get("student_type")
        )
        programme = clean_text(
            raw_row.get("course")
            or row.get("course")
            or schedule_course_map.get(group_name)
        )

        key = (
            student_name
            + "|"
            + applicant_id
            + "|"
            + group_name
        )

        if key in seen:
            continue

        seen.append(key)
        rows.append([
            student_name or applicant_id,
            student_id or applicant_id or "Not recorded",
            study_type or "Not recorded",
            programme or "Not recorded",
            group_name or "Not recorded"
        ])

        if group_name:
            sources.append(
                source(
                    "Student Group",
                    "Student Group",
                    group_name,
                    "Class"
                )
            )

    rows = sorted(
        rows,
        key=lambda row: (
            clean_text(row[3]),
            clean_text(row[4]),
            clean_text(row[0])
        )
    )

    class_groups_in_rows = []

    for row in rows:
        group_name = clean_text(row[4])

        if group_name and group_name not in class_groups_in_rows:
            class_groups_in_rows.append(group_name)

    if schedules:
        answer = (
            str(len(rows))
            + " student-class record(s) are shown across "
            + str(len(class_groups_in_rows))
            + " matched class group(s). "
            + str(len(scheduled_groups))
            + " Course Schedule group(s) were recorded for today."
        )
        confidence = "Confirmed"
        warnings = []

        if len(class_groups_in_rows) < len(scheduled_groups):
            warnings.append(
                str(len(scheduled_groups) - len(class_groups_in_rows))
                + " scheduled group(s) had no matching Student Roll rows."
            )
    else:
        answer = (
            str(len(rows))
            + " student-class record(s) have module periods covering today."
        )
        confidence = "Partial"
        warnings = [
            "No Course Schedule was found for today. "
            "Student Roll module dates were used."
        ]

    visuals = [
        {
            "type": "summary",
            "title": "Class coverage today",
            "items": [
                {
                    "label": "Course Schedule Groups",
                    "value": len(scheduled_groups)
                },
                {
                    "label": "Matched Student Groups",
                    "value": len(class_groups_in_rows)
                },
                {
                    "label": "Student-Class Records",
                    "value": len(rows)
                }
            ]
        },
        {
            "type": "table",
            "title": "Students in class today",
            "columns": [
                "Student", "Student / Applicant ID",
                "Study Type", "Programme", "Student Group"
            ],
            "rows": rows
        }
    ] if rows else [{
        "type": "summary",
        "title": "Class coverage today",
        "items": [
            {
                "label": "Course Schedule Groups",
                "value": len(scheduled_groups)
            },
            {
                "label": "Matched Student Groups",
                "value": 0
            },
            {
                "label": "Student-Class Records",
                "value": 0
            }
        ]
    }]

    return response_base(
        answer,
        visuals=visuals,
        sources=sources,
        warnings=warnings,
        ai_used=ai_used,
        confidence=confidence if rows else "Missing data"
    )
def handle_graduation_list(question, strict_graduated, ai_used):
    period = month_range_from_question(question)
    admissions = safe_db_list(
        "Student Admission UCC",
        filters={
            "docstatus": ["<", 2],
            "completion_date": ["between", [period.get("start_date"), period.get("end_date")]]
        },
        fields=[
            "name", "student_applicant", "student", "student_name", "program",
            "completion_date", "application_status"
        ],
        order_by="completion_date asc, student_name asc",
        limit=5000
    )

    student_map = get_student_map([row.get("student") for row in admissions])
    selected = []

    for admission in admissions:
        student = student_map.get(admission.get("student")) or {}
        academic_status = normalise(student.get("custom_academic_status"))

        if strict_graduated and academic_status != "graduated":
            continue

        selected.append({
            "admission": admission,
            "academic_status": student.get("custom_academic_status") or "Not recorded"
        })

    if strict_graduated:
        answer = str(len(selected)) + " student(s) are marked Graduated with completion dates in " + period.get("label") + "."
        title = "Students graduated in " + period.get("label")
    else:
        answer = str(len(selected)) + " student(s) are scheduled to complete in " + period.get("label") + ". Completion date alone does not confirm graduation."
        title = "Students completing in " + period.get("label")

    rows = []
    sources = []

    for item in selected:
        admission = item.get("admission")
        rows.append([
            admission.get("student_name") or admission.get("student_applicant") or "",
            admission.get("student") or admission.get("student_applicant") or "",
            admission.get("program") or "",
            format_date(admission.get("completion_date")),
            item.get("academic_status")
        ])
        sources.append(source("Admission", "Student Admission UCC", admission.get("name"), "Admission"))

    visuals = [{
        "type": "table",
        "title": title,
        "columns": ["Student", "Student / Applicant ID", "Programme", "Completion Date", "Academic Status"],
        "rows": rows
    }] if rows else []

    return response_base(answer, visuals=visuals, sources=sources, ai_used=ai_used)


def handle_leave_count(question, ai_used):
    period = date_range_from_question(question)
    leaves = safe_db_list(
        "Student Leave Application",
        filters={"docstatus": ["<", 2]},
        fields=[
            "name", "student", "student_name", "workflow_state", "from_date", "to_date",
            "total_leave_days", "reason"
        ],
        order_by="from_date asc",
        limit=10000
    )

    selected = []
    seen = []

    for leave in leaves:
        if not approved_workflow(leave.get("workflow_state")):
            continue

        start = iso_date(leave.get("from_date"))
        end = iso_date(leave.get("to_date"))

        if not start or not end:
            continue

        if start > period.get("end_date") or end < period.get("start_date"):
            continue

        key = leave.get("student") or leave.get("student_name") or leave.get("name")

        if key in seen:
            continue

        seen.append(key)
        selected.append(leave)

    answer = str(len(selected)) + " student(s) have approved leave overlapping " + period.get("label") + "."
    visuals = [{
        "type": "table",
        "title": "Students on leave",
        "columns": ["Student", "Student ID", "From", "To", "Status"],
        "rows": [[
            leave.get("student_name") or leave.get("student") or "",
            leave.get("student") or "",
            format_date(leave.get("from_date")),
            format_date(leave.get("to_date")),
            leave.get("workflow_state") or "Approved"
        ] for leave in selected]
    }] if selected else []
    sources = [source("Leave Application", "Student Leave Application", leave.get("name"), "Leave") for leave in selected]
    return response_base(answer, visuals=visuals, sources=sources, ai_used=ai_used)


question = clean_text(frappe.form_dict.get("question"))
request_api_key = clean_text(frappe.form_dict.get("openai_api_key"))
if request_api_key:
    OPENAI_API_KEY = request_api_key
selected_applicant = clean_text(frappe.form_dict.get("student_applicant"))
conversation_input = frappe.form_dict.get("conversation") or "[]"
student_roll_input = frappe.form_dict.get("student_roll_rows") or "[]"

try:
    conversation = json.loads(conversation_input) if isinstance(conversation_input, str) else conversation_input
except Exception:
    conversation = []

try:
    raw_student_roll_rows = json.loads(student_roll_input) if isinstance(student_roll_input, str) else student_roll_input
except Exception:
    raw_student_roll_rows = []

student_roll_rows = []

for raw_row in raw_student_roll_rows or []:
    if isinstance(raw_row, dict):
        student_roll_rows.append(normalise_student_roll_row(raw_row))

if not question:
    frappe.response["message"] = {
        "status": "error",
        "answer": "Please enter a question.",
        "visuals": [],
        "sources": [],
        "warnings": [],
        "ai_used": False
    }

else:
    direct_intent = detect_intent(question)

    if direct_intent == "unsupported":
        route = {
            "intent": "unsupported",
            "canonical_question": question,
            "ai_used": False
        }
    else:
        route = ai_route(question, conversation, selected_applicant)

    canonical_question = clean_text(route.get("canonical_question")) or question
    intent = clean_text(route.get("intent")) or direct_intent
    ai_used = bool(route.get("ai_used"))

    if detect_intent(question) == "unsupported":
        intent = "unsupported"
        canonical_question = question
        ai_used = False

    global_intents = [
        "class_today", "cohort_types", "cohort_count",
        "graduation_list", "graduated_list", "leave_count"
    ]

    if intent == "class_today":
        frappe.response["message"] = handle_class_today(ai_used, student_roll_rows)

    elif intent == "cohort_types":
        frappe.response["message"] = handle_cohort_types(canonical_question, ai_used)

    elif intent == "cohort_count":
        frappe.response["message"] = handle_cohort_count(canonical_question, ai_used)

    elif intent == "graduation_list":
        frappe.response["message"] = handle_graduation_list(canonical_question, False, ai_used)

    elif intent == "graduated_list":
        frappe.response["message"] = handle_graduation_list(canonical_question, True, ai_used)

    elif intent == "leave_count":
        frappe.response["message"] = handle_leave_count(canonical_question, ai_used)

    elif intent == "cohort_dashboard":
        frappe.response["message"] = handle_cohort_dashboard(student_roll_rows, ai_used)

    elif intent == "unsupported":
        frappe.response["message"] = response_base(
            "This is not an Admission Journey question. Ask about a student, course, module, result, attendance, leave, class, fees, graduation or cohort.",
            ai_used=False,
            confidence="Not applicable"
        )

    else:
        applicants = safe_db_list(
            "Student Applicant",
            filters={"docstatus": ["<", 2]},
            fields=["name", "first_name", "middle_name", "last_name", "student_type", "program"],
            order_by="modified desc",
            limit=5000
        )

        applicant_result = find_applicant(applicants, canonical_question, selected_applicant)

        if applicant_result.get("status") == "student_required":
            frappe.response["message"] = {
                "status": "student_required",
                "answer": "Please include the student's full name or Student Applicant ID.",
                "visuals": [],
                "sources": [],
                "warnings": [],
                "ai_used": ai_used
            }

        elif applicant_result.get("status") == "choose_student":
            frappe.response["message"] = {
                "status": "choose_student",
                "answer": "More than one student matches. Select the correct student.",
                "candidates": [candidate_output(item) for item in applicant_result.get("candidates") or []],
                "visuals": [],
                "sources": [],
                "warnings": [],
                "ai_used": ai_used
            }

        else:
            applicant = applicant_result.get("applicant")
            context = build_individual_context(applicant, student_roll_rows)

            if intent == "current_module":
                result = handle_current_module(context, ai_used)
            elif intent == "commencement":
                result = handle_commencement(context, ai_used)
            elif intent == "completion":
                result = handle_completion(context, ai_used)
            elif intent == "course":
                result = handle_course(context, ai_used)
            elif intent == "graduation_status":
                result = handle_graduation_status(context, ai_used)
            elif intent == "module_completion_status":
                result = handle_module_completion(context, ai_used)
            elif intent == "module_result":
                result = handle_module_result(context, canonical_question, ai_used)
            elif intent == "all_results":
                result = handle_all_results(context, ai_used)
            elif intent == "nationality":
                result = handle_nationality(context, ai_used)
            elif intent == "attendance":
                result = handle_attendance(context, ai_used)
            elif intent == "student_group":
                result = handle_student_group(context, ai_used)
            elif intent == "finance":
                result = handle_finance(context, ai_used)
            elif intent == "documents":
                result = handle_documents(context, ai_used)
            elif intent == "fps":
                result = handle_fps(context, ai_used)
            elif intent == "graduation_readiness":
                result = handle_graduation_readiness(context, ai_used)
            elif intent == "risk_summary":
                result = handle_risk_summary(context, ai_used)
            elif intent == "academic_progress":
                result = handle_academic_progress(context, ai_used)
            elif intent == "grade_analytics":
                result = handle_grade_analytics(context, ai_used)
            elif intent == "attendance_trend":
                result = handle_attendance_trend(context, ai_used)
            elif intent == "leave_history":
                result = handle_leave_history(context, ai_used)
            elif intent == "payment_timeline":
                result = handle_payment_timeline(context, ai_used)
            elif intent == "diagnostics":
                result = handle_diagnostics(context, intent, ai_used)
            elif intent == "lifecycle":
                result = handle_lifecycle(context, ai_used)
            elif intent == "assessment_date":
                result = handle_assessment_date(context, canonical_question, ai_used)
            elif intent == "leave_status":
                result = handle_leave_status(context, ai_used)
            elif intent == "all_results":
                result = handle_all_results(context, ai_used)
            elif intent == "nationality":
                result = handle_nationality(context, ai_used)
            elif intent == "full_journey":
                result = handle_full_journey(context, ai_used)
            else:
                result = handle_profile(context, ai_used)

            result["student_applicant"] = applicant.get("name")
            result["student_name"] = full_applicant_name(applicant)
            frappe.response["message"] = result
