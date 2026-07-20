#!/usr/bin/env python3
"""Validate UCC Intelligence Platform v1.9.5 without a live Frappe site."""

from __future__ import annotations

import ast
import json
import re
import shutil
import subprocess
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VERSION = "1.9.5"
# Active (enabled) visual counts. Cut visuals are retained in source with
# enabled:false (LIVE/C4) or listed in C5_DISABLED_VISUALS (C5) and archived in
# documentation/archived-visuals.md; they are not counted here.
EXPECTED_VISUALS = {
    "criterion_1": 30,
    "criterion_2": 30,
    "criterion_3": 30,
    "criterion_4": 30,
    "criterion_5": 32,
    "criterion_6": 30,
    "criterion_7": 30,
}

REQUIRED = [
    "README.md",
    "AI_CONTEXT.md",
    "CHANGELOG.md",
    "VERSION.json",
    "build-manifest.json",
    "src/html/platform.html",
    "src/css/platform.css",
    "src/js/00-shared-runtime.js",
    "src/js/10-platform-runtime.js",
    "src/js/20-explore-runtime.js",
    "src/js/30-live-foundation-runtime.js",
    "src/js/40-visual-navigation-runtime.js",
    "custom-html-block/HTML.html",
    "custom-html-block/CSS.css",
    "custom-html-block/JAVASCRIPT.js",
    "server-scripts/UCC Analytics - Bootstrap.py",
    "server-scripts/UCC Analytics - Criterion 1.py",
    "server-scripts/UCC Analytics - Criterion 2.py",
    "server-scripts/UCC Analytics - Criterion 3.py",
    "server-scripts/UCC Analytics - Criterion Catalogue.py",
    "server-scripts/UCC Analytics - Criterion 4.py",
    "server-scripts/UCC Analytics - Criterion 5.py",
    "server-scripts/UCC Analytics - Criterion 6.py",
    "server-scripts/UCC Analytics - Criterion 7.py",
    "server-scripts/UCC Shared - Diagnostics.py",
    "reference/dashboard-registry.json",
]


class IdParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"])


def report(ok: bool, message: str) -> bool:
    print(("PASS" if ok else "FAIL") + ": " + message)
    return ok


def extract_json_constant(text: str, name: str) -> dict:
    match = re.search(rf"const {re.escape(name)}=(\{{.*?\}});", text, re.S)
    if not match:
        raise ValueError(f"Could not find {name}")
    return json.loads(match.group(1))


def combined(paths: list[str]) -> str:
    return "\n".join((ROOT / path).read_text(encoding="utf-8").rstrip() for path in paths) + "\n"


def main() -> int:
    checks: list[bool] = []

    for relative in REQUIRED:
        checks.append(report((ROOT / relative).is_file(), f"required file {relative}"))

    version = json.loads((ROOT / "VERSION.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "build-manifest.json").read_text(encoding="utf-8"))
    checks.append(report(version.get("version") == EXPECTED_VERSION, f"VERSION.json is {EXPECTED_VERSION}"))
    checks.append(report(manifest.get("version") == EXPECTED_VERSION, f"build manifest is {EXPECTED_VERSION}"))
    checks.append(report(version.get("visual_targets") == EXPECTED_VISUALS, "VERSION.json visual targets match the approved catalogue"))

    html = (ROOT / "custom-html-block/HTML.html").read_text(encoding="utf-8")
    css = (ROOT / "custom-html-block/CSS.css").read_text(encoding="utf-8")
    javascript = (ROOT / "custom-html-block/JAVASCRIPT.js").read_text(encoding="utf-8")
    source_html = (ROOT / "src/html/platform.html").read_text(encoding="utf-8")
    source_js = (ROOT / "src/js/10-platform-runtime.js").read_text(encoding="utf-8")
    live_js = (ROOT / "src/js/30-live-foundation-runtime.js").read_text(encoding="utf-8")
    navigation_js = (ROOT / "src/js/40-visual-navigation-runtime.js").read_text(encoding="utf-8")

    checks.append(report(html == combined(manifest["html"]), "built HTML matches source manifest"))
    checks.append(report(css == combined(manifest["css"]), "built CSS matches source manifest"))
    checks.append(report(javascript == combined(manifest["javascript"]), "built JavaScript matches source manifest"))

    parser = IdParser()
    parser.feed(html)
    duplicates = [name for name, count in Counter(parser.ids).items() if count > 1]
    checks.append(report(not duplicates, "HTML IDs are unique" + (f": {duplicates}" if duplicates else "")))

    checks.append(report("#26345b" in css.lower(), "CSS contains UCC Blue #26345B"))
    checks.append(report("#ce9e5d" in css.lower(), "CSS contains UCC Gold #CE9E5D"))
    checks.append(report(css.count("{") == css.count("}"), "CSS brace counts match"))
    checks.append(report("ucc-demo-view-toggle" not in source_html + live_js + css, "separate live-foundation toggle CSS and markup were removed"))
    checks.append(report(".mini-toggle" in css and 'class="mini-toggle"' in source_html, "all Diagram/Table controls use the Criterion 5 mini-toggle pattern"))

    def active(items):
        return [item for item in items if item.get("enabled") is not False]

    live_definitions = extract_json_constant(live_js, "LIVE_VISUAL_EXPANSION")
    for dashboard in ("criterion_1", "criterion_2", "criterion_3", "criterion_6", "criterion_7"):
        detected = sum(len(active(items)) for items in live_definitions[dashboard].values())
        checks.append(report(detected == EXPECTED_VISUALS[dashboard], f"{dashboard} has {detected} active live visual definitions"))

    c4_definitions = extract_json_constant(source_js, "C4_VISUAL_EXPANSION")
    c4_count = sum(len(active(items)) for items in c4_definitions.values())
    checks.append(report(c4_count == EXPECTED_VISUALS["criterion_4"], f"criterion_4 has {c4_count} active discoverable visual definitions"))

    c5_total = len(set(re.findall(r'data-chart="([^"]+)"', source_html)))
    c5_disabled_match = re.search(r"const C5_DISABLED_VISUALS=new Set\((\[.*?\])\)", source_js, re.S)
    c5_disabled = set(json.loads(c5_disabled_match.group(1))) if c5_disabled_match else set()
    c5_count = c5_total - len(c5_disabled)
    checks.append(report(c5_count == EXPECTED_VISUALS["criterion_5"], f"criterion_5 has {c5_count} active live visual definitions ({len(c5_disabled)} archived)"))

    checks.append(report("UCCC4VisualDefinitions" in source_js, "Criterion 4 visual definitions are exposed to the universal navigator"))
    checks.append(report("visual-navigator" in source_html and "source-mapping" in source_html, "View tools contains functional visual and source actions"))
    checks.append(report("visualHoverReady" in navigation_js and "ucc-visual-hover-menu" in navigation_js, "universal visual menu is installed"))
    checks.append(report("invalidSvgReason" in navigation_js and "NaN|undefined|Infinity" in navigation_js, "invalid SVG and blank visual guard is installed"))
    checks.append(report("ucc_shared_diagnostics" in navigation_js, "source mapping report calls the diagnostics API"))
    checks.append(report("data-source-mapping-copy" in navigation_js and "Detected fields" in navigation_js, "source mapping report exposes field inventory and a copyable report"))
    checks.append(report(
        "platform.appendChild(mappingDialog)" in navigation_js
        and 'anchor.insertAdjacentElement("afterend", menu)' in navigation_js
        and "platform.querySelectorAll(" in navigation_js,
        "overlay UI remains inside the scoped Custom HTML Block"
    ))
    checks.append(report('platform.addEventListener("click", event =>' in navigation_js and 'button.closest("[data-demo-dashboard]")' in navigation_js, "dynamic source-mapping buttons use scoped event delegation"))
    checks.append(report("UCCLiveVisualDefinitions" in live_js and "Object.entries(global.UCCLiveVisualDefinitions" in (ROOT / "src/js/20-explore-runtime.js").read_text(encoding="utf-8"), "explorer uses the approved live visual definitions"))
    checks.append(report("data-live-section" in live_js and "syncLiveSectionVisibility" in live_js, "grouped live panels show only the active subcriterion catalogue"))
    criterion1 = (ROOT / "server-scripts/UCC Analytics - Criterion 1.py").read_text(encoding="utf-8")
    criterion2 = (ROOT / "server-scripts/UCC Analytics - Criterion 2.py").read_text(encoding="utf-8")
    checks.append(report("'staff_goal': ['Goal']" in criterion1 and "custom_department" in criterion1, "Criterion 1 uses the confirmed Goal mapping and supplied UCC fields"))
    checks.append(report("Training Needs Analysis" in criterion2 and "Material Vetting Form" in criterion2, "Criterion 2 uses confirmed UCC DocTypes"))
    checks.append(report("reviewed_by" in criterion2 and "approval_status" in criterion2, "Criterion 2 uses supplied review and approval fields"))

    catalogue = (ROOT / "server-scripts/UCC Analytics - Criterion Catalogue.py").read_text(encoding="utf-8")
    diagnostics = (ROOT / "server-scripts/UCC Shared - Diagnostics.py").read_text(encoding="utf-8")
    checks.append(report("End of Module Survey (Student)" not in diagnostics and "Naming Series Register" not in diagnostics, "retired Criterion 2 source assumptions are removed from diagnostics"))
    checks.append(report("if requested_dashboard and requested_dashboard not in criteria" in diagnostics, "diagnostics are restricted to the selected criterion"))
    criterion6 = (ROOT / "server-scripts/UCC Analytics - Criterion 6.py").read_text(encoding="utf-8")
    checks.append(report('"version": "1.9.5"' in catalogue, "Criterion catalogue reports platform version 1.9.5"))
    checks.append(report('"provider_rating": ["Provider Rating", "Supplier Rating"]' in criterion6, "Criterion 6 uses the approved Provider Rating fallback pair"))
    checks.append(report("resolution_attempts" in criterion6 and "continue" in criterion6, "Criterion 6 continues to approved fallbacks after a stale candidate error"))
    checks.append(report("APPROVED_SOURCE_GROUPS" in diagnostics and "field_inventory" in diagnostics, "shared diagnostics reports candidate, metadata and field-level mapping"))
    checks.append(report("arbitrary DocTypes" in diagnostics, "diagnostics script documents its approved-only boundary"))

    node = shutil.which("node")
    if node:
        for script in sorted((ROOT / "src/js").glob("*.js")):
            process = subprocess.run([node, "--check", str(script)], capture_output=True, text=True)
            checks.append(report(process.returncode == 0, f"JavaScript parses: {script.name}"))
            if process.returncode != 0:
                print(process.stderr)
        process = subprocess.run([node, "--check", str(ROOT / "custom-html-block/JAVASCRIPT.js")], capture_output=True, text=True)
        checks.append(report(process.returncode == 0, "combined JavaScript parses with Node"))
        if process.returncode != 0:
            print(process.stderr)
    else:
        print("SKIP: Node is not installed; JavaScript syntax was not checked.")

    for script in sorted((ROOT / "server-scripts").glob("*.py")):
        try:
            ast.parse(script.read_text(encoding="utf-8"))
            checks.append(report(True, f"Python parses: {script.name}"))
        except SyntaxError as error:
            checks.append(report(False, f"Python parses: {script.name}: {error}"))

    for reference in sorted((ROOT / "reference").glob("*.json")):
        try:
            json.loads(reference.read_text(encoding="utf-8"))
            checks.append(report(True, f"JSON parses: {reference.name}"))
        except json.JSONDecodeError as error:
            checks.append(report(False, f"JSON parses: {reference.name}: {error}"))

    registry = json.loads((ROOT / "reference/dashboard-registry.json").read_text(encoding="utf-8"))
    dashboards = registry.get("dashboards", [])
    checks.append(report(registry.get("version") == EXPECTED_VERSION, "dashboard registry version is current"))
    checks.append(report(len(dashboards) == 7 and all(item.get("enabled") for item in dashboards), "all seven live dashboards are enabled in the registry"))

    secret_markers = [token for token in ("Bearer ", "password=") if token in javascript]
    checks.append(report(not secret_markers, "no obvious embedded frontend secret"))

    passed = all(checks)
    print()
    print(f"VALIDATION {'PASSED' if passed else 'FAILED'}: {sum(checks)}/{len(checks)} checks")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
