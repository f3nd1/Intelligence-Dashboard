# Criterion 4 Runtime Configuration Reference

This file preserves the active configuration extracted from:

```text
server-scripts/UCC Analytics - Criterion 4.py
```

## Allowed actions

```json
[
  "summary",
  "source_status",
  "policy_registry",
  "drilldown"
]
```

## Policy registry

```json
{
  "4.1.1": {
    "title": "Pre-Course Counselling, Selection and Admissions",
    "policy": "PPD-SSO-AD-4.1.1",
    "version": "2.2"
  },
  "4.2.1": {
    "title": "Student Contract",
    "policy": "PPD-SSO-AD-4.2.1",
    "version": "2.2"
  },
  "4.2.2": {
    "title": "Fee Collection and Fee Protection Scheme",
    "policy": "PPD-SSO-AD-4.2.2",
    "version": "2.3"
  },
  "4.3.1": {
    "title": "Course Transfer, Deferment and Withdrawal",
    "policy": "PPD-SSO-SS-4.3.1",
    "version": "2.2"
  },
  "4.4.1": {
    "title": "Refund",
    "policy": "PPD-SSO-SS-4.4.1",
    "version": "2.2"
  },
  "4.5.1": {
    "title": "Student Support Services",
    "policy": "PPD-SSO-SS-4.5.1",
    "version": "2.3"
  },
  "4.6.1": {
    "title": "Student Conduct and Attendance",
    "policy": "PPD-SSO-SS-4.6.1",
    "version": "2.2"
  }
}
```

## Source and metric configuration

```json
{
  "4.1.1": {
    "sources": {
      "applicant": [
        "Student Applicant"
      ],
      "admission": [
        "Student Admission UCC"
      ],
      "counselling": [
        "Pre Course Counselling Declaration"
      ],
      "adjustments": [
        "Student Log"
      ]
    },
    "metrics": [
      {
        "id": "c411-counselling",
        "label": "Counselling declarations",
        "source": "counselling",
        "field": [
          "name"
        ],
        "mode": "all"
      },
      {
        "id": "c411-acknowledged",
        "label": "Applicant acknowledgements",
        "source": "counselling",
        "field": [
          "declaration_check"
        ],
        "mode": "truthy"
      },
      {
        "id": "c411-pdpa",
        "label": "PDPA consents",
        "source": "counselling",
        "field": [
          "pdpa_check"
        ],
        "mode": "truthy"
      },
      {
        "id": "c411-staff-complete",
        "label": "Staff declarations completed",
        "source": "counselling",
        "field": [
          "name_of_staff"
        ],
        "mode": "truthy",
        "requires": [
          {
            "field": [
              "date"
            ],
            "mode": "truthy"
          }
        ]
      },
      {
        "id": "c411-unacknowledged",
        "label": "Applicant acknowledgement missing",
        "source": "counselling",
        "field": [
          "declaration_check"
        ],
        "mode": "falsy"
      },
      {
        "id": "c411-pdpa-missing",
        "label": "PDPA consent missing",
        "source": "counselling",
        "field": [
          "pdpa_check"
        ],
        "mode": "falsy"
      },
      {
        "id": "c411-complete",
        "label": "Approved applications",
        "source": "applicant",
        "field": [
          "application_status"
        ],
        "mode": "contains",
        "values": [
          "approved",
          "admitted",
          "enrolled"
        ]
      },
      {
        "id": "c411-conditional",
        "label": "Conditional admissions",
        "source": "admission",
        "field": [
          "conditional"
        ],
        "mode": "truthy"
      },
      {
        "id": "c411-late",
        "label": "Late-admission requests",
        "source": "adjustments",
        "child_doctype": "Course Adjustment Request Form",
        "child_table_field": "custom_course_adjustment",
        "field": [
          "type"
        ],
        "mode": "equals",
        "values": [
          "Late Admission"
        ]
      }
    ]
  },
  "4.2.1": {
    "sources": {
      "contract": [
        "Student Admission UCC"
      ],
      "invoice": [
        "Sales Invoice"
      ]
    },
    "metrics": [
      {
        "id": "c421-generated",
        "label": "Contracts generated",
        "source": "contract",
        "field": [
          "contract_url",
          "student_contract"
        ],
        "mode": "truthy"
      },
      {
        "id": "c421-approved",
        "label": "Approved contracts",
        "source": "contract",
        "field": [
          "application_status"
        ],
        "mode": "contains",
        "values": [
          "approved",
          "enrolled",
          "done"
        ]
      },
      {
        "id": "c421-signed",
        "label": "Signed contracts",
        "source": "contract",
        "field": [
          "contract_signed_by_student_date",
          "student_signed_date"
        ],
        "mode": "truthy"
      },
      {
        "id": "c421-pending",
        "label": "Sent but not signed",
        "source": "contract",
        "field": [
          "contract_sent_date"
        ],
        "mode": "truthy",
        "requires": [
          {
            "field": [
              "contract_signed_by_student_date",
              "student_signed_date"
            ],
            "mode": "falsy"
          }
        ]
      }
    ]
  },
  "4.2.2": {
    "sources": {
      "contract": [
        "Student Admission UCC"
      ],
      "invoice": [
        "Sales Invoice"
      ],
      "payment": [
        "Payment Entry"
      ],
      "fps": [
        "FPS Record"
      ]
    },
    "metrics": [
      {
        "id": "c422-invoiced",
        "label": "Students invoiced",
        "source": "contract",
        "field": [
          "sales_invoice"
        ],
        "mode": "truthy"
      },
      {
        "id": "c422-paid",
        "label": "Submitted receipts",
        "source": "payment",
        "field": [
          "payment_type"
        ],
        "mode": "contains",
        "values": [
          "receive"
        ],
        "requires": [
          {
            "field": [
              "docstatus"
            ],
            "mode": "equals",
            "values": [
              "1"
            ]
          }
        ]
      },
      {
        "id": "c422-fps",
        "label": "FPS declarations processed",
        "source": "fps",
        "field": [
          "fps_status"
        ],
        "mode": "contains",
        "values": [
          "processed",
          "approved"
        ]
      },
      {
        "id": "c422-late",
        "label": "Late-payment exceptions",
        "source": "invoice",
        "field": [
          "status"
        ],
        "mode": "contains",
        "values": [
          "overdue"
        ]
      }
    ]
  },
  "4.3.1": {
    "sources": {
      "adjustments": [
        "Student Log"
      ],
      "contract": [
        "Student Admission UCC"
      ],
      "fps": [
        "FPS Record"
      ]
    },
    "metrics": [
      {
        "id": "c431-overdue",
        "label": "Open requests beyond 21 working days",
        "source": "adjustments",
        "child_doctype": "Course Adjustment Request Form",
        "child_table_field": "custom_course_adjustment",
        "field": [
          "posting_date"
        ],
        "mode": "older_than_days",
        "days": 29,
        "requires": [
          {
            "field": [
              "type"
            ],
            "mode": "contains",
            "values": [
              "course transfer",
              "course deferment",
              "course withdrawal"
            ]
          },
          {
            "field": [
              "approved_date"
            ],
            "mode": "falsy"
          }
        ]
      },
      {
        "id": "c431-transfer",
        "label": "Transfer requests",
        "source": "adjustments",
        "child_doctype": "Course Adjustment Request Form",
        "child_table_field": "custom_course_adjustment",
        "field": [
          "type"
        ],
        "mode": "equals",
        "values": [
          "Course Transfer"
        ]
      },
      {
        "id": "c431-defer",
        "label": "Deferment requests",
        "source": "adjustments",
        "child_doctype": "Course Adjustment Request Form",
        "child_table_field": "custom_course_adjustment",
        "field": [
          "type"
        ],
        "mode": "equals",
        "values": [
          "Course Deferment"
        ]
      },
      {
        "id": "c431-withdraw",
        "label": "Withdrawal requests",
        "source": "adjustments",
        "child_doctype": "Course Adjustment Request Form",
        "child_table_field": "custom_course_adjustment",
        "field": [
          "type"
        ],
        "mode": "equals",
        "values": [
          "Course Withdrawal"
        ]
      }
    ]
  },
  "4.4.1": {
    "sources": {
      "adjustments": [
        "Student Log"
      ],
      "payment": [
        "Payment Entry"
      ],
      "contract": [
        "Student Admission UCC"
      ]
    },
    "metrics": [
      {
        "id": "c441-open",
        "label": "Open refund requests",
        "source": "adjustments",
        "child_doctype": "Course Adjustment Request Form",
        "child_table_field": "custom_course_adjustment",
        "field": [
          "type"
        ],
        "mode": "equals",
        "values": [
          "Refund"
        ],
        "requires": [
          {
            "field": [
              "approved_date"
            ],
            "mode": "falsy"
          }
        ]
      },
      {
        "id": "c441-eligible",
        "label": "Approved refund requests",
        "source": "adjustments",
        "child_doctype": "Course Adjustment Request Form",
        "child_table_field": "custom_course_adjustment",
        "field": [
          "type"
        ],
        "mode": "equals",
        "values": [
          "Refund"
        ],
        "requires": [
          {
            "field": [
              "approved_date"
            ],
            "mode": "truthy"
          }
        ]
      },
      {
        "id": "c441-overdue",
        "label": "Open refunds beyond 7 days",
        "source": "adjustments",
        "child_doctype": "Course Adjustment Request Form",
        "child_table_field": "custom_course_adjustment",
        "field": [
          "posting_date"
        ],
        "mode": "older_than_days",
        "days": 7,
        "requires": [
          {
            "field": [
              "type"
            ],
            "mode": "equals",
            "values": [
              "Refund"
            ]
          },
          {
            "field": [
              "approved_date"
            ],
            "mode": "falsy"
          }
        ]
      },
      {
        "id": "c441-paid",
        "label": "Refund payments recorded",
        "source": "payment",
        "field": [
          "remarks"
        ],
        "mode": "contains",
        "values": [
          "refund"
        ],
        "requires": [
          {
            "field": [
              "payment_type"
            ],
            "mode": "contains",
            "values": [
              "pay"
            ]
          },
          {
            "field": [
              "docstatus"
            ],
            "mode": "equals",
            "values": [
              "1"
            ]
          }
        ]
      }
    ]
  },
  "4.5.1": {
    "sources": {
      "student_log": [
        "Student Log"
      ],
      "academic_support": [
        "Intervention Issue Academic Support"
      ],
      "wellness_support": [
        "Intervention Issue Wellness Services"
      ],
      "integrity_support": [
        "Intervention Issue Academic Integrity"
      ]
    },
    "metrics": [
      {
        "id": "c451-services",
        "label": "Student Logs",
        "source": "student_log",
        "field": [
          "name"
        ],
        "mode": "all"
      },
      {
        "id": "c451-cases",
        "label": "Academic-support records",
        "source": "academic_support",
        "field": [
          "name"
        ],
        "mode": "all"
      },
      {
        "id": "c451-followup",
        "label": "Wellness-support records",
        "source": "wellness_support",
        "field": [
          "name"
        ],
        "mode": "all"
      },
      {
        "id": "c451-outcomes",
        "label": "Academic-integrity records",
        "source": "integrity_support",
        "field": [
          "name"
        ],
        "mode": "all"
      }
    ]
  },
  "4.6.1": {
    "sources": {
      "attendance": [
        "Student Attendance"
      ],
      "student_log": [
        "Student Log"
      ],
      "warning": [
        "Dismissal Letters due to Attendance Requirements"
      ],
      "leave": [
        "Student Leave Application"
      ]
    },
    "metrics": [
      {
        "id": "c461-attendance",
        "label": "Attendance records",
        "source": "attendance",
        "field": [
          "name"
        ],
        "mode": "all"
      },
      {
        "id": "c461-risk",
        "label": "Absent or late records",
        "source": "attendance",
        "field": [
          "status"
        ],
        "mode": "contains",
        "values": [
          "absent",
          "late"
        ]
      },
      {
        "id": "c461-warning",
        "label": "Attendance-dismissal records",
        "source": "warning",
        "field": [
          "name"
        ],
        "mode": "all"
      },
      {
        "id": "c461-intervention",
        "label": "Student Logs",
        "source": "student_log",
        "field": [
          "name"
        ],
        "mode": "all"
      }
    ]
  }
}
```

## Question registry

```json
{
  "4.1.1": [
    {
      "id": "q411-1",
      "metric_id": "c411-counselling",
      "question": "How many pre-course counselling declarations are recorded?",
      "logic": "Count Pre Course Counselling Declaration records in the current filter scope."
    },
    {
      "id": "q411-2",
      "metric_id": "c411-acknowledged",
      "question": "How many applicants acknowledged that the pre-course information was communicated?",
      "logic": "Count Pre Course Counselling Declaration.declaration_check values that are enabled."
    },
    {
      "id": "q411-3",
      "metric_id": "c411-pdpa",
      "question": "How many applicants provided PDPA consent?",
      "logic": "Count Pre Course Counselling Declaration.pdpa_check values that are enabled."
    },
    {
      "id": "q411-4",
      "metric_id": "c411-staff-complete",
      "question": "How many counselling declarations contain both the staff representative and declaration date?",
      "logic": "Count records with name_of_staff and date populated."
    },
    {
      "id": "q411-5",
      "metric_id": "c411-complete",
      "question": "How many applications are approved or admitted?",
      "logic": "Count Student Applicant records with approved, admitted or enrolled status."
    },
    {
      "id": "q411-6",
      "metric_id": "c411-conditional",
      "question": "How many admissions remain conditional?",
      "logic": "Count Student Admission UCC records where conditional is enabled."
    },
    {
      "id": "q411-7",
      "metric_id": "c411-late",
      "question": "How many late-admission requests require monitoring?",
      "logic": "Count Late Admission rows in Student Log course adjustments."
    }
  ],
  "4.2.1": [
    {
      "id": "q421-1",
      "metric_id": "c421-generated",
      "question": "How many student contracts have been generated?",
      "logic": "Count Student Admission UCC records with a contract URL or contract content."
    },
    {
      "id": "q421-2",
      "metric_id": "c421-approved",
      "question": "How many contracts have an approved admission status?",
      "logic": "Count approved, enrolled or completed admission records."
    },
    {
      "id": "q421-3",
      "metric_id": "c421-signed",
      "question": "How many contracts have been signed by the student?",
      "logic": "Count records with a student contract signed date."
    },
    {
      "id": "q421-4",
      "metric_id": "c421-pending",
      "question": "How many sent contracts are still unsigned?",
      "logic": "Count records with contract sent date and no student signed date."
    }
  ],
  "4.2.2": [
    {
      "id": "q422-1",
      "metric_id": "c422-invoiced",
      "question": "How many admissions have a linked sales invoice?",
      "logic": "Count Student Admission UCC records with sales_invoice populated."
    },
    {
      "id": "q422-2",
      "metric_id": "c422-paid",
      "question": "How many submitted incoming payment records are available?",
      "logic": "Count submitted Payment Entry records with Receive payment type."
    },
    {
      "id": "q422-3",
      "metric_id": "c422-fps",
      "question": "How many FPS declarations are processed or approved?",
      "logic": "Count FPS Record rows with Processed or Approved status."
    },
    {
      "id": "q422-4",
      "metric_id": "c422-late",
      "question": "How many invoices are overdue?",
      "logic": "Count Sales Invoice records with Overdue status."
    }
  ],
  "4.3.1": [
    {
      "id": "q431-1",
      "metric_id": "c431-transfer",
      "question": "How many course transfer requests are recorded?",
      "logic": "Count Course Transfer child rows under Student Log."
    },
    {
      "id": "q431-2",
      "metric_id": "c431-defer",
      "question": "How many course deferment requests are recorded?",
      "logic": "Count Course Deferment child rows under Student Log."
    },
    {
      "id": "q431-3",
      "metric_id": "c431-withdraw",
      "question": "How many course withdrawal requests are recorded?",
      "logic": "Count Course Withdrawal child rows under Student Log."
    },
    {
      "id": "q431-4",
      "metric_id": "c431-overdue",
      "question": "How many movement requests exceed the processing threshold?",
      "logic": "Count applicable requests older than the configured working-day approximation."
    }
  ],
  "4.4.1": [
    {
      "id": "q441-1",
      "metric_id": "c441-open",
      "question": "How many refund requests are recorded?",
      "logic": "Count Refund rows in Student Log course adjustments."
    },
    {
      "id": "q441-2",
      "metric_id": "c441-eligible",
      "question": "How many refund requests have an approval date?",
      "logic": "Count refund rows with approved_date populated."
    },
    {
      "id": "q441-3",
      "metric_id": "c441-paid",
      "question": "How many refund cases are marked complete by the available workflow evidence?",
      "logic": "Count refund rows matching the confirmed completion rule."
    },
    {
      "id": "q441-4",
      "metric_id": "c441-overdue",
      "question": "How many refund requests exceed seven working days?",
      "logic": "Count refund requests older than the configured calendar-day approximation."
    }
  ],
  "4.5.1": [
    {
      "id": "q451-1",
      "metric_id": "c451-services",
      "question": "How many student support service records are available?",
      "logic": "Count readable intervention or counselling records."
    },
    {
      "id": "q451-2",
      "metric_id": "c451-cases",
      "question": "How many student support cases are recorded?",
      "logic": "Count Student Log rows containing support, intervention, counselling, wellness or academic terms."
    },
    {
      "id": "q451-3",
      "metric_id": "c451-followup",
      "question": "How many support cases require follow-up?",
      "logic": "Count Student Log rows containing follow-up, action-plan, pending or review terms."
    },
    {
      "id": "q451-4",
      "metric_id": "c451-outcomes",
      "question": "How many support cases contain an outcome?",
      "logic": "Count Student Log rows containing resolved, completed, closed, outcome or effective terms."
    }
  ],
  "4.6.1": [
    {
      "id": "q461-1",
      "metric_id": "c461-attendance",
      "question": "How many attendance records are available?",
      "logic": "Count readable Student Attendance records."
    },
    {
      "id": "q461-2",
      "metric_id": "c461-risk",
      "question": "How many attendance records indicate absence or lateness?",
      "logic": "Count Student Attendance rows with Absent or Late status."
    },
    {
      "id": "q461-3",
      "metric_id": "c461-warning",
      "question": "How many attendance warning or dismissal records are available?",
      "logic": "Count readable warning or dismissal records."
    },
    {
      "id": "q461-4",
      "metric_id": "c461-intervention",
      "question": "How many conduct or attendance interventions are open in Student Log evidence?",
      "logic": "Count Student Log rows containing intervention, warning, dismissal, attendance or counselling terms."
    }
  ]
}
```

## Exception metrics

```json
[
  "c411-unacknowledged",
  "c411-pdpa-missing",
  "c411-conditional",
  "c411-late",
  "c421-pending",
  "c422-late",
  "c431-overdue",
  "c441-open",
  "c441-overdue",
  "c451-followup",
  "c461-risk",
  "c461-intervention"
]
```
