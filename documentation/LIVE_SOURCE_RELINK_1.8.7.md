# Live Source Relink — v1.8.7

## Confirmed package defect

The v1.8.6 Criterion 1, 2, 3, 6 and 7 Server Scripts performed this sequence:

```text
frappe.get_meta(doctype)
    ↓
frappe.has_permission(doctype, "read")
    ↓
frappe.get_list(...)
```

Frappe Server Script safe-exec does not reliably expose every normal Frappe
helper. When `frappe.has_permission` was unavailable, the script caught the
exception and converted it to:

```text
permission_denied
```

That caused every source and every dependent metric to appear unavailable even
when the DocType was installed and readable.

## Corrected resolver

v1.8.7 uses the same runtime pattern as the mature Criterion 4 API:

```text
frappe.get_meta(doctype)
    ↓
frappe.get_list(doctype, fields=["name"], ...)
```

A successful `get_list` result means the source is installed and readable.

- Empty result: source is available with zero records.
- Permission exception: permission denied.
- Other query exception: source error.
- Metadata failure for every candidate: source unavailable.

## Affected APIs

- `ucc_analytics_criterion_1`
- `ucc_analytics_criterion_2`
- `ucc_analytics_criterion_3`
- `ucc_analytics_criterion_6`
- `ucc_analytics_criterion_7`

## Frontend changes

The live-foundation runtime now:

- parses nested or JSON-string API responses;
- records clearer API errors in Diagnostics;
- guards every chart value with a finite-number check;
- tells users to open Readiness for exact DocType, field or permission details.

Criterion 4 visual values also receive finite-number guards to prevent malformed
SVG geometry when a live value cannot be converted to a number.

## Deployment

Replace all five affected API Server Script bodies and all three Custom HTML
Block fields. Clear Frappe cache and hard-refresh before testing.
