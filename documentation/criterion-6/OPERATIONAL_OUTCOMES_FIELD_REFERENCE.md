# Operational Outcomes Cost and Time Saving Field Reference

## DocType metadata

```text
DocType: Operational Outcomes Cost Time Saving
Module: Educ Sg
Naming: naming_series
```

## Classification note

The supplied field description says:

```text
The reporting year for Criterion 7 monitoring, one document per year.
```

This source can still support **Criterion 6.3** because it aggregates innovation
and Quality Action savings. It must be treated as a cross-criterion source until
the business owner confirms whether Criterion 6, Criterion 7 or both own the
official reporting output.

## Fields

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

## Candidate calculations

- total gross saving;
- implementation and maintenance cost;
- total net saving;
- variance to benchmark;
- people, technology and physical savings;
- savings by innovation type;
- savings by innovation category;
- monthly throughput trend.
