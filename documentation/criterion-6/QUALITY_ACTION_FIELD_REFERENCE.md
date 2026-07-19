# Quality Action Field Reference

## Source status

The supplied CSV is a Frappe **Bulk Edit Fields** export. It contains
118 field definitions.

The field set strongly identifies the target as `Quality Action`, including:

- naming series `UCC-QAC-.YY.####`;
- `resolutions` → Quality Action Resolution;
- corrective/preventive classification;
- innovation and continual-improvement fields;
- QIPI, TACEI and CEI;
- cost and time savings;
- budget, risk, records and evidence.

The original CSV is preserved at:

```text
source-material/Quality Action Fields.csv
```

## Normalized fields

| Label | Type | Fieldname | Options / linked DocType | Depends on |
| --- | --- | --- | --- | --- |
| 📋 Overview | Tab Break | custom__overview | — | — |
| quality_action_ui | HTML | custom_quality_action_ui | — | — |
| — | Section Break | custom_section_break_uhjgr | — | — |
| Naming series | Select | naming_series | UCC-QAC-.YY.#### / UCC-QAC-.25.#### / UCC-QAC-.24.#### | — |
| Quality Action Overview | Section Break | custom_quality_action_overview | — | — |
| — | Column Break | cb_00 | — | — |
| — | HTML | custom_custom_html2 | Instructions / The Quality Action DocType is designed to streamline the management of quality improvement processes within the institution, focusing on problem resolution, performance monitoring, and continual improvement. This system facilitates the documentation, tracking, and analysis of actions taken to enhance operational excellence and compliance. /  /  /      /         Tab Name /         Description /      /      /         🎯 Resolution /         Focuses on identifying and documenting problems and actions taken, detailing responsibilities and tracking the status of each action for clear accountability. /      /      /         🚀 Performance and Evaluation /         Includes monitoring of performance indicators and evaluation criteria to assess the impact and effectiveness of actions taken, guiding future quality improvements. /      /      /         🚧 Risk and Resources /         Details the identification of potential risks and opportunities, and outlines the resources required to support quality initiatives, ensuring preparedness and strategic resource allocation. /      /      /         👾 Documentation /         Manages the storage and retrieval of all documentation related to quality actions, facilitating easy access to historical data and compliance records. /      /  /  / Utilize this DocType to enhance your quality management processes, ensuring robust documentation, effective resolution, and continual organizational improvement. | — |
| — | Column Break | custom_column_break_m0vin | — | — |
| Updates | Select | custom_status_updates | Open / In Progress / Planned / Completed / Inactive | — |
| Status (Not in used) | Select | status | Open / Completed | — |
| Corrective/Preventive | Select | corrective_preventive | Corrective / Preventive | — |
| Date | Date | date | — | — |
| Posting Date | Date | custom_proposed_date | — | — |
| Completed Date | Date | custom_completed_date | — | — |
| Type of Innovation | Select | custom_type_of_innovation | Disruptive / Radical / Incremental / Architectural | eval:doc.custom_innovation != 0 |
| Innovation Category | Select | custom_innovation_category | Architectural / Business Model / Organisational / Process / Service / Technology | eval:doc.custom_innovation != 0 |
| Innovation | Check | custom_innovation | — | — |
| Continuous Improvement | Check | custom_continuous_improvement | Innovation / Continuous Improvement | — |
| Subject | Data | custom_subject | — | — |
| — | HTML | custom_instruction | ➡️ Find out more about Innovation and Continuous Improvement here | — |
| — | Section Break | custom_section_break_8p3vu | — | — |
| Quality Goal | Link | goal | Quality Goal | — |
| Quality Goal Justification | Text Editor | custom_quality_goal_justification | — | — |
| — | Column Break | custom_column_break_qbs5f | — | — |
| Review | Link | review | Quality Review | — |
| Procedure | Link | procedure | Quality Procedure | — |
| Feedback | Link | feedback | Quality Feedback | — |
| Quality Meeting | Link | custom_quality_meeting | Quality Meeting | — |
| Overall Closure Verification | Section Break | custom_overall_closure_verification | — | — |
| Sign-off Records | Table | custom_signoff_records | Quality Meeting Attendance Childtable | — |
| 🎯 Resolution | Tab Break | custom__resolution | — | — |
| Resolution Management Metadata | Section Break | custom_resolution_management_metadata | — | — |
| Resolutions | Table | resolutions | Quality Action Resolution | — |
| Resolution Management | Section Break | sb_00 | — | — |
| QAR Inline Editor | HTML | custom_qar_inline_editor | — | — |
| — | Section Break | custom_section_break_p5k2p | — | — |
| compliance_tracking_html_label | HTML | custom_compliance_tracking_html_label | ℹ️ /    /    /      /       The Compliance Tracking child table below is auto-generated and linked to the relevant  /       Quality Action. If no entries appear, you may perform a bulk update of the  /       custom_quality_action fields using the 'Report View'. | — |
| Compliance Tracking | Table | custom_compliance_tracking | Quality Action Compliance Tracking | — |
| — | Section Break | custom_section_break_7xw4r | — | — |
| Project | Link | custom_project | Project | — |
| — | Column Break | custom_column_break_hszzs | — | — |
| Task | Link | custom_task | Task | — |
| Value Quality Policy Module Alignment | Section Break | custom_value_quality_policy_module_alignment | — | — |
| — | Table | custom_value_quality_policy_module_alignment_childtable2 | Value Quality Policy Module Alignment Childtable | — |
| 🚀 Performance and Evaluation | Tab Break | custom__performance_and_evaluation | — | — |
| Performance Indicators | Section Break | custom_performance_indicators | — | — |
| Quantitative Performance Review | Table | custom_performance | Quality Action Performance Indicators Childtable | — |
| — | Section Break | custom_section_break_ei2sy | — | — |
| Quality & Innovation Performance Index (QIPI) | Data | custom_aggregated_performance_index_api | — | — |
| TACEI | Data | custom_timeadjusted_cost_efficiency_index_tacei | — | — |
| — | Column Break | custom_column_break_5bwrm | — | — |
| Implementation Duration (Day) | Data | custom_implementation_duration | — | — |
| CEI | Data | custom_cost_efficiency_index_cei | — | — |
| QIPI Legend | Section Break | custom_section_break_yjidr | — | — |
| Legend | HTML | custom_legend | Quality & Innovation Performance Index (QIPI) / Definition: A composite score representing the average normalised change across all performance indicators—i.e., your combined measure of quality actions and innovation impact.  /   / Formula: Quality & Innovation Performance (QIPI) = Sum of Normalised Change Outcomes (%) ÷ Number of Indicators /   / How to Read It:  /  /     Higher QIPI: Greater overall performance improvement in both quality and innovation. /     Lower QIPI: Smaller or less impactful changes. /  /   / Description /  /     Perspective: Represents the high-level category or area being assessed (e.g., Internal Processes, Financial, CSR Impact). This groups performance indicators into overarching themes for easier interpretation. /     BSC Criteria: Indicates the specific metric or focus area being evaluated within the perspective (e.g., Resource Allocation, Process Innovation). These criteria align with broader organisational goals. /     UOM (Unit of Measure): The unit used to measure the indicator (e.g., minutes, percentage, numbers). It specifies how the before and after values are quantified. /     Before:  The baseline value recorded before the quality action or initiative was implemented. This serves as a reference point for comparison. /     After: The value recorded after the quality action or initiative was implemented. This indicates the result or impact of the initiative. /     Min Value: The smallest possible or relevant value for this indicator within the current context. Used as part of the normalisation process to standardise values across different scales. /     Max Value: The largest possible or relevant value for this indicator within the current context. Also used in the normalisation process to ensure consistency. /     Diff (%) (Automatically Calculated) /          /             Formula: ((After - Before) / Before) × 100 /             Positive Number: Indicates an increase in the value from before to after. Whether this is favourable or unfavourable depends on the context (e.g., higher revenue is good, but higher error rates are bad). /             Negative Number: Indicates a decrease in the value from before to after. Similarly, the desirability depends on the context (e.g., lower processing time is good, but lower customer satisfaction is bad). /             Interpreting Smaller vs Bigger: Smaller values are better when reducing inefficiencies (e.g., processing time), while bigger values are better when achieving growth or positive improvements (e.g., satisfaction scores). /          /      /     Norm Diff (%) (Full Name: Normalised Difference) /          /             Formula: \|((After - Before) / (Max Value - Min Value)) × 100\| /             The value is always converted to positive (absolute) because the aim is to compare the magnitude of the impact, regardless of the direction. /             Why Positive? This ensures consistency in aggregating results, as some improvements naturally result in negative changes (e.g., reduced time) while others result in positive changes (e.g., increased revenue). /             Interpreting Smaller vs Bigger: A bigger value represents a larger impact relative to the defined range (Min Value to Max Value). Smaller values indicate less significant change or improvement. /          /      /  /   / Summary of Reading the Table: /  /     Use the Diff (%) to understand directional change (positive or negative). /     Refer to Norm Diff (%) to assess the scale of the impact across all indicators in a standardised way. /     Context matters: Always consider whether the performance indicator benefits from an increase or decrease. For example: /             Time savings → Smaller is better (e.g., reduced processing time). /             Revenue growth → Bigger is better (e.g., increased earnings). /          /      /  /   / For more information refer to: Quality & Innovation Performance Index | — |
| Index Explanation | HTML | custom_index_explanation | Aggregated Performance Index (API): /  /     Definition: /          /             A composite score representing the average normalised change across all performance indicators. /             Formula:API = Sum of Normalised Change Outcomes (%) ÷ Number of Indicators /          /      /     How to Read API: /          /             Higher API: Indicates significant improvements across performance indicators. Bigger is better, as it reflects higher performance improvements. /             Lower API: Suggests minimal changes or less impactful actions. /          /      /     Use Case: /          /             Provides a general overview of performance improvements. /             Helps identify whether quality actions are leading to meaningful and measurable changes. | — |
| Cost Saving Details | Section Break | custom_cost_saving_section | — | — |
| — | Table | custom_cost_saving_table | Quality Action Cost Saving Childtable | — |
| — | Section Break | custom_cost_saving_details_section | — | — |
| Total Savings | Data | custom_cost_saving_data | — | — |
| People Calculator | Section Break | custom_cost_time_saving_section | — | — |
| — | Column Break | custom_before_cost_column | — | — |
| People Cost Before(SGD) | Data | custom_before_cost | — | — |
| Cycle per Month | Data | custom_cycle_per_month | — | — |
| — | Column Break | custom_before_time_column | — | — |
| Before Time (Man-Day) | Data | custom_before_time | — | — |
| Total Cycles per Year | Data | custom_total_cycles_per_year | — | — |
| — | Column Break | custom_after_cost_column | — | — |
| Man-Day Rate (SGD) | Data | custom_manday_rate | — | — |
| Annual People Cost (Before) | Data | custom_annual_people_cost_before | — | — |
| — | Column Break | custom_after_time_column | — | — |
| After Time (Man-Day) | Data | custom_after_time | — | — |
| Annual People Cost (After) | Data | custom_annual_people_cost_after | — | — |
| — | Column Break | custom_ctei_savings_column | — | — |
| People Cost After(SGD) | Data | custom_after_cost | — | — |
| Annual People Savings (CTEI) | Data | custom_annual_people_savings_ctei | — | — |
| — | Column Break | custom_column_break_lvtu4 | — | — |
| People Savings (SGD) | Data | custom_ctei_savings | — | — |
| — | Section Break | custom_section_break_d1fmn | — | — |
| People Calculator Display | HTML | custom_people_calculator_display | — | — |
| — | Section Break | custom_section_break_lzmlq | — | — |
| Note | Text Editor | custom_note_ctei | — | — |
| CTEI Legend Section | Section Break | custom_ctei_legend_section | — | — |
| CTEI html | HTML | custom_ctei_html | CTEI – Cost-Time Efficiency Index /     CTEI measures the financial value of efficiency improvements achieved through operational changes, digitalisation, or innovation initiatives by converting time savings (expressed in man-days, where 1 man-day = 8 working hours) and cost reductions into Singapore dollar value (SGD). /  /  /       /  /  /     Formula: /     CTEI Savings = ((Before Time − After Time) × Man-Day Rate) + (Before Cost − After Cost) /       /  /  /     Definitions: /  /  /      /         Before Cost (SGD): Operating cost before improvement /      /      /         Before Time (Man-Day): Time taken before the improvement, expressed in man-days (1 man-day = 8 working hours) /      /      /         After Cost (SGD): Operating cost after the improvement /      /      /         After Time (Man-Day): Time taken after the improvement, in man-days (1 man-day = 8 working hours) /      /      /         Man-Day Rate: Fixed staff cost per man-day (e.g. SGD 280/day) /      /      /         CTEI Savings (SGD): Total cost-time efficiency gain in Singapore dollars /      /  /  /       /  /  /     Output Unit: /     SGD ($) – Total quantified value of cost/time efficiency gained. /  /  /       /  /  /     Compliance Relevance: /     Aligns with EduTrust 6.3.1 Innovation and Continual Improvement /7.23 Operational Outcomes and ISO 9001:2015 (Clauses 8.5.1, 9.1.3, 10.3) by providing auditable evidence of continual improvement, strategic investment, and resource optimisation. | — |
| — | Section Break | custom_section_break_d5cyn | — | — |
| Qualitative Performance Review | Text Editor | custom_notes | — | — |
| Project Execution Evaluation Criteria | Section Break | custom_section_break_te0kz | — | — |
| Urgency | Rating | custom_urgency | — | — |
| Impact | Rating | custom_impact | — | — |
| Time Required | Rating | custom_time_required | — | — |
| Priority Score | Data | custom_priority_score | — | — |
| — | Column Break | custom_column_break_udavg | — | — |
| Complexity | Rating | custom_complexity | — | — |
| Resources | Rating | custom_resources | — | — |
| RPN | Rating | custom_rpn | — | — |
| 🚧 Risk and Resources | Tab Break | custom__risk_and_resources | — | — |
| Resource Management | Section Break | custom_project_support_details | — | — |
| — | Table | custom_resource_management_childtable | Resource Management childtable | — |
| Additional Notes | Text Editor | custom_resource_needed | — | — |
| Budget Management | Section Break | custom_budget_management2 | — | — |
| — | Table | custom_reegege | Resource Budget Management Childtable | — |
| — | Section Break | custom_section_break_gahvd | — | — |
| Total Budget Fee (SGD) | Currency | custom_total_budget_fee | — | — |
| — | Column Break | custom_column_break_tok1g | — | — |
| Total Actual Spending (SGD) | Currency | custom_total_actual_spending | — | — |
| — | Column Break | custom_column_break_twn3j | — | — |
| Spending Difference (%) | Data | custom_spending_difference | — | — |
| Risk Management and Mitigation | Section Break | custom_risk_management_and_mitigation2 | — | — |
| Risk Assessment | Table | custom_risk_identification_table | Risk Identification Childtable | — |
| Risk Mitigation | Table | custom_risk_mitigation | Risk Justification Childtable | — |
| Additional Notes | Text Editor | custom_risk_and_opportunities_identified | — | — |
| 👾 Documentation | Tab Break | custom__documentation | — | — |
| Documentation | Section Break | custom_documentation | — | — |
| Quality Record | Table | custom_quality_record | Oversight Framework File Childtable | — |
| Documentation Evidence | Table | custom_documentation_evidence | Quality Action Documentation Childtable | — |
| Evidences | Table | custom_evidences | Evidence Collection Childtable | — |
| — | Section Break | custom_section_break_xbvbg | — | — |
| General Notes | Text Editor | custom_general_notes | — | — |
