# Server Script Deployment — v1.8.9

## Required replacements

### Criterion 3

```text
Visible name: UCC Analytics - Criterion 3
API method: ucc_analytics_criterion_3
Script type: API
Enabled: Yes
Allow Guest: No
```

Paste:

```text
server-scripts/UCC Analytics - Criterion 3.py
```

### Criterion 6

```text
Visible name: UCC Analytics - Criterion 6
API method: ucc_analytics_criterion_6
Script type: API
Enabled: Yes
Allow Guest: No
```

Paste:

```text
server-scripts/UCC Analytics - Criterion 6.py
```

## Provider Rating check

Both scripts try these approved technical candidates in order:

1. `Provider Rating`
2. `Supplier Rating`

The first installed and readable source is returned as `source.doctype`.

## Frontend replacement

Paste all three files from:

```text
custom-html-block/
├── HTML.html
├── CSS.css
└── JAVASCRIPT.js
```

Do not mix v1.8.9 frontend files with an older version.

## Cache and UAT

1. Clear Frappe cache.
2. Clear website cache.
3. Hard refresh.
4. Confirm the displayed platform version is v1.8.9.
5. Change between all seven criteria and verify the page returns to the hero.
6. Verify all tab rows remain one row and can scroll horizontally.
7. Verify Criterion 5 child sections are visible.
8. Test matching-record and source-list actions.
9. Test Provider Rating with an authorised and restricted role.
