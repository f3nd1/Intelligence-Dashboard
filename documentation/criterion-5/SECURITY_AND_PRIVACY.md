# Criterion 5 Security and Privacy

## Permission model

- `Allow Guest` must remain disabled for the Server Script.
- Frontend queries and API queries must honour current-user read permissions.
- Permission-denied, unavailable, unsupported-field and zero-record states must
  remain distinguishable.

## Data minimisation

Criterion 5 may process:

- student identity and attendance;
- assessment results and grades;
- teacher names and observations;
- survey responses and open comments;
- contracts and admissions;
- partnership and provider evaluations.

Dashboards should prefer aggregates. Drill-downs and exports must use approved
field allow-lists.

## Diagnostics

The validated frontend maintains a large diagnostics log with sensitive-key
redaction. New migration code must not log full student, survey or contract
payloads.

## Open-ended responses

Survey and review comments may contain personal or sensitive information.
Do not place raw open-ended text into summary charts or broad CSV exports
without explicit approval.

## Full-record sources

Several sources are currently configured with `full: true`. API migration should
replace broad full-record retrieval with the minimum fields required for each
metric.
