## v1.8.2 deployment

Replace the three Custom HTML Block fields together. Read `custom-html-block/DEPLOYMENT_NOTES.md`. The new Criterion Catalogue Server Script is optional until an API consumer requires it.

# Deployment Guide

## Prerequisites

You need permission to:

- edit the target Custom HTML Block;
- create or edit API Server Scripts;
- read the relevant ERPNext DocTypes.

## Step 1 — Back up the current blocks

Copy the current HTML, CSS and JavaScript fields to a dated backup before replacing them.

Back up existing assistant Server Scripts as well.

## Step 2 — Install Ask UCC Server Scripts

Create separate API Server Scripts.

| File | API method |
|---|---|
| UCC Ask - Student Journey.py | `ucc_ask_student_journey` |
| UCC Ask - Recruitment Agent.py | `ucc_ask_recruitment_agent` |
| UCC Ask - Quality Action.py | `ucc_ask_quality_action` |

Settings:

- Enabled: Yes
- Allow Guest: No

## Step 3 — Install supporting Server Scripts

Install as needed:

- `ucc_analytics_bootstrap`
- `ucc_analytics_criterion_5`
- `ucc_analytics_drilldown`
- `ucc_shared_record_search`
- `ucc_shared_diagnostics`

Criterion 5 remains on the validated direct-client path in v1.1.0.

## Step 4 — Replace the Custom HTML Block

Paste:

```text
custom-html-block/HTML.html       → HTML field
custom-html-block/CSS.css         → CSS field
custom-html-block/JAVASCRIPT.js   → JavaScript field
```

Do not add `<style>` or `<script>` wrappers.

## Step 5 — Clear cache

- save the Custom HTML Block;
- clear Frappe cache if available;
- hard-refresh the browser;
- verify the dashboard build warning does not appear.

## Step 6 — Validate live behaviour

Follow `TESTING_GUIDE.md`.

## Rollback

Restore the backed-up HTML, CSS, JavaScript and previous API method names.

The consolidated Ask UCC JavaScript calls the new names:

```text
ucc_ask_student_journey
ucc_ask_recruitment_agent
ucc_ask_quality_action
```

If the old Server Script names must temporarily remain, either rename the API methods in Frappe or change the three `apiMethod` values in `JAVASCRIPT.js`.
