# Server Script Deployment — v1.8.8

Create or update each item as a separate Frappe **API Server Script**.

Common settings:

```text
Script Type: API
Enabled: Yes
Allow Guest: No
```

## Mandatory replacements

| Visible name | API method | File |
|---|---|---|
| UCC Analytics - Criterion 1 | `ucc_analytics_criterion_1` | `UCC Analytics - Criterion 1.py` |
| UCC Analytics - Criterion 2 | `ucc_analytics_criterion_2` | `UCC Analytics - Criterion 2.py` |
| UCC Analytics - Criterion 3 | `ucc_analytics_criterion_3` | `UCC Analytics - Criterion 3.py` |
| UCC Analytics - Criterion 5 | `ucc_analytics_criterion_5` | `UCC Analytics - Criterion 5.py` |
| UCC Analytics - Criterion 6 | `ucc_analytics_criterion_6` | `UCC Analytics - Criterion 6.py` |
| UCC Analytics - Criterion 7 | `ucc_analytics_criterion_7` | `UCC Analytics - Criterion 7.py` |

## Criterion 7 verification request

```json
{
  "payload": {
    "action": "summary",
    "subcriterion": "7.1.1",
    "filters": {
      "month": "2026-07"
    },
    "page_size": 100
  }
}
```

Endpoint:

```text
/api/method/ucc_analytics_criterion_7
```

Expected result:

- no `_unpack_sequence_` exception;
- `message.ok = true`;
- source and metric readiness returned;
- unavailable fields reported as `unsupported_field`, not as a server crash.

## Cache

Server Script body changes apply after saving. A browser hard refresh is
recommended, but the Custom HTML Block does not need to be replaced for this
specific runtime fix.
