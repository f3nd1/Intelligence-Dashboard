# Criterion 5 — Academic Systems and Processes

## Purpose

This folder documents the current Criterion 5 frontend and Server Script so
future work can migrate calculations safely without losing output parity.

## Current status

Criterion 5 is live in the user interface, but its backend migration is not
complete.

```text
Frontend:
    validated direct-client calculations and permission-aware Frappe queries

Server Script:
    ucc_analytics_criterion_5
    migration foundation only
```

The Server Script currently supports base, overview and selected 5.1.1 source
loads. Other Criterion 5 sections still rely on the active frontend calculation
path.

## Important rule

Do not delete a frontend calculation merely because a matching API action has
been added. Compare values section by section before migration.

## Documentation in this folder

- `API_AND_MIGRATION_STATUS.md`
- `DOCTYPE_INVENTORY.md`
- `FIELD_REFERENCE.md`
- `ANALYTICS_MAPPING.md`
- `VISUAL_INVENTORY.md`
- `SECURITY_AND_PRIVACY.md`
- `OPEN_ITEMS.md`
- `RUNTIME_CONFIG_REFERENCE.md`
- `REVISION.json`
