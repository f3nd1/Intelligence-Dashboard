## v1.8.2 regression

Test compact-left navigation, View tools, Explore search focus, Clear, hero contrast, Criterion 4/5 typography, all seven selector options, placeholder subcriterion tabs, live Criterion 4/5 APIs and all Ask UCC assistants.

# Testing Guide

The package can be statically validated offline, but live ERPNext verification is required.

## Static validation

Run:

```bash
python tools/validate_package.py
```

Expected checks:

- required files exist;
- JavaScript parses with Node when available;
- Python scripts parse;
- HTML IDs are unique;
- official UCC colours exist;
- required API names exist;
- no Criterion 1–4 or 6–7 implementation is falsely enabled.

## Platform shell

- Analytics Hub opens by default.
- Ask UCC opens without reloading the page.
- Dashboard selector shows Criteria 1–7.
- Only Criterion 5 is selectable.
- UCC Blue and Gold have readable contrast.
- Mobile layout remains usable.

## Criterion 5 regression

- Academic Year loads.
- Module Class Details loads.
- Course loads.
- Month filter works.
- Overview renders.
- Tabs 5.1–5.5 open.
- 5.1.1, 5.1.2, 5.2.1, 5.2.2 and 5.3.1 local navigation works.
- Diagram/Table toggles work.
- Chart and count drill-downs open records.
- Q&A filter works.
- Data Quality and Sources work.
- Q&A and exception CSV export work.
- Diagnostics CSV and JSON export work.
- No deployment build mismatch appears.

## Ask UCC regression

### Student Journey

- Student list/search loads.
- A student can be pinned.
- Every question category renders.
- Profile, journey, results, attendance, finance and graduation questions return.
- Record links open correctly.
- Guided mode works with no OpenAI key.

### Recruitment Agent

- Agent Contract records load.
- An agent can be pinned.
- profile, contract, recruitment, rating, revenue, commission and renewal questions return.
- New Bridge mapping is verified if that record exists.

### Quality Action

- Quality Actions load.
- Search by ID or subject works.
- record and portfolio questions return.
- overdue and closure rules match the source implementation.

## Permission testing

Test at least:

- System Manager;
- intended management/quality role;
- restricted academic user;
- a user without finance permission.

Confirm that unavailable and not-permitted states are not displayed as zero records.

## Performance

Test:

- first load;
- tab switching;
- a large drill-down;
- repeated filter changes;
- Ask UCC search with many records.

Capture the diagnostics export for slow or failed sections.

## Unverified in this build environment

- live UCC DocType names and custom fields;
- actual role permissions;
- live report availability;
- external D3 access;
- OpenAI connectivity.
