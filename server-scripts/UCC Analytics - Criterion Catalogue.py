"""
UCC Intelligence Platform Server Script

Visible name:
    UCC Analytics - Criterion Catalogue

Script type:
    API

API method:
    ucc_analytics_criterion_catalogue

Purpose:
    Return the approved EduTrust Criterion 1–7 catalogue, policy versions,
    API methods and current live-readiness state.

Status:
    Criteria 1, 2, 3, 6 and 7 use permission-aware live API foundations.
    Criterion 4 is live through its mature permission-aware API.
    Criterion 5 remains live through the validated frontend with a migration API.

Deployment:
    Allow Guest must remain disabled.
"""

CRITERIA = [{'criterion': '1',
  'title': 'Leadership and Strategic Planning',
  'weight': 60,
  'status': 'live_foundation',
  'api_method': 'ucc_analytics_criterion_1',
  'subcriteria': [{'code': '1.1.1',
                   'title': 'Leadership and Corporate Governance',
                   'policy': 'PPD-SGL-CG-1.1.1',
                   'version': '2.2'},
                  {'code': '1.2.1', 'title': 'Strategic Planning', 'policy': 'PPD-SGL-SQ-1.2.1', 'version': '1.2'}]},
 {'criterion': '2',
  'title': 'Corporate Administration',
  'weight': 100,
  'status': 'live_foundation',
  'api_method': 'ucc_analytics_criterion_2',
  'subcriteria': [{'code': '2.1.1',
                   'title': 'Staff Selection and Management',
                   'policy': 'PPD-OEE-HR-2.1.1',
                   'version': '2.2'},
                  {'code': '2.1.2',
                   'title': 'Staff Training and Development',
                   'policy': 'PPD-OEE-HR-2.1.2',
                   'version': '1.2'},
                  {'code': '2.2.1',
                   'title': 'Internal and External Communication',
                   'policy': 'PPD-SES-MG-2.2.1',
                   'version': '1.2'},
                  {'code': '2.3.1',
                   'title': 'Data and Information Management',
                   'policy': 'PPD-OEE-IT-2.3.1',
                   'version': '1.2'},
                  {'code': '2.3.2', 'title': 'Knowledge Management', 'policy': 'PPD-OE-IT-2.3.2', 'version': '1.2'},
                  {'code': '2.4.1', 'title': 'Feedback Management', 'policy': 'PPD-SGL-SQ-2.4.1', 'version': '2.3'},
                  {'code': '2.4.2',
                   'title': 'Student Satisfaction Survey',
                   'policy': 'PPD-SGL-SQ-2.4.2',
                   'version': '2.2'},
                  {'code': '2.4.3',
                   'title': 'Staff Satisfaction Survey',
                   'policy': 'PPD-SGL-SQ-2.4.3',
                   'version': '2.2'}]},
 {'criterion': '3',
  'title': 'External Recruitment Agents',
  'weight': 60,
  'status': 'live_foundation',
  'api_method': 'ucc_analytics_criterion_3',
  'subcriteria': [{'code': '3.1.1',
                   'title': 'Selection and Appointment of External Recruitment Agents',
                   'policy': 'PPD-SES-SL-3.1.1',
                   'version': '1.2'},
                  {'code': '3.2.1',
                   'title': 'Management and Evaluation of Recruitment Agents',
                   'policy': 'PPD-SES-SL-3.2.1',
                   'version': '1.2'}]},
 {'criterion': '4',
  'title': 'Student Protection and Support Services',
  'weight': 200,
  'status': 'live',
  'api_method': 'ucc_analytics_criterion_4',
  'subcriteria': [{'code': '4.1.1',
                   'title': 'Pre-Course Counselling, Student Selection and Admissions',
                   'policy': 'PPD-SSO-AD-4.1.1'},
                  {'code': '4.2.1', 'title': 'Student Contract', 'policy': 'PPD-SSO-AD-4.2.1'},
                  {'code': '4.2.2', 'title': 'Fee Collection and Fee Protection Scheme', 'policy': 'PPD-SSO-AD-4.2.2'},
                  {'code': '4.3.1', 'title': 'Course Transfer, Deferment and Withdrawal', 'policy': 'PPD-SSO-SS-4.3.1'},
                  {'code': '4.4.1', 'title': 'Refund', 'policy': 'PPD-SSO-SS-4.4.1'},
                  {'code': '4.5.1', 'title': 'Student Support Services', 'policy': 'PPD-SSO-SS-4.5.1'},
                  {'code': '4.6.1',
                   'title': 'Student Conduct and Attendance',
                   'policy': 'PPD-SSO-SS-4.6.1',
                   'version': '2.2'}]},
 {'criterion': '5',
  'title': 'Academic Systems and Processes',
  'weight': 200,
  'status': 'live_frontend',
  'api_method': 'ucc_analytics_criterion_5',
  'subcriteria': [{'code': '5.1.1', 'title': 'Course Design and Development'},
                  {'code': '5.1.2', 'title': 'Course Review'},
                  {'code': '5.2.1', 'title': 'Course Planning'},
                  {'code': '5.2.2', 'title': 'Course Delivery'},
                  {'code': '5.3.1', 'title': 'Partnership Management'},
                  {'code': '5.4', 'title': 'Student Learning'},
                  {'code': '5.5', 'title': 'Student Assessment'}]},
 {'criterion': '6',
  'title': 'Quality Assurance, Innovation and Continual Improvement',
  'weight': 50,
  'status': 'live_foundation',
  'api_method': 'ucc_analytics_criterion_6',
  'subcriteria': [{'code': '6.1.1',
                   'title': 'Internal Assessment and Quality Audits',
                   'policy': 'PPD-SGL-SQ-6.1.1',
                   'version': '1.2'},
                  {'code': '6.2.1', 'title': 'Management Review', 'policy': 'PPD-SGL-SQ-6.2.1', 'version': '1.3'},
                  {'code': '6.3.1',
                   'title': 'Innovation and Continual Improvement',
                   'policy': 'PPD-SGL-SQ-6.3.1',
                   'version': '1.2'},
                  {'code': '6.4.1',
                   'title': "Provider's Accreditation and Evaluation",
                   'policy': 'PPD-OE-FN-6.4.1',
                   'version': '1.2'},
                  {'code': '6.5.3',
                   'title': 'Hazard Identification and Risk Assessment',
                   'policy': 'PPD-SGL-SQ-6.5.3',
                   'version': '1.2'}]},
 {'criterion': '7',
  'title': 'Performance Outcomes',
  'weight': 330,
  'status': 'live_foundation',
  'api_method': 'ucc_analytics_criterion_7',
  'subcriteria': [{'code': '7.1.1',
                   'title': 'Measurement of Outcomes',
                   'policy': 'PPD-SGL-SQ-7.1.1',
                   'version': '1.2'}]}]

frappe.response["message"] = {
    "ok": True,
    "version": "1.9.5",
    "criteria": CRITERIA,
    "note": "All seven criteria now use live data paths. Unsupported sources or fields are reported explicitly rather than replaced with dummy values."
}
