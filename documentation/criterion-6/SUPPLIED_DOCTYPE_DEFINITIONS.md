# Supplied Criterion 6 DocType Definitions

## Quality Action Resolution

```text
Module: Quality Management
Child table: Yes
Editable grid: Yes
```

| Fieldname | Label | Type | Options / link | Use |
| --- | --- | --- | --- | --- |
| problem | Problem | Text Editor |  | Issue, context and operational impact |
| resolution | Root Cause & Resolution | Text Editor |  | Root cause, resolution plan, resources and expected outcomes |
| action_taken | Action Taken | Text Editor |  | Implemented steps, dates and current progress |
| status | Current Status | Select | Open / Planned / In Progress / Completed | Resolution state |
| responsible | Assigned To | Data | User | Responsible staff, department or team |
| finding_type | Finding Type | Select | OBS / OFI / NC / Min. NC / Maj. NC | Audit or quality finding classification |
| target_date | Target Completion Date | Date |  | Expected completion date |
| completion_by | Completed On | Date |  | Actual completion date |
| full_name | Full Name | Data | Fetch: responsible.full_name | Resolved responsible-person name |

## Operational Outcomes Cost Time Saving

```text
Module: Educ Sg
Naming rule: naming_series
Default print format: Operational Outcomes Cost Time Saving
```

| Fieldname | Label | Type | Options / child DocType | Use |
| --- | --- | --- | --- | --- |
| monitoring_year | Monitoring Year | Select | 2023–2030 | One document per monitoring year |
| period_start | Period Start | Date |  | Monitoring period start |
| period_end | Period End | Date |  | Monitoring period end |
| naming_series | Naming Series | Select | UCC-CTS-.YY.#### and year-specific series | Document naming |
| benchmark_type | Benchmark Type | Select | Target / Prior Year / Budget / Not Applicable | Comparison basis |
| benchmark_value | Benchmark Value | Currency |  | Comparison amount |
| variance_to_benchmark | Variance to Benchmark (SGD) | Currency |  | Total net saving minus benchmark |
| table_tsns | Quality Action Summary | Table | Operational Outcomes Cost Time Saving Childtable | Yearly Quality Action rows |
| total_people_saving | Total People Saving (SGD) | Currency |  | Auto-sum |
| total_technology_saving | Total Technology Saving (SGD) | Currency |  | Auto-sum |
| total_physical_saving | Total Physical Saving (SGD) | Currency |  | Auto-sum |
| total_gross_saving | Total Gross Saving (SGD) | Currency |  | Auto-sum |
| total_implementation_cost | Total Implementation Cost (SGD) | Currency |  | Auto-sum |
| total_maintenance_cost | Total Maintenance Cost (SGD) | Currency |  | Auto-sum |
| total_net_saving | Total Net Saving (SGD) | Currency |  | Gross minus implementation and maintenance |
| monitoring_notes | Monitoring Notes | Text Editor |  | Yearly conclusion and follow-up |
| savings_by_type_of_innovation | Savings by Type of Innovation | Table | Operational Outcomes Savings by Type of Innovation | Innovation-type portfolio |
| innovation_category_breakdown | Savings by Innovation Category | Table | Operational Outcomes Savings by Innovation Category | Category portfolio |
| monthly_throughput_breakdown | Monthly Throughput | Table | Operational Outcomes Monthly Throughput | Monthly trend |

## Raw source files

The exact supplied Quality Action CSV and Management Review text are stored in:

```text
source-material/Quality Action Fields.csv
source-material/Management Review.txt
```
