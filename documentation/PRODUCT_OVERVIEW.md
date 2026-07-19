# v1.8.7 Current-State Notice

Criteria 1–7 now use live data paths. Criteria 1, 2, 3, 6 and 7 use
permission-aware live foundations; Criterion 4 is mature live; Criterion 5 keeps
its validated live frontend. Any older preview discussion below is retained only
as historical design context and is not the active runtime.

# Product Overview — v1.8.4

## Purpose

The UCC Intelligence Platform gives authorised UCC users one place to inspect
analytics, open underlying records, explore diagrams and ask guided questions.

## Analytics

- Criteria 4 and 5 are live.
- Criteria 1–3 and 6–7 are interactive dummy previews.
- Criterion 3 contains 19 policy-grounded diagrams.
- Criterion 4 contains 24 live diagrams.
- Criterion 5 retains 94 existing diagrams.
- Criterion 6 contains 36 policy-grounded diagrams.

Every criterion uses the Criterion 5 visual framework.

## Explore

Explore searches the existing visual catalogue. Opening an item activates the
original criterion, section and diagram rather than creating a second copy.

## Ask UCC

The record-first workflow is:

```text
Choose role/module
→ search and select the student, agent or quality action
→ choose a guided question
→ display a chat-style answer with ERPNext evidence
```

Implemented modules:

- Student Journey
- Recruitment Agent
- Quality Action

## Data integrity

ERPNext/Frappe is the factual source of truth. Dummy preview values are always
labelled and must not be used for reporting.
