# Criterion 5 API and Migration Status

## API method

```text
ucc_analytics_criterion_5
```

`Allow Guest` must remain disabled.

## Supported actions

- `base`
- `overview`
- `c511_summary`
- `c511_proposals`
- `c511_modules`
- `c511_reviews`
- `c511_gaps`

## Action coverage

| Action | Sources loaded | Status |
| --- | --- | --- |
| base | Academic Year, Student Group, Course, Program | Migration foundation |
| overview | Academic Year, Student Group, Course, Program | Migration foundation |
| c511_summary | Course Proposal, Course, Program, Course Review, Assessment Plan | Migration foundation |
| c511_proposals | Course Proposal | Migration foundation |
| c511_modules | Course, Program, Assessment Plan | Migration foundation |
| c511_reviews | Course Review | Migration foundation |
| c511_gaps | Course Proposal, Course, Course Review | Migration foundation |

## Current response

```text
ok
meta
filters
data
sources
warnings
```

The API metadata reports:

```text
status = migration_foundation
```

## Migration boundary

### Already represented by the Server Script

- base filters;
- overview source loading;
- selected 5.1.1 proposal, module, review and gap source loading.

### Still primarily calculated in the frontend

- complete 5.1.1 calculations;
- 5.1.2;
- 5.2;
- 5.2.1;
- 5.2.2;
- 5.3;
- 5.3.1;
- 5.4;
- 5.5;
- many data-quality and exception calculations;
- all validated visual outputs requiring direct-client parity.

## Safe migration sequence

```text
define API action
    ↓
return source rows and readiness
    ↓
compare API and frontend values
    ↓
verify filters and permissions
    ↓
switch one section
    ↓
remove only the matching old calculation
```
