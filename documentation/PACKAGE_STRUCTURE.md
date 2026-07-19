## v1.8.9 documentation

```text
documentation/
├── UNIVERSAL_ANALYTICS_UI_1.8.9.md
└── SERVER_SCRIPT_DEPLOYMENT_1.8.9.md
```

## v1.8.8 hotfix references

```text
documentation/
├── SAFE_EXEC_SEQUENCE_HOTFIX_1.8.8.md
└── SERVER_SCRIPT_DEPLOYMENT_1.8.8.md
```

## v1.8.7 diagnostic documentation

```text
documentation/
├── LIVE_SOURCE_RELINK_1.8.7.md
└── CONSOLE_ERROR_ASSESSMENT_1.8.7.md
```

# Package Structure — v1.8.7

```text
ucc-intelligence-platform-v1.8.7/
├── README.md
├── CHANGELOG.md
├── AI_CONTEXT.md
├── VERSION.json
├── build-manifest.json
├── custom-html-block/
│   ├── HTML.html
│   ├── CSS.css
│   ├── JAVASCRIPT.js
│   └── DEPLOYMENT_NOTES.md
├── server-scripts/
│   ├── README.md
│   ├── UCC Analytics - Bootstrap.py
│   ├── UCC Analytics - Criterion Catalogue.py
│   ├── UCC Analytics - Criterion 1.py
│   ├── UCC Analytics - Criterion 2.py
│   ├── UCC Analytics - Criterion 3.py
│   ├── UCC Analytics - Criterion 4.py
│   ├── UCC Analytics - Criterion 5.py
│   ├── UCC Analytics - Criterion 6.py
│   ├── UCC Analytics - Criterion 7.py
│   └── supporting Ask UCC, drill-down and diagnostics scripts
├── documentation/
│   ├── SERVER_SCRIPT_DEPLOYMENT_1.8.7.md
│   ├── criterion-1/
│   ├── criterion-2/
│   ├── criterion-3/
│   ├── criterion-4/
│   ├── criterion-5/
│   ├── criterion-6/
│   └── criterion-7/
├── reference/
├── src/
├── dist/
├── tools/
└── archive/
```

## Active deployment sources

Only these three files are pasted into the Frappe Custom HTML Block:

```text
custom-html-block/HTML.html
custom-html-block/CSS.css
custom-html-block/JAVASCRIPT.js
```

Each file under `server-scripts/` is created as its own API Server Script.

## Policy source material

Original approved policy DOCX files supplied for Criteria 1, 2 and 7 are retained
inside each criterion's `source-material/` folder. Criteria 3–6 retain their
existing source inventories and implementation notes.

## Legacy content

`archive/` and the legacy placeholder API are retained only for traceability.
They are not active dashboard data paths.
