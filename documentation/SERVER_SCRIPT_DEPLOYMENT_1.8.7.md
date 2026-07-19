# Server Script Deployment — v1.8.7

Create every file as a separate Frappe **API Server Script**.

Common settings:

```text
Script Type: API
Enabled: Yes
Allow Guest: No
```

## Required analytics methods

| Visible name | API method | File |
|---|---|---|
| UCC Analytics - Bootstrap | `ucc_analytics_bootstrap` | `UCC Analytics - Bootstrap.py` |
| UCC Analytics - Criterion Catalogue | `ucc_analytics_criterion_catalogue` | `UCC Analytics - Criterion Catalogue.py` |
| UCC Analytics - Criterion 1 | `ucc_analytics_criterion_1` | `UCC Analytics - Criterion 1.py` |
| UCC Analytics - Criterion 2 | `ucc_analytics_criterion_2` | `UCC Analytics - Criterion 2.py` |
| UCC Analytics - Criterion 3 | `ucc_analytics_criterion_3` | `UCC Analytics - Criterion 3.py` |
| UCC Analytics - Criterion 4 | `ucc_analytics_criterion_4` | `UCC Analytics - Criterion 4.py` |
| UCC Analytics - Criterion 5 | `ucc_analytics_criterion_5` | `UCC Analytics - Criterion 5.py` |
| UCC Analytics - Criterion 6 | `ucc_analytics_criterion_6` | `UCC Analytics - Criterion 6.py` |
| UCC Analytics - Criterion 7 | `ucc_analytics_criterion_7` | `UCC Analytics - Criterion 7.py` |
| UCC Analytics - Drilldown | `ucc_analytics_drilldown` | `UCC Analytics - Drilldown.py` |

## Test endpoints

```text
/api/method/ucc_analytics_criterion_1
/api/method/ucc_analytics_criterion_2
/api/method/ucc_analytics_criterion_3
/api/method/ucc_analytics_criterion_4
/api/method/ucc_analytics_criterion_5
/api/method/ucc_analytics_criterion_6
/api/method/ucc_analytics_criterion_7
```

Example request:

```json
{
  "payload": {
    "action": "summary",
    "subcriterion": "2.4.2",
    "filters": {}
  }
}
```

When testing through an HTTP form request, send `payload` as a JSON string.

## UAT

Test each method using:

1. a System Manager;
2. an authorised operational role;
3. a restricted user;
4. a source with zero matching records;
5. a missing optional custom DocType;
6. a metric requiring an unavailable field;
7. drill-down and CSV export.

Expected states include:

```text
available
permission_denied
unavailable
unsupported
unsupported_field
error
```

Do not change an unavailable or unsupported state into a zero value.


## v1.8.7 resolver correction

Replace the following API Server Script bodies, even when the visible names and
API methods already exist:

- `UCC Analytics - Criterion 1.py`
- `UCC Analytics - Criterion 2.py`
- `UCC Analytics - Criterion 3.py`
- `UCC Analytics - Criterion 6.py`
- `UCC Analytics - Criterion 7.py`

The previous foundation called `frappe.has_permission`, which is not reliably
exposed in Frappe Server Script safe-exec. When unavailable, the caught
exception was converted into `permission_denied` for every source. v1.8.7 uses
the same permission-aware `frappe.get_list` probe as the mature Criterion 4
implementation.

After replacing the scripts, replace all three Custom HTML Block fields and
clear the Frappe cache.
