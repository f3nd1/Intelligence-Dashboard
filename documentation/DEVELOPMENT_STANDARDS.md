# Development Standards

## Naming

### Product

```text
UCC Intelligence Platform
Analytics Hub
Ask UCC
```

### Server Scripts

```text
UCC Analytics - <name>
UCC Ask - <domain>
UCC Shared - <function>
```

### API methods

```text
ucc_analytics_<name>
ucc_ask_<domain>
ucc_shared_<function>
```

## Frontend rules

- Keep one HTML, one CSS and one JavaScript deployment file.
- Scope styles beneath `.ucc-platform`, `.ucc-c5-v41` or `.aja-app`.
- Preserve stable IDs and `data-*` hooks.
- Keep UCC Blue `#26345B` and UCC Gold `#CE9E5D`.
- Use white text on UCC Blue.
- Use dark text on UCC Gold.
- Do not calculate a new official KPI only in JavaScript if it will also be used by Ask UCC.
- Do not load inactive dashboards at startup.
- Do not add a framework merely to imitate a normal application build.

## Server Script rules

- Allow Guest: disabled.
- Prefer `frappe.get_list`.
- Validate actions, entities, datasets, fields and page sizes.
- Check read permissions.
- Return structured errors.
- Never accept an arbitrary DocType from the browser.
- Never expose passwords, tokens or permanent API keys.
- Keep scripts self-contained.
- Do not create placeholder scripts for unconfirmed criteria.

## Data rules

- Missing means unknown, not zero.
- Permission denied means unavailable, not no records.
- User-facing translations do not change technical field or DocType names.
- Distinguish confirmed, inferred and unknown mappings.
- Include supporting record links where possible.

## Change process

1. State the requested behaviour.
2. Identify affected files and current behaviour.
3. Make the smallest coherent change.
4. Run package validation.
5. Test the affected live flow.
6. Update version and change log.
7. Record any unverified point.
