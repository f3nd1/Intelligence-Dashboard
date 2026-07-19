# Challenges and Decisions

| Challenge | Decision | Reason |
|---|---|---|
| Only Custom HTML Block and Server Script access | Use one deployed HTML/CSS/JS block plus independent APIs | Matches actual permissions |
| Two products have different designs | Apply one UCC Blue and Gold shell and component overrides | Feels like one product without rewriting working flows |
| Existing dashboard is very large | Preserve v5.6.1 first | Reduces regression risk |
| Dashboard Python API is incomplete | Label it a migration foundation | Avoids false claims |
| Platform may grow to Criteria 1–7 | Add a dashboard registry and disabled planned entries | Future-ready without fake implementations |
| Ask UCC may grow | Use `ucc_ask_<domain>` naming | Predictable and searchable |
| One JS field can become hard to maintain | Keep isolated roots, IIFEs and section markers | Practical within Frappe |
| Independent Server Scripts cannot share imports | Keep scripts self-contained | Matches Frappe constraint |
| Browser and Python could disagree | Move calculations section-by-section to Python | Allows parity checks |
| Large datasets can be slow | Lazy load, paginate, summarise | Prevents loading everything |
| Permission leakage risk | Use permission-aware list calls and whitelists | Protects user data |
| AI may be unavailable or sensitive | Keep guided questions deterministic and AI optional | Core product still works |
| Technical names differ from UCC labels | Keep translations presentation-only | Prevents DocType-not-found errors |
| Future developer or AI may invent a backend app | Include AI_CONTEXT.md and explicit constraints | Reduces architectural drift |

## Deliberate deviation from the original dashboard architecture

The uploaded dashboard documentation recommended one Custom HTML Block per criterion.

The current product decision is one shared frontend shell for Criteria 1–7 because the user has only one frontend deployment surface and wants one product experience.

To control the risk:

- only the active criterion is loaded;
- each criterion must have its own API;
- future criteria are not implemented as empty code;
- generic containers and registries should be used where practical;
- a custom app should be reconsidered if complexity exceeds Server Script limits.
