# Scalability and Limits

## Is the design scalable?

It is scalable enough for an internal UCC platform with Criteria 1–7 and several Ask UCC domains, provided the boundaries below are followed.

It is not equivalent to a full custom Frappe application.

## How the large system is kept manageable

### One physical frontend, several logical components

The deployment has one HTML, CSS and JavaScript field, but the code is separated by stable roots and IIFEs.

### One script per business responsibility

Criteria and Ask UCC domains must not be merged into one giant Python script.

### Lazy loading

Load only:

- the selected dashboard;
- the selected dashboard section;
- the requested drill-down page;
- the selected Ask UCC question.

Do not preload Criteria 1–7.

### Standard registries

Dashboard and Ask UCC registries identify:

- ID;
- label;
- status;
- API method;
- enabled state.

### Standard contracts

New APIs should use consistent request envelopes, errors, metadata and record links.

### Pagination and summarisation

Large record lists must be summarised server-side and paginated for drill-down.

## Main limits

### Custom HTML Block size

The combined frontend is large because it preserves two mature source interfaces. It must remain organised and validated.

### Server Script code reuse

Independent Server Scripts cannot be treated as importable modules. Shared validation patterns may need controlled duplication.

### Criterion 5 hybrid logic

Criterion 5 currently calculates in JavaScript. This should be migrated incrementally, not rewritten all at once.

### Live schema variation

Custom DocTypes and fields may differ from repository snapshots. Runtime source resolution and diagnostics remain necessary.

### Browser dependency

D3 is loaded from an external CDN. A site with restricted outbound access must provide an approved alternative.

## Scaling trigger

Consider requesting custom-app access when any of these becomes true:

- more than seven complex dashboards;
- frequent cross-script helper changes;
- long-running analytics;
- scheduled refresh or materialised datasets;
- formal automated backend tests are required;
- Server Script size or sandbox limits become operational blockers.

Until then, the current approach is the least risky solution within the access constraint.
