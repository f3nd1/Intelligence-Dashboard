# Criterion 6 Security and Privacy

## Sensitive content

Criterion 6 may contain:

- root-cause investigations;
- audit findings and nonconformities;
- staff assignments and performance;
- risk descriptions and mitigation plans;
- financial costs, savings and budgets;
- provider evaluations;
- meeting minutes;
- confidential evidence and attachments;
- free-text executive and review notes.

## Dashboard rules

- Aggregate findings and actions whenever possible.
- Use approved field allow-lists for drill-downs.
- Do not export unrestricted Text Editor content.
- Do not expose attachment payloads or signatures.
- Do not expose confidential meeting minutes to users without permission.
- Keep provider and staff evaluation comments permission-controlled.
- Do not log full Quality Action or Management Review payloads.
- `Allow Guest` must remain disabled for a future live API.

## Financial data

Operational Outcomes and Quality Action contain financial measures. Access to:

- implementation cost;
- maintenance cost;
- budget;
- actual spending;
- savings;
- benchmark values;

must follow the relevant finance and management roles.

## Free-text fields

Fields such as problem, root cause, executive summary, risk notes and qualitative
reviews can contain personal or sensitive material. Summary analytics should
prefer status, dates, ownership and calculated measures.
