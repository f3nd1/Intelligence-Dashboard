/* UCC DIAGRAM EXPLORER v1.9.6 */
(function (global) {
"use strict";

const platformRoot = typeof root_element !== "undefined"
? root_element.querySelector("#uccIntelligencePlatform")
: document.querySelector("#uccIntelligencePlatform");

if (!platformRoot || platformRoot.dataset.exploreReady === "1") return;
platformRoot.dataset.exploreReady = "1";

const exploreRoot = platformRoot.querySelector("[data-ucc-explore]");
if (!exploreRoot) return;

const listNode = exploreRoot.querySelector("[data-ucc-explore-list]");
const searchNode = exploreRoot.querySelector("[data-ucc-explore-search]");
const sectionNode = exploreRoot.querySelector("[data-ucc-explore-section]");
const typeNode = exploreRoot.querySelector("[data-ucc-explore-type]");
const resultNode = exploreRoot.querySelector("[data-ucc-explore-result-count]");
const clearButton = exploreRoot.querySelector("[data-ucc-explore-clear]");
const dashboardSelect = platformRoot.querySelector("#uccDashboardSelect");
const workspaceButtons = Array.from(platformRoot.querySelectorAll("[data-ucc-workspace]"));

const parentTabMap = Object.freeze({
c511: "c51",
c512: "c51",
c521: "c52",
c522: "c52",
c531: "c53"
});

let entries = [];
let lastExploreScroll = 0;
let highlightedCard = null;

const returnButton = document.createElement("button");
returnButton.type = "button";
returnButton.className = "ucc-explore-return";
returnButton.textContent = "← Back to Explore";
returnButton.hidden = true;
platformRoot.appendChild(returnButton);

function text(value) {
return String(value == null ? "" : value).replace(/\s+/g, " ").trim();
}

function titleFrom(node) {
const card = node.closest("article, .panel");
const heading = card ? card.querySelector("h2,h3") : null;
return text(heading ? heading.textContent : node.dataset.chart || node.dataset.c4Visual || "Untitled visual");
}

function sectionLabel(entry) {
if (entry.kind === "demo") {
const button = platformRoot.querySelector(`[data-dashboard-panel="${CSS.escape(entry.dashboard)}"] [data-demo-tab="${CSS.escape(entry.panel || "overview")}"]`);
return text(button ? button.textContent : entry.panel || "Live foundation");
}
if (entry.dashboard === "criterion_4") {
const button = platformRoot.querySelector(`[data-c4-tab="${CSS.escape(entry.panel || "overview")}"]`);
return text(button ? button.textContent : entry.panel || "Criterion 4");
}
const button = platformRoot.querySelector(`[data-tab="${CSS.escape(parentTabMap[entry.panel] || entry.panel || "overview")}"]`);
const local = entry.panel && entry.panel !== (parentTabMap[entry.panel] || entry.panel)
? platformRoot.querySelector(`[data-section="${CSS.escape(entry.panel)}"]`)
: null;
return text(local ? local.textContent : button ? button.textContent : entry.panel || "Criterion 5");
}

function inferType(id, title) {
const value = `${id} ${title}`.toLowerCase();
const rules = [
["network", ["network"]],
["timeline", ["timeline", "trend", "aging", "recency"]],
["funnel", ["funnel", "flow", "lifecycle", "cycle"]],
["donut", ["donut", "ring", "orbit"]],
["heatmap", ["heatmap", "matrix"]],
["bubble", ["bubble", "constellation"]],
["radial", ["radial", "radar"]],
["decision", ["decision"]],
["ladder", ["ladder"]],
["reconciliation", ["reconciliation"]]
];
for (const [type, terms] of rules) {
if (terms.some(term => value.includes(term))) return type;
}
return "chart";
}

function sourceHint(node) {
const card = node.closest("article, .panel");
if (!card) return "Configured live source";
const sourceLink = card.querySelector(".source-doctype-link,.source-link,[data-source]");
return text(sourceLink ? sourceLink.textContent : "Configured live source");
}

function createEntry(node, dashboard, kind) {
const id = kind === "c4" ? node.dataset.c4Visual : kind === "demo" ? node.dataset.demoChart : node.dataset.chart;
if (!id) return null;
const panelNode = kind === "demo" ? node.closest("[data-demo-panel]") : dashboard === "criterion_4" ? node.closest("[data-c4-panel]") : node.closest("[data-panel]");
const title = kind === "demo" ? text(node.dataset.demoChartTitle || titleFrom(node)) : titleFrom(node);
const entry = {
key: `${dashboard}:${kind}:${id}`,id,kind,dashboard,node,title,
panel: kind === "demo" ? panelNode?.dataset.demoPanel || "overview" : dashboard === "criterion_4" ? panelNode?.dataset.c4Panel || "overview" : panelNode?.dataset.panel || "overview",
c511Panel: node.closest("[data-c511-panel]")?.dataset.c511Panel || "",
localPanel: node.closest("[data-local-panel]")?.dataset.localPanel || "",
type: kind === "demo" ? node.dataset.demoChartType || "live-foundation" : inferType(id, title),
source: kind === "demo" ? "Permission-aware live API foundation" : sourceHint(node)
};
entry.section = sectionLabel(entry);
return entry;
}

function buildRegistry() {
const registry = new Map();

Object.entries(global.UCCC4VisualDefinitions || {}).forEach(([panel, definitions]) => {
(definitions || []).forEach(definition => {
const entry = {
key: `criterion_4:c4-expanded:${definition.id}`,
id: definition.id,
kind: "c4-expanded",
dashboard: "criterion_4",
node: platformRoot.querySelector(`[data-c4-expanded-chart="${CSS.escape(definition.id)}"]`),
title: text(definition.title),
panel,
c511Panel: "",
localPanel: "",
type: definition.type || inferType(definition.id, definition.title),
source: "Permission-aware Criterion 4 API metrics"
};
entry.section = sectionLabel(entry);
if (!registry.has(entry.key)) registry.set(entry.key, entry);
});
});

platformRoot.querySelectorAll('[data-dashboard-panel="criterion_5"] [data-chart]').forEach(node => {
const entry = createEntry(node, "criterion_5", "c5");
if (entry && !registry.has(entry.key)) registry.set(entry.key, entry);
});

Object.entries(global.UCCLiveVisualDefinitions || {}).forEach(([dashboard, sections]) => {
Object.entries(sections || {}).forEach(([panel, definitions]) => {
(definitions || []).forEach(definition => {
const entry = {
key: `${dashboard}:demo:${definition.id}`,
id: definition.id,
kind: "demo",
dashboard,
node: platformRoot.querySelector(`[data-demo-chart="${CSS.escape(definition.id)}"]`),
title: text(definition.title),
panel,
c511Panel: "",
localPanel: "",
type: definition.type || inferType(definition.id, definition.title),
source: "Permission-aware live API metrics"
};
entry.section = sectionLabel(entry);
if (!registry.has(entry.key)) registry.set(entry.key, entry);
});
});
});

entries = Array.from(registry.values()).sort((a, b) =>
a.section.localeCompare(b.section) || a.title.localeCompare(b.title)
);

["criterion_1", "criterion_2", "criterion_3", "criterion_4", "criterion_5", "criterion_6", "criterion_7"].forEach(dashboard => {
const count = exploreRoot.querySelector(`[data-ucc-explore-count="${dashboard}"]`);
if (count) count.textContent = String(entries.filter(entry => entry.dashboard === dashboard).length);
});
}

function currentDashboard() {
return dashboardSelect ? dashboardSelect.value : "criterion_5";
}

function fillFilters() {
const dashboard = currentDashboard();
const dashboardEntries = entries.filter(entry => entry.dashboard === dashboard);
const previousSection = sectionNode.value;
const previousType = typeNode.value;
const sections = Array.from(new Set(dashboardEntries.map(entry => entry.section))).sort();
const types = Array.from(new Set(dashboardEntries.map(entry => entry.type))).sort();

sectionNode.innerHTML = '<option value="">All sections</option>' +
sections.map(value => `<option value="${value.replace(/"/g, "&quot;")}">${value}</option>`).join("");
typeNode.innerHTML = '<option value="">All visual types</option>' +
types.map(value => `<option value="${value.replace(/"/g, "&quot;")}">${value}</option>`).join("");

if (sections.includes(previousSection)) sectionNode.value = previousSection;
if (types.includes(previousType)) typeNode.value = previousType;
}

function filteredEntries() {
const dashboard = currentDashboard();
const query = text(searchNode.value).toLowerCase();
return entries.filter(entry =>
entry.dashboard === dashboard &&
(!query || `${entry.title} ${entry.section} ${entry.type} ${entry.source}`.toLowerCase().includes(query)) &&
(!sectionNode.value || entry.section === sectionNode.value) &&
(!typeNode.value || entry.type === typeNode.value)
);
}

function renderList() {
const dashboard = currentDashboard();
const liveDashboard = dashboard === "criterion_4" || dashboard === "criterion_5";
const rows = filteredEntries();
resultNode.textContent = `${rows.length} live diagram${rows.length === 1 ? "" : "s"}`;

const grouped = rows.reduce((result, entry) => {
(result[entry.section] ||= []).push(entry);
return result;
}, {});

listNode.innerHTML = Object.entries(grouped).map(([section, sectionEntries]) => `
<section class="ucc-explore-group">
<h2>${section}</h2>
${sectionEntries.map(entry => `
<button type="button" class="ucc-explore-item" data-ucc-explore-entry="${entry.key}">
<span>
<strong>${entry.title}</strong>
<small>${entry.source}</small>
</span>
<em>${entry.type}</em>
</button>
`).join("")}
</section>
`).join("") || '<div class="ucc-explore-empty">No diagrams match the current search and filters.</div>';
}

function chooseDashboard(dashboard) {
if (!dashboardSelect) return;
dashboardSelect.value = dashboard;
dashboardSelect.dispatchEvent(new Event("change", { bubbles: true }));
}

function chooseCriterion5Panel(entry, callback) {
const parent = parentTabMap[entry.panel] || entry.panel || "overview";
const parentButton = platformRoot.querySelector(
`[data-dashboard-panel="criterion_5"] [data-tab="${CSS.escape(parent)}"]`
);
if (parentButton) parentButton.click();

setTimeout(() => {
if (entry.panel && entry.panel !== parent) {
const sectionButton = platformRoot.querySelector(
`[data-dashboard-panel="criterion_5"] [data-section="${CSS.escape(entry.panel)}"]`
);
if (sectionButton) sectionButton.click();
}
setTimeout(callback, 180);
}, 100);
}

function resolveEntryNode(entry) {
if (entry.node && entry.node.isConnected) return entry.node;
if (entry.kind === "c4-expanded") {
entry.node = platformRoot.querySelector(`[data-c4-expanded-chart="${CSS.escape(entry.id)}"]`);
} else if (entry.kind === "demo") {
entry.node = platformRoot.querySelector(`[data-demo-chart="${CSS.escape(entry.id)}"]`);
} else if (entry.dashboard === "criterion_5") {
entry.node = platformRoot.querySelector(`[data-dashboard-panel="criterion_5"] [data-chart="${CSS.escape(entry.id)}"]`);
}
return entry.node || null;
}

function revealNestedViews(entry) {
const node = resolveEntryNode(entry);
if (entry.kind === "demo") {
window.UCCDemoAnalytics?.showTab(entry.dashboard, entry.panel || "overview");
node?.closest("[data-demo-card]")?.querySelector('[data-demo-view="diagram"]')?.click();
return;
}
if (entry.c511Panel) {
const button = platformRoot.querySelector(
`[data-dashboard-panel="criterion_5"] [data-c511-tab="${CSS.escape(entry.c511Panel)}"]`
);
if (button) button.click();
}
if (entry.localPanel) {
const panel = node?.closest("[data-panel]");
const button = panel ? panel.querySelector(
`[data-local-tab="${CSS.escape(entry.localPanel)}"]`
) : null;
if (button) button.click();
}
const card = node?.closest("article, .panel");
if (card) {
const diagramButton = entry.kind === "c4-expanded"
? card.querySelector('[data-c4-expanded-view="diagram"]')
: entry.dashboard === "criterion_4"
? card.querySelector('[data-c4-card-view="diagram"]')
: card.querySelector('[data-card-view="diagram"]');
if (diagramButton) diagramButton.click();
}
}

function highlightEntry(entry, attempt = 0) {
const node = resolveEntryNode(entry);
if (!node) {
if (attempt < 24) setTimeout(() => highlightEntry(entry, attempt + 1), 250);
else if (window.frappe && frappe.show_alert) frappe.show_alert({ message: "The selected visual could not be mounted. Open Source Mapping Report for details.", indicator: "orange" });
return;
}
if (highlightedCard) highlightedCard.classList.remove("ucc-explore-highlight");
highlightedCard = node.closest("article, .panel") || node;
highlightedCard.classList.add("ucc-explore-highlight");
highlightedCard.scrollIntoView({ behavior: "smooth", block: "center" });
setTimeout(() => highlightedCard?.classList.remove("ucc-explore-highlight"), 4200);
returnButton.hidden = false;
}

function openLiveEntry(entry) {
lastExploreScroll = Math.max(
Number(window.scrollY || 0),
Number(document.documentElement?.scrollTop || 0)
);
platformRoot.querySelector('[data-ucc-workspace="analytics"]')?.click();
chooseDashboard(entry.dashboard);

const finish = () => {
revealNestedViews(entry);
setTimeout(() => {
revealNestedViews(entry);
highlightEntry(entry);
window.dispatchEvent(new Event("resize"));
}, 220);
};

if (entry.kind === "demo") {
window.UCCDemoAnalytics?.showTab(entry.dashboard, entry.panel || "overview");
setTimeout(finish, 120);
} else if (entry.dashboard === "criterion_4") {
const tab = platformRoot.querySelector(
`[data-dashboard-panel="criterion_4"] [data-c4-tab="${CSS.escape(entry.panel || "overview")}"]`
);
if (tab) tab.click();
setTimeout(finish, 180);
} else {
chooseCriterion5Panel(entry, finish);
}
}

listNode.addEventListener("click", event => {
const switchButton = event.target.closest("[data-ucc-explore-switch]");
if (switchButton) {
chooseDashboard(switchButton.dataset.uccExploreSwitch);
fillFilters();
renderList();
return;
}
const button = event.target.closest("[data-ucc-explore-entry]");
if (!button) return;
const entry = entries.find(item => item.key === button.dataset.uccExploreEntry);
if (entry) openLiveEntry(entry);
});

function resetFilters() {
searchNode.value = "";
sectionNode.value = "";
typeNode.value = "";
renderList();
}

searchNode.addEventListener("input", renderList);
sectionNode.addEventListener("change", renderList);
typeNode.addEventListener("change", renderList);
["pointerdown", "mousedown", "click", "keydown", "keyup", "keypress", "focus", "focusin"].forEach(function (eventName) {
searchNode.addEventListener(eventName, function (event) {
event.stopPropagation();
if (typeof event.stopImmediatePropagation === "function") event.stopImmediatePropagation();
});
});
searchNode.addEventListener("keydown", function (event) {
if (event.key === "Escape") {
event.preventDefault();
resetFilters();
searchNode.focus();
}
});
clearButton.addEventListener("pointerdown", function (event) {
event.stopPropagation();
});
clearButton.addEventListener("click", function (event) {
event.preventDefault();
event.stopPropagation();
resetFilters();
searchNode.focus();
});

dashboardSelect?.addEventListener("change", () => {
fillFilters();
renderList();
});

workspaceButtons.forEach(button => {
button.addEventListener("click", () => {
if (button.dataset.uccWorkspace === "explore") {
returnButton.hidden = true;
setTimeout(() => window.scrollTo({ top: lastExploreScroll, behavior: "smooth" }), 0);
}
});
});

returnButton.addEventListener("click", () => {
platformRoot.querySelector('[data-ucc-workspace="explore"]')?.click();
});

buildRegistry();
fillFilters();
renderList();

global.UCCExplore = Object.freeze({
entries: () => entries.slice(),
openEntry: keyOrEntry => {
const entry = typeof keyOrEntry === "string" ? entries.find(item => item.key === keyOrEntry) : keyOrEntry;
if (entry) openLiveEntry(entry);
},
openNavigator: dashboard => {
if (dashboard) chooseDashboard(dashboard);
platformRoot.querySelector('[data-ucc-workspace="explore"]')?.click();
setTimeout(() => searchNode?.focus(), 80);
},
rebuild: () => {
buildRegistry();
fillFilters();
renderList();
}
});
})(window);
