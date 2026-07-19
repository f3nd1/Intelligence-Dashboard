# Management Review Field Reference

## DocType metadata

```text
DocType: Management Review
Module: Educ Sg
Statuses: Scheduled, In Progress, Completed, Postponed
```

The original supplied definition is preserved at:

```text
source-material/Management Review.txt
```

## THESIS structure

```text
T — Tactical Strategy
H — Harmonising Resources
E — Evaluating Performance
S — Securing Compliance
I — Implementing Resilience
S — Sustaining Progression
```

## Normalized fields

| No. | Label | Type | Fieldname | Options / linked DocType |
| --- | --- | --- | --- | --- |
| 1 | — | Section Break | section_break_enoz | — |
| 2 | — | HTML | html_eexb | — |
| 3 | — | Column Break | column_break_topz | — |
| 4 | Review Date | Date | review_date | — |
| 5 | Review Period | Select | review_period | Quarterly / Semi-Annualy / Annually |
| 6 | Review Type | Select | review_type | Initial / Scheduled / Adhoc |
| 7 | Review Status | Select | review_status | Scheduled / In Progress / Completed / Postponed |
| 8 | Chairperson | Link | chairperson | User |
| 9 | Chairperson (Full Name) | Data | chairperson_full_name | — |
| 10 | Minutes of Meeting | Link | minutes_of_meeting | Meeting Minutes |
| 11 | Next Review Date | Date | next_review_date | — |
| 12 | — | Section Break | section_break_ilhv | — |
| 13 | Executive Summary | Text Editor | executive_summary | — |
| 14 | 🎯 Strategy | Tab Break | strategy_tab | — |
| 15 | Leadership and Corporate Governance | Section Break | leadership_and_corporate_governance_section | — |
| 16 | List of Essential Information | Table | essential_information | Strategic Planning Essential Information |
| 17 | Notes | Text Editor | leaderhip_note | — |
| 18 | Policies and Procedures | Section Break | policy_and_procedure_section | — |
| 19 | List of Policies and Procedures | Table | policy_procedure | Strategic Planning Policy and Procedure |
| 20 | Notes | Text Editor | ppd__note | — |
| 21 | Current State Baseline | Section Break | current_state_baseline_section | — |
| 22 | Note | Text Editor | note_current_state | — |
| 23 | Strategic Direction Narrative | Section Break | direction_section | — |
| 24 | Note | Text Editor | note_direction | — |
| 25 | Planning Horizon Clarity | Section Break | horizon__section | — |
| 26 | Note | Text Editor | note_horizon | — |
| 27 | Strategic Assumptions | Section Break | assumptions__section | — |
| 28 | Note | Text Editor | note_assumption | — |
| 29 | Strategic Prioritisation and Exclusions | Section Break | prio__section | — |
| 30 | Note | Text Editor | note_strategic_prio | — |
| 31 | Boundary Between Strategic Planning and Performance Review | Section Break | boundary__section | — |
| 32 | Note | Text Editor | note_boundary | — |
| 33 | 💼 Resources | Tab Break | resources_tab | — |
| 34 | Resource Management | Section Break | resource_management_section | — |
| 35 | List of Resource Management | Table | table_bhwb | Strategic Planning Business Continuity Plans |
| 36 | List of Training Events | Table | training_event | Management Review Training Event Childtable |
| 37 | Notes | Text Editor | resource_note | — |
| 38 | Asset Management | Section Break | aseets_management_section | — |
| 39 | List of Data Asset Inventory | Table | data_asset_inventory | Strategic Planning Business Continuity Plans |
| 40 | Hardware and Software Assets | Table | hardware_and_software_assets | Strategic Planning Asset Childtable |
| 41 | Notes | Text Editor | notes | — |
| 42 | Financial and Budget Management | Section Break | financial_metrics_and_management_practices_section | — |
| 43 | — | Table | table_pbnt | Strategic Planning Financial Metrics and Management Practices |
| 44 | Notes | Text Editor | finace_note | — |
| 45 | 📈 Performance | Tab Break | performance_tab | — |
| 46 | Quality Goal | Section Break | quality_objective_section | — |
| 47 | — | Table | quality_objective | Quality Procedure Quality Objective Childtable |
| 48 | Notes | Text Editor | quality_obectives_note | — |
| 49 | Process Performance, Conformity, and Audit Compliance | Section Break | process_performance_and_conformity_section | — |
| 50 | — | Table | process_performace_conformity | Strategic Planning Process Performance and Conformity |
| 51 | Notes | Text Editor | process_performance_note | — |
| 52 | Audit Results | Section Break | audit_results_section | — |
| 53 | — | HTML | label_here | — |
| 54 | — | Table | table_efwt | Strategic Planning Audit Results |
| 55 | Notes | Text Editor | audit__note | — |
| 56 | APSR Review Summary (Approach, Process, System, Review) | Section Break | apsr_review | — |
| 57 | — | Table | table_lnhy | Strategic Planning QMR |
| 58 | Notes | Text Editor | apsr_note | — |
| 59 | Performance of External Providers | Section Break | performance_of_external_providers_section | — |
| 60 | — | HTML | label_here_copy | — |
| 61 | List of Providers | Table | table_kenc | Strategic Planning Performance of External Providers |
| 62 | Notes | Text Editor | provider_note | — |
| 63 | 🔒 Compliance | Tab Break | compliance_tab | — |
| 64 | Nonconformities and Corrective Actions | Section Break | nonconformities_and_corrective_actions_section | — |
| 65 | List of Compliance Tracking | Table | nonconformities_corrective_actions | Strategic Planning Nonconformities and Corrective Actions |
| 66 | Notes | Text Editor | nonconformities_note | — |
| 67 | Risks and Opportunities | Section Break | risk_and_opportunities_section | — |
| 68 | List of Risk Category | Table | risk_opportunities | Strategic Planning Risk and Opportunities |
| 69 | Notes | Text Editor | risk_note | — |
| 70 | Market Positioning and Competitive Analysis | Section Break | external_and_internal_factors_section | — |
| 71 | PESTEL Analysis | Table | pestel_analysis | Strategic Planning PESTEL Analysis |
| 72 | SWOT Analysis | Table | swot_analysis | Strategic Planning SWOT Analysis |
| 73 | Porter's Five Forces | Table | porters_five_forces | Strategic Planning Porter Five Forces Analysis |
| 74 | Other Documents | Table | other_documents | Strategic Planning External and Internal Factors Documents |
| 75 | Notes | Text Editor | external_internal_note | — |
| 76 | 🛡️ Resilience | Tab Break | resilience_tab | — |
| 77 | Business Continuity Plans | Section Break | business_continuity_plans_section | — |
| 78 | List of BC/DR | Table | business_continuity | Strategic Planning Business Continuity Plans |
| 79 | Notes | Text Editor | bcp__note | — |
| 80 | Change Management Strategy | Section Break | change_management_strategy_section | — |
| 81 | Change Execution Framework | Text Editor | change_execution_framework | — |
| 82 | Change Risk and Communication Management | Text Editor | change_risk_and_communication_management | — |
| 83 | Environmental, Social, and Governance (ESG) Sustainability | Section Break | social_responsibility_initiatives_section | — |
| 84 | List of ESG Initiatives | Table | table_ttgw | Strategic Planning ESG Childtable |
| 85 | Notes | Text Editor | social_responsibility_note | — |
| 86 | 💡 Progression | Tab Break | enhancement_tab | — |
| 87 | Performance Outcomes | Section Break | customer_satisfaction_and_feedback_section | — |
| 88 | List of Performance Outcomes | Table | table_tznr | Strategic Planning Cust Satisfaction n Feedback Childtable |
| 89 | Notes | Text Editor | cust_satisfaction_note | — |
| 90 | Opportunities for Improvement | Section Break | opportunities_for_improvement_section | — |
| 91 | List of Quality Actions | Table | table_qzdd | Management Review Strategic Planning Innovation Childtable |
| 92 | Notes | Text Editor | opportunities_note | — |

## Key operational fields

- `review_date`
- `review_period`
- `review_type`
- `review_status`
- `chairperson`
- `minutes_of_meeting`
- `next_review_date`
- `executive_summary`

## Key review-output tables

- `quality_objective`
- `process_performace_conformity`
- `table_efwt` — audit results
- `table_lnhy` — APSR / QMR
- `table_kenc` — external providers
- `nonconformities_corrective_actions`
- `risk_opportunities`
- `business_continuity`
- `table_tznr` — performance outcomes
- `table_qzdd` — Quality Actions
