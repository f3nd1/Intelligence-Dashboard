## Placeholder criterion journey

A user may select any Criterion 1–7. Live Criteria 4 and 5 show analytics. Placeholder criteria show their approved subcriteria and the next configuration steps without pretending data exists.

# User Journeys

## Journey 1 — Analytics first

```text
Open platform
→ Analytics Hub
→ choose Criterion 5
→ apply Academic Year / Module Class / Course / Month filters
→ review KPIs and charts
→ switch Diagram / Table where available
→ open underlying records
→ export or inspect diagnostics
```

## Journey 2 — Ask UCC first

```text
Open platform
→ Ask UCC
→ select Student Journey, Recruitment Agent or Quality Action
→ find and pin a record
→ choose a predefined category and question
→ review answer, tables, timeline, warnings and source links
→ optionally ask a free-form follow-up
```

## Journey 3 — Management review

```text
Analytics Hub
→ Management Questions and Data-Based Answers
→ filter by criterion or subcriterion
→ inspect warning or risk answer
→ open supporting records
→ export Q&A or exceptions
```

## Journey 4 — Data troubleshooting

```text
Analytics Hub
→ Sources or Data Quality
→ open Diagnostics Log
→ identify unavailable DocType, fallback or permission issue
→ export CSV/JSON log
→ send log with screenshot to developer
```

## AI behaviour

AI is not required for guided questions.

- predefined questions use deterministic Server Script logic;
- free-form interpretation may require an OpenAI key;
- ERPNext remains the source of facts;
- the system must state missing data rather than guess.
