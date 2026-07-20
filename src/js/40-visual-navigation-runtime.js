/* UCC universal visual navigation and diagnostics v1.9.6 */
(function (global) {
"use strict";

const platform = typeof root_element !== "undefined"
? root_element.querySelector("#uccIntelligencePlatform")
: document.querySelector("#uccIntelligencePlatform");

if (!platform || platform.dataset.universalVisualMenuReady === "1") return;
platform.dataset.universalVisualMenuReady = "1";

const expectedCounts = Object.freeze({
criterion_1: 84,
criterion_2: 99,
criterion_3: 90,
criterion_4: 84,
criterion_5: 94,
criterion_6: 96,
criterion_7: 80
});
const criterionLabels = Object.freeze({
criterion_1: "Criterion 1",
criterion_2: "Criterion 2",
criterion_3: "Criterion 3",
criterion_4: "Criterion 4",
criterion_5: "Criterion 5",
criterion_6: "Criterion 6",
criterion_7: "Criterion 7"
});
const c5Children = Object.freeze({
c51: ["c51", "c511", "c512"],
c52: ["c52", "c521", "c522"],
c53: ["c53", "c531"]
});
const issues = [];
const blankFirstSeen = new WeakMap();
let activeTrigger = null;
let activeEntries = [];
let activeDashboard = "";
let activeSection = "";
let suppressNextTabMenu = false;
let lastMappingResult = null;

function clean(value) {
return String(value == null ? "" : value).replace(/\s+/g, " ").trim();
}
function esc(value) {
return String(value == null ? "" : value)
.replaceAll("&", "&amp;")
.replaceAll("<", "&lt;")
.replaceAll(">", "&gt;")
.replaceAll('"', "&quot;");
}
function notify(message, indicator) {
if (global.frappe && frappe.show_alert) frappe.show_alert({ message, indicator: indicator || "blue" });
}
function registry() {
return global.UCCExplore && typeof global.UCCExplore.entries === "function"
? global.UCCExplore.entries()
: [];
}
function triggerSection(trigger) {
return trigger.dataset.demoTab || trigger.dataset.c4Tab || trigger.dataset.tab || "overview";
}
function triggerDashboard(trigger) {
return trigger.closest("[data-dashboard-panel]")?.dataset.dashboardPanel || "";
}
function sectionPanels(dashboard, section) {
if (dashboard === "criterion_5" && c5Children[section]) return c5Children[section];
return [section];
}
function entriesFor(dashboard, section) {
const panels = sectionPanels(dashboard, section);
return registry().filter(entry => entry.dashboard === dashboard && panels.includes(entry.panel || "overview"));
}
function tabLabel(trigger) {
const clone = trigger.cloneNode(true);
clone.querySelectorAll(".ucc-tab-visual-count").forEach(node => node.remove());
return clean(clone.textContent) || "Section";
}
function directTabTriggers() {
return Array.from(platform.querySelectorAll(
'[data-dashboard-panel] nav.tabs > button[data-demo-tab], ' +
'[data-dashboard-panel] nav.tabs > button[data-c4-tab], ' +
'[data-dashboard-panel="criterion_5"] nav.tabs > button[data-tab], ' +
'[data-dashboard-panel="criterion_5"] nav.tabs > .ucc-c5-menu-group > button[data-tab]'
));
}

const menu = document.createElement("section");
menu.className = "ucc-visual-hover-menu";
menu.hidden = true;
menu.setAttribute("role", "region");
menu.setAttribute("aria-label", "Section visual menu");
menu.innerHTML = '<header><div><strong data-visual-menu-title>Section visuals</strong><br><span data-visual-menu-count>0 visuals</span></div></header><div class="ucc-visual-hover-menu-list" data-visual-menu-list></div><div class="ucc-visual-hover-menu-footer"><button type="button" data-visual-menu-section>Open section</button><button type="button" data-visual-menu-all>View all visuals</button></div>';
const menuTitle = menu.querySelector("[data-visual-menu-title]");
const menuCount = menu.querySelector("[data-visual-menu-count]");
const menuList = menu.querySelector("[data-visual-menu-list]");

function placeMenu(trigger) {
// In-flow panel: anchor it directly below the tab bar it belongs to,
// outside any position:sticky wrapper, so it pushes following content
// (readiness strip, KPI cards, panels) down instead of floating over it.
const anchor = trigger.closest(".sticky-navigation") || trigger.closest("nav") || trigger.parentElement;
if (anchor && anchor.nextElementSibling !== menu) anchor.insertAdjacentElement("afterend", menu);
}
function closeMenu() {
menu.hidden = true;
if (activeTrigger) activeTrigger.setAttribute("aria-expanded", "false");
activeTrigger = null;
activeEntries = [];
activeDashboard = "";
activeSection = "";
}
function openMenu(trigger) {
const dashboard = triggerDashboard(trigger);
const section = triggerSection(trigger);
const entries = entriesFor(dashboard, section);
if (activeTrigger && activeTrigger !== trigger) activeTrigger.setAttribute("aria-expanded", "false");
activeTrigger = trigger;
activeEntries = entries;
activeDashboard = dashboard;
activeSection = section;
trigger.setAttribute("aria-expanded", "true");
menuTitle.textContent = tabLabel(trigger);
menuCount.textContent = entries.length + " visual" + (entries.length === 1 ? "" : "s");
menuList.innerHTML = entries.length
? entries.map(entry => '<button type="button" data-visual-entry="' + esc(entry.key) + '"><span class="ucc-visual-hover-menu-label"><strong>' + esc(entry.title) + '</strong>' + (entry.description ? '<span class="ucc-visual-menu-desc"> — ' + esc(entry.description) + '</span>' : '') + '</span><small class="ucc-visual-menu-type">' + esc(entry.type) + '</small></button>').join("")
: '<div class="ucc-visual-diagnostic"><strong>No visual is registered for this section</strong><span>Use Source Mapping Report to check whether a DocType, permission or field mapping prevented the visual catalogue from loading.</span><button type="button" data-ucc-open-mapping>Source mapping report</button></div>';
placeMenu(trigger);
menu.hidden = false;
}
function toggleMenu(trigger) {
if (activeTrigger === trigger && !menu.hidden) closeMenu();
else openMenu(trigger);
}
function addCountBadge(trigger) {
const dashboard = triggerDashboard(trigger);
const section = triggerSection(trigger);
const count = entriesFor(dashboard, section).length;
if (!count) {
trigger.querySelector(":scope > .ucc-tab-visual-count")?.remove();
trigger.removeAttribute("aria-haspopup");
return;
}
let badge = trigger.querySelector(":scope > .ucc-tab-visual-count");
if (!badge) {
badge = document.createElement("span");
badge.className = "ucc-tab-visual-count";
badge.setAttribute("aria-hidden", "true");
trigger.appendChild(badge);
}
badge.textContent = String(count);
trigger.title = count + " visual" + (count === 1 ? "" : "s") + " in this section";
trigger.setAttribute("aria-haspopup", "true");
trigger.setAttribute("aria-expanded", "false");
}
function bindTabs() {
directTabTriggers().forEach(trigger => {
addCountBadge(trigger);
if (trigger.dataset.visualHoverReady === "1") return;
trigger.dataset.visualHoverReady = "1";
trigger.addEventListener("keydown", event => {
if (event.key === "ArrowDown") {
event.preventDefault();
if (activeTrigger !== trigger || menu.hidden) openMenu(trigger);
setTimeout(() => menuList.querySelector("button")?.focus(), 0);
}
if (event.key === "Escape" && activeTrigger === trigger) closeMenu();
});
trigger.addEventListener("click", () => {
if (suppressNextTabMenu) { suppressNextTabMenu = false; return; }
setTimeout(() => toggleMenu(trigger), 0);
});
});
Object.keys(expectedCounts).forEach(dashboard => {
const countNode = platform.querySelector('[data-ucc-explore-count="' + dashboard + '"]');
if (countNode) countNode.textContent = String(registry().filter(entry => entry.dashboard === dashboard).length);
});
}

menu.addEventListener("click", event => {
const entryButton = event.target.closest("[data-visual-entry]");
if (entryButton) {
global.UCCExplore?.openEntry(entryButton.dataset.visualEntry);
closeMenu();
return;
}
if (event.target.closest("[data-visual-menu-section]")) {
const trigger = activeTrigger;
closeMenu();
if (trigger) { suppressNextTabMenu = true; trigger.click(); }
return;
}
if (event.target.closest("[data-visual-menu-all]")) {
global.UCCExplore?.openNavigator(activeDashboard);
closeMenu();
return;
}
if (event.target.closest("[data-ucc-open-mapping]")) {
event.preventDefault();
event.stopPropagation();
const dashboard = activeDashboard;
closeMenu();
openSourceMapping(dashboard);
return;
}
});
// The panel is in-flow (not floating), so it never overlaps neighbouring
// content: an outside click no longer needs to close it. The panel only
// ever closes by clicking its own (now-active) tab again, or switches by
// clicking a different tab -- both handled by toggleMenu() above.
document.addEventListener("keydown", event => { if (event.key === "Escape") { closeMenu(); closeSourceMapping(); } });

const mappingDialog = document.createElement("section");
mappingDialog.className = "ucc-source-mapping-dialog";
mappingDialog.hidden = true;
mappingDialog.setAttribute("role", "dialog");
mappingDialog.setAttribute("aria-modal", "true");
mappingDialog.setAttribute("aria-label", "Source mapping report");
mappingDialog.innerHTML = '<div class="ucc-source-mapping-card"><header><div><h2>Source Mapping Report</h2><p>Installed DocTypes, readable fallbacks, metadata, detected fields and visual rendering issues for the signed-in user.</p></div><div class="ucc-source-mapping-actions"><button type="button" data-source-mapping-copy>Copy report</button><button type="button" data-source-mapping-close aria-label="Close">×</button></div></header><div class="ucc-source-mapping-body" data-source-mapping-body><div class="ucc-visual-diagnostic"><strong>Loading source diagnostics…</strong><span>The report checks only approved UCC source candidates.</span></div></div></div>';
platform.appendChild(mappingDialog);
const mappingBody = mappingDialog.querySelector("[data-source-mapping-body]");

function statusClass(status) {
if (["available", "resolved"].includes(status)) return "ucc-source-status-good";
if (["fallback", "permission_denied", "field_mismatch"].includes(status)) return "ucc-source-status-warning";
return "ucc-source-status-risk";
}
function visualCountSummary() {
return Object.keys(expectedCounts).map(dashboard => {
const actual = registry().filter(entry => entry.dashboard === dashboard).length;
return { dashboard, actual, expected: expectedCounts[dashboard], status: actual === expectedCounts[dashboard] ? "available" : "count_mismatch" };
});
}
function normaliseSourceRows(result) {
const groups = Array.isArray(result?.source_groups) ? result.source_groups : [];
if (groups.length) return groups;
return (result?.sources || []).map(source => ({
key: source.key || source.doctype,
label: source.label || source.doctype,
candidates: source.candidates || [source.doctype],
resolved_doctype: source.resolved_doctype || (source.readable ? source.doctype : ""),
status: source.status || (source.readable ? "available" : source.exists ? "permission_denied" : "unavailable"),
detail: source.detail || source.error || "",
attempts: source.attempts || []
}));
}
function renderMapping(result) {
lastMappingResult = result || {};
const rows = normaliseSourceRows(result);
const countRows = visualCountSummary();
const unresolved = rows.filter(row => !["available", "fallback", "resolved"].includes(row.status)).length;
const fallbacks = rows.filter(row => row.status === "fallback").length;
const issueRows = issues.slice(-50);
mappingBody.innerHTML = `
<div class="ucc-source-mapping-summary">
<span>${rows.length} approved source groups</span>
<span>${unresolved} unresolved</span>
<span>${fallbacks} fallbacks used</span>
<span>${issueRows.length} visual issues detected</span>
</div>
<h3>Visual catalogue</h3>
<div class="table-wrap"><table><thead><tr><th>Criterion</th><th>Expected</th><th>Detected</th><th>Status</th></tr></thead><tbody>${countRows.map(row => `<tr><td>${esc(criterionLabels[row.dashboard])}</td><td>${row.expected}</td><td>${row.actual}</td><td class="${statusClass(row.status)}">${row.status === "available" ? "Complete" : "Count mismatch"}</td></tr>`).join("")}</tbody></table></div>
<h3>Approved DocType mapping</h3>
<div class="table-wrap"><table><thead><tr><th>Source key</th><th>Approved candidates</th><th>Resolved DocType</th><th>Status</th><th>Detected fields</th><th>Diagnostic detail</th></tr></thead><tbody>${rows.length ? rows.map(row => {
const rowAttempts = row.attempts || [];
const attempts = rowAttempts.map(item => `${item.doctype || "Candidate"}: ${item.status || item.stage || "checked"}${item.message ? " (" + item.message + ")" : ""}`).join("; ");
const resolvedAttempt = rowAttempts.find(item => item.doctype === row.resolved_doctype) || rowAttempts.find(item => (item.fields || []).length) || {};
const detectedFields = Array.isArray(resolvedAttempt.fields) ? resolvedAttempt.fields : [];
const fieldCount = Number(resolvedAttempt.field_count || detectedFields.length || 0);
const fieldCell = fieldCount
? `<details class="ucc-source-field-list"><summary>${fieldCount} fields</summary><small>${esc(detectedFields.join(", ") || "Field names were not returned")}</small></details>`
: "No fields detected";
return `<tr><td>${esc(row.label || row.key)}</td><td>${esc((row.candidates || []).join(" → "))}</td><td>${esc(row.resolved_doctype || row.doctype || "Not resolved")}</td><td class="${statusClass(row.status)}">${esc(row.status || "unknown")}</td><td>${fieldCell}</td><td>${esc(row.detail || row.message || attempts || "No additional detail")}</td></tr>`;
}).join("") : '<tr><td colspan="6">No source diagnostics were returned.</td></tr>'}</tbody></table></div>
<h3>Visual rendering issues in this browser session</h3>
<div class="table-wrap"><table><thead><tr><th>Time</th><th>Criterion</th><th>Section</th><th>Visual</th><th>Reason</th></tr></thead><tbody>${issueRows.length ? issueRows.map(row => `<tr><td>${esc(row.time)}</td><td>${esc(row.dashboard)}</td><td>${esc(row.panel)}</td><td>${esc(row.visual)}</td><td>${esc(row.reason)}</td></tr>`).join("") : '<tr><td colspan="5">No invalid or blank visual has been detected in the current browser session.</td></tr>'}</tbody></table></div>`;
}
function renderMappingError(error) {
lastMappingResult = null;
mappingBody.innerHTML = '<div class="ucc-visual-diagnostic"><strong>Source diagnostics could not be loaded</strong><span>' + esc(error?.message || error || "Unknown API error") + '</span></div>';
}
function openSourceMapping(dashboard) {
lastMappingResult = null;
mappingDialog.hidden = false;
mappingBody.innerHTML = '<div class="ucc-visual-diagnostic"><strong>Loading source diagnostics…</strong><span>Checking approved DocType candidates, metadata access and current-user readability.</span></div>';
if (!(global.frappe && typeof frappe.call === "function")) {
renderMappingError("frappe.call is unavailable on this page.");
return;
}
frappe.call({
method: "ucc_shared_diagnostics",
args: { payload: JSON.stringify({ dashboard: dashboard || "" }) },
callback: response => renderMapping(response?.message || response || {}),
error: error => renderMappingError(error)
});
}
function closeSourceMapping() {
mappingDialog.hidden = true;
}
function copySourceMapping() {
if (!lastMappingResult) {
notify("The source mapping report has not finished loading.", "orange");
return;
}
const report = JSON.stringify({
platform_version: "1.9.6",
source_mapping: lastMappingResult,
visual_catalogue: visualCountSummary(),
visual_issues: issues.slice()
}, null, 2);
const task = navigator.clipboard?.writeText
? navigator.clipboard.writeText(report)
: Promise.reject(new Error("Clipboard unavailable"));
task.then(() => notify("Source mapping report copied.", "green"))
.catch(() => window.prompt("Copy the source mapping report", report));
}
mappingDialog.addEventListener("click", event => {
if (event.target.closest("[data-source-mapping-copy]")) {
event.preventDefault();
copySourceMapping();
return;
}
if (event.target === mappingDialog || event.target.closest("[data-source-mapping-close]")) closeSourceMapping();
});
platform.addEventListener("ucc:open-source-mapping", event => openSourceMapping(event.detail?.dashboard || ""));
platform.addEventListener("click", event => {
const button = event.target.closest("[data-ucc-open-mapping]");
if (!button || button.closest(".ucc-visual-hover-menu")) return;
event.preventDefault();
event.stopPropagation();
openSourceMapping(button.closest("[data-dashboard-panel]")?.dataset.dashboardPanel || button.closest("[data-demo-dashboard]")?.dataset.demoDashboard || "");
});

function visualIdentity(node) {
return node.dataset.c4Visual || node.dataset.c4ExpandedChart || node.dataset.chart || node.dataset.demoChart || "unknown-visual";
}
function visualPanel(node) {
return node.closest("[data-c4-panel]")?.dataset.c4Panel || node.closest("[data-panel]")?.dataset.panel || node.closest("[data-demo-panel]")?.dataset.demoPanel || "overview";
}
function visualDashboard(node) {
return node.closest("[data-dashboard-panel]")?.dataset.dashboardPanel || "unknown";
}
function recordIssue(node, reason) {
const signature = visualDashboard(node) + "|" + visualPanel(node) + "|" + visualIdentity(node) + "|" + reason;
if (issues.some(item => item.signature === signature)) return;
issues.push({
signature,
time: new Date().toISOString(),
dashboard: visualDashboard(node),
panel: visualPanel(node),
visual: visualIdentity(node),
reason
});
}
function diagnosticMarkup(reason) {
return '<div class="ucc-visual-diagnostic"><strong>Visual could not be rendered</strong><span>' + esc(reason) + ' Open Source Mapping Report to see missing DocTypes, permissions, candidate fallbacks and field checks.</span><button type="button" data-ucc-open-mapping>Source mapping report</button></div>';
}
function invalidSvgReason(node) {
const candidates = node.querySelectorAll("svg [d],svg [points],svg [transform],svg [x],svg [y],svg [cx],svg [cy],svg [r],svg [width],svg [height]");
for (const element of candidates) {
for (const attribute of element.getAttributeNames()) {
const value = element.getAttribute(attribute) || "";
if (/NaN|undefined|Infinity/i.test(value)) return "Invalid SVG " + attribute + '="' + value.slice(0, 120) + '".';
}
}
return "";
}
function isLoading(node) {
const dashboard = node.closest("[data-demo-dashboard],[data-dashboard-panel]");
const liveOverlay = dashboard?.querySelector("[data-demo-loading-overlay]:not(.hidden),[data-loading-overlay]:not(.hidden)");
return Boolean(liveOverlay || node.querySelector(".ucc-c4-visual-loading,.loading,.spinner,[data-loading]"));
}
function meaningfulVisual(node) {
if (node.querySelector("svg,canvas,img,.ucc-demo-bars,.ucc-live-empty,.empty-state,.ucc-visual-diagnostic")) return true;
return clean(node.textContent).length > 12;
}
function scanVisuals() {
const now = Date.now();
platform.querySelectorAll("[data-c4-visual],[data-c4-expanded-chart],[data-chart],[data-demo-chart]").forEach(node => {
if (!node.isConnected || node.getClientRects().length === 0 || isLoading(node)) return;
const invalid = invalidSvgReason(node);
if (invalid) {
recordIssue(node, invalid);
node.dataset.visualGuardReplaced = "invalid-svg";
node.innerHTML = diagnosticMarkup(invalid);
return;
}
if (meaningfulVisual(node)) {
blankFirstSeen.delete(node);
return;
}
const firstSeen = blankFirstSeen.get(node) || now;
blankFirstSeen.set(node, firstSeen);
if (now - firstSeen < 20000) return;
const reason = "The diagram area remained blank after the section finished loading.";
recordIssue(node, reason);
node.dataset.visualGuardReplaced = "blank";
node.innerHTML = diagnosticMarkup(reason);
});
}

bindTabs();
setTimeout(bindTabs, 300);
setTimeout(scanVisuals, 1800);
setInterval(scanVisuals, 3500);
platform.addEventListener("click", event => {
if (event.target.closest("[data-demo-tab],[data-c4-tab],[data-tab],[data-demo-view],[data-c4-card-view],[data-card-view]")) {
setTimeout(bindTabs, 120);
setTimeout(scanVisuals, 1200);
}
});

const observer = new MutationObserver(mutations => {
if (mutations.some(mutation => mutation.addedNodes.length)) {
setTimeout(bindTabs, 80);
setTimeout(scanVisuals, 900);
}
});
observer.observe(platform, { childList: true, subtree: true });

global.UCCVisualDiagnostics = Object.freeze({
issues: () => issues.slice(),
scan: scanVisuals,
openSourceMapping,
expectedCounts
});
})(window);
