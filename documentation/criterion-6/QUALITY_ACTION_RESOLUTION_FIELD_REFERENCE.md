# Quality Action Resolution Field Reference

## DocType metadata

```text
DocType: Quality Action Resolution
Module: Quality Management
Child table: Yes
Editable grid: Yes
```

## Fields

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

## Candidate calculations

- open, planned, in-progress and completed resolution counts;
- finding-type distribution;
- overdue resolution count:
  `target_date < today` and status not completed;
- average completion duration;
- completion timeliness;
- ownership completeness;
- root-cause and action-description completeness.

Exact completeness rules require business approval.
