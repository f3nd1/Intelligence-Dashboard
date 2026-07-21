/* UCC SHARED RUNTIME v1.7.0 */
(function (global) {
"use strict";
if (global.UCCShared) return;

function escapeHtml(value) {
const div = document.createElement("div");
div.textContent = value == null ? "" : String(value);
return div.innerHTML;
}

function csvCell(value) {
return `"${String(value == null ? "" : value)
      .replace(/"/g, '""')
      .replace(/\s+/g, " ")
      .trim()}"`;
}

function tableToCsv(table) {
return Array.from(table.querySelectorAll("tr"))
.map(row =>
Array.from(row.querySelectorAll("th,td"))
.map(cell => csvCell(cell.innerText))
.join(",")
)
.join("\n");
}

function download(name, content, type) {
const mime = type || "text/csv;charset=utf-8";
const blob = new Blob(["\ufeff", content], { type: mime });
const url = URL.createObjectURL(blob);
const anchor = document.createElement("a");
anchor.href = url;
anchor.download = name;
document.body.appendChild(anchor);
anchor.click();
anchor.remove();
URL.revokeObjectURL(url);
}

function doctypeRoute(doctype) {
if (!doctype) return "#";
let slug = "";
if (
global.frappe &&
frappe.router &&
typeof frappe.router.slug === "function"
) {
slug = frappe.router.slug(doctype);
} else {
slug = String(doctype)
.trim()
.toLowerCase()
.replace(/[^a-z0-9]+/g, "-")
.replace(/^-+|-+$/g, "");
}
return "/app/" + slug;
}

function openDoctype(doctype) {
if (!doctype) return;
global.open(doctypeRoute(doctype), "_blank", "noopener,noreferrer");
}

function readStorage(key, fallback) {
try {
const value = localStorage.getItem(key);
return value == null ? fallback : value;
} catch (error) {
return fallback;
}
}

function writeStorage(key, value) {
try {
localStorage.setItem(key, value);
} catch (error) {}
}

global.UCCShared = Object.freeze({
escapeHtml,
csvCell,
tableToCsv,
download,
doctypeRoute,
openDoctype,
readStorage,
writeStorage
});
})(window);
// Consolidates a dashboard's separate "Data Quality" and "Sources" tabs into a
// single "Sources & Data Quality" tab: the Data Quality panel's content is moved
// into the Sources panel and the Data Quality tab button is removed. Shared by
// all three dashboard architectures (demo/C4/C5) via their own tab attributes.
window.__uccMergeSourcesQuality=function(dash,tabAttr,panelAttr){
if(!dash||dash.dataset.sqMerged==="1")return;
const sourcesTab=dash.querySelector(`[${tabAttr}="sources"]`),qualityTab=dash.querySelector(`[${tabAttr}="quality"]`);
const sourcesPanel=dash.querySelector(`[${panelAttr}="sources"]`),qualityPanel=dash.querySelector(`[${panelAttr}="quality"]`);
if(!sourcesTab||!sourcesPanel)return;
dash.dataset.sqMerged="1";
sourcesTab.textContent="Sources & Data Quality";
if(qualityPanel){while(qualityPanel.firstChild)sourcesPanel.appendChild(qualityPanel.firstChild);qualityPanel.remove();}
if(qualityTab)qualityTab.remove();
};
(function () {
"use strict";
const root = typeof root_element !== "undefined"
? root_element.querySelector("#uccIntelligencePlatform")
: document.querySelector("#uccIntelligencePlatform");
if (!root || root.dataset.platformReady === "1") {
return;
}
root.dataset.platformReady = "1";
const workspaceButtons = Array.from(
root.querySelectorAll("[data-ucc-workspace]")
);
const workspacePanels = Array.from(
root.querySelectorAll("[data-ucc-workspace-panel]")
);
const dashboardControl = root.querySelector("[data-ucc-dashboard-control]");
const status = root.querySelector("[data-ucc-platform-status]");
const dashboardSelect = root.querySelector("#uccDashboardSelect");
function setWorkspace(workspace) {
workspaceButtons.forEach(function (button) {
const active = button.dataset.uccWorkspace === workspace;
button.classList.toggle("is-active", active);
button.setAttribute("aria-pressed", active ? "true" : "false");
});
workspacePanels.forEach(function (panel) {
panel.hidden = panel.dataset.uccWorkspacePanel !== workspace;
});
if (dashboardControl) {
dashboardControl.hidden = workspace !== "analytics" && workspace !== "explore";
}
if (status) {
if (workspace === "analytics") {
status.textContent = "Analytics is active. Criteria 1–7 now use permission-aware live sources or live API foundations; unavailable fields are shown explicitly.";
} else if (workspace === "explore") {
status.textContent = "Explore is active. Search the visual catalogue and open the original live diagram in one click.";
} else {
status.textContent = "Ask UCC is active. Choose the assistant and record first; guided questions work without OpenAI.";
}
}
}
workspaceButtons.forEach(function (button) {
button.addEventListener("click", function () {
setWorkspace(button.dataset.uccWorkspace);
});
});
const dashboardPanels = Array.from(root.querySelectorAll("[data-dashboard-panel]"));
const shell = root.querySelector(".ucc-platform-shell");
const shellToggle = root.querySelector("[data-shell-toggle]");
const shellToggleIcon = root.querySelector("[data-shell-toggle-icon]");
const shellToggleLabel = root.querySelector("[data-shell-toggle-label]");
const CRITERION_LABELS = Object.freeze({"criterion_1": "Criterion 1 · Leadership and Strategic Planning", "criterion_2": "Criterion 2 · Corporate Administration", "criterion_3": "Criterion 3 · External Recruitment Agents", "criterion_4": "Criterion 4 · Student Protection and Support Services", "criterion_5": "Criterion 5 · Academic Systems and Processes", "criterion_6": "Criterion 6 · Quality Assurance, Innovation and Continual Improvement", "criterion_7": "Criterion 7 · Performance Outcomes"});
let shellCollapsed = false;

function activeWorkspaceName() {
const active = workspaceButtons.find(function (button) { return button.classList.contains("is-active"); });
return active ? active.dataset.uccWorkspace : "analytics";
}
function scrollDashboardToTop(dashboard) {
const panel = dashboardPanels.find(function (item) { return item.dataset.dashboardPanel === dashboard; });
const target = panel ? (panel.querySelector(".hero") || panel) : root;
requestAnimationFrame(function () {
try {
target.scrollIntoView({ behavior: "smooth", block: "start", inline: "nearest" });
} catch (error) {
try { target.scrollIntoView(true); } catch (ignored) {}
}
let current = root.parentElement;
while (current && current !== document.body) {
const style = window.getComputedStyle(current);
const scrollable = /(auto|scroll)/.test(style.overflowY || "") && current.scrollHeight > current.clientHeight;
if (scrollable) {
const top = Math.max(0, target.getBoundingClientRect().top - current.getBoundingClientRect().top + current.scrollTop - 12);
try { current.scrollTo({ top: top, behavior: "smooth" }); } catch (error) { current.scrollTop = top; }
break;
}
current = current.parentElement;
}
});
}
function setDashboard(dashboard) {
dashboardPanels.forEach(function (panel) { panel.classList.toggle("ucc-hidden", panel.dataset.dashboardPanel !== dashboard); });
if (dashboardSelect && dashboardSelect.value !== dashboard) dashboardSelect.value = dashboard;
if (status) {
const workspace = activeWorkspaceName();
if (workspace === "explore") status.textContent = "Explore is active. Search the live visual catalogue for the selected criterion.";
else if (workspace === "ask") status.textContent = "Ask UCC is active. Choose the assistant and record first.";
else {
const label = CRITERION_LABELS[dashboard] || dashboard;
const fullLive = dashboard === "criterion_4" || dashboard === "criterion_5";
status.textContent = fullLive
? label + " is active with mature live, permission-aware analytics."
: label + " is active with a permission-aware live API foundation. Unsupported fields are shown explicitly.";
}
}
try { localStorage.setItem("ucc.dashboard", dashboard); } catch (error) {}
scrollDashboardToTop(dashboard);
try { root.dispatchEvent(new CustomEvent("ucc:dashboard-change", { detail: { dashboard: dashboard } })); } catch (error) {}
}
if (dashboardSelect) dashboardSelect.addEventListener("change", function () { setDashboard(dashboardSelect.value); });
function applyShellState() {
if (!shell || !shellToggle) return;
shell.classList.toggle("is-collapsed", shellCollapsed);
shellToggle.setAttribute("aria-expanded", shellCollapsed ? "false" : "true");
shellToggle.setAttribute("aria-label", shellCollapsed ? "Expand UCC navigation" : "Minimise UCC navigation");
shellToggle.setAttribute("title", shellCollapsed ? "Expand navigation" : "Minimise navigation");
if (shellToggleIcon) shellToggleIcon.textContent = shellCollapsed ? "›" : "‹";
if (shellToggleLabel) shellToggleLabel.textContent = shellCollapsed ? "Expand navigation" : "Minimise navigation";
}
let shellPlaceholder = null;
function frappeTopOffset() {
const navbar = document.querySelector(".navbar.navbar-expand, header.navbar, .desk-navbar, .navbar");
if (!navbar) return 8;
const rect = navbar.getBoundingClientRect();
return rect.bottom > 0 ? Math.max(8, Math.round(rect.bottom + 8)) : 8;
}
function syncFloatingShell() {
if (!shell || !root.isConnected) return;
if (!shellPlaceholder) {
shellPlaceholder = document.createElement("div");
shellPlaceholder.className = "ucc-platform-shell-placeholder";
shell.parentNode.insertBefore(shellPlaceholder, shell);
}
const top = frappeTopOffset();
const rootRect = root.getBoundingClientRect();
const anchorRect = shellPlaceholder.getBoundingClientRect();
const shellHeight = Math.max(58, Math.round(shell.getBoundingClientRect().height || shell.offsetHeight || 58));
const shouldFloat = anchorRect.top <= top && rootRect.bottom > top + shellHeight + 16;
shell.classList.toggle("is-floating", shouldFloat);
root.classList.toggle("has-floating-shell", shouldFloat);
root.style.setProperty("--ucc-dashboard-sticky-top", String(top + shellHeight + 10) + "px");
if (shouldFloat) {
const width = shellCollapsed ? Math.min(108, rootRect.width) : Math.min(1500, rootRect.width);
const left = shellCollapsed ? rootRect.left : rootRect.left + Math.max(0, (rootRect.width - width) / 2);
shell.style.setProperty("--ucc-shell-floating-top", String(top) + "px");
shell.style.setProperty("--ucc-shell-floating-left", String(Math.round(left)) + "px");
shell.style.setProperty("--ucc-shell-floating-width", String(Math.round(width)) + "px");
shellPlaceholder.style.height = String(shellHeight + 10) + "px";
} else {
shell.style.removeProperty("--ucc-shell-floating-top");
shell.style.removeProperty("--ucc-shell-floating-left");
shell.style.removeProperty("--ucc-shell-floating-width");
shellPlaceholder.style.height = "0px";
}
}
if (shellToggle) shellToggle.addEventListener("click", function (event) {
event.preventDefault();
event.stopPropagation();
shellCollapsed = !shellCollapsed;
applyShellState();
requestAnimationFrame(syncFloatingShell);
});
let savedDashboard = "criterion_5";
try { savedDashboard = localStorage.getItem("ucc.dashboard") || savedDashboard; } catch (error) {}
try {
const urlDashboard = new URLSearchParams(location.search).get("dashboard");
if (urlDashboard) savedDashboard = urlDashboard;
} catch (error) {}
if (!["criterion_1", "criterion_2", "criterion_3", "criterion_4", "criterion_5", "criterion_6", "criterion_7"].includes(savedDashboard)) savedDashboard = "criterion_5";
setWorkspace("analytics");
setDashboard(savedDashboard);
applyShellState();
requestAnimationFrame(syncFloatingShell);
document.addEventListener("scroll", syncFloatingShell, true);
window.addEventListener("resize", syncFloatingShell);
if (typeof ResizeObserver !== "undefined") {
const shellResizeObserver = new ResizeObserver(syncFloatingShell);
shellResizeObserver.observe(root);
shellResizeObserver.observe(shell);
}
})();
(function(){
"use strict";
const root=typeof root_element!=="undefined"?root_element.querySelector(".ucc-c5-v41"):document.querySelector(".ucc-c5-v41");
if(!root||root.dataset.c5FoundationReady==="1")return;
root.dataset.c5FoundationReady="1";
root.dataset.demoDashboard="criterion_5";
root.dataset.demoActiveTab="overview";
const sections=[
["overview","Overview"],
["5.1.1","5.1.1 Course Design & Development"],
["5.1.2","5.1.2 Course Review"],
["5.2.1","5.2.1 Course Planning"],
["5.2.2","5.2.2 Course Delivery"],
["5.3.1","5.3.1 Partnerships"],
["5.4","5.4 Student Feedback & Learning Support"],
["5.5","5.5 Assessment"],
["quality","Data Quality"],
["sources","Sources"]
];
function qaTable(){return '<div class="table-wrap"><table class="qa-table"><thead><tr><th>Section</th><th>Management question</th><th>Live answer</th><th>Source</th><th>Status</th></tr></thead><tbody data-demo-qa></tbody></table></div>';}
function panel(key,title){
if(key==="quality")return '<section class="panel ucc-shared-panel hidden" data-demo-panel="quality"><div class="section-heading"><div><span>Criterion 5 assurance</span><h2>Data Quality</h2></div><small>Unsupported fields and unavailable sources are reported explicitly.</small></div><div class="table-wrap"><table><thead><tr><th>Check</th><th>Source</th><th>Status</th><th>Detail</th></tr></thead><tbody data-demo-quality="criterion_5"></tbody></table></div></section>';
if(key==="sources")return '<section class="panel ucc-shared-panel hidden" data-demo-panel="sources"><div class="section-heading"><div><span>Criterion 5 assurance</span><h2>Sources</h2></div><small>Resolved against the signed-in user\'s permissions.</small></div><div class="table-wrap"><table><thead><tr><th>Resolved DocType</th><th>Source key</th><th>Status</th><th>Records</th></tr></thead><tbody data-demo-sources="criterion_5"></tbody></table></div></section>';
return '<section class="panel ucc-shared-panel '+(key==="overview"?'':'hidden')+'" data-demo-panel="'+key+'"><div class="section-heading"><div><span>'+(key==="overview"?'EduTrust Criterion 5':'Subcriterion '+key)+'</span><h2>'+title+'</h2></div><small>Permission-aware live evidence and management questions</small></div><div class="ucc-section-visual-anchor" data-c5-visual-anchor="'+key+'"></div><h2 class="ucc-management-heading">Management Questions and Data-Based Answers</h2>'+qaTable()+'</section>';
}
const panels=sections.map(function(item){return panel(item[0],item[1]);}).join("");
const menu='<nav class="tabs ucc-shared-tabs ucc-c5-hierarchical-tabs" aria-label="Criterion 5 sections">'
+'<button type="button" class="active" data-demo-tab="overview">Overview</button>'
+'<button type="button" data-demo-tab="5.1.1">5.1.1</button>'
+'<button type="button" data-demo-tab="5.1.2">5.1.2</button>'
+'<button type="button" data-demo-tab="5.2.1">5.2.1</button>'
+'<button type="button" data-demo-tab="5.2.2">5.2.2</button>'
+'<button type="button" data-demo-tab="5.3.1">5.3.1</button>'
+'<button type="button" data-demo-tab="5.4">5.4 Student Learning</button>'
+'<button type="button" data-demo-tab="5.5">5.5 Assessment</button>'
+'<button type="button" data-demo-tab="quality" hidden>Data Quality</button>'
+'<button type="button" data-demo-tab="sources">Sources & Data Quality</button>'
+'</nav>';
const controls='<section class="controls ucc-shared-controls"><div class="control-grid ucc-c5-filter-grid">'
+'<div><label for="uccC5AcademicYear">Academic Year</label><input id="uccC5AcademicYear" data-demo-filter="year" type="text" placeholder="All academic years"></div>'
+'<div><label for="uccC5ModuleClass">Module Class Details</label><input id="uccC5ModuleClass" data-demo-filter="student_group" type="text" placeholder="All module classes"></div>'
+'<div><label for="uccC5Course">Course</label><input id="uccC5Course" data-demo-filter="program" type="text" placeholder="All courses"></div>'
+'<div><label for="uccC5Status">Status</label><input id="uccC5Status" data-demo-filter="status" type="text" placeholder="All statuses"></div>'
+'</div></section>';
root.innerHTML='<div class="ucc-c5-foundation"><header class="hero ucc-shared-hero"><div class="hero-copy"><span class="ucc-criterion-kicker">EDUTRUST CRITERION 5</span><h1>Criterion 5 · Academic Systems and Processes</h1><p>Live, permission-aware ERPNext/Frappe analytics for course design, review, planning, delivery, partnerships, feedback and assessment.</p></div><div aria-label="Criterion 5 analytics actions" class="hero-action-card ucc-shared-action-card"><button type="button" class="primary-btn" data-demo-action="refresh">Refresh</button><button type="button" data-demo-action="export-qa">Export Q&A CSV</button><button type="button" data-demo-action="export-exceptions">Export Exceptions CSV</button><button type="button" data-demo-action="diagnostics">Diagnostics Log (<span data-demo-log-count>0</span>)</button><div class="ucc-hero-tools" data-ucc-tools><button type="button" class="ucc-hero-tools-trigger" data-ucc-tools-trigger aria-expanded="false">View tools <span aria-hidden="true">▾</span></button><div class="ucc-hero-tools-menu" data-ucc-tools-menu hidden><button type="button" data-ucc-tool-action="export-current">Export current table</button><button type="button" data-ucc-tool-action="export-exceptions">Export exception list</button><button type="button" data-ucc-tool-action="copy-link">Copy filtered link</button></div></div></div></header><div class="sticky-navigation">'+controls+menu+'</div><div class="ucc-criterion-notice ucc-readiness-strip" data-status="loading"><div class="ucc-criterion-notice-copy"><strong data-demo-readiness-title>Loading Criterion 5 analytics…</strong><span data-demo-readiness-copy>Current-user permissions and the selected section are being checked.</span></div></div><section class="kpis ucc-shared-kpis" data-demo-kpis></section><div class="ucc-c5-panel-stack">'+panels+'</div><div class="loading-overlay hidden" data-demo-loading-overlay><div class="loading-card"><div class="spinner"></div><strong data-demo-loading-title>Loading Criterion 5</strong><div class="progress-track"><div class="progress-fill" data-demo-progress-fill></div></div><div class="progress-text"><span data-demo-progress-value>0%</span> · Permission-aware sources</div></div></div></div>';
})();
(function () {
"use strict";
const root = typeof root_element !== "undefined" ? root_element : document;
const app = root ? root.querySelector("#ajaApp") : null;
if (!app || app.dataset.admissionJourneyReady === "1") {
return;
}
app.dataset.admissionJourneyReady = "1";
const MODULE_CONFIG = {
student_journey: {
label: "Student Journey",
apiMethod: "ucc_ask_student_journey",
entityLabel: "student",
entityLabelTitle: "Student",
pinnedLabel: "Pinned student",
findLabel: "Find student",
recentLabel: "Recent students",
searchPlaceholder: "Type name or Applicant ID",
headerTitle: "Ask UCC · Student Journey",
headerSubtitle: "Ask about students, courses, modules, assessments, classes, leave and graduation.",
comingSoon: false
},
recruitment_agent: {
label: "Recruitment Agent",
apiMethod: "ucc_ask_recruitment_agent",
entityLabel: "agent",
entityLabelTitle: "Recruitment Agent",
pinnedLabel: "Pinned agent",
findLabel: "Find recruitment agent",
recentLabel: "Recent agents",
searchPlaceholder: "Type agent, company or contract ID",
headerTitle: "Ask UCC · Recruitment Agent",
headerSubtitle: "Ask about agent profiles, contracts, expiry, recruitment performance, ratings and renewal.",
comingSoon: false
},
quality_action: {
label: "Quality Action",
apiMethod: "ucc_ask_quality_action",
entityLabel: "quality action",
entityLabelTitle: "Quality Action",
pinnedLabel: "Pinned Quality Action",
findLabel: "Find Quality Action",
recentLabel: "Recent Quality Actions",
searchPlaceholder: "Type Quality Action ID or subject",
headerTitle: "Ask UCC · Quality Action",
headerSubtitle: "Ask about findings, root causes, actions, assignments, due dates, closure readiness and quality review.",
comingSoon: false
},
hr_assistant: {
label: "HR",
entityLabel: "employee",
entityLabelTitle: "Employee",
comingSoon: true
}
};
function activeModuleConfig() {
return MODULE_CONFIG[state.activeModule] || MODULE_CONFIG.student_journey;
}
const moduleSelect = root.querySelector("#ajaModuleSelect");
const moduleStatus = root.querySelector("#ajaModuleStatus");
const pinnedLabel = root.querySelector("#ajaPinnedLabel");
const findLabel = root.querySelector("#ajaFindLabel");
const recentLabel = root.querySelector("#ajaRecentLabel");
const headerTitle = root.querySelector("#ajaHeaderTitle");
const headerSubtitle = root.querySelector("#ajaHeaderSubtitle");
const comingSoon = root.querySelector("#ajaComingSoon");
const chat = root.querySelector("#ajaChat");
const questionInput = root.querySelector("#ajaQuestion");
const sendButton = root.querySelector("#ajaSend");
const printButton = root.querySelector("#ajaPrint");
const statusElement = root.querySelector("#ajaStatus");
const currentStudentElement = root.querySelector("#ajaCurrentStudent .aja-current-value");
const suggestionsContainer = root.querySelector("#ajaSuggestions");
const categorySelect = root.querySelector("#ajaQuestionCategory");
const categoryButtons = root.querySelector("#ajaQuestionCategoryButtons");
const clearChatButton = root.querySelector("#ajaClearChat");
const controlledQuestions = root.querySelector("#ajaControlledQuestions");
const studentSearch = root.querySelector("#ajaStudentSearch");
const studentMatches = root.querySelector("#ajaStudentMatches");
const studentPager = root.querySelector("#ajaStudentPager");
const courseFilter = root.querySelector("#ajaCourseFilter");
const recentStudents = root.querySelector("#ajaRecentStudents");
const changeStudentButton = root.querySelector("#ajaChangeStudent");
const resetContextButton = root.querySelector("#ajaResetContext");
const exportCsvButton = root.querySelector("#ajaExportCsv");
const diagnosticsButton = root.querySelector("#ajaDiagnostics");
const apiButton = root.querySelector("#ajaApiButton");
const apiModal = root.querySelector("#ajaApiModal");
const apiKeyInput = root.querySelector("#ajaApiKeyInput");
const apiCancel = root.querySelector("#ajaApiCancel");
const apiSkip = root.querySelector("#ajaApiSkip");
const apiConnect = root.querySelector("#ajaApiConnect");
let pendingFreeQuestion = "";
const state = {
activeModule: "student_journey",
moduleRecords: null,
loading: false,
studentApplicant: "",
studentName: "",
history: [],
studentRollRows: null,
lastQuestion: "",
recentStudents: [],
lastResult: null,
lastVisualRows: [],
lastExportSections: [],
searchPage: 1,
searchPageSize: 8
};
function safeArray(value) {
return Array.isArray(value) ? value : [];
}
function cleanText(value) {
return String(value === null || value === undefined ? "" : value)
.replace(/\s+/g, " ")
.trim();
}
function formatDate(value) {
if (!value) return "";
const text = String(value).trim();
let match = text.match(/^(\d{4})-(\d{2})-(\d{2})(?:[ T].*)?$/);
if (!match) {
match = text.match(/^(\d{1,2})[-\/]([0-9]{1,2})[-\/](\d{4})$/);
if (!match) return text;
const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
return String(Number(match[1])).padStart(2, "0") + " " + months[Number(match[2]) - 1] + " " + match[3];
}
const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
return String(Number(match[3])).padStart(2, "0") + " " + months[Number(match[2]) - 1] + " " + match[1];
}
function formatDatesInText(value) {
return String(value === null || value === undefined ? "" : value).replace(
/\b(\d{4}-\d{2}-\d{2})(?:[T ][0-9:.+-Z]+)?\b/g,
function (matched) {
return formatDate(matched.slice(0, 10));
}
);
}
function displayValue(value) {
if (value === null || value === undefined || value === "") {
return "Not recorded";
}
if (value && typeof value === "object" && !Array.isArray(value)) {
return formatDatesInText(
value.text || value.label || value.name || "Not recorded"
);
}
if (typeof value === "string") {
return formatDatesInText(value);
}
return String(value);
}
function setStatus(text, loading) {
if (statusElement) {
statusElement.textContent = text || "Ready";
}
const catStatus = root.querySelector("#ajaCatStatus");
if (catStatus) {
catStatus.classList.toggle("is-working", Boolean(loading));
}
}
function updateSuggestionState() {
if (!suggestionsContainer) {
return;
}
suggestionsContainer
.querySelectorAll(".aja-suggestion")
.forEach(function (button) {
button.disabled = false;
button.title = state.studentApplicant
? "Ask about " + (state.studentName || state.studentApplicant)
: "Select a student first";
});
}
function updateCurrentStudent() {
if (!currentStudentElement) return;
if (!state.studentApplicant) {
currentStudentElement.textContent = "Not selected";
return;
}
currentStudentElement.textContent =
(state.studentName || state.studentApplicant) +
" (" + state.studentApplicant + ")";
}
function uniqueStudentsFromRoll() {
if (state.activeModule === "recruitment_agent") {
return safeArray(state.moduleRecords).map(function (row) {
return {
id: cleanText(row.name),
name: cleanText(row.party_name) || cleanText(row.name),
course: cleanText(row.personal_id) || "Agent Contract"
};
}).filter(function (item) {
return Boolean(item.id);
}).sort(function (a, b) {
return a.name.localeCompare(b.name);
});
}
if (state.activeModule === "quality_action") {
return safeArray(state.moduleRecords).map(function (row) {
return {
id: cleanText(row.name),
name: cleanText(row.custom_subject) || cleanText(row.name),
course: "Quality Action"
};
}).filter(function (item) {
return Boolean(item.id);
}).sort(function (a, b) {
return a.name.localeCompare(b.name);
});
}
const map = new Map();
safeArray(state.studentRollRows).forEach(function (row) {
const id = cleanText(row.student_applicant_id);
const name = cleanText(row.student_name);
if (!id || map.has(id)) return;
map.set(id, {
id: id,
name: name || id,
course: cleanText(row.course)
});
});
return Array.from(map.values()).sort(function (a, b) {
return a.name.localeCompare(b.name);
});
}
function availableCourses() {
const courses = new Set();
if (state.activeModule !== "student_journey") {
return [];
}
safeArray(state.studentRollRows).forEach(function (row) {
const course = cleanText(row.course);
if (course) courses.add(course);
});
return Array.from(courses).sort(function (a, b) {
return a.localeCompare(b);
});
}
function renderCourseFilter() {
if (!courseFilter) return;
const selected = courseFilter.value || "";
courseFilter.innerHTML = '<option value="">All courses</option>';
availableCourses().forEach(function (course) {
const option = document.createElement("option");
option.value = course;
option.textContent = course;
courseFilter.appendChild(option);
});
if (selected && availableCourses().includes(selected)) {
courseFilter.value = selected;
}
}
function rememberStudent(id, name) {
if (!id) return;
state.recentStudents = state.recentStudents.filter(function (item) {
return item.id !== id;
});
state.recentStudents.unshift({ id: id, name: name || id });
state.recentStudents = state.recentStudents.slice(0, 5);
saveRecentStudents();
renderRecentStudents();
}
function loadRecentStudents() {
try {
const value = JSON.parse(
window.localStorage.getItem("uccAiRecent_" + state.activeModule) || "[]"
);
state.recentStudents = Array.isArray(value) ? value : [];
} catch (error) {
state.recentStudents = [];
}
}
function saveRecentStudents() {
try {
window.localStorage.setItem(
"uccAiRecent_" + state.activeModule,
JSON.stringify(state.recentStudents)
);
} catch (error) {
console.warn("Could not save recent students", error);
}
}
function removeRecentStudent(id) {
state.recentStudents = state.recentStudents.filter(function (item) {
return item.id !== id;
});
saveRecentStudents();
renderRecentStudents();
}
function renderRecentStudents() {
if (!recentStudents) return;
recentStudents.innerHTML = "";
state.recentStudents.forEach(function (item) {
const row = document.createElement("div");
row.className = "aja-recent-row";
const button = document.createElement("button");
button.type = "button";
button.className = "aja-recent-button";
button.textContent = item.name;
button.dataset.studentApplicant = item.id;
button.dataset.studentName = item.name;
const remove = document.createElement("button");
remove.type = "button";
remove.className = "aja-recent-remove";
remove.textContent = "×";
remove.title = "Remove from recent students";
remove.setAttribute("aria-label", "Remove " + item.name);
remove.dataset.removeStudent = item.id;
row.appendChild(button);
row.appendChild(remove);
recentStudents.appendChild(row);
});
}
function selectStudent(id, name) {
state.studentApplicant = id || "";
state.studentName = name || id || "";
updateCurrentStudent();
updateSuggestionState();
rememberStudent(state.studentApplicant, state.studentName);
}
function renderStudentMatches(query) {
if (!studentMatches) return;
studentMatches.innerHTML = "";
if (studentPager) {
studentPager.innerHTML = "";
}
const value = cleanText(query).toLowerCase();
const selectedCourse = courseFilter
? cleanText(courseFilter.value)
: "";
if (!value && !selectedCourse) return;
if (state.activeModule === "student_journey" && !state.studentRollRows) {
const loading = document.createElement("div");
loading.className = "aja-search-loading";
loading.textContent = "Loading students...";
studentMatches.appendChild(loading);
return;
}
const filtered = uniqueStudentsFromRoll()
.filter(function (item) {
const matchesText = (
!value
|| item.name.toLowerCase().includes(value)
|| item.id.toLowerCase().includes(value)
);
const matchesCourse = (
state.activeModule !== "student_journey"
|| !selectedCourse
|| cleanText(item.course) === selectedCourse
);
return matchesText && matchesCourse;
});
const total = filtered.length;
const pageSize = state.searchPageSize;
const totalPages = Math.max(1, Math.ceil(total / pageSize));
if (state.searchPage > totalPages) {
state.searchPage = totalPages;
}
const startIndex = (state.searchPage - 1) * pageSize;
const pageItems = filtered.slice(startIndex, startIndex + pageSize);
if (!pageItems.length) {
const empty = document.createElement("div");
empty.className = "aja-search-empty";
empty.textContent = "No matching " + activeModuleConfig().entityLabel + " records.";
studentMatches.appendChild(empty);
}
pageItems.forEach(function (item) {
const button = document.createElement("button");
button.type = "button";
button.className = "aja-student-match";
button.dataset.studentApplicant = item.id;
button.dataset.studentName = item.name;
const strong = document.createElement("strong");
strong.textContent = item.name;
const meta = document.createElement("span");
meta.textContent = item.id + " | " + item.course;
button.appendChild(strong);
button.appendChild(meta);
studentMatches.appendChild(button);
});
if (studentPager && total) {
const count = document.createElement("span");
count.className = "aja-pager-count";
count.textContent =
String(startIndex + 1)
+ "-"
+ String(Math.min(startIndex + pageSize, total))
+ " of "
+ String(total);
const controls = document.createElement("div");
controls.className = "aja-pager-controls";
const prev = document.createElement("button");
prev.type = "button";
prev.className = "aja-pager-button";
prev.textContent = "‹";
prev.disabled = state.searchPage <= 1;
prev.dataset.pageAction = "prev";
const next = document.createElement("button");
next.type = "button";
next.className = "aja-pager-button";
next.textContent = "›";
next.disabled = state.searchPage >= totalPages;
next.dataset.pageAction = "next";
controls.appendChild(prev);
controls.appendChild(next);
studentPager.appendChild(count);
studentPager.appendChild(controls);
}
}
function csvEscape(value) {
const text = String(value === null || value === undefined ? "" : value);
return '"' + text.replace(/"/g, '""') + '"';
}
function exportLastResultCsv() {
const sections = safeArray(state.lastExportSections);
if (!sections.length) {
frappe.show_alert({
message: "Run a question with a table or summary before exporting.",
indicator: "orange"
});
return;
}
const lines = [];
sections.forEach(function (section, sectionIndex) {
if (sectionIndex) lines.push("");
lines.push(csvEscape(section.title || "Admission Journey Export"));
safeArray(section.rows).forEach(function (row) {
lines.push(safeArray(row).map(csvEscape).join(","));
});
});
const csv = "\uFEFF" + lines.join("\r\n");
const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
const url = window.URL.createObjectURL(blob);
const link = document.createElement("a");
const studentPart = cleanText(state.studentName || "cohort")
.replace(/[^a-z0-9]+/gi, "-")
.replace(/^-+|-+$/g, "")
.toLowerCase();
link.style.display = "none";
link.href = url;
link.download = "admission-journey-" + (studentPart || "export") + ".csv";
document.body.appendChild(link);
link.click();
window.setTimeout(function () {
document.body.removeChild(link);
window.URL.revokeObjectURL(url);
}, 1000);
frappe.show_alert({
message: "CSV export prepared.",
indicator: "green"
});
}
function scrollBottom() {
window.requestAnimationFrame(function () {
chat.scrollTop = chat.scrollHeight;
});
}
function addUserMessage(text) {
const wrapper = document.createElement("div");
wrapper.className = "aja-message aja-message-user";
const bubble = document.createElement("div");
bubble.className = "aja-user-bubble";
bubble.textContent = text;
wrapper.appendChild(bubble);
chat.appendChild(wrapper);
scrollBottom();
}
function createAssistantBubble() {
const wrapper = document.createElement("div");
wrapper.className = "aja-message aja-message-assistant";
const bubble = document.createElement("div");
bubble.className = "aja-assistant-bubble";
const header = document.createElement("div");
header.className = "aja-assistant-header";
const avatar = document.createElement("div");
avatar.className = "aja-avatar";
avatar.textContent = "AI";
const title = document.createElement("span");
title.textContent =
activeModuleConfig().headerTitle
|| activeModuleConfig().label
|| "UCC AI Assistant";
const content = document.createElement("div");
content.className = "aja-assistant-content";
header.appendChild(avatar);
header.appendChild(title);
bubble.appendChild(header);
bubble.appendChild(content);
wrapper.appendChild(bubble);
chat.appendChild(wrapper);
scrollBottom();
return wrapper;
}
function addLoadingMessage() {
const wrapper = createAssistantBubble();
const content = wrapper.querySelector(".aja-assistant-content");
content.innerHTML = '<div class="aja-loading">Checking ERPNext records...</div>';
return wrapper;
}
function buildUrl(source) {
if (!source || !source.doctype || !source.name) return "";
const slug =
frappe.router && typeof frappe.router.slug === "function"
? frappe.router.slug(source.doctype)
: String(source.doctype)
.toLowerCase()
.replace(/[^a-z0-9]+/g, "-")
.replace(/^-+|-+$/g, "");
return window.location.origin + "/app/" + slug + "/" + encodeURIComponent(source.name);
}
function renderSummary(container, visual) {
const grid = document.createElement("div");
grid.className = "aja-summary-grid";
safeArray(visual.items).forEach(function (item) {
const card = document.createElement("div");
card.className = "aja-summary-card";
const label = document.createElement("div");
label.className = "aja-summary-label";
label.textContent = item.label || "";
const value = document.createElement("div");
value.className = "aja-summary-value";
value.textContent = displayValue(item.value);
card.appendChild(label);
card.appendChild(value);
grid.appendChild(card);
});
container.appendChild(grid);
}
function renderTable(container, visual) {
const wrap = document.createElement("div");
wrap.className = "aja-table-wrap";
const table = document.createElement("table");
table.className = "aja-table";
const thead = document.createElement("thead");
const headRow = document.createElement("tr");
safeArray(visual.columns).forEach(function (column) {
const th = document.createElement("th");
th.textContent = column;
headRow.appendChild(th);
});
thead.appendChild(headRow);
table.appendChild(thead);
const tbody = document.createElement("tbody");
safeArray(visual.rows).forEach(function (row) {
const tr = document.createElement("tr");
safeArray(row).forEach(function (value) {
const td = document.createElement("td");
if (
value
&& typeof value === "object"
&& !Array.isArray(value)
&& value.doctype
&& value.name
) {
const link = document.createElement("a");
link.className = "aja-record-link";
link.href = "/app/"
+ frappe.router.slug(value.doctype)
+ "/"
+ encodeURIComponent(value.name);
link.target = "_blank";
link.rel = "noopener noreferrer";
link.textContent = displayValue(value);
link.title = "Open " + value.doctype + " " + value.name;
td.appendChild(link);
} else {
td.textContent = displayValue(value);
}
tr.appendChild(td);
});
tbody.appendChild(tr);
});
table.appendChild(tbody);
wrap.appendChild(table);
container.appendChild(wrap);
}
function renderSources(container, sources) {
const seen = new Set();
const wrapper = document.createElement("div");
wrapper.className = "aja-source-links";
safeArray(sources).forEach(function (source) {
if (!source || !source.doctype || !source.name) return;
const key = source.doctype + "::" + source.name;
if (seen.has(key)) return;
seen.add(key);
const url = buildUrl(source);
if (!url) return;
const link = document.createElement("a");
link.className = "aja-source-link";
link.href = url;
link.target = "_blank";
link.rel = "noopener noreferrer";
link.title = source.label || source.name;
link.textContent = "Source: " + (source.short_label || source.label || source.name);
wrapper.appendChild(link);
});
if (wrapper.children.length) {
container.appendChild(wrapper);
}
}
function renderTimeline(container, visual) {
const timeline = document.createElement("div");
timeline.className = "aja-timeline";
safeArray(visual.items).forEach(function (item) {
const row = document.createElement("div");
row.className = "aja-timeline-item";
const marker = document.createElement("div");
marker.className = "aja-timeline-marker";
const body = document.createElement("div");
body.className = "aja-timeline-body";
const date = document.createElement("div");
date.className = "aja-timeline-date";
date.textContent = item.date || "Not recorded";
const title = document.createElement("div");
title.className = "aja-timeline-title";
title.textContent = item.title || "";
const description = document.createElement("div");
description.className = "aja-timeline-description";
description.textContent = item.description || "";
body.appendChild(date);
body.appendChild(title);
body.appendChild(description);
row.appendChild(marker);
row.appendChild(body);
timeline.appendChild(row);
});
container.appendChild(timeline);
}
function renderResponse(result) {
state.lastResult = result || null;
state.lastVisualRows = [];
state.lastExportSections = [];
const wrapper = createAssistantBubble();
const content = wrapper.querySelector(".aja-assistant-content");
const answer = document.createElement("div");
answer.className = "aja-answer";
answer.textContent = formatDatesInText(result.answer || "No answer was returned.");
const outOfScope = (
result.confidence === "Not applicable"
|| cleanText(result.answer).toLowerCase().includes("outside the admission journey scope")
|| cleanText(result.answer).toLowerCase().includes("not an admission journey question")
);
if (outOfScope) {
wrapper.classList.add("aja-message-out-of-scope");
answer.innerHTML =
'<span class="aja-out-scope-icon">!</span>'
+ '<span>'
+ frappe.utils.escape_html(
formatDatesInText(result.answer || "This question is outside the Admission Journey scope.")
)
+ '</span>';
}
content.appendChild(answer);
safeArray(result.warnings).forEach(function (warning) {
const box = document.createElement("div");
box.className = "aja-warning";
box.textContent = "Warning: " + formatDatesInText(warning);
content.appendChild(box);
});
safeArray(result.visuals).forEach(function (visual) {
const section = document.createElement("section");
section.className = "aja-visual";
const title = document.createElement("div");
title.className = "aja-visual-title";
title.textContent = visual.title || "Student information";
section.appendChild(title);
if (visual.type === "table" || visual.type === "timeline_table") {
const tableRows = [safeArray(visual.columns)].concat(safeArray(visual.rows));
state.lastVisualRows = tableRows;
state.lastExportSections.push({
title: visual.title || "Table",
rows: tableRows
});
} else if (visual.type === "summary") {
state.lastExportSections.push({
title: visual.title || "Summary",
rows: [["Field", "Value"]].concat(
safeArray(visual.items).map(function (item) {
return [item.label || "", displayValue(item.value)];
})
)
});
}
if (visual.type === "summary") {
renderSummary(section, visual);
} else if (visual.type === "table" || visual.type === "timeline_table") {
renderTable(section, visual);
} else if (visual.type === "timeline") {
renderTimeline(section, visual);
}
content.appendChild(section);
});
renderSources(content, result.sources || result.source_links);
if (result.confidence) {
const confidence = document.createElement("div");
confidence.className = "aja-confidence";
confidence.textContent = "Confidence: " + result.confidence;
content.appendChild(confidence);
}
if (result.diagnostics && Object.keys(result.diagnostics).length) {
const details = document.createElement("details");
details.className = "aja-diagnostic-details";
const summary = document.createElement("summary");
summary.textContent = "Diagnostic details";
const pre = document.createElement("pre");
pre.textContent = JSON.stringify(result.diagnostics, null, 2);
details.appendChild(summary);
details.appendChild(pre);
content.appendChild(details);
}
if (result.ai_used) {
const note = document.createElement("div");
note.className = "aja-ai-note";
note.textContent = "OpenAI interpreted the question. ERPNext supplied the facts.";
content.appendChild(note);
}
if (result.student_applicant || result.agent_contract) {
state.studentApplicant =
result.student_applicant || result.agent_contract;
state.studentName =
result.student_name || result.agent_name || state.studentApplicant;
updateCurrentStudent();
}
scrollBottom();
}
function renderCandidateSelection(result, originalQuestion) {
const wrapper = createAssistantBubble();
const content = wrapper.querySelector(".aja-assistant-content");
const answer = document.createElement("div");
answer.className = "aja-answer";
answer.textContent = result.answer || "More than one student matches. Select the correct student below.";
content.appendChild(answer);
const list = document.createElement("div");
list.className = "aja-candidate-list";
safeArray(result.candidates).forEach(function (candidate) {
const button = document.createElement("button");
button.type = "button";
button.className = "aja-candidate";
button.dataset.studentApplicant = candidate.student_applicant || "";
button.dataset.studentName = candidate.student_name || "";
button.dataset.question = originalQuestion;
const strong = document.createElement("strong");
strong.textContent = candidate.student_name || candidate.student_applicant;
const detail = document.createElement("span");
detail.textContent = [
candidate.student_applicant,
candidate.program,
candidate.student_type
].filter(Boolean).join(" | ");
button.appendChild(strong);
button.appendChild(detail);
list.appendChild(button);
});
content.appendChild(list);
scrollBottom();
}
async function loadRecruitmentAgents() {
if (state.moduleRecords) {
return state.moduleRecords;
}
try {
const response = await frappe.call({
method: "frappe.client.get_list",
args: {
doctype: "Agent Contract",
fields: ["name", "party_name", "personal_id"],
filters: [],
order_by: "modified desc",
limit_page_length: 500
},
freeze: false
});
state.moduleRecords = response && Array.isArray(response.message)
? response.message
: [];
} catch (error) {
console.warn("Recruitment agents could not be loaded", error);
state.moduleRecords = [];
}
return state.moduleRecords;
}
async function loadQualityActions() {
if (state.moduleRecords) {
return state.moduleRecords;
}
try {
const response = await frappe.call({
method: "frappe.client.get_list",
args: {
doctype: "Quality Action",
fields: ["name", "custom_subject", "modified"],
filters: [],
order_by: "modified desc",
limit_page_length: 1000
},
freeze: false
});
state.moduleRecords = response && Array.isArray(response.message)
? response.message
: [];
} catch (error) {
console.warn("Quality Actions could not be loaded", error);
state.moduleRecords = [];
}
return state.moduleRecords;
}
async function loadActiveModuleData() {
if (state.activeModule === "recruitment_agent") {
return loadRecruitmentAgents();
}
if (state.activeModule === "student_journey") {
return loadStudentRollReport();
}
if (state.activeModule === "quality_action") {
return loadQualityActions();
}
return [];
}
async function loadStudentRollReport() {
if (state.studentRollRows) {
return state.studentRollRows;
}
try {
const response = await frappe.call({
method: "frappe.desk.query_report.run",
args: {
report_name: "Student Roll",
filters: {
from_date: "2000-01-01",
to_date: "2100-12-31"
},
ignore_prepared_report: true,
are_default_filters: false
},
freeze: false
});
const message = response ? response.message : null;
state.studentRollRows =
message && Array.isArray(message.result)
? message.result
: [];
} catch (error) {
console.warn("Student Roll report could not be loaded", error);
state.studentRollRows = [];
}
renderCourseFilter();
return state.studentRollRows;
}
async function sendQuestion(question, selectedApplicant, showUserMessage) {
const text = cleanText(question);
if (!text || state.loading) return;
state.loading = true;
state.lastQuestion = text;
sendButton.disabled = true;
setStatus("Checking records", true);
if (showUserMessage !== false) {
addUserMessage(text);
state.history.push({ role: "user", content: text });
}
const loadingMessage = addLoadingMessage();
try {
await loadActiveModuleData();
const moduleConfig = activeModuleConfig();
const selectedRecord = (
selectedApplicant === "__GLOBAL__"
? ""
: (selectedApplicant || state.studentApplicant || "")
);
const requestArgs = {
question: text,
conversation: JSON.stringify(state.history.slice(-20))
};
try {
const sessionKey = window.sessionStorage.getItem("uccAiOpenAIKey") || "";
if (sessionKey) requestArgs.openai_api_key = sessionKey;
} catch (error) {
}
if (state.activeModule === "student_journey") {
requestArgs.student_applicant = selectedRecord;
requestArgs.student_roll_rows = JSON.stringify(state.studentRollRows || []);
} else if (state.activeModule === "recruitment_agent") {
requestArgs.agent_contract = selectedRecord;
} else if (state.activeModule === "quality_action") {
requestArgs.quality_action = selectedRecord;
}
const response = await frappe.call({
method: moduleConfig.apiMethod,
args: requestArgs,
freeze: false
});
loadingMessage.remove();
const result = response && response.message ? response.message : response;
if (result && result.status === "choose_student") {
renderCandidateSelection(result, text);
return;
}
renderResponse(result || {
status: "error",
answer: "No response was returned.",
warnings: [],
visuals: [],
sources: []
});
state.history.push({
role: "assistant",
content: result && result.answer ? result.answer : ""
});
} catch (error) {
loadingMessage.remove();
console.error("Admission Journey Assistant error", error);
renderResponse({
status: "error",
answer: "Unable to retrieve the information.",
warnings: ["Open the browser console for the exact ERPNext error."],
visuals: [],
sources: []
});
} finally {
state.loading = false;
sendButton.disabled = false;
setStatus("Ready", false);
questionInput.focus();
}
}
function resetChatPanel() {
if (!chat) return;
chat.innerHTML = "";
if (comingSoon) {
comingSoon.hidden = true;
comingSoon.innerHTML = "";
chat.appendChild(comingSoon);
}
const welcome = document.createElement("div");
welcome.className = "aja-welcome";
const avatar = document.createElement("div");
avatar.className = "aja-avatar";
avatar.textContent = "AI";
const content = document.createElement("div");
const title = document.createElement("strong");
title.textContent = "Ready to review";
const paragraph = document.createElement("p");
paragraph.textContent = "Select a record, then choose a guided question.";
const example = document.createElement("div");
example.className = "aja-example";
example.textContent = "ERPNext evidence, tables, warnings and AI interpretation will appear here.";
content.appendChild(title);
content.appendChild(paragraph);
content.appendChild(example);
welcome.appendChild(avatar);
welcome.appendChild(content);
chat.appendChild(welcome);
state.history = [];
state.lastQuestion = "";
state.lastResult = null;
state.lastVisualRows = [];
state.lastExportSections = [];
}
function closeApiModal() {
if (apiModal) apiModal.hidden = true;
}
function proceedFreeQuestion(useStoredKey) {
const question = cleanText(pendingFreeQuestion || (questionInput ? questionInput.value : ""));
pendingFreeQuestion = "";
closeApiModal();
if (!question) return;
if (questionInput) questionInput.value = "";
sendQuestion(question, "", true);
}
sendButton.addEventListener("click", function () {
const question = questionInput.value.trim();
if (!question) return;
let hasSessionKey = false;
try {
hasSessionKey = Boolean(window.sessionStorage.getItem("uccAiOpenAIKey"));
} catch (error) {}
if (hasSessionKey || !apiModal) {
questionInput.value = "";
sendQuestion(question, "", true);
return;
}
pendingFreeQuestion = question;
apiModal.hidden = false;
if (apiKeyInput) apiKeyInput.focus();
});
if (apiButton) {
apiButton.addEventListener("click", function () {
pendingFreeQuestion = "";
if (apiModal) apiModal.hidden = false;
if (apiKeyInput) apiKeyInput.focus();
});
}
if (clearChatButton) {
clearChatButton.addEventListener("click", function () {
resetChatPanel();
setStatus("Ready", false);
});
}
if (apiCancel) apiCancel.addEventListener("click", function () {
pendingFreeQuestion = "";
closeApiModal();
});
if (apiSkip) apiSkip.addEventListener("click", function () {
proceedFreeQuestion(false);
});
if (apiConnect) apiConnect.addEventListener("click", function () {
const key = cleanText(apiKeyInput ? apiKeyInput.value : "");
if (!key) {
if (apiKeyInput) apiKeyInput.focus();
return;
}
try {
window.sessionStorage.setItem("uccAiOpenAIKey", key);
} catch (error) {}
if (apiKeyInput) apiKeyInput.value = "";
proceedFreeQuestion(true);
});
function blockGlobalSearch(event) {
const path = event.composedPath ? event.composedPath() : [];
if (!path.includes(questionInput)) return;
event.stopPropagation();
if (event.key === "Enter" && !event.shiftKey) {
event.preventDefault();
sendButton.click();
}
}
["keydown", "keypress", "keyup"].forEach(function (eventName) {
app.addEventListener(eventName, blockGlobalSearch, true);
});
if (studentSearch) {
["click", "mousedown", "keydown", "keyup", "input"].forEach(function (eventName) {
studentSearch.addEventListener(eventName, function (event) {
event.stopPropagation();
});
});
studentSearch.addEventListener("input", function () {
state.searchPage = 1;
renderStudentMatches(studentSearch.value);
});
}
if (courseFilter) {
courseFilter.addEventListener("change", function (event) {
event.stopPropagation();
state.searchPage = 1;
renderStudentMatches(studentSearch ? studentSearch.value : "");
});
}
if (studentPager) {
studentPager.addEventListener("click", function (event) {
const button = event.target.closest(".aja-pager-button");
if (!button) return;
event.preventDefault();
event.stopPropagation();
if (button.dataset.pageAction === "prev" && state.searchPage > 1) {
state.searchPage = state.searchPage - 1;
}
if (button.dataset.pageAction === "next") {
state.searchPage = state.searchPage + 1;
}
renderStudentMatches(studentSearch ? studentSearch.value : "");
});
}
if (studentMatches) {
studentMatches.addEventListener("pointerdown", function (event) {
const button = event.target.closest(".aja-student-match");
if (!button) return;
event.preventDefault();
event.stopPropagation();
selectStudent(
button.dataset.studentApplicant,
button.dataset.studentName
);
studentMatches.innerHTML = "";
studentSearch.value = "";
questionInput.focus();
});
}
if (recentStudents) {
recentStudents.addEventListener("click", function (event) {
const removeButton = event.target.closest(".aja-recent-remove");
if (removeButton) {
event.preventDefault();
event.stopPropagation();
removeRecentStudent(removeButton.dataset.removeStudent || "");
return;
}
const button = event.target.closest(".aja-recent-button");
if (!button) return;
selectStudent(
button.dataset.studentApplicant,
button.dataset.studentName
);
});
}
if (changeStudentButton) {
changeStudentButton.addEventListener("click", function () {
studentSearch.focus();
});
}
if (resetContextButton) {
resetContextButton.addEventListener("click", function () {
state.studentApplicant = "";
state.studentName = "";
state.history = [];
updateCurrentStudent();
setStatus("Context reset", false);
});
}
if (exportCsvButton) {
exportCsvButton.addEventListener("click", exportLastResultCsv);
}
if (diagnosticsButton) {
diagnosticsButton.addEventListener("click", function () {
if (!state.studentApplicant) {
setStatus("Select a student first", false);
return;
}
sendQuestion(
"Show admin diagnostics for this student",
state.studentApplicant,
true
);
});
}
loadRecentStudents();
renderRecentStudents();
printButton.addEventListener("click", function () {
window.print();
});
const studentQuestionMap = {
profile: [
["Student profile", "Show this student's profile"],
["Course", "What course is this student in?"],
["Nationality", "What is this student's nationality?"],
["Commencement", "When did this student start?"],
["Completion", "When is this student completing the course?"]
],
journey: [
["Full timeline", "Show this student's journey"],
["Current module", "Which module is this student in right now?"],
["Class and group", "Show this student's class and student group"],
["Current leave", "Is this student on leave now?"]
],
academic: [
["All results", "Show all this student's results and grades"],
["Module completion", "Has this student finished all modules?"],
["Graduation status", "Has this student graduated?"],
["Results and grades", "Show all this student\'s results and grades"]
],
attendance: [
["Attendance summary", "Show this student's attendance"],
["Current leave", "Is this student on leave now?"],
["Leave history", "Show this student's leave records"]
],
finance: [
["Payment status", "Show this student's fee and payment status"],
["Outstanding fees", "Does this student have outstanding fees?"],
["Invoices", "Show this student's invoices"],
["FPS status", "What is this student's FPS status?"]
],
graduation: [
["Readiness", "Is this student ready to graduate?"],
["Risk summary", "Show this student's risk summary"],
["Follow-up actions", "What follow-up actions are needed for this student?"],
["Admission documents", "Show this student's attached admission documents"]
],
cohort: [
["Cohort dashboard", "Show the cohort dashboard"],
["Class today", "Who are the students in class today?"],
["Graduating this month", "Who is graduating this month?"],
["Graduated months ago", "Who graduated 6 months ago?"],
["Leave count", "How many students are on leave from 15 to 30 August 2026?"]
]
};
const recruitmentQuestionMap = {
profile: [
["Agent profile", "Show this agent's profile"],
["Contract status", "Is this agent's contract active?"],
["Contract dates", "Show this agent's contract dates"]
],
journey: [
["Agent journey", "Show this agent's complete journey"],
["Latest contract", "Show this agent's latest contract"],
["Expiry", "When does this agent's contract expire?"]
],
academic: [
["Students recruited", "How many students did this agent recruit?"],
["Recruitment list", "Show students recruited by this agent"]
],
attendance: [
["Latest rating", "What is this agent's latest rating?"],
["Rating threshold", "Does this agent meet the minimum rating?"]
],
finance: [
["Revenue contribution", "What revenue came from this agent?"],
["Commission status", "Show this agent's commission status"]
],
graduation: [
["Renewal readiness", "Should this agent's contract be renewed?"],
["Compliance issues", "Show this agent's compliance issues"],
["Risk summary", "Show this agent's risk summary"]
],
cohort: [
["Active agents", "How many recruitment agents have active contracts?"],
["Expiring contracts", "Which agent contracts are expiring soon?"]
]
};
const qualityActionQuestionMap = {
profile: [
["Quality Action overview", "Show this Quality Action"],
["Problem", "What is the problem?"],
["Current status", "What is the current status?"]
],
journey: [
["Root cause and resolution", "Show the root cause and resolution"],
["Action taken", "What action has been taken?"],
["Assigned person", "Who is assigned?"]
],
academic: [
["Due date", "When is it due?"],
["Overdue check", "Is it overdue?"],
["Completion status", "What is the current status?"]
],
attendance: [
["Closure readiness", "Is this Quality Action ready for closure?"],
["Quality review", "Run a quality review of the root cause and action taken"],
["Root-cause review", "Assess the root cause and resolution"]
],
finance: [
["Open Quality Actions", "Show all open Quality Actions"],
["Overdue Quality Actions", "Show overdue Quality Actions"]
],
graduation: [
["NC findings", "Show NC findings"],
["OFI findings", "Show OFI findings"]
],
cohort: [
["All open actions", "Show all open Quality Actions"],
["All overdue actions", "Show overdue Quality Actions"],
["All NC findings", "Show NC findings"],
["All OFI findings", "Show OFI findings"]
]
};
function renderCategoryButtons() {
if (!categoryButtons || !categorySelect) return;
categoryButtons.innerHTML = "";
Array.from(categorySelect.options).forEach(function (option) {
const button = document.createElement("button");
button.type = "button";
button.className = "aja-category-button";
button.dataset.value = option.value;
button.textContent = option.textContent;
if (option.value === categorySelect.value) {
button.classList.add("active");
}
button.addEventListener("click", function () {
categorySelect.value = option.value;
categorySelect.dispatchEvent(new Event("change", { bubbles: true }));
});
categoryButtons.appendChild(button);
});
}
function renderControlledQuestions() {
if (!controlledQuestions || !categorySelect) {
return;
}
renderCategoryButtons();
controlledQuestions.innerHTML = "";
const category = categorySelect.value || "profile";
const questionMap = state.activeModule === "recruitment_agent"
? recruitmentQuestionMap
: (
state.activeModule === "quality_action"
? qualityActionQuestionMap
: studentQuestionMap
);
const questions = questionMap[category] || [];
questions.forEach(function (item) {
const button = document.createElement("button");
button.type = "button";
button.className = "aja-suggestion";
button.dataset.question = item[1];
button.textContent = item[0];
controlledQuestions.appendChild(button);
});
}
if (categorySelect) {
categorySelect.addEventListener("change", renderControlledQuestions);
}
suggestionsContainer.addEventListener("click", function (event) {
const button = event.target.closest(".aja-suggestion");
if (!button) return;
const question = button.dataset.question || button.textContent.trim();
const isCohortQuestion = (
categorySelect
&& categorySelect.value === "cohort"
);
if (isCohortQuestion) {
sendQuestion(question, "__GLOBAL__", true);
return;
}
if (state.studentApplicant) {
sendQuestion(question, state.studentApplicant, true);
return;
}
const moduleConfig = activeModuleConfig();
questionInput.value = "";
questionInput.placeholder =
"Enter or select a " + moduleConfig.entityLabel + " first";
questionInput.focus();
setStatus("Select a " + moduleConfig.entityLabel + " first", false);
});
function resetModuleContext() {
state.studentApplicant = "";
state.studentName = "";
state.history = [];
state.lastResult = null;
state.lastVisualRows = [];
state.lastExportSections = [];
state.searchPage = 1;
state.moduleRecords = null;
if (studentSearch) studentSearch.value = "";
if (studentMatches) studentMatches.innerHTML = "";
if (studentPager) studentPager.innerHTML = "";
updateCurrentStudent();
}
function renderCategoryOptions() {
if (!categorySelect) return;
const options = state.activeModule === "recruitment_agent"
? [
["profile", "Profile and Contract"],
["journey", "Agent Journey"],
["academic", "Recruitment Performance"],
["attendance", "Ratings"],
["finance", "Revenue and Commission"],
["graduation", "Compliance and Renewal"],
["cohort", "Agent Portfolio"]
]
: (
state.activeModule === "quality_action"
? [
["profile", "Overview"],
["journey", "Root Cause and Action"],
["academic", "Status and Due Dates"],
["attendance", "Review and Closure"],
["finance", "Open and Overdue"],
["graduation", "Finding Types"],
["cohort", "Quality Action Portfolio"]
]
: [
["profile", "Profile"],
["journey", "Student Journey"],
["academic", "Academic and Results"],
["attendance", "Attendance and Leave"],
["finance", "Fees and Payments"],
["graduation", "Graduation and Risk"],
["cohort", "Cohort Questions"]
]
);
categorySelect.innerHTML = "";
options.forEach(function (item) {
const option = document.createElement("option");
option.value = item[0];
option.textContent = item[1];
categorySelect.appendChild(option);
});
}
async function applyModule(moduleId) {
state.activeModule = moduleId || "student_journey";
resetModuleContext();
const config = activeModuleConfig();
if (pinnedLabel) pinnedLabel.textContent = config.pinnedLabel || "Pinned record";
if (findLabel) findLabel.textContent = config.findLabel || "Find record";
if (recentLabel) recentLabel.textContent = config.recentLabel || "Recent records";
if (studentSearch) studentSearch.placeholder = config.searchPlaceholder || "Type to search";
if (headerTitle) headerTitle.textContent = config.headerTitle || config.label;
if (headerSubtitle) headerSubtitle.textContent = config.headerSubtitle || "";
if (moduleStatus) {
moduleStatus.textContent = config.comingSoon
? config.label + " is coming soon."
: config.label + " is active.";
}
if (courseFilter) {
courseFilter.hidden = state.activeModule !== "student_journey";
}
if (comingSoon) {
comingSoon.hidden = !config.comingSoon;
comingSoon.textContent = config.comingSoon
? config.label + " is planned for a future version."
: "";
}
if (questionInput) questionInput.disabled = Boolean(config.comingSoon);
if (sendButton) sendButton.disabled = Boolean(config.comingSoon);
if (suggestionsContainer) suggestionsContainer.hidden = Boolean(config.comingSoon);
renderCategoryOptions();
renderControlledQuestions();
if (!config.comingSoon) {
setStatus("Loading " + config.entityLabel + " records", true);
await loadActiveModuleData();
renderCourseFilter();
setStatus("Ready", false);
} else {
setStatus("Coming soon", false);
}
}
if (moduleSelect) {
moduleSelect.addEventListener("change", function () {
applyModule(moduleSelect.value);
});
}
renderControlledQuestions();
applyModule("student_journey");
updateCurrentStudent();
updateSuggestionState();
})();
(function(){
"use strict";
const root=typeof root_element!=="undefined"
?root_element.querySelector("#uccIntelligencePlatform")
:document.querySelector("#uccIntelligencePlatform");
if(!root||root.dataset.v110Ready==="1")return;
root.dataset.v110Ready="1";
const STORAGE_KEY="ucc-intelligence-platform-v1.2.0-view";
const $=(selector,scope=root)=>scope.querySelector(selector);
const $$=(selector,scope=root)=>Array.from(scope.querySelectorAll(selector));
function notify(message,indicator="blue"){
if(window.frappe&&frappe.show_alert)frappe.show_alert({message,indicator},5);
else console.info("[UCC]",message);
}
function visiblePanel(){
return $$(".panel-view").find(panel=>!panel.classList.contains("hidden")&&panel.offsetParent!==null)
|| $$(".panel-view").find(panel=>!panel.classList.contains("hidden"));
}
function activeTable(){
const panel=visiblePanel()||root;
return $$("table",panel).find(table=>table.offsetParent!==null)||$("table",panel);
}
const csvCell=UCCShared.csvCell;
function tableToCsv(table){return UCCShared.tableToCsv(table);}
function download(name,content,type="text/csv;charset=utf-8"){return UCCShared.download(name,content,type);}
function exportCurrentTable(){
const table=activeTable();
if(!table){notify("No visible table to export.","orange");return}
download("ucc-current-table.csv",tableToCsv(table));
}
function exportExceptions(){
const panel=visiblePanel()||root;
const candidate=$$("table",panel).find(table=>/exception|gap|risk|attention/i.test(table.closest(".panel")?.innerText||""));
if(!candidate){notify("No visible exception table in this view.","orange");return}
download("ucc-current-exceptions.csv",tableToCsv(candidate));
}
function selectedState(){
const selected={};
const activeMain=$(".tabs [data-tab].active");
const activeLocal=$(".section-local-tabs [data-local-tab].active");
const activeWorkspace=$("[data-ucc-workspace].is-active");
if(activeMain)selected.tab=activeMain.dataset.tab;
if(activeLocal)selected.localTab=activeLocal.dataset.localTab;
if(activeWorkspace)selected.workspace=activeWorkspace.dataset.uccWorkspace;
selected.filters={};
$$("[data-filter]").forEach(el=>selected.filters[el.dataset.filter]=el.value);
return selected;
}
function saveState(){
try{localStorage.setItem(STORAGE_KEY,JSON.stringify(selectedState()))}catch(e){console.warn("[UCC] state persistence unavailable",e)}
}
function copyFilteredLink(){
const state=selectedState(),url=new URL(location.href);
if(state.tab)url.searchParams.set("ucc_tab",state.tab);
if(state.localTab)url.searchParams.set("ucc_subpage",state.localTab);
Object.entries(state.filters).forEach(([key,value])=>{if(value)url.searchParams.set("ucc_"+key,value);else url.searchParams.delete("ucc_"+key)});
const value=url.toString();
const copy=navigator.clipboard?.writeText?navigator.clipboard.writeText(value):Promise.reject();
copy.then(()=>notify("Filtered link copied.","green")).catch(()=>{
const input=document.createElement("textarea");input.value=value;document.body.appendChild(input);input.select();document.execCommand("copy");input.remove();notify("Filtered link copied.","green")
});
}
root.addEventListener("click",event=>{
const action=event.target.closest("[data-universal-action]")?.dataset.universalAction;
if(action==="export-table")exportCurrentTable();
if(action==="export-exceptions")exportExceptions();
if(action==="copy-link")copyFilteredLink();
if(event.target.closest("[data-tab],[data-local-tab],[data-ucc-workspace]"))setTimeout(saveState,20);
});
root.addEventListener("change",event=>{if(event.target.matches("[data-filter],select,input"))saveState()});
function restoreState(){
let stored={};
try{stored=JSON.parse(localStorage.getItem(STORAGE_KEY)||"{}")}catch{}
const url=new URL(location.href);
const tab=url.searchParams.get("ucc_tab")||stored.tab;
const localTab=url.searchParams.get("ucc_subpage")||stored.localTab;
const workspace=stored.workspace;
if(workspace)$(`[data-ucc-workspace="${CSS.escape(workspace)}"]`)?.click();
if(tab)$(`[data-tab="${CSS.escape(tab)}"]`)?.click();
setTimeout(()=>{if(localTab)$(`[data-local-tab="${CSS.escape(localTab)}"]`)?.click()},80);
$$("[data-filter]").forEach(el=>{
const value=url.searchParams.get("ucc_"+el.dataset.filter)??stored.filters?.[el.dataset.filter];
if(value!==undefined&&value!==null&&Array.from(el.options||[]).some(o=>o.value===value))el.value=value;
});
}
function ensureChartToggles(){
$$("[data-chart]").forEach(chart=>{
const panel=chart.closest(".panel");if(!panel)return;
chart.classList.add("ucc-clickable-result");
const key=chart.dataset.chart;
if(panel.querySelector("[data-card-toggle]"))return;
const table=$(`[data-table="${CSS.escape(key)}"]`)?.closest(".table-wrap");
if(!table)return;
const head=$(".panel-head",panel)||$("h2",panel)?.parentElement;
if(!head||$(`[data-auto-toggle="${CSS.escape(key)}"]`,panel))return;
const wrap=document.createElement("div");
wrap.className="mini-toggle";wrap.dataset.autoToggle=key;
wrap.innerHTML='<button type="button" class="active" data-auto-view="diagram">Diagram</button><button type="button" data-auto-view="table">Table</button>';
head.appendChild(wrap);
table.classList.add("ucc-hidden");
wrap.addEventListener("click",event=>{
const button=event.target.closest("[data-auto-view]");if(!button)return;
$$("button",wrap).forEach(x=>x.classList.toggle("active",x===button));
chart.classList.toggle("ucc-hidden",button.dataset.autoView==="table");
table.classList.toggle("ucc-hidden",button.dataset.autoView==="diagram");
});
});
}
function classifyEmptyStates(){
$$("[data-table] tr td:only-child,.empty-state,.source-empty").forEach(node=>{
const text=node.textContent.toLowerCase();
let type="no-data",title="No matching data";
if(/permission|not permitted|403/.test(text)){type="permission";title="Permission denied"}
else if(/unavailable|missing doctype|source not/.test(text)){type="unavailable";title="Source unavailable"}
else if(/unsupported|missing field|unknown column/.test(text)){type="unsupported";title="Unsupported or missing fields"}
if(node.closest(".ucc-empty-state"))return;
node.classList.add("ucc-empty-state");node.dataset.state=type;
if(!node.querySelector("strong"))node.innerHTML="<strong>"+title+"</strong>"+node.innerHTML;
});
}
function makeCountsClickable(){
$$("[data-kpi],[data-new-kpi],.kpis strong").forEach(node=>{
node.classList.add("ucc-clickable-result");node.tabIndex=0;
const activate=()=>{
const card=node.closest("article"),label=card?.querySelector("span")?.textContent||"Result";
const panel=visiblePanel(),table=panel&&$("table",panel);
if(table){table.scrollIntoView({behavior:"smooth",block:"center"});notify(label+": review the visible drill-down table.","blue")}
};
node.addEventListener("click",activate);
node.addEventListener("keydown",event=>{if(event.key==="Enter"||event.key===" ")activate()});
});
}
function makeTableRowsDrillable(){
$$("tbody tr").forEach(row=>{
if(row.dataset.v110Drill==="1")return;row.dataset.v110Drill="1";
row.classList.add("ucc-clickable-result");
row.addEventListener("dblclick",()=>row.querySelector("a.open-record-link")?.click());
});
}
const observer=new MutationObserver(()=>{ensureChartToggles();classifyEmptyStates();makeCountsClickable();makeTableRowsDrillable()});
observer.observe(root,{childList:true,subtree:true});
setTimeout(()=>{restoreState();ensureChartToggles();classifyEmptyStates();makeCountsClickable();makeTableRowsDrillable()},250);
})();
(function(){
"use strict";
const platform=typeof root_element!=="undefined"
? root_element.querySelector("#uccIntelligencePlatform")
: document.querySelector("#uccIntelligencePlatform");
if(!platform)return;
const root=platform.querySelector('[data-dashboard-panel="criterion_4"]');
if(!root||root.dataset.ready==="1")return;
root.dataset.ready="1";
window.__uccMergeSourcesQuality(root,"data-c4-tab","data-c4-panel");
const $$=(selector,scope=root)=>Array.from(scope.querySelectorAll(selector));
const $=(selector,scope=root)=>scope.querySelector(selector);
const TAB_MAP={
c411:"4.1.1",c421:"4.2.1",c422:"4.2.2",c431:"4.3.1",
c441:"4.4.1",c451:"4.5.1",c461:"4.6.1"
};
const CODE_TO_TAB=Object.fromEntries(Object.entries(TAB_MAP).map(entry=>[entry[1],entry[0]]));
const API_TABS=Object.keys(TAB_MAP);
const STORAGE_KEY="ucc.c4.v130";
const EXCEPTION_IDS=new Set([
"c411-conditional","c411-late","c421-pending","c422-late",
"c431-overdue","c441-open","c441-overdue","c451-followup",
"c461-risk","c461-intervention"
]);
const state={
tab:"overview",
results:new Map(),
metrics:new Map(),
qa:[],
exceptions:[],
quality:[],
drillRows:[],
loading:false,
logs:[],
requestId:0,
visuals:{}
};

let c4D3Promise=null;
function ensureC4D3(){
if(window.d3)return Promise.resolve(window.d3);
if(c4D3Promise)return c4D3Promise;
c4D3Promise=new Promise((resolve,reject)=>{
let script=document.querySelector('script[data-ucc-d3],script[src*="d3.v7.min.js"]');
const loaded=()=>{
if(window.d3)resolve(window.d3);
else reject(new Error("D3 loaded without exposing window.d3."));
};
const failed=()=>reject(new Error("D3 could not be loaded."));
if(script){
script.addEventListener("load",loaded,{once:true});
script.addEventListener("error",failed,{once:true});
window.setTimeout(()=>{
if(window.d3)resolve(window.d3);
},50);
return;
}
script=document.createElement("script");
script.src="https://d3js.org/d3.v7.min.js";
script.async=true;
script.dataset.uccD3="1";
script.addEventListener("load",loaded,{once:true});
script.addEventListener("error",failed,{once:true});
document.head.appendChild(script);
});
return c4D3Promise;
}
function c4DoctypeRoute(doctype){return UCCShared.doctypeRoute(doctype);}
function openC4Source(doctype){return UCCShared.openDoctype(doctype);}
function c4QaSourceCell(question){
const doctype=question?.doctype||"";
const link=doctype?`<a class="source-doctype-link ucc-qa-action" href="${escapeHtml(c4DoctypeRoute(doctype))}" target="_blank" rel="noopener noreferrer">Open ${escapeHtml(doctype)} list ↗</a>`:'<span class="source-unavailable">No readable source list</span>';
return`<div>${escapeHtml(question?.source_logic||"Live API calculation")}</div>${link}`;
}
function c4FiniteNumber(value,fallback=0){
const number=Number(value);
return Number.isFinite(number)?number:fallback;
}
function c4VisualStage(raw){
let metric=null;
let value=null;
let status="unavailable";
let doctype=raw.source||null;
let field=null;
if(raw.metric){
metric=state.metrics.get(raw.metric)||null;
if(metric){
value=metric.status==="available"?c4FiniteNumber(metric.value,0):metric.value;
status=metric.status||"unavailable";
doctype=metric.doctype||doctype;
field=metric.field||null;
}
}
if(Array.isArray(raw.aggregate)){
let total=0;
let found=false;
let available=true;
raw.aggregate.forEach(metricId=>{
const item=state.metrics.get(metricId);
if(!item)return;
found=true;
if(item.status!=="available")available=false;
if(item.value!==null&&item.value!==undefined){
total=total+c4FiniteNumber(item.value,0);
}
});
value=found?total:null;
status=found&&available?"available":found?"unsupported_field":"unavailable";
}
return {
label:raw.label,
metricId:raw.metric||null,
value,
status,
doctype,
field,
exception:raw.exception===true
};
}
function c4VisualData(tab){
const config=state.visuals[tab];
if(!config)return null;
return {
type:config.type,
title:config.title,
stages:config.stages.map(c4VisualStage)
};
}
function c4VisualCount(stage){
return stage.value===null||stage.value===undefined?"—":String(stage.value);
}
function c4VisualFill(stage){
if(stage.status!=="available")return "#aeb7c8";
if(stage.exception&&c4FiniteNumber(stage.value,0)>0)return "#ce9e5d";
return "#26345b";
}
function c4VisualStroke(stage){
if(stage.status!=="available")return "#818ba0";
if(stage.exception&&c4FiniteNumber(stage.value,0)>0)return "#a9783b";
return "#1f2a49";
}
function bindC4Stage(selection,container,stageAccessor){
const resolveStage=typeof stageAccessor==="function"?stageAccessor:datum=>datum;
selection
.attr("role","button")
.attr("tabindex",0)
.style("cursor",datum=>resolveStage(datum)?.metricId?"pointer":"default")
.on("click",function(event,datum){
const stage=resolveStage(datum)||{};
if(stage.metricId)openDrilldown(stage.metricId);
})
.on("keydown",function(event,datum){
const stage=resolveStage(datum)||{};
if((event.key==="Enter"||event.key===" ")&&stage.metricId){
event.preventDefault();
openDrilldown(stage.metricId);
}
})
.on("mouseenter",function(event,datum){
const stage=resolveStage(datum)||{};
const tooltip=container.querySelector(".ucc-c4-chart-tooltip");
if(!tooltip)return;
tooltip.hidden=false;
tooltip.innerHTML=
`<strong>${escapeHtml(stage.label||"Visual stage")}</strong>`
+`<span>Count: ${escapeHtml(c4VisualCount(stage))}</span>`
+`<span>Status: ${escapeHtml(statusText(stage.status||"unavailable"))}</span>`
+`<span>Source: ${escapeHtml(stage.doctype||"Not resolved")}</span>`
+(stage.metricId?`<em>Click to view matching records</em>`:"");
})
.on("mousemove",function(event){
const tooltip=container.querySelector(".ucc-c4-chart-tooltip");
if(!tooltip)return;
const rect=container.getBoundingClientRect();
tooltip.style.left=Math.min(rect.width-230,event.clientX-rect.left+14)+"px";
tooltip.style.top=Math.max(8,event.clientY-rect.top-22)+"px";
})
.on("mouseleave",function(){
const tooltip=container.querySelector(".ucc-c4-chart-tooltip");
if(tooltip)tooltip.hidden=true;
});
}
function addC4SourceText(group,stage,x,y,anchor="middle"){
const text=group.append("text")
.attr("class","ucc-c4-d3-source")
.attr("x",x)
.attr("y",y)
.attr("text-anchor",anchor)
.text(stage.doctype||"Source not resolved");
if(stage.doctype){
text
.attr("role","link")
.attr("tabindex",0)
.on("click",function(event){
event.stopPropagation();
openC4Source(stage.doctype);
})
.on("keydown",function(event){
if(event.key==="Enter"||event.key===" "){
event.preventDefault();
event.stopPropagation();
openC4Source(stage.doctype);
}
});
}
}
function prepareC4Svg(container,height){
container.innerHTML='<div class="ucc-c4-chart-tooltip" hidden></div>';
const width=Math.max(container.clientWidth||720,360);
return {
width,
height,
svg:d3.select(container)
.append("svg")
.attr("class","ucc-c4-d3-svg")
.attr("viewBox",`0 0 ${width} ${height}`)
.attr("preserveAspectRatio","xMidYMid meet")
};
}
function renderC4Funnel(container,stages){
const rowHeight=70;
const height=stages.length*rowHeight+36;
const chart=prepareC4Svg(container,height);
const width=chart.width;
const maxValue=d3.max(stages,stage=>c4FiniteNumber(stage.value,0))||1;
const minWidth=Math.min(250,width*.42);
const maxWidth=Math.min(610,width-64);
const center=width/2;
const groups=chart.svg.selectAll("g.ucc-c4-funnel-stage")
.data(stages)
.join("g")
.attr("class","ucc-c4-funnel-stage");
bindC4Stage(groups,container);
groups.each(function(stage,index){
const group=d3.select(this);
const ratio=stage.status==="available"
?Math.max(.28,c4FiniteNumber(stage.value,0)/maxValue)
:.42;
const topWidth=minWidth+(maxWidth-minWidth)*ratio;
const next=stages[index+1];
const nextRatio=next&&next.status==="available"
?Math.max(.28,c4FiniteNumber(next.value,0)/maxValue)
:Math.max(.24,ratio-.08);
const bottomWidth=minWidth+(maxWidth-minWidth)*nextRatio;
const y=18+index*rowHeight;
const points=[
[center-topWidth/2,y],
[center+topWidth/2,y],
[center+bottomWidth/2,y+54],
[center-bottomWidth/2,y+54]
];
group.append("path")
.attr("d","M"+points.map(point=>point.join(",")).join("L")+"Z")
.attr("fill",c4VisualFill(stage))
.attr("stroke",c4VisualStroke(stage))
.attr("stroke-width",1.5);
group.append("text")
.attr("class","ucc-c4-d3-label is-inverse")
.attr("x",center)
.attr("y",y+24)
.attr("text-anchor","middle")
.text(stage.label);
group.append("text")
.attr("class","ucc-c4-d3-value is-inverse")
.attr("x",center)
.attr("y",y+43)
.attr("text-anchor","middle")
.text(c4VisualCount(stage));
addC4SourceText(group,stage,center+topWidth/2+10,y+31,"start");
});
}
function renderC4Lifecycle(container,stages){
const chart=prepareC4Svg(container,300);
const width=chart.width;
const x=d3.scalePoint()
.domain(d3.range(stages.length))
.range([72,width-72])
.padding(.25);
const y=126;
chart.svg.append("path")
.attr("class","ucc-c4-d3-connector")
.attr("d",d3.line().curve(d3.curveMonotoneX)(
stages.map((stage,index)=>[x(index),y])
));
const groups=chart.svg.selectAll("g.ucc-c4-life-node")
.data(stages)
.join("g")
.attr("class","ucc-c4-life-node")
.attr("transform",(stage,index)=>`translate(${x(index)},${y})`);
bindC4Stage(groups,container);
groups.append("circle")
.attr("r",stage=>26+Math.min(12,Math.sqrt(c4FiniteNumber(stage.value,0))*1.4))
.attr("fill",c4VisualFill)
.attr("stroke",c4VisualStroke)
.attr("stroke-width",3);
groups.append("text")
.attr("class","ucc-c4-d3-value is-inverse")
.attr("text-anchor","middle")
.attr("dy","0.35em")
.text(c4VisualCount);
groups.append("text")
.attr("class","ucc-c4-d3-label")
.attr("text-anchor","middle")
.attr("y",(stage,index)=>index%2===0?-60:66)
.each(function(stage){
const words=stage.label.split(/\s+/);
const text=d3.select(this);
const midpoint=Math.ceil(words.length/2);
text.append("tspan").attr("x",0).text(words.slice(0,midpoint).join(" "));
if(words.length>midpoint){
text.append("tspan").attr("x",0).attr("dy",15)
.text(words.slice(midpoint).join(" "));
}
});
groups.each(function(stage,index){
addC4SourceText(
d3.select(this),
stage,
0,
index%2===0?-91:96,
"middle"
);
});
}
function renderC4Reconciliation(container,stages){
const chart=prepareC4Svg(container,350);
const width=chart.width;
const positions=[
{x:width*.18,y:95},
{x:width*.50,y:95},
{x:width*.82,y:95},
{x:width*.50,y:265}
];
const links=[[0,1],[1,2],[0,3]];
chart.svg.selectAll("path.ucc-c4-reconcile-link")
.data(links)
.join("path")
.attr("class","ucc-c4-reconcile-link")
.attr("d",link=>{
const source=positions[link[0]];
const target=positions[link[1]];
const mid=(source.x+target.x)/2;
return `M${source.x},${source.y} C${mid},${source.y} ${mid},${target.y} ${target.x},${target.y}`;
});
const groups=chart.svg.selectAll("g.ucc-c4-reconcile-node")
.data(stages)
.join("g")
.attr("class","ucc-c4-reconcile-node")
.attr("transform",(stage,index)=>`translate(${positions[index].x},${positions[index].y})`);
bindC4Stage(groups,container);
groups.append("rect")
.attr("x",-92)
.attr("y",-42)
.attr("width",184)
.attr("height",84)
.attr("rx",18)
.attr("fill",c4VisualFill)
.attr("stroke",c4VisualStroke)
.attr("stroke-width",2);
groups.append("text")
.attr("class","ucc-c4-d3-label is-inverse")
.attr("text-anchor","middle")
.attr("y",-8)
.text(stage=>stage.label);
groups.append("text")
.attr("class","ucc-c4-d3-value is-inverse")
.attr("text-anchor","middle")
.attr("y",20)
.text(c4VisualCount);
groups.each(function(stage){
addC4SourceText(d3.select(this),stage,0,65,"middle");
});
}
function renderC4Decision(container,stages){
const chart=prepareC4Svg(container,410);
const width=chart.width;
const rootData={
stage:stages[0],
children:[
{stage:stages[1]},
{stage:stages[2],children:[{stage:stages[4]}]},
{stage:stages[3]}
]
};
const hierarchy=d3.hierarchy(rootData);
d3.tree().size([width-130,285])(hierarchy);
chart.svg.selectAll("path.ucc-c4-tree-link")
.data(hierarchy.links())
.join("path")
.attr("class","ucc-c4-tree-link")
.attr("d",d3.linkVertical()
.x(link=>link.x+65)
.y(link=>link.y+42));
const groups=chart.svg.selectAll("g.ucc-c4-tree-node")
.data(hierarchy.descendants())
.join("g")
.attr("class","ucc-c4-tree-node")
.attr("transform",node=>`translate(${node.x+65},${node.y+42})`);
groups.each(function(node){
const stage=node.data.stage;
const group=d3.select(this);
bindC4Stage(group,container);
group.append("rect")
.attr("x",-75)
.attr("y",-28)
.attr("width",150)
.attr("height",56)
.attr("rx",15)
.attr("fill",c4VisualFill(stage))
.attr("stroke",c4VisualStroke(stage))
.attr("stroke-width",2);
group.append("text")
.attr("class","ucc-c4-d3-label is-inverse")
.attr("text-anchor","middle")
.attr("y",-3)
.text(stage.label);
group.append("text")
.attr("class","ucc-c4-d3-value is-inverse")
.attr("text-anchor","middle")
.attr("y",18)
.text(c4VisualCount(stage));
addC4SourceText(group,stage,0,48,"middle");
});
}
function renderC4Radial(container,stages){
const chart=prepareC4Svg(container,380);
const width=chart.width;
const centerX=Math.min(width*.38,300);
const centerY=185;
const radius=Math.min(130,width*.23);
const values=stages.map(stage=>Math.max(1,c4FiniteNumber(stage.value,0)));
const pie=d3.pie().sort(null).value((stage,index)=>values[index])(stages);
const arc=d3.arc().innerRadius(radius*.47).outerRadius(radius);
const groups=chart.svg.append("g")
.attr("transform",`translate(${centerX},${centerY})`)
.selectAll("g.ucc-c4-radial-stage")
.data(pie)
.join("g")
.attr("class","ucc-c4-radial-stage");
bindC4Stage(groups,container,segment=>segment.data);
groups.append("path")
.attr("d",segment=>arc(segment))
.attr("fill",segment=>c4VisualFill(segment.data))
.attr("stroke","#fff")
.attr("stroke-width",3);
groups.append("text")
.attr("class","ucc-c4-d3-value is-inverse")
.attr("transform",segment=>`translate(${arc.centroid(segment)})`)
.attr("text-anchor","middle")
.text(segment=>c4VisualCount(segment.data));
const total=d3.sum(stages,stage=>c4FiniteNumber(stage.value,0));
chart.svg.append("text")
.attr("class","ucc-c4-radial-total")
.attr("x",centerX)
.attr("y",centerY-6)
.attr("text-anchor","middle")
.text(total);
chart.svg.append("text")
.attr("class","ucc-c4-d3-source")
.attr("x",centerX)
.attr("y",centerY+16)
.attr("text-anchor","middle")
.text("tracked events");
const legend=chart.svg.selectAll("g.ucc-c4-radial-legend")
.data(stages)
.join("g")
.attr("class","ucc-c4-radial-legend")
.attr("transform",(stage,index)=>`translate(${Math.max(centerX+radius+45,width*.62)},${78+index*66})`);
bindC4Stage(legend,container);
legend.append("rect")
.attr("x",0)
.attr("y",-17)
.attr("width",15)
.attr("height",15)
.attr("rx",4)
.attr("fill",c4VisualFill);
legend.append("text")
.attr("class","ucc-c4-d3-label")
.attr("x",25)
.attr("y",-4)
.text(stage=>`${stage.label}: ${c4VisualCount(stage)}`);
legend.each(function(stage){
addC4SourceText(d3.select(this),stage,25,17,"start");
});
}
function renderC4Network(container,stages){
const chart=prepareC4Svg(container,370);
const width=chart.width;
const rootStage=stages[0];
const childStages=stages.slice(1);
const rootPosition={x:width*.24,y:185};
const childPositions=childStages.map((stage,index)=>({
x:width*.74,
y:80+index*105
}));
const maxValue=d3.max(childStages,stage=>c4FiniteNumber(stage.value,0))||1;
chart.svg.selectAll("path.ucc-c4-network-link")
.data(childStages)
.join("path")
.attr("class","ucc-c4-network-link")
.attr("stroke-width",stage=>4+18*(c4FiniteNumber(stage.value,0)/maxValue))
.attr("d",(stage,index)=>{
const target=childPositions[index];
const mid=(rootPosition.x+target.x)/2;
return `M${rootPosition.x+80},${rootPosition.y} C${mid},${rootPosition.y} ${mid},${target.y} ${target.x-80},${target.y}`;
});
const allStages=[rootStage].concat(childStages);
const allPositions=[rootPosition].concat(childPositions);
const groups=chart.svg.selectAll("g.ucc-c4-network-node")
.data(allStages)
.join("g")
.attr("class","ucc-c4-network-node")
.attr("transform",(stage,index)=>`translate(${allPositions[index].x},${allPositions[index].y})`);
bindC4Stage(groups,container);
groups.append("rect")
.attr("x",-88)
.attr("y",-35)
.attr("width",176)
.attr("height",70)
.attr("rx",18)
.attr("fill",c4VisualFill)
.attr("stroke",c4VisualStroke)
.attr("stroke-width",2);
groups.append("text")
.attr("class","ucc-c4-d3-label is-inverse")
.attr("text-anchor","middle")
.attr("y",-5)
.text(stage=>stage.label);
groups.append("text")
.attr("class","ucc-c4-d3-value is-inverse")
.attr("text-anchor","middle")
.attr("y",19)
.text(c4VisualCount);
groups.each(function(stage){
addC4SourceText(d3.select(this),stage,0,55,"middle");
});
}
function renderC4Ladder(container,stages){
const chart=prepareC4Svg(container,370);
const width=chart.width;
const margin=55;
const available=width-margin*2;
const stepWidth=available/stages.length;
chart.svg.append("path")
.attr("class","ucc-c4-ladder-line")
.attr("d",d3.line().curve(d3.curveStepAfter)(
stages.map((stage,index)=>[
margin+index*stepWidth+stepWidth*.5,
285-index*58
])
));
const groups=chart.svg.selectAll("g.ucc-c4-ladder-stage")
.data(stages)
.join("g")
.attr("class","ucc-c4-ladder-stage")
.attr("transform",(stage,index)=>`translate(${margin+index*stepWidth},${270-index*58})`);
bindC4Stage(groups,container);
groups.append("rect")
.attr("x",3)
.attr("y",-35)
.attr("width",Math.max(100,stepWidth-10))
.attr("height",70)
.attr("rx",14)
.attr("fill",c4VisualFill)
.attr("stroke",c4VisualStroke)
.attr("stroke-width",2);
groups.append("text")
.attr("class","ucc-c4-d3-label is-inverse")
.attr("x",stepWidth*.5)
.attr("y",-5)
.attr("text-anchor","middle")
.text(stage=>stage.label);
groups.append("text")
.attr("class","ucc-c4-d3-value is-inverse")
.attr("x",stepWidth*.5)
.attr("y",20)
.attr("text-anchor","middle")
.text(c4VisualCount);
groups.each(function(stage){
addC4SourceText(
d3.select(this),
stage,
stepWidth*.5,
56,
"middle"
);
});
}
function renderC4VisualTable(tab,data){
const tbody=$(`[data-c4-visual-table="${CSS.escape(tab)}"]`);
if(!tbody)return;
tbody.innerHTML=data.stages.map(stage=>{
const drill=stage.metricId&&stage.status==="available"
?`<button type="button" class="record-link" data-c4-visual-drill="${escapeHtml(stage.metricId)}">View ${escapeHtml(c4VisualCount(stage))} record(s) ↗</button>`
:'<span class="ucc-c4-visual-muted">No record drill-down</span>';
const source=stage.doctype
?`<a class="source-doctype-link" href="${escapeHtml(c4DoctypeRoute(stage.doctype))}" target="_blank" rel="noopener noreferrer">Open ${escapeHtml(stage.doctype)} list ↗</a>`
:'<span class="ucc-c4-visual-muted">Source not resolved</span>';
return `<tr>
        <td><strong>${escapeHtml(stage.label)}</strong></td>
        <td>${escapeHtml(c4VisualCount(stage))}</td>
        <td><span class="ucc-c4-status-pill" data-status="${escapeHtml(stage.status)}">${escapeHtml(statusText(stage.status))}</span></td>
        <td>${source}</td>
        <td>${drill}</td>
      </tr>`;
}).join("");
$$("[data-c4-visual-drill]",tbody).forEach(button=>{
button.addEventListener("click",()=>{
openDrilldown(button.dataset.c4VisualDrill);
});
});
}
function drawC4Visual(tab,data){
const container=$(`[data-c4-visual="${CSS.escape(tab)}"]`);
if(!container)return;
const renderers={
funnel:renderC4Funnel,
lifecycle:renderC4Lifecycle,
reconciliation:renderC4Reconciliation,
decision:renderC4Decision,
radial:renderC4Radial,
network:renderC4Network,
ladder:renderC4Ladder
};
const renderer=renderers[data.type];
if(!renderer){
container.innerHTML='<div class="empty-state">No diagram renderer is configured.</div>';
return;
}
renderer(container,data.stages);
container.dataset.visualType=data.type;
}
function renderC4Visual(keyOrPanel){
const direct=state.visuals[keyOrPanel];
const keys=direct&&direct.panel&&direct.panel!==keyOrPanel?[keyOrPanel]:Object.keys(state.visuals).filter(key=>(state.visuals[key].panel||key)===keyOrPanel);
if(!keys.length&&direct)keys.push(keyOrPanel);
keys.forEach(key=>{
const data=c4VisualData(key);
if(!data)return;
renderC4VisualTable(key,data);
const container=$(`[data-c4-visual="${CSS.escape(key)}"]`);
if(!container)return;
container.innerHTML='<div class="ucc-c4-visual-loading">Preparing live diagram…</div>';
ensureC4D3().then(()=>drawC4Visual(key,data)).catch(error=>{container.innerHTML=`<div class="empty-state">Diagram unavailable: ${escapeHtml(error.message||String(error))}. Use the Table view for the same data.</div>`;});
});
}
function escapeHtml(value){
return String(value??"").replace(/[&<>"']/g,char=>({
"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"
}[char]));
}
function notify(message,indicator="blue"){
if(window.frappe&&frappe.show_alert)frappe.show_alert({message,indicator});
}
function addLog(level,event,detail){
const row={
time:new Date().toISOString(),
level:String(level||"INFO"),
event:String(event||"event"),
detail:typeof detail==="string"?detail:JSON.stringify(detail||{})
};
state.logs.push(row);
if(state.logs.length>5000)state.logs.splice(0,state.logs.length-5000);
const count=$("[data-c4-log-count]");
if(count)count.textContent=String(state.logs.length);
renderDiagnostics();
return row;
}
function statusText(status){
return {
available:"Available",
unavailable:"Source unavailable",
permission_denied:"Permission denied",
unsupported_field:"Unsupported or missing field",
error:"Runtime error",
loading:"Loading"
}[status]||status||"Unknown";
}
function filters(){
const output={};
$$("[data-c4-filter]").forEach(element=>{
output[element.dataset.c4Filter]=element.value||"";
});
return output;
}
function callApi(subcriterion,action="summary",extra={}){
return new Promise((resolve,reject)=>{
if(!(window.frappe&&frappe.call)){
reject(new Error("Frappe API client is unavailable."));
return;
}
const payload={
action,
subcriterion,
filters:filters(),
page_size:100
};
Object.keys(extra||{}).forEach(key=>payload[key]=extra[key]);
addLog("INFO","api_request",{subcriterion,action});
frappe.call({
method:"ucc_analytics_criterion_4",
args:{payload:JSON.stringify(payload)},
callback(response){
const message=response&&response.message;
if(message&&message.ok){
addLog("INFO","api_success",{
subcriterion,
action,
sources:(message.sources||[]).length,
metrics:(message.metrics||[]).length
});
resolve(message);
}else{
const errorMessage=message&&message.message||"Criterion 4 request failed.";
addLog("ERROR","api_failure",{subcriterion,action,message:errorMessage});
reject(new Error(errorMessage));
}
},
error(error){
const errorMessage=error&&error.message||"Criterion 4 request failed.";
addLog("ERROR","api_error",{subcriterion,action,message:errorMessage});
reject(error instanceof Error?error:new Error(errorMessage));
}
});
});
}
function setLoading(active,progress=0,task="Preparing…"){
const overlay=$("[data-c4-loading-overlay]");
if(overlay)overlay.classList.toggle("hidden",!active);
const fill=$("[data-c4-progress-fill]");
const value=$("[data-c4-progress-value]");
const taskNode=$("[data-c4-progress-task]");
if(fill)fill.style.width=Math.max(0,Math.min(100,progress))+"%";
if(value)value.textContent=Math.round(progress)+"%";
if(taskNode)taskNode.textContent=task;
}
function setNotice(message,status="available"){
const notice=$("[data-c4-source-notice]");
if(!notice)return;
if(notice.dataset.dismissed==="1"&&status==="available")return;
if(status!=="available")notice.dataset.dismissed="0";
notice.hidden=false;
notice.dataset.status=status;
const strong=$("strong",notice);
const span=$("span",notice);
if(strong){
strong.textContent=status==="available"
?"Criterion 4 live analytics active."
:"Criterion 4 live analytics active with limitations.";
}
if(span)span.textContent=message;
}
function sourceDetail(item){
if(item.message)return item.message;
if(Array.isArray(item.errors)&&item.errors.length){
return item.errors.map(error=>error&&error.message).filter(Boolean).join(" | ");
}
return statusText(item.status);
}
function renderMetricCards(result,tab){
(result.metrics||[]).forEach(metric=>{
const contextualMetric=Object.assign({},metric,{criterion:TAB_MAP[tab]});
state.metrics.set(metric.id,contextualMetric);
const card=root.querySelector(`[data-c4-drill="${CSS.escape(metric.id)}"]`);
if(!card)return;
const value=$("strong",card);
const detail=$("small",card);
card.dataset.mappingStatus=metric.status||"unknown";
if(value)value.textContent=metric.value===null||metric.value===undefined?"—":String(metric.value);
if(detail){
detail.textContent=metric.status==="available"
? [metric.doctype,metric.field].filter(Boolean).join(" · ")
: statusText(metric.status);
}
card.title=metric.status==="available"
? `Click to view ${metric.value||0} matching records`
: statusText(metric.status);
});
}
function renderQuestionRows(tab,result){
const tbody=$(`[data-c4-qa-table="${CSS.escape(tab)}"]`);
if(!tbody)return;
const questions=Array.isArray(result.questions)?result.questions:[];
tbody.innerHTML=questions.map(question=>{
const count=Number(question.record_count||0);
const drill=question.metric_id&&question.status==="available"
?`<button type="button" class="record-link ucc-qa-action" data-c4-question-drill="${escapeHtml(question.metric_id)}">View ${count} matching record${count===1?"":"s"} ↗</button>`
:"";
return `
      <tr>
        <td>${escapeHtml(question.criterion||result.policy?.criterion||tab)}</td>
        <td>${escapeHtml(question.question)}</td>
        <td><div>${escapeHtml(question.answer)}</div>${drill}</td>
        <td>${c4QaSourceCell(question)}</td>
        <td><span class="ucc-c4-status-pill" data-status="${escapeHtml(question.status)}">${escapeHtml(question.confidence)}</span></td>
      </tr>`;
}).join("")||'<tr><td colspan="5">No management questions are configured.</td></tr>';
$$("[data-c4-question-drill]",tbody).forEach(button=>{
button.addEventListener("click",()=>openDrilldown(button.dataset.c4QuestionDrill));
});
}
function renderSourceRows(tab,result){
const tbody=$(`[data-c4-source-table="${CSS.escape(tab)}"]`);
if(!tbody)return;
tbody.innerHTML=(result.sources||[]).map(source=>`
      <tr>
        <td>${escapeHtml(source.key)}</td>
        <td>${source.doctype
          ?`<a class="source-doctype-link" href="${escapeHtml(c4DoctypeRoute(source.doctype))}" target="_blank" rel="noopener noreferrer">Open ${escapeHtml(source.doctype)} list ↗</a>`
          :escapeHtml((source.candidates||[]).join(" / "))}</td>
        <td><span class="ucc-c4-status-pill" data-status="${escapeHtml(source.status)}">${escapeHtml(statusText(source.status))}</span></td>
        <td>${escapeHtml(sourceDetail(source))}</td>
      </tr>
    `).join("")||'<tr><td colspan="4">No source registry rows were returned.</td></tr>';
}
function renderExceptionRows(tab,result){
const panel=$(`[data-c4-panel="${CSS.escape(tab)}"]`);
if(!panel)return;
$$("[data-c4-exception-row]",panel).forEach(row=>{
const metric=state.metrics.get(row.dataset.c4ExceptionRow);
const value=$("[data-c4-exception-value]",row);
const status=$("[data-c4-exception-status]",row);
if(!metric){
if(value)value.textContent="—";
if(status)status.textContent="No mapping";
return;
}
if(value)value.textContent=metric.value===null||metric.value===undefined?"—":String(metric.value);
if(status)status.textContent=statusText(metric.status);
row.dataset.status=metric.status||"unknown";
});
}

const C4_VISUAL_EXPANSION={"c411":[{"id":"v190-c4-c411-01","title":"Admission and Counselling Funnel","type":"bar","description":"Tracks applicants from counselling through to a completed admission decision.","i":0},{"id":"v190-c4-c411-02","title":"Counselling Evidence Coverage","type":"donut","description":"Shows what share of counselling sessions have documented supporting evidence.","i":1},{"id":"v190-c4-c411-03","title":"Application Status Distribution","type":"funnel","description":"Compares how applications are distributed across each status stage.","i":2},{"id":"v190-c4-c411-07","title":"PDPA and Consent Coverage","type":"gauge","description":"Gauges what share of admissions have completed PDPA and consent capture.","i":6},{"id":"v190-c4-c411-10","title":"Counselling Source Readiness","type":"donut","description":"Tracks how readable the underlying counselling data sources currently are.","i":9}],"c421":[{"id":"v190-c4-c421-01","title":"Student Contract Lifecycle","type":"bar","description":"Maps a student contract from drafted through signature to activation.","i":0},{"id":"v190-c4-c421-02","title":"Contract Signature Coverage","type":"donut","description":"Gauges what share of student contracts have a completed signature.","i":1},{"id":"v190-c4-c421-05","title":"Contract Evidence Completeness","type":"radar","description":"Compares how complete supporting contract evidence is across students.","i":4},{"id":"v190-c4-c421-10","title":"Contract Source Readiness","type":"donut","description":"Tracks how readable the underlying student contract data sources are.","i":9}],"c422":[{"id":"v190-c4-c422-01","title":"Fee Collection Profile","type":"bar","description":"Compares fee collection results across the areas measured.","i":0},{"id":"v190-c4-c422-02","title":"Fee Protection Coverage","type":"donut","description":"Shows what share of student fees have fee protection scheme coverage.","i":1},{"id":"v190-c4-c422-03","title":"Invoice and Payment Status","type":"funnel","description":"Compares how invoices and payments are distributed across status.","i":2},{"id":"v190-c4-c422-07","title":"FPS Status Distribution","type":"gauge","description":"Shows how FPS coverage is distributed across enrolled students.","i":6},{"id":"v190-c4-c422-10","title":"Fee Source Readiness","type":"donut","description":"Tracks how readable the underlying fee data sources currently are.","i":9}],"c431":[{"id":"v190-c4-c431-01","title":"Movement Request Lifecycle","type":"bar","description":"Maps a student movement request from submitted through to actioned.","i":0},{"id":"v190-c4-c431-02","title":"Transfer Request Status","type":"donut","description":"Compares transfer requests across the different status stages.","i":1},{"id":"v190-c4-c431-07","title":"Approval Coverage","type":"gauge","description":"Gauges what share of movement requests have completed approval.","i":6},{"id":"v190-c4-c431-10","title":"Movement Source Readiness","type":"donut","description":"Tracks how readable the underlying movement request data sources are.","i":9}],"c441":[{"id":"v190-c4-c441-01","title":"Refund Request Lifecycle","type":"bar","description":"Maps a refund request from submitted through to disbursed.","i":0},{"id":"v190-c4-c441-02","title":"Refund Status Distribution","type":"donut","description":"Compares refund requests across their current status.","i":1},{"id":"v190-c4-c441-05","title":"Refund Completion Coverage","type":"radar","description":"Gauges what share of eligible refunds have been completed.","i":4},{"id":"v190-c4-c441-10","title":"Refund Source Readiness","type":"donut","description":"Tracks how readable the underlying refund data sources currently are.","i":9}],"c451":[{"id":"v190-c4-c451-01","title":"Support Service Demand","type":"bar","description":"Compares demand for student support services across categories.","i":0},{"id":"v190-c4-c451-02","title":"Support Case Status","type":"donut","description":"Shows the current status mix of student support cases.","i":1},{"id":"v190-c4-c451-07","title":"Support Outcome Coverage","type":"gauge","description":"Gauges what share of support cases reached a positive outcome.","i":6},{"id":"v190-c4-c451-10","title":"Support Source Readiness","type":"donut","description":"Tracks how readable the underlying student support data sources are.","i":9}],"c461":[{"id":"v190-c4-c461-01","title":"Attendance Status Distribution","type":"bar","description":"Compares student attendance records across each status category.","i":0},{"id":"v190-c4-c461-03","title":"Warning and Intervention Funnel","type":"funnel","description":"Tracks students from a warning issued through to intervention taken.","i":2},{"id":"v190-c4-c461-07","title":"Intervention Completion","type":"gauge","description":"Gauges what share of required interventions have been completed.","i":6},{"id":"v190-c4-c461-10","title":"Conduct Source Readiness","type":"donut","description":"Tracks how readable the underlying conduct data sources currently are.","i":9}]};
window.UCCC4VisualDefinitions=C4_VISUAL_EXPANSION
function c4ExpandedRows(result,index){
const available=(result.metrics||[]).filter(metric=>metric.status==="available");
if(!available.length){
const sourceSummary=result.source_summary||{};
const metricSummary=result.metric_summary||{};
return[
{label:"Available sources",value:Number(sourceSummary.available||0),metric:null},
{label:"Source issues",value:Number(sourceSummary.issues||0),metric:null},
{label:"Available metrics",value:Number(metricSummary.available||0),metric:null},
{label:"Metric issues",value:Number(metricSummary.issues||0),metric:null}
];
}
const size=Math.min(5,available.length);
const start=(index*size)%available.length;
const rows=[];
for(let offset=0;offset<size;offset+=1){
const metric=available[(start+offset)%available.length];
rows.push({label:metric.label,value:c4FiniteNumber(metric.value,0),metric});
}
return rows;
}
function c4ExpandedChartMarkup(chart){
return`<article class="panel ucc-c4-expanded-card" data-c4-expanded-card="${escapeHtml(chart.id)}">
<div class="panel-head">
<h2>${escapeHtml(chart.title)}<span class="ucc-card-desc-inline"> — ${escapeHtml(chart.description||"Live Criterion 4 API metrics.")}</span></h2>
<div class="mini-toggle">
<button type="button" class="active" data-c4-expanded-view="diagram">Diagram</button>
<button type="button" data-c4-expanded-view="table">Table</button>
</div>
</div>
<div class="chart ucc-c4-expanded-chart" data-c4-expanded-chart="${escapeHtml(chart.id)}"></div>
<div class="table-wrap hidden" data-c4-expanded-table="${escapeHtml(chart.id)}">
<table><thead><tr><th>Measure</th><th>Live value</th><th>Source / Calculation</th><th>Records</th></tr></thead><tbody></tbody></table>
</div>
</article>`;
}
function c4ExpandedPairs(rows){return rows.map(row=>[row.label,Number.isFinite(row.value)?row.value:0]);}
function c4ExpandedRenderBars(node,rows){
const pairs=c4ExpandedPairs(rows),max=Math.max(...pairs.map(row=>row[1]),1);
node.innerHTML=`<div class="ucc-demo-bars">${pairs.map(row=>`<div class="ucc-demo-bar"><label>${escapeHtml(row[0])}</label><div><i style="width:${Math.max(4,row[1]/max*100)}%"></i></div><strong>${escapeHtml(row[1])}</strong></div>`).join("")}</div>`;
}
function c4ExpandedRenderDonut(node,rows){
const pairs=c4ExpandedPairs(rows),total=pairs.reduce((sum,row)=>sum+row[1],0)||1;
let cursor=0;
const stops=pairs.map((row,index)=>{const start=cursor/total*360;cursor+=row[1];const end=cursor/total*360;return`var(--ucc-chart-${index%6}) ${start}deg ${end}deg`;}).join(",");
node.innerHTML=`<div class="ucc-demo-donut-layout"><div class="ucc-demo-donut" style="background:conic-gradient(${stops})"><span>${escapeHtml(total)}</span><small>Total</small></div><div class="ucc-demo-legend">${pairs.map((row,index)=>`<div><i style="background:var(--ucc-chart-${index%6})"></i><span>${escapeHtml(row[0])}</span><strong>${escapeHtml(row[1])}</strong></div>`).join("")}</div></div>`;
}
function c4ExpandedRenderFunnel(node,rows){
const pairs=c4ExpandedPairs(rows),max=Math.max(...pairs.map(row=>row[1]),1);
node.innerHTML=`<div class="ucc-demo-funnel">${pairs.map(row=>`<div class="ucc-demo-funnel-stage" style="width:${Math.max(38,row[1]/max*100)}%"><span>${escapeHtml(row[0])}</span><strong>${escapeHtml(row[1])}</strong></div>`).join("")}</div>`;
}
function c4ExpandedRenderLifecycle(node,rows){
node.innerHTML=`<div class="ucc-demo-lifecycle">${rows.map((row,index)=>`<div class="ucc-demo-life-step"><i>${index+1}</i><span>${escapeHtml(row.label)}</span><strong>${escapeHtml(row.value)}</strong></div>${index<rows.length-1?'<b aria-hidden="true">→</b>':""}`).join("")}</div>`;
}
function c4ExpandedRenderMatrix(node,rows){
const max=Math.max(...rows.map(row=>c4FiniteNumber(row.value,0)),1);
node.innerHTML=`<div class="ucc-demo-matrix">${rows.map(row=>`<div style="--ucc-intensity:${Math.max(.18,c4FiniteNumber(row.value,0)/max)}"><span>${escapeHtml(row.label)}</span><strong>${escapeHtml(row.value)}</strong></div>`).join("")}</div>`;
}
function c4ExpandedRenderGauge(node,rows){
const total=rows.reduce((sum,row)=>sum+c4FiniteNumber(row.value,0),0),value=rows.length?c4FiniteNumber(rows[0].value,0):0,pct=Math.max(0,Math.min(100,total?value/total*100:0));
node.innerHTML=`<div class="ucc-demo-gauge"><div style="--ucc-gauge:${pct}deg"><strong>${escapeHtml(value)}</strong><span>${escapeHtml(rows[0]?.label||"Live value")}</span></div></div>`;
}
function c4ExpandedRenderRadar(node,rows){
const size=320,cx=160,cy=160,radius=105,count=Math.max(rows.length,3),max=Math.max(...rows.map(row=>Number(row.value||0)),1);
const points=rows.map((row,index)=>{const angle=-Math.PI/2+index*2*Math.PI/count,r=radius*(c4FiniteNumber(row.value,0)/max);return[cx+Math.cos(angle)*r,cy+Math.sin(angle)*r];});
const axes=rows.map((row,index)=>{const angle=-Math.PI/2+index*2*Math.PI/count,x=cx+Math.cos(angle)*radius,y=cy+Math.sin(angle)*radius,lx=cx+Math.cos(angle)*(radius+28),ly=cy+Math.sin(angle)*(radius+28);return`<line x1="${cx}" y1="${cy}" x2="${x}" y2="${y}"></line><text x="${lx}" y="${ly}" text-anchor="middle">${escapeHtml(row.label)}</text>`;}).join("");
node.innerHTML=`<div class="ucc-demo-radar"><svg viewBox="0 0 ${size} ${size}"><circle cx="${cx}" cy="${cy}" r="${radius}"></circle><circle cx="${cx}" cy="${cy}" r="${radius*.66}"></circle><circle cx="${cx}" cy="${cy}" r="${radius*.33}"></circle>${axes}<polygon points="${points.map(point=>point.join(",")).join(" ")}"></polygon></svg></div>`;
}
function c4ExpandedRenderTrend(node,rows){
const width=560,height=250,pad=38,max=Math.max(...rows.map(row=>Number(row.value||0)),1),step=(width-pad*2)/Math.max(1,rows.length-1);
const points=rows.map((row,index)=>[pad+index*step,height-pad-(c4FiniteNumber(row.value,0)/max)*(height-pad*2)]);
node.innerHTML=`<div class="ucc-demo-trend"><svg viewBox="0 0 ${width} ${height}"><line class="axis" x1="${pad}" y1="${height-pad}" x2="${width-pad}" y2="${height-pad}"></line><polyline points="${points.map(point=>point.join(",")).join(" ")}"></polyline>${points.map((point,index)=>`<circle cx="${point[0]}" cy="${point[1]}" r="5"></circle><text x="${point[0]}" y="${height-10}" text-anchor="middle">${escapeHtml(rows[index].label)}</text>`).join("")}</svg></div>`;
}
function c4ExpandedRenderChart(node,type,rows){
if(!rows.length){node.innerHTML='<div class="empty-state">No readable live metric for this visual.</div>';return;}
if(type==="donut")return c4ExpandedRenderDonut(node,rows);
if(type==="funnel")return c4ExpandedRenderFunnel(node,rows);
if(type==="lifecycle")return c4ExpandedRenderLifecycle(node,rows);
if(type==="matrix")return c4ExpandedRenderMatrix(node,rows);
if(type==="gauge")return c4ExpandedRenderGauge(node,rows);
if(type==="radar")return c4ExpandedRenderRadar(node,rows);
if(type==="trend")return c4ExpandedRenderTrend(node,rows);
return c4ExpandedRenderBars(node,rows);
}
function ensureC4ExpandedVisuals(tab,result){
const definitions=C4_VISUAL_EXPANSION[tab]||[];
const panel=root.querySelector(`[data-c4-panel="${CSS.escape(tab)}"]`);
if(!panel||!definitions.length)return;
let grid=panel.querySelector(":scope > .ucc-c4-expanded-grid");
if(!grid){
grid=document.createElement("div");
grid.className="grid2 ucc-c4-expanded-grid";
const qa=Array.from(panel.children).find(child=>/Management Questions and Data-Based Answers/i.test(child.textContent||""));
panel.insertBefore(grid,qa||null);
}
definitions.map((chart,index)=>({chart,index:chart.i??index})).filter(o=>o.chart.enabled!==false).sort((a,b)=>(a.chart.title||"").localeCompare(b.chart.title||"",undefined,{sensitivity:"base"})).forEach(({chart,index})=>{
if(!grid.querySelector(`[data-c4-expanded-card="${CSS.escape(chart.id)}"]`)){
grid.insertAdjacentHTML("beforeend",c4ExpandedChartMarkup(chart));
}
const card=grid.querySelector(`[data-c4-expanded-card="${CSS.escape(chart.id)}"]`);
card._c4CardPending={chart,index,result};
card.dataset.c4CardRendered="";
card.querySelectorAll("[data-c4-expanded-view]").forEach(button=>button.onclick=()=>{
renderC4ExpandedCardNow(card);
card.querySelectorAll("[data-c4-expanded-view]").forEach(item=>item.classList.toggle("active",item===button));
card.querySelector("[data-c4-expanded-chart]").classList.toggle("hidden",button.dataset.c4ExpandedView!=="diagram");
card.querySelector("[data-c4-expanded-table]").classList.toggle("hidden",button.dataset.c4ExpandedView!=="table");
});
renderC4ExpandedCardNow(card);
});
}
function renderC4ExpandedCardNow(card){
if(!card||!card._c4CardPending||card.dataset.c4CardRendered==="1")return;
const{chart,index,result}=card._c4CardPending;
const rows=c4ExpandedRows(result,index);
c4ExpandedRenderChart(card.querySelector("[data-c4-expanded-chart]"),chart.type,rows);
const tbody=card.querySelector("tbody");
tbody.innerHTML=rows.map(row=>{
const metric=row.metric;
const source=metric?.doctype?`<a class="source-doctype-link" href="${escapeHtml(c4DoctypeRoute(metric.doctype))}" target="_blank" rel="noopener noreferrer">Open ${escapeHtml(metric.doctype)} list ↗</a>`:"Live readiness calculation";
const drill=metric?.id?`<button type="button" class="record-link" data-c4-expanded-drill="${escapeHtml(metric.id)}">View ${escapeHtml(metric.record_count||metric.value||0)} matching records ↗</button>`:"—";
return`<tr><td>${escapeHtml(row.label)}</td><td>${escapeHtml(row.value)}</td><td>${source}</td><td>${drill}</td></tr>`;
}).join("");
card.querySelectorAll("[data-c4-expanded-drill]").forEach(button=>button.onclick=()=>openDrilldown(button.dataset.c4ExpandedDrill));
card.dataset.c4CardRendered="1";
}

function mergeC4ServerConfig(result){
const registry=result&&result.visual_registry;
if(registry&&typeof registry==="object")Object.assign(state.visuals,registry);
}
function renderDetailed(tab,result){
renderMetricCards(result,tab);
ensureC4ExpandedVisuals(tab,result);
renderQuestionRows(tab,result);
renderSourceRows(tab,result);
renderExceptionRows(tab,result);
renderC4Visual(tab);
const sourceSummary=result.source_summary||{};
const metricSummary=result.metric_summary||{};
const policy=result.policy||{};
const issueCount=(sourceSummary.issues||0)+(metricSummary.issues||0);
setNotice(
`Live data connected · `
+`${sourceSummary.available||0} of ${sourceSummary.total||0} sources available · `
+`${metricSummary.available||0} of ${metricSummary.total||0} metrics available`
+(issueCount?` · ${issueCount} item${issueCount===1?"":"s"} need review`:""),
issueCount?"warning":"available"
);
}
async function loadTab(tab,{force=false}={}){
const code=TAB_MAP[tab];
if(!code)return null;
if(!force&&state.results.has(tab)){
const cached=state.results.get(tab);
renderDetailed(tab,cached);
return cached;
}
const result=await callApi(code,"summary");
mergeC4ServerConfig(result);
state.results.set(tab,result);
renderDetailed(tab,result);
rebuildAggregates();
return result;
}
async function loadAll({force=false}={}){
if(state.loading)return;
state.loading=true;
const requestId=++state.requestId;
setLoading(true,2,"Preparing Criterion 4 sources");
setNotice("Loading all Criterion 4 source mappings and management answers…","loading");
try{
for(let index=0;index<API_TABS.length;index+=1){
const tab=API_TABS[index];
const code=TAB_MAP[tab];
setLoading(true,5+(index/API_TABS.length)*88,`Loading ${code}`);
if(force||!state.results.has(tab)){
const result=await callApi(code,"summary");
if(requestId!==state.requestId)return;
mergeC4ServerConfig(result);
state.results.set(tab,result);
renderDetailed(tab,result);
}
}
rebuildAggregates();
setLoading(true,98,"Rendering management answers");
setNotice("All Criterion 4 sections loaded for the current user and filters.","available");
}catch(error){
setNotice(error.message||"Unable to load Criterion 4 analytics.","error");
notify(error.message||"Criterion 4 request failed.","red");
addLog("ERROR","load_all_failed",error.message||String(error));
}finally{
state.loading=false;
setTimeout(()=>setLoading(false,100,"Complete"),120);
}
}
function rebuildAggregates(){
state.qa=[];
state.exceptions=[];
state.quality=[];
let availableSources=0;
let totalSources=0;
let availableMetrics=0;
let totalMetrics=0;
let answeredQuestions=0;
let openExceptions=0;
const gapRows=[];
const sourceRows=[];
const qualityRows=[];
API_TABS.forEach(tab=>{
const result=state.results.get(tab);
if(!result)return;
const code=TAB_MAP[tab];
const sourceSummary=result.source_summary||{};
const metricSummary=result.metric_summary||{};
availableSources+=Number(sourceSummary.available||0);
totalSources+=Number(sourceSummary.total||0);
availableMetrics+=Number(metricSummary.available||0);
totalMetrics+=Number(metricSummary.total||0);
(result.questions||[]).forEach(question=>{
state.qa.push(question);
if(question.status==="available")answeredQuestions+=1;
});
(result.exceptions||[]).forEach(metric=>{
state.exceptions.push({...metric,criterion:code});
if(metric.status==="available")openExceptions+=Number(metric.value||0);
});
(result.data_quality||[]).forEach(item=>{
state.quality.push(item);
qualityRows.push(`
          <tr>
            <td>${escapeHtml(code)}</td>
            <td>${escapeHtml(item.check)}</td>
            <td>${escapeHtml(item.source)}</td>
            <td><span class="ucc-c4-status-pill" data-status="${escapeHtml(item.status)}">${escapeHtml(statusText(item.status))}</span></td>
            <td>${escapeHtml(item.detail)}</td>
          </tr>
        `);
});
(result.sources||[]).forEach(source=>{
sourceRows.push(`
          <tr>
            <td>${escapeHtml(code)}</td>
            <td>${escapeHtml(source.key)}</td>
            <td>${escapeHtml((source.candidates||[]).join(" / "))}</td>
            <td>${source.doctype
              ?`<a class="source-doctype-link" href="${escapeHtml(c4DoctypeRoute(source.doctype))}" target="_blank" rel="noopener noreferrer">Open ${escapeHtml(source.doctype)} list ↗</a>`
              :"—"}</td>
            <td><span class="ucc-c4-status-pill" data-status="${escapeHtml(source.status)}">${escapeHtml(statusText(source.status))}</span></td>
            <td>${escapeHtml(sourceDetail(source))}</td>
          </tr>
        `);
});
const sourcePct=sourceSummary.total?Math.round((sourceSummary.available/sourceSummary.total)*100):0;
const metricPct=metricSummary.total?Math.round((metricSummary.available/metricSummary.total)*100):0;
gapRows.push(`
        <article>
          <div><strong>${escapeHtml(code)}</strong><span>${sourceSummary.available||0}/${sourceSummary.total||0} sources · ${metricSummary.available||0}/${metricSummary.total||0} metrics</span></div>
          <div class="ucc-c4-gap-track"><i style="width:${Math.round((sourcePct+metricPct)/2)}%"></i></div>
        </article>
      `);
});
const setKpi=(name,value)=>{
const node=$(`[data-c4-overall-kpi="${name}"]`);
if(node)node.textContent=String(value);
};
setKpi("sources",`${availableSources}/${totalSources}`);
setKpi("metrics",`${availableMetrics}/${totalMetrics}`);
setKpi("questions",answeredQuestions);
setKpi("exceptions",openExceptions);
setKpi("quality",state.quality.length);
const gap=$("[data-c4-gap-summary]");
if(gap)gap.innerHTML=gapRows.join("")||'<div class="empty-state">Load Criterion 4 data to see target gaps.</div>';
const sourceSummaryBox=$("[data-c4-source-summary]");
if(sourceSummaryBox){
const unavailable=Math.max(0,totalSources-availableSources);
sourceSummaryBox.innerHTML=`
        <article><strong>${availableSources}</strong><span>Available</span></article>
        <article><strong>${unavailable}</strong><span>Unavailable or restricted</span></article>
        <article><strong>${totalSources}</strong><span>Total checks</span></article>
      `;
}
const sourceTotal=$("[data-c4-source-total]");
if(sourceTotal)sourceTotal.textContent=`${totalSources} source checks`;
const qualityTable=$("[data-c4-quality-table]");
if(qualityTable){
qualityTable.innerHTML=qualityRows.join("")
||'<tr><td colspan="5">No source or field issues were reported.</td></tr>';
}
const registryTable=$("[data-c4-registry-table]");
if(registryTable){
registryTable.innerHTML=sourceRows.join("")
||'<tr><td colspan="6">Load Criterion 4 data to populate the source registry.</td></tr>';
}
renderOverviewQa();
renderC4Visual("overview");
const updated=$("[data-c4-overview-updated]");
if(updated)updated.textContent=`Updated ${new Date().toLocaleTimeString()}`;
}
function renderOverviewQa(){
const tbody=$("[data-c4-overview-qa]");
if(!tbody)return;
const selected=$("[data-c4-qa-filter]")?.value||"";
const rows=state.qa.filter(question=>!selected||question.criterion===selected);
tbody.innerHTML=rows.map(question=>{
const count=Number(question.record_count||0);
const drill=question.metric_id&&question.status==="available"
?`<button type="button" class="record-link ucc-qa-action" data-c4-overview-drill="${escapeHtml(question.metric_id)}">View ${count} matching record${count===1?"":"s"} ↗</button>`
:"";
return `
      <tr>
        <td>${escapeHtml(question.criterion)}</td>
        <td>${escapeHtml(question.question)}</td>
        <td><div>${escapeHtml(question.answer)}</div>${drill}</td>
        <td>${c4QaSourceCell(question)}</td>
        <td><span class="ucc-c4-status-pill" data-status="${escapeHtml(question.status)}">${escapeHtml(question.confidence)}</span></td>
      </tr>`;
}).join("")||'<tr><td colspan="5">No management questions match the current filter.</td></tr>';
$$("[data-c4-overview-drill]",tbody).forEach(button=>{
button.addEventListener("click",()=>openDrilldown(button.dataset.c4OverviewDrill));
});
}
function selectTab(tab,{load=true}={}){
$$("[data-c4-tab]").forEach(button=>{
button.classList.toggle("active",button.dataset.c4Tab===tab);
});
$$("[data-c4-panel]").forEach(panel=>{
panel.classList.toggle("hidden",panel.dataset.c4Panel!==tab);
});
state.tab=tab;
root.dataset.activeC4Tab=tab;
try{
const stored={tab,filters:filters()};
localStorage.setItem(STORAGE_KEY,JSON.stringify(stored));
}catch(error){}
const url=new URL(window.location.href);
url.searchParams.set("dashboard","criterion_4");
url.searchParams.set("c4tab",tab);
history.replaceState(null,"",url.toString());
if(!load)return;
if(TAB_MAP[tab]){
loadTab(tab).catch(error=>{
setNotice(error.message||"Unable to load Criterion 4 section.","error");
notify(error.message||"Criterion 4 request failed.","red");
});
}else{
loadAll().catch(()=>{});
}
}
function currentVisiblePanel(){
return $(`[data-c4-panel="${CSS.escape(state.tab)}"]`)||root;
}
function currentTable(){
const panel=currentVisiblePanel();
return $$("table",panel).find(table=>table.offsetParent!==null)||$("table",panel);
}
const csvCell=UCCShared.csvCell;
function rowsToCsv(rows){
if(!rows||!rows.length)return "";
const columns=[];
rows.forEach(row=>{
Object.keys(row||{}).forEach(key=>{
if(!columns.includes(key))columns.push(key);
});
});
const output=[columns.map(csvCell).join(",")];
rows.forEach(row=>{
output.push(columns.map(column=>csvCell(row[column])).join(","));
});
return output.join("\n");
}
function tableToCsv(table){return UCCShared.tableToCsv(table);}
function download(name,content,type="text/csv;charset=utf-8"){return UCCShared.download(name,content,type);}
function exportCurrent(){
const table=currentTable();
if(!table){
notify("No visible table to export.","orange");
return;
}
download(`criterion-4-${state.tab}.csv`,tableToCsv(table));
}
function exportAnswers(){
if(!state.qa.length){
notify("Load Criterion 4 data before exporting answers.","orange");
return;
}
download("criterion-4-management-answers.csv",rowsToCsv(state.qa));
}
function exportExceptions(){
if(!state.exceptions.length){
notify("No Criterion 4 exception data is loaded.","orange");
return;
}
download("criterion-4-exceptions.csv",rowsToCsv(state.exceptions));
}
async function copyFilteredLink(){
const url=new URL(window.location.href);
url.searchParams.set("dashboard","criterion_4");
url.searchParams.set("c4tab",state.tab);
Object.entries(filters()).forEach(entry=>{
const key="c4_"+entry[0];
const value=entry[1];
if(value)url.searchParams.set(key,value);
else url.searchParams.delete(key);
});
try{
await navigator.clipboard.writeText(url.toString());
notify("Filtered link copied.","green");
}catch(error){
window.prompt("Copy this link",url.toString());
}
}
function renderDrilldown(metric){
const dialog=$("[data-c4-drill-dialog]");
const title=$("[data-c4-drill-title]");
const stateBox=$("[data-c4-drill-state]");
const wrap=$("[data-c4-drill-table-wrap]");
const head=$("[data-c4-drill-head-row]");
const body=$("[data-c4-drill-body]");
if(title)title.textContent=metric.label||"Criterion 4 drill-down";
if(!dialog)return;
if(typeof dialog.showModal==="function"&&!dialog.open)dialog.showModal();
else dialog.setAttribute("open","");
if(metric.status!=="available"){
if(stateBox){
stateBox.classList.remove("hidden");
stateBox.textContent=statusText(metric.status);
}
if(wrap)wrap.classList.add("hidden");
return;
}
const rows=metric.rows||[];
state.drillRows=rows;
if(!rows.length){
if(stateBox){
stateBox.classList.remove("hidden");
stateBox.textContent="No matching records for the active filters.";
}
if(wrap)wrap.classList.add("hidden");
return;
}
const columns=[];
rows.forEach(row=>{
Object.keys(row||{}).forEach(key=>{
if(!columns.includes(key))columns.push(key);
});
});
if(head)head.innerHTML="<tr>"+columns.map(column=>`<th>${escapeHtml(column)}</th>`).join("")+"</tr>";
if(body)body.innerHTML=rows.map(row=>
"<tr>"+columns.map(column=>`<td>${escapeHtml(row[column])}</td>`).join("")+"</tr>"
).join("");
if(stateBox)stateBox.classList.add("hidden");
if(wrap)wrap.classList.remove("hidden");
}
async function openDrilldown(metricId){
const metric=state.metrics.get(metricId);
if(!metric){
notify("Metric mapping has not loaded yet.","orange");
return;
}
if(metric.status!=="available"){
renderDrilldown(metric);
return;
}
try{
const code=TAB_MAP[state.tab]||metric.criterion;
const result=await callApi(code,"drilldown",{metric_id:metric.id});
renderDrilldown(result.drilldown||metric);
}catch(error){
renderDrilldown({...metric,status:"error",message:error.message});
notify(error.message||"Unable to load drill-down.","red");
}
}
function renderDiagnostics(){
const body=$("[data-c4-diagnostics-body]");
if(!body)return;
body.innerHTML=state.logs.slice().reverse().map(row=>`
      <tr>
        <td>${escapeHtml(row.time)}</td>
        <td>${escapeHtml(row.level)}</td>
        <td>${escapeHtml(row.event)}</td>
        <td>${escapeHtml(row.detail)}</td>
      </tr>
    `).join("")||'<tr><td colspan="4">No diagnostics recorded.</td></tr>';
}
function openDiagnostics(){
const dialog=$("[data-c4-diagnostics-dialog]");
if(!dialog)return;
renderDiagnostics();
if(typeof dialog.showModal==="function"&&!dialog.open)dialog.showModal();
else dialog.setAttribute("open","");
}
function closeDialog(dialog){
if(!dialog)return;
if(typeof dialog.close==="function"&&dialog.open)dialog.close();
else dialog.removeAttribute("open");
}
function bindActions(){
$$("[data-c4-tab]").forEach(button=>{
button.addEventListener("click",()=>selectTab(button.dataset.c4Tab));
});
$$("[data-c4-filter]").forEach(input=>{
input.addEventListener("change",()=>{
state.results.clear();
state.metrics.clear();
try{
localStorage.setItem(STORAGE_KEY,JSON.stringify({tab:state.tab,filters:filters()}));
}catch(error){}
if(TAB_MAP[state.tab])loadTab(state.tab,{force:true}).catch(()=>{});
else loadAll({force:true}).catch(()=>{});
});
});
$$("[data-c4-card-toggle]").forEach(toggle=>{
const card=toggle.closest(".panel");
const visual=card?card.querySelector("[data-c4-visual]"):null;
const visualTab=visual?visual.dataset.c4Visual:"";
const storageKey=visualTab?`ucc.c4.visual.${visualTab}`:"";
let initialView="diagram";
if(storageKey){
try{
initialView=localStorage.getItem(storageKey)||"diagram";
}catch(error){}
}
$$("[data-c4-card-view]",toggle).forEach(item=>{
item.classList.toggle("active",item.dataset.c4CardView===initialView);
});
if(card){
$$("[data-c4-card-panel]",card).forEach(panel=>{
panel.classList.toggle("hidden",panel.dataset.c4CardPanel!==initialView);
});
}
$$("[data-c4-card-view]",toggle).forEach(button=>{
button.addEventListener("click",()=>{
const owner=button.closest(".panel");
if(!owner)return;
const view=button.dataset.c4CardView;
$$("[data-c4-card-view]",toggle).forEach(item=>item.classList.toggle("active",item===button));
$$("[data-c4-card-panel]",owner).forEach(panel=>{
panel.classList.toggle("hidden",panel.dataset.c4CardPanel!==view);
});
if(storageKey){
try{
localStorage.setItem(storageKey,view);
}catch(error){}
}
if(view==="diagram"&&visualTab){
renderC4Visual(visualTab);
}
});
});
});
$$("[data-c4-drill]").forEach(card=>{
card.addEventListener("click",()=>openDrilldown(card.dataset.c4Drill));
});
$("[data-c4-qa-filter]")?.addEventListener("change",renderOverviewQa);
root.addEventListener("click",event=>{
const button=event.target.closest("[data-c4-action]");
if(!button)return;
const action=button.dataset.c4Action;
if(action==="refresh"){
state.results.clear();
state.metrics.clear();
loadAll({force:true}).catch(()=>{});
}
if(action==="export-current")exportCurrent();
if(action==="export-answers")exportAnswers();
if(action==="export-exceptions")exportExceptions();
if(action==="copy-link")copyFilteredLink();
if(action==="show-diagnostics")openDiagnostics();
});
$("[data-c4-drill-close]")?.addEventListener("click",()=>closeDialog($("[data-c4-drill-dialog]")));
$("[data-c4-drill-export]")?.addEventListener("click",()=>{
if(!state.drillRows.length){
notify("No drill-down rows to export.","orange");
return;
}
download(`criterion-4-${state.tab}-drilldown.csv`,rowsToCsv(state.drillRows));
});
$("[data-c4-diagnostics-close]")?.addEventListener("click",()=>closeDialog($("[data-c4-diagnostics-dialog]")));
$("[data-c4-diagnostics-clear]")?.addEventListener("click",()=>{
state.logs=[];
renderDiagnostics();
const count=$("[data-c4-log-count]");
if(count)count.textContent="0";
});
$("[data-c4-diagnostics-export]")?.addEventListener("click",()=>{
if(!state.logs.length){
notify("No diagnostics to export.","orange");
return;
}
download("criterion-4-diagnostics.csv",rowsToCsv(state.logs));
});
}
function restoreState(){
let tab="overview";
let stored={};
try{
stored=JSON.parse(localStorage.getItem(STORAGE_KEY)||"{}");
}catch(error){}
const url=new URL(window.location.href);
tab=url.searchParams.get("c4tab")||stored.tab||tab;
if(!root.querySelector(`[data-c4-tab="${CSS.escape(tab)}"]`))tab="overview";
$$("[data-c4-filter]").forEach(input=>{
const urlValue=url.searchParams.get("c4_"+input.dataset.c4Filter);
const storedValue=stored.filters&&stored.filters[input.dataset.c4Filter];
const value=urlValue!==null?urlValue:storedValue;
if(value!==undefined&&value!==null)input.value=value;
});
selectTab(tab);
}
let c4ResizeFrame=0;
window.addEventListener("resize",()=>{
if(c4ResizeFrame)return;
c4ResizeFrame=window.requestAnimationFrame(()=>{
c4ResizeFrame=0;
if(TAB_MAP[state.tab])renderC4Visual(state.tab);
});
},{passive:true});
bindActions();
addLog("INFO","criterion_4_initialized",{version:"1.9.11"});
if(!root.classList.contains("ucc-hidden")){
restoreState();
}else{
platform.addEventListener("ucc:dashboard-change",function onFirstShow(event){
if(event.detail&&event.detail.dashboard==="criterion_4"){
platform.removeEventListener("ucc:dashboard-change",onFirstShow);
restoreState();
}
});
}
})();
(function(){
"use strict";
const platform=typeof root_element!=="undefined"?root_element.querySelector("#uccIntelligencePlatform"):document.querySelector("#uccIntelligencePlatform");
if(!platform||platform.dataset.sharedHeroToolsReady==="1")return;
platform.dataset.sharedHeroToolsReady="1";
const csvCell=UCCShared.csvCell;
function dashboardOwner(toolbar){return toolbar.closest("[data-dashboard-panel]")||platform;}
function activePanel(owner){return Array.from(owner.querySelectorAll(".panel-view")).find(panel=>!panel.classList.contains("hidden")&&!panel.classList.contains("ucc-hidden"))||owner;}
function tableCandidates(owner,exceptionsOnly){const panel=activePanel(owner);let tables=Array.from(panel.querySelectorAll("table"));if(exceptionsOnly){const filtered=tables.filter(table=>/exception|gap|risk|overdue|attention|quality/i.test((table.closest(".panel")?.innerText||"")+" "+(table.className||"")));if(filtered.length)tables=filtered;}tables.sort((a,b)=>(b.offsetParent!==null?1:0)-(a.offsetParent!==null?1:0));return tables;}
function notify(message,indicator){if(window.frappe&&frappe.show_alert)frappe.show_alert({message,indicator:indicator||"blue"});}
function exportTable(owner,exceptionsOnly){const table=tableCandidates(owner,exceptionsOnly)[0];if(!table){notify("No table is available in the current section.","orange");return;}const rows=Array.from(table.rows).map(row=>Array.from(row.cells).map(cell=>csvCell(cell.innerText.trim())).join(","));UCCShared.download(exceptionsOnly?"ucc-current-exceptions.csv":"ucc-current-table.csv",rows.join("\n"),"text/csv;charset=utf-8");}
function copyLink(owner){const url=new URL(window.location.href),dashboard=owner.dataset.dashboardPanel;if(dashboard)url.searchParams.set("dashboard",dashboard);if(owner.dataset.demoActiveTab)url.searchParams.set("demo_tab",owner.dataset.demoActiveTab);if(owner.dataset.activeTab)url.searchParams.set("ucc_tab",owner.dataset.activeTab);const value=url.toString(),task=navigator.clipboard?.writeText?navigator.clipboard.writeText(value):Promise.reject(new Error("Clipboard unavailable"));task.then(()=>notify("Filtered link copied.","green")).catch(()=>window.prompt("Copy this link",value));}
function handleAction(action,owner){
if(action==="visual-navigator"){window.UCCExplore?.openNavigator(owner?.dataset?.dashboardPanel);return;}
if(action==="source-mapping"){platform.dispatchEvent(new CustomEvent("ucc:open-source-mapping",{detail:{dashboard:owner?.dataset?.dashboardPanel||""}}));return;}
if(owner&&owner.matches&&owner.matches("[data-demo-dashboard]")){owner.dispatchEvent(new CustomEvent("ucc:live-tool-action",{detail:{action}}));return;}
if(action==="export-current")exportTable(owner,false);
if(action==="export-exceptions")exportTable(owner,true);
if(action==="copy-link")copyLink(owner);
}
function toolbarMenu(toolbar){return toolbar._uccToolsMenu||toolbar.querySelector("[data-ucc-tools-menu]");}
function restoreMenu(toolbar){const menu=toolbarMenu(toolbar);if(menu&&menu.parentNode!==toolbar)toolbar.appendChild(menu);if(menu){menu.classList.remove("ucc-tools-portal");menu.style.removeProperty("top");menu.style.removeProperty("left");menu.style.removeProperty("width");}}
function positionMenu(toolbar){const trigger=toolbar.querySelector("[data-ucc-tools-trigger]"),menu=toolbarMenu(toolbar);if(!trigger||!menu||menu.hidden)return;const rect=trigger.getBoundingClientRect();const width=Math.max(220,Math.round(rect.width));const left=Math.max(8,Math.min(window.innerWidth-width-8,rect.right-width));menu.style.top=Math.round(rect.bottom+6)+"px";menu.style.left=Math.round(left)+"px";menu.style.width=width+"px";}
function close(toolbar){const trigger=toolbar.querySelector("[data-ucc-tools-trigger]"),menu=toolbarMenu(toolbar);toolbar.removeAttribute("open");if(menu)menu.hidden=true;if(trigger)trigger.setAttribute("aria-expanded","false");restoreMenu(toolbar);}
function closeAll(except){platform.querySelectorAll("[data-ucc-tools][open]").forEach(toolbar=>{if(toolbar!==except)close(toolbar);});}
platform.querySelectorAll("[data-ucc-tools]").forEach(toolbar=>{
if(toolbar.dataset.toolsReady==="1")return;
toolbar.dataset.toolsReady="1";
const trigger=toolbar.querySelector("[data-ucc-tools-trigger]"),menu=toolbar.querySelector("[data-ucc-tools-menu]");
if(!trigger||!menu)return;
toolbar._uccToolsMenu=menu;
trigger.addEventListener("click",event=>{event.preventDefault();event.stopPropagation();const opening=!toolbar.hasAttribute("open");closeAll(toolbar);if(!opening){close(toolbar);return;}toolbar.setAttribute("open","");trigger.setAttribute("aria-expanded","true");menu.classList.add("ucc-tools-portal");document.body.appendChild(menu);menu.hidden=false;positionMenu(toolbar);});
menu.addEventListener("click",event=>{const button=event.target.closest("[data-ucc-tool-action]");if(!button)return;event.preventDefault();event.stopPropagation();handleAction(button.dataset.uccToolAction,dashboardOwner(toolbar));close(toolbar);});
});
document.addEventListener("click",event=>{if(!event.target.closest("[data-ucc-tools]")&&!event.target.closest(".ucc-tools-portal"))closeAll();});
document.addEventListener("keydown",event=>{if(event.key==="Escape")closeAll();});
window.addEventListener("resize",()=>platform.querySelectorAll("[data-ucc-tools][open]").forEach(positionMenu));
document.addEventListener("scroll",()=>platform.querySelectorAll("[data-ucc-tools][open]").forEach(positionMenu),true);
})();
(function(){
"use strict";
const platform=typeof root_element!=="undefined"
?root_element.querySelector("#uccIntelligencePlatform")
:document.querySelector("#uccIntelligencePlatform");
if(!platform||platform.dataset.criterionNoticesReady==="1")return;
platform.dataset.criterionNoticesReady="1";
platform.querySelectorAll("[data-notice-dismiss]").forEach(button=>{
button.addEventListener("click",()=>{
const notice=button.closest(".ucc-criterion-notice");
if(!notice)return;
notice.dataset.dismissed="1";
notice.hidden=true;
});
});
})();

/* UCC Intelligence Platform v1.8.2 integrated interaction controls */
(function () {
"use strict";

const root = typeof root_element !== "undefined"
? root_element.querySelector("#uccIntelligencePlatform")
: document.querySelector("#uccIntelligencePlatform");

if (!root || root.dataset.v182ControlsReady === "1") return;
root.dataset.v182ControlsReady = "1";

function closeToolMenus(except) {
root.querySelectorAll(".ucc-hero-tools[open]").forEach(function (details) {
if (details !== except) {
details.removeAttribute("open");
const summary = details.querySelector("summary");
if (summary) summary.setAttribute("aria-expanded", "false");
}
});
}

root.querySelectorAll(".ucc-hero-tools").forEach(function (details) {
const summary = details.querySelector(":scope > summary");
if (!summary) return;
summary.setAttribute("role", "button");
summary.setAttribute("aria-expanded", details.hasAttribute("open") ? "true" : "false");
summary.addEventListener("click", function (event) {
event.preventDefault();
event.stopPropagation();
const willOpen = !details.hasAttribute("open");
closeToolMenus(details);
details.toggleAttribute("open", willOpen);
summary.setAttribute("aria-expanded", willOpen ? "true" : "false");
});
details.querySelectorAll("button").forEach(function (button) {
button.addEventListener("click", function () {
details.removeAttribute("open");
summary.setAttribute("aria-expanded", "false");
});
});
});

document.addEventListener("click", function (event) {
if (!event.target.closest(".ucc-hero-tools")) closeToolMenus();
});
document.addEventListener("keydown", function (event) {
if (event.key === "Escape") closeToolMenus();
});

root.addEventListener("click", function (event) {
const tab = event.target.closest("[data-ucc-placeholder-tab]");
if (!tab) return;
const dashboard = tab.closest("[data-dashboard-panel]");
if (!dashboard) return;
const key = tab.dataset.uccPlaceholderTab;
dashboard.querySelectorAll("[data-ucc-placeholder-tab]").forEach(function (button) {
button.classList.toggle("is-active", button === tab);
});
dashboard.querySelectorAll("[data-ucc-placeholder-panel]").forEach(function (panel) {
const active = panel.dataset.uccPlaceholderPanel === key;
panel.hidden = !active;
panel.classList.toggle("is-active", active);
});
});

})();
/* UCC live foundation analytics v1.9.11 */
(function(){
"use strict";
const platform=typeof root_element!=="undefined"?root_element.querySelector("#uccIntelligencePlatform"):document.querySelector("#uccIntelligencePlatform");
if(!platform||platform.dataset.liveFoundationReady==="1")return;
platform.dataset.liveFoundationReady="1";
const CONFIG={"criterion_1":{"number":"1","title":"Leadership and Strategic Planning","description":"Live, permission-aware analytics foundation for leadership, governance and strategic planning. Source and metric availability is resolved from ERPNext permissions.","subcriteria":[["1.1.1","Leadership and Corporate Governance"],["1.2.1","Strategic Planning"]],"sections":{"overview":{"title":"Overview","charts":[{"id":"criterion_1-overview-targets","title":"Target Gap Summary","type":"bar"},{"id":"criterion_1-overview-sources","title":"Source Availability","type":"donut"}]},"1.1":{"title":"Leadership and Corporate Governance","charts":[{"id":"criterion_1-11-coverage","title":"Leadership and Corporate Governance Control Coverage","type":"bar"},{"id":"criterion_1-11-status","title":"Leadership and Corporate Governance Status Distribution","type":"donut"}]},"1.2":{"title":"Strategic Planning","charts":[{"id":"criterion_1-12-coverage","title":"Strategic Planning Control Coverage","type":"bar"},{"id":"criterion_1-12-status","title":"Strategic Planning Status Distribution","type":"donut"}]},"1.1.1":{"title":"Leadership and Corporate Governance","charts":[{"id":"criterion_1-11-coverage","title":"Leadership and Corporate Governance Control Coverage","type":"bar"},{"id":"criterion_1-11-status","title":"Leadership and Corporate Governance Status Distribution","type":"donut"}]},"1.2.1":{"title":"Strategic Planning","charts":[{"id":"criterion_1-12-coverage","title":"Strategic Planning Control Coverage","type":"bar"},{"id":"criterion_1-12-status","title":"Strategic Planning Status Distribution","type":"donut"}]}},"apiMethod":"ucc_analytics_criterion_1","defaultSection":"1.1.1","apiSections":{"overview":"1.1.1","1.1.1":"1.1.1","1.2.1":"1.2.1","quality":"1.1.1","sources":"1.1.1"},"panelMap":{"overview":"overview","1.1.1":"1.1","1.2.1":"1.2","quality":"quality","sources":"sources"}},"criterion_2":{"number":"2","title":"Corporate Administration","description":"Live, permission-aware analytics foundation for human resources, communication, knowledge management and feedback. Unsupported fields are shown explicitly.","subcriteria":[["2.1.1","Staff Selection and Management"],["2.1.2","Staff Training and Development"],["2.2.1","Internal and External Communication"],["2.3.1","Data and Information Management"],["2.3.2","Knowledge Management"],["2.4.1","Feedback Management"],["2.4.2","Student Satisfaction Survey"],["2.4.3","Staff Satisfaction Survey"]],"sections":{"overview":{"title":"Overview","charts":[{"id":"criterion_2-overview-targets","title":"Target Gap Summary","type":"bar"},{"id":"criterion_2-overview-sources","title":"Source Availability","type":"donut"}]},"2.1":{"title":"Human Resource","charts":[{"id":"criterion_2-21-coverage","title":"Human Resource Control Coverage","type":"bar"},{"id":"criterion_2-21-status","title":"Human Resource Status Distribution","type":"donut"}]},"2.2":{"title":"Communication","charts":[{"id":"criterion_2-22-coverage","title":"Communication Control Coverage","type":"bar"},{"id":"criterion_2-22-status","title":"Communication Status Distribution","type":"donut"}]},"2.3":{"title":"Data, Information and Knowledge Management","charts":[{"id":"criterion_2-23-coverage","title":"Data, Information and Knowledge Management Control Coverage","type":"bar"},{"id":"criterion_2-23-status","title":"Data, Information and Knowledge Management Status Distribution","type":"donut"}]},"2.4":{"title":"Feedback Management","charts":[{"id":"criterion_2-24-coverage","title":"Feedback Management Control Coverage","type":"bar"},{"id":"criterion_2-24-status","title":"Feedback Management Status Distribution","type":"donut"}]},"2.1.1":{"title":"Human Resource","charts":[{"id":"criterion_2-21-coverage","title":"Human Resource Control Coverage","type":"bar"},{"id":"criterion_2-21-status","title":"Human Resource Status Distribution","type":"donut"}]},"2.1.2":{"title":"Staff Training and Development","charts":[{"id":"criterion_2-21-coverage","title":"Human Resource Control Coverage","type":"bar"},{"id":"criterion_2-21-status","title":"Human Resource Status Distribution","type":"donut"}]},"2.2.1":{"title":"Communication","charts":[{"id":"criterion_2-22-coverage","title":"Communication Control Coverage","type":"bar"},{"id":"criterion_2-22-status","title":"Communication Status Distribution","type":"donut"}]},"2.3.1":{"title":"Data, Information and Knowledge Management","charts":[{"id":"criterion_2-23-coverage","title":"Data, Information and Knowledge Management Control Coverage","type":"bar"},{"id":"criterion_2-23-status","title":"Data, Information and Knowledge Management Status Distribution","type":"donut"}]},"2.3.2":{"title":"Knowledge Management","charts":[{"id":"criterion_2-23-coverage","title":"Data, Information and Knowledge Management Control Coverage","type":"bar"},{"id":"criterion_2-23-status","title":"Data, Information and Knowledge Management Status Distribution","type":"donut"}]},"2.4.1":{"title":"Feedback Management","charts":[{"id":"criterion_2-24-coverage","title":"Feedback Management Control Coverage","type":"bar"},{"id":"criterion_2-24-status","title":"Feedback Management Status Distribution","type":"donut"}]},"2.4.2":{"title":"Student Satisfaction Survey","charts":[{"id":"criterion_2-24-coverage","title":"Feedback Management Control Coverage","type":"bar"},{"id":"criterion_2-24-status","title":"Feedback Management Status Distribution","type":"donut"}]},"2.4.3":{"title":"Staff Satisfaction Survey","charts":[{"id":"criterion_2-24-coverage","title":"Feedback Management Control Coverage","type":"bar"},{"id":"criterion_2-24-status","title":"Feedback Management Status Distribution","type":"donut"}]}},"apiMethod":"ucc_analytics_criterion_2","defaultSection":"2.1.1","apiSections":{"overview":"2.1.1","2.1.1":"2.1.1","2.1.2":"2.1.2","2.2.1":"2.2.1","2.3.1":"2.3.1","2.3.2":"2.3.2","2.4.1":"2.4.1","2.4.2":"2.4.2","2.4.3":"2.4.3","quality":"2.1.1","sources":"2.1.1"},"panelMap":{"overview":"overview","2.1.1":"2.1","2.1.2":"2.1","2.2.1":"2.2","2.3.1":"2.3","2.3.2":"2.3","2.4.1":"2.4","2.4.2":"2.4","2.4.3":"2.4","quality":"quality","sources":"sources"}},"criterion_5":{"number":"5","title":"Academic Systems and Processes","description":"Lightweight, permission-aware analytics foundation for course design, review, planning, delivery, partnerships, student feedback and assessment. Unsupported fields are shown explicitly.","subcriteria":[["5.1.1","Course Design and Development"],["5.1.2","Course Review"],["5.2.1","Course Planning"],["5.2.2","Course Delivery"],["5.3.1","Partnerships"],["5.4","Student Feedback and Learning Support"],["5.5","Assessment"]],"sections":{"overview":{"title":"Overview","charts":[{"id":"c5-overview-readiness","title":"Academic System Readiness","type":"bar","description":"Compares the live academic-system metrics returned for the selected Criterion 5 area.","i":0},{"id":"c5-overview-availability","title":"Source Availability","type":"donut","description":"Shows readable sources, source issues, readable metrics and metric issues.","i":1},{"id":"c5-overview-health","title":"Criterion 5 System Health","type":"matrix","description":"Summarises available metrics, unavailable metrics, sources and exceptions.","i":2},{"id":"c5-overview-exceptions","title":"Criterion 5 Exception Profile","type":"funnel","description":"Highlights live exceptions that require academic or data-quality follow-up.","i":3}]},"5.1.1":{"title":"Course Design and Development","charts":[{"id":"c5-511-coverage","title":"Course Design Control Coverage","type":"bar","description":"Compares course proposal, module design, programme mapping and assessment-plan evidence.","i":0},{"id":"c5-511-status","title":"Course Design Status Distribution","type":"donut","description":"Shows available design metrics, source readiness and exceptions.","i":1},{"id":"c5-511-readiness","title":"Course Design Evidence Readiness","type":"radar","description":"Compares readiness across the main course design and development controls.","i":2},{"id":"c5-511-gaps","title":"Course Design Gap Profile","type":"funnel","description":"Highlights course design controls that require follow-up.","i":3}]},"5.1.2":{"title":"Course Review","charts":[{"id":"c5-512-coverage","title":"Course Review Control Coverage","type":"bar","description":"Compares module review, course review, approval and recommendation evidence.","i":0},{"id":"c5-512-status","title":"Course Review Status Distribution","type":"donut","description":"Shows review source and metric readiness.","i":1},{"id":"c5-512-cycle","title":"Course Review Lifecycle","type":"lifecycle","description":"Follows review evidence from recorded through approval and recommendation follow-up.","i":2},{"id":"c5-512-gaps","title":"Review Exception Profile","type":"funnel","description":"Highlights overdue or incomplete review controls.","i":3}]},"5.2.1":{"title":"Course Planning","charts":[{"id":"c5-521-coverage","title":"Course Planning Control Coverage","type":"bar","description":"Compares intake, module class, schedule and student-contract planning evidence.","i":0},{"id":"c5-521-status","title":"Course Planning Status Distribution","type":"donut","description":"Shows planning source and metric readiness.","i":1},{"id":"c5-521-flow","title":"Planning Readiness Flow","type":"lifecycle","description":"Follows planning evidence from intake through class, schedule and contract readiness.","i":2},{"id":"c5-521-gaps","title":"Planning Exception Profile","type":"funnel","description":"Highlights incomplete planning controls requiring follow-up.","i":3}]},"5.2.2":{"title":"Course Delivery","charts":[{"id":"c5-522-coverage","title":"Course Delivery Control Coverage","type":"bar","description":"Compares schedules, attendance, observations and sign-off evidence.","i":0},{"id":"c5-522-status","title":"Course Delivery Status Distribution","type":"donut","description":"Shows delivery source and metric readiness.","i":1},{"id":"c5-522-readiness","title":"Delivery Evidence Readiness","type":"radar","description":"Compares attendance, observation and sign-off evidence across delivery controls.","i":2},{"id":"c5-522-gaps","title":"Delivery Exception Profile","type":"funnel","description":"Highlights delivery controls requiring follow-up.","i":3}]},"5.3.1":{"title":"Partnerships","charts":[{"id":"c5-531-coverage","title":"Partnership Control Coverage","type":"bar","description":"Compares agreement, monitoring, evaluation and provider-rating evidence.","i":0},{"id":"c5-531-status","title":"Partnership Status Distribution","type":"donut","description":"Shows partnership source and metric readiness.","i":1},{"id":"c5-531-risk","title":"Partnership Risk Profile","type":"funnel","description":"Highlights expiry, NDA and threshold risks requiring follow-up.","i":2},{"id":"c5-531-readiness","title":"Partnership Evidence Readiness","type":"matrix","description":"Grids readiness across partnership management controls.","i":3}]},"5.4":{"title":"Student Feedback and Learning Support","charts":[{"id":"c5-54-coverage","title":"Student Feedback Control Coverage","type":"bar","description":"Compares survey, score and attendance-risk evidence.","i":0},{"id":"c5-54-status","title":"Student Feedback Status Distribution","type":"donut","description":"Shows feedback source and metric readiness.","i":1},{"id":"c5-54-readiness","title":"Feedback Evidence Readiness","type":"radar","description":"Compares survey and learning-support evidence across key controls.","i":2},{"id":"c5-54-gaps","title":"Feedback Exception Profile","type":"funnel","description":"Highlights feedback controls requiring follow-up.","i":3}]},"5.5":{"title":"Assessment","charts":[{"id":"c5-55-coverage","title":"Assessment Control Coverage","type":"bar","description":"Compares assessment plans, control fields, results, grades and scores.","i":0},{"id":"c5-55-status","title":"Assessment Status Distribution","type":"donut","description":"Shows assessment source and metric readiness.","i":1},{"id":"c5-55-readiness","title":"Assessment Evidence Readiness","type":"radar","description":"Compares readiness across assessment planning and result controls.","i":2},{"id":"c5-55-gaps","title":"Assessment Exception Profile","type":"funnel","description":"Highlights assessment controls requiring correction or follow-up.","i":3}]},"quality":{"title":"Data Quality","charts":[]},"sources":{"title":"Sources","charts":[]}},"apiMethod":"ucc_analytics_criterion_5","defaultSection":"5.1.1","apiSections":{"overview":"5.1.1","5.1.1":"5.1.1","5.1.2":"5.1.2","5.2.1":"5.2.1","5.2.2":"5.2.2","5.3.1":"5.3.1","5.4":"5.4","5.5":"5.5","quality":"5.1.1","sources":"5.1.1"},"panelMap":{"overview":"overview","5.1.1":"5.1.1","5.1.2":"5.1.2","5.2.1":"5.2.1","5.2.2":"5.2.2","5.3.1":"5.3.1","5.4":"5.4","5.5":"5.5","quality":"quality","sources":"sources"}},"criterion_3":{"number":"3","title":"External Recruitment Agents","description":"Policy-aligned live analytics foundation for agent selection, appointment, onboarding, performance evaluation, renewal and offboarding. Unsupported fields are shown explicitly.","policy_set":[{"code":"PPD-SES-SL-3.1.1","version":"1.2","title":"Selection and Appointment of External Recruitment Agents","updated":"15 January 2026"},{"code":"PPD-SES-SL-3.2.1","version":"1.2","title":"Management and Evaluation of Recruitment Agents","updated":"15 January 2026"}],"subcriteria":[["3.1.1","Selection and Appointment"],["3.2.1","Management and Evaluation"]],"filters":[["review_year","Review Year",["All Review Years","2026","2025"]],["agent_status","Agent Status",["All Agent Statuses","Active","Pending","Inactive"]],["market","Market / Region",["All Markets","Southeast Asia","South Asia","Greater China","Other"]],["renewal_cycle","Renewal Cycle",["All Renewal Cycles","June","December"]]],"sections":{"overview":{"title":"Criterion 3 Overview","charts":[{"id":"c3-overview-lifecycle","title":"Agent Lifecycle Coverage","type":"lifecycle"},{"id":"c3-overview-policy","title":"Policy Control Coverage","type":"donut"},{"id":"c3-overview-health","title":"Agent Control Health","type":"radar"},{"id":"c3-overview-renewal","title":"Renewal and Evaluation Trend","type":"trend"},{"id":"c3-overview-exceptions","title":"Open Exception Profile","type":"bar"}]},"3.1.1":{"title":"Selection and Appointment of External Recruitment Agents","charts":[{"id":"c311-identification","title":"Identification Pathways","type":"donut"},{"id":"c311-screening","title":"Selection and Screening Funnel","type":"funnel"},{"id":"c311-weighting","title":"Selection Criteria Weighting","type":"radar"},{"id":"c311-score","title":"Selection Score Distribution","type":"bar"},{"id":"c311-approval","title":"Approval and Background Check","type":"lifecycle"},{"id":"c311-contract","title":"Contract and NDA Readiness","type":"matrix"},{"id":"c311-listing","title":"Agent Listing and Status","type":"donut"}]},"3.2.1":{"title":"Management and Evaluation of Recruitment Agents","charts":[{"id":"c321-onboarding","title":"Agent Onboarding Funnel","type":"funnel"},{"id":"c321-training","title":"Training Coverage","type":"radar"},{"id":"c321-service","title":"Service Delivery Controls","type":"matrix"},{"id":"c321-evaluation","title":"Performance Evaluation Distribution","type":"bar"},{"id":"c321-renewal","title":"Renewal Checkpoint Flow","type":"lifecycle"},{"id":"c321-complaints","title":"Complaints and Breaches","type":"donut"},{"id":"c321-offboarding","title":"Offboarding and Exit Security","type":"flow"}]}},"apiMethod":"ucc_analytics_criterion_3","defaultSection":"3.1.1","apiSections":{"overview":"3.1.1","3.1.1":"3.1.1","3.2.1":"3.2.1","quality":"3.1.1","sources":"3.1.1"},"panelMap":{"overview":"overview","3.1.1":"3.1.1","3.2.1":"3.2.1","quality":"quality","sources":"sources"}},"criterion_6":{"number":"6","title":"Quality Assurance, Innovation and Continual Improvement","description":"Policy-aligned live analytics foundation for audits, management review, innovation, providers, risk and business continuity. Unsupported fields are shown explicitly.","policy_set":[{"code":"PPD-SGL-SQ-6.1.1","version":"1.2","title":"Internal Assessment and Quality Audits","updated":"15 January 2026"},{"code":"PPD-SGL-SQ-6.2.1","version":"1.3","title":"Management Review","updated":"10 April 2026"},{"code":"PPD-SGL-SQ-6.3.1","version":"1.2","title":"Innovation and Continual Improvement","updated":"15 January 2026"},{"code":"PPD-OE-FN-6.4.1","version":"1.2","title":"Provider's Accreditation and Evaluation","updated":"15 January 2026"},{"code":"PPD-SGL-SQ-6.5.3","version":"1.2","title":"Hazard Identification and Risk Assessment","updated":"15 January 2026"}],"subcriteria":[["6.1.1","Internal Assessment and Quality Audits"],["6.2.1","Management Review"],["6.3.1","Innovation and Continual Improvement"],["6.4.1","Provider Accreditation and Evaluation"],["6.5.3","Hazard Identification and Risk Assessment"]],"filters":[["review_year","Review Year",["All Review Years","2026","2025"]],["department","Department",["All Departments","SGL / SQ","Academic","Student Services","Finance"]],["quality_area","Quality Area",["All Quality Areas","Audit","Management Review","Innovation","Providers","Risk"]],["month","Month",["All Months","January 2026","April 2026","July 2026","December 2026"]]],"sections":{"overview":{"title":"Criterion 6 Overview","charts":[{"id":"c6-overview-cycle","title":"Quality Management Cycle","type":"lifecycle"},{"id":"c6-overview-policy","title":"Policy Evidence Coverage","type":"donut"},{"id":"c6-overview-health","title":"Quality System Health","type":"radar"},{"id":"c6-overview-calendar","title":"Quality Calendar Completion","type":"trend"},{"id":"c6-overview-actions","title":"Action Status","type":"bar"},{"id":"c6-overview-readiness","title":"Source Readiness","type":"matrix"}]},"6.1.1":{"title":"Internal Assessment and Quality Audits","charts":[{"id":"c611-programme","title":"Annual Audit Programme","type":"donut"},{"id":"c611-scope","title":"Audit Scope Coverage","type":"radar"},{"id":"c611-lifecycle","title":"Audit Lifecycle","type":"funnel"},{"id":"c611-auditors","title":"Auditor Qualification and Independence","type":"matrix"},{"id":"c611-findings","title":"Audit Findings by Severity","type":"bar"},{"id":"c611-cap","title":"Corrective Action Closure","type":"trend"}]},"6.2.1":{"title":"Management Review","charts":[{"id":"c621-thesis","title":"THESIS Review Coverage","type":"radar"},{"id":"c621-preparation","title":"Management Review Preparation","type":"funnel"},{"id":"c621-inputs","title":"Review Input Completeness","type":"matrix"},{"id":"c621-outputs","title":"Review Outputs","type":"donut"},{"id":"c621-ageing","title":"Action Ageing","type":"bar"},{"id":"c621-effectiveness","title":"Action Effectiveness","type":"trend"}]},"6.3.1":{"title":"Innovation and Continual Improvement","charts":[{"id":"c631-types","title":"Innovation Type Mix","type":"donut"},{"id":"c631-lifecycle","title":"Improvement Initiative Lifecycle","type":"funnel"},{"id":"c631-investment","title":"Innovation Performance Categories","type":"radar"},{"id":"c631-qipi","title":"QIPI Outcome Trend","type":"trend"},{"id":"c631-impact","title":"Before and After Impact","type":"gauge"},{"id":"c631-status","title":"Improvement Action Status","type":"matrix"}]},"6.4.1":{"title":"Provider's Accreditation and Evaluation","charts":[{"id":"c641-tier","title":"Provider Tier Profile","type":"donut"},{"id":"c641-screening","title":"Provider Accreditation Funnel","type":"funnel"},{"id":"c641-package","title":"Compliance Package","type":"matrix"},{"id":"c641-delivery","title":"Service Delivery and Purchase Controls","type":"lifecycle"},{"id":"c641-rating","title":"Provider Rating Weighting","type":"radar"},{"id":"c641-outcomes","title":"Provider Evaluation Outcomes","type":"donut"}]},"6.5.3":{"title":"Hazard Identification and Risk Assessment","charts":[{"id":"c653-reporting","title":"Hazard Reporting Funnel","type":"funnel"},{"id":"c653-levels","title":"Risk Level Distribution","type":"donut"},{"id":"c653-matrix","title":"5×5 Risk Matrix","type":"risk-matrix"},{"id":"c653-treatment","title":"Risk Treatment Lifecycle","type":"lifecycle"},{"id":"c653-residual","title":"Residual Risk Trend","type":"trend"},{"id":"c653-bcdr","title":"Business Continuity Readiness","type":"radar"}]}},"apiMethod":"ucc_analytics_criterion_6","defaultSection":"6.1.1","apiSections":{"overview":"6.1.1","6.1.1":"6.1.1","6.2.1":"6.2.1","6.3.1":"6.3.1","6.4.1":"6.4.1","6.5.3":"6.5.3","quality":"6.1.1","sources":"6.1.1"},"panelMap":{"overview":"overview","6.1.1":"6.1.1","6.2.1":"6.2.1","6.3.1":"6.3.1","6.4.1":"6.4.1","6.5.3":"6.5.3","quality":"quality","sources":"sources"}},"criterion_7":{"number":"7","title":"Performance Outcomes","description":"Live, permission-aware analytics foundation for outcome measurement, target achievement and stakeholder performance. Unsupported fields are shown explicitly.","subcriteria":[["7.1.1","Measurement of Outcomes"]],"sections":{"overview":{"title":"Overview","charts":[{"id":"criterion_7-overview-targets","title":"Target Gap Summary","type":"bar"},{"id":"criterion_7-overview-sources","title":"Source Availability","type":"donut"}]},"7.1":{"title":"Measurement of Outcomes","charts":[{"id":"criterion_7-71-coverage","title":"Measurement of Outcomes Control Coverage","type":"bar"},{"id":"criterion_7-71-status","title":"Measurement of Outcomes Status Distribution","type":"donut"}]},"7.1.1":{"title":"Measurement of Outcomes","charts":[{"id":"criterion_7-71-coverage","title":"Measurement of Outcomes Control Coverage","type":"bar"},{"id":"criterion_7-71-status","title":"Measurement of Outcomes Status Distribution","type":"donut"}]}},"apiMethod":"ucc_analytics_criterion_7","defaultSection":"7.1.1","apiSections":{"overview":"7.1.1","7.1.1":"7.1.1","quality":"7.1.1","sources":"7.1.1"},"panelMap":{"overview":"overview","7.1.1":"7.1","quality":"quality","sources":"sources"}}};
const LIVE_VISUAL_EXPANSION={"criterion_1":{"overview":[{"id":"v190-c1-overview-01","title":"Governance and Strategy Metric Profile","type":"bar","description":"Compares key governance and strategic planning metrics side by side for this criterion.","i":0},{"id":"v190-c1-overview-02","title":"Live Source Availability","type":"donut","description":"Shows what share of the underlying DocTypes and fields are currently readable.","i":1},{"id":"v190-c1-overview-06","title":"Evidence Readiness Matrix","type":"matrix","description":"Grids evidence completeness against each governance and strategy control area.","i":5},{"id":"v190-c1-overview-08","title":"Leadership Responsibility Coverage","type":"trend","description":"Tracks over time how many leadership roles have clearly assigned responsibilities.","i":7},{"id":"v190-c1-overview-17","title":"Governance Risk Exposure","type":"bar","description":"Compares governance risk exposure across the areas this criterion covers.","i":16},{"id":"v190-c1-overview-20","title":"Evidence Completeness","type":"lifecycle","description":"Follows evidence records from missing through to fully documented and verified.","i":19},{"id":"v190-c1-overview-27","title":"Target Achievement Gauge","type":"funnel","description":"Tracks strategic targets from set through to fully achieved.","i":26},{"id":"v190-c1-overview-28","title":"Overall Criterion Readiness","type":"lifecycle","description":"Summarises how ready Criterion 1 is overall, from raw data through to verified evidence.","i":27}],"1.1.1":[{"id":"v190-c1-111-01","title":"Governance Control Coverage","type":"bar","description":"Compares how many governance controls are in place across different control areas.","i":0},{"id":"v190-c1-111-02","title":"Governance Status Distribution","type":"donut","description":"Shows the current status mix of governance records, from open to resolved.","i":1},{"id":"v190-c1-111-03","title":"Leadership and Role Readiness","type":"funnel","description":"Tracks leadership roles from defined through to fully staffed and ready.","i":2},{"id":"v190-c1-111-04","title":"Policy and Review Lifecycle","type":"lifecycle","description":"Follows a governance policy from drafted through approval to its next review.","i":3},{"id":"v190-c1-111-05","title":"Governance Evidence Matrix","type":"radar","description":"Compares evidence strength across the different governance control areas.","i":4},{"id":"v190-c1-111-06","title":"Governance Action Completion","type":"matrix","description":"Grids governance action completion against each responsible area or owner.","i":5},{"id":"v190-c1-111-15","title":"Policy Approval Status","type":"gauge","description":"Gauges what share of governance policies have completed formal approval.","i":14},{"id":"v190-c1-111-19","title":"Conflict and Independence Controls","type":"funnel","description":"Tracks conflict-of-interest declarations from required through to confirmed and cleared.","i":18},{"id":"v190-c1-111-22","title":"Governance Records Readiness","type":"matrix","description":"Grids how ready governance records are for audit against each control area.","i":21},{"id":"v190-c1-111-27","title":"Governance Source Readiness","type":"funnel","description":"Tracks the underlying governance data sources from unread through to fully readable.","i":26},{"id":"v190-c1-111-28","title":"Governance Metric Readiness","type":"lifecycle","description":"Follows governance metrics from unavailable through to fully calculated and ready.","i":27}],"1.2.1":[{"id":"v190-c1-121-01","title":"Strategic Planning Control Coverage","type":"bar","description":"Compares how many strategic planning controls are documented across each planning area.","i":0},{"id":"v190-c1-121-02","title":"Strategic Objective Status","type":"donut","description":"Shows the current status mix of strategic objectives, from drafted to achieved.","i":1},{"id":"v190-c1-121-03","title":"Strategic Target Readiness","type":"funnel","description":"Tracks strategic targets from set through to having a measurable result recorded.","i":2},{"id":"v190-c1-121-04","title":"Plan-to-Review Lifecycle","type":"lifecycle","description":"Follows a strategic plan from drafted through implementation to its formal review.","i":3},{"id":"v190-c1-121-06","title":"Strategic Action Completion","type":"matrix","description":"Grids strategic action completion against each objective or planning area.","i":5},{"id":"v190-c1-121-09","title":"Target versus Actual Profile","type":"bar","description":"Compares planned targets against actual results across strategic objectives.","i":8},{"id":"v190-c1-121-10","title":"Milestone Completion","type":"donut","description":"Shows what share of strategic plan milestones have been completed on time.","i":9},{"id":"v190-c1-121-16","title":"Planning Evidence Completeness","type":"trend","description":"Tracks how complete the supporting evidence for strategic planning has been over time.","i":15},{"id":"v190-c1-121-22","title":"Objective Ownership Coverage","type":"matrix","description":"Grids strategic objectives against whether each one has a clearly named owner.","i":21},{"id":"v190-c1-121-27","title":"Strategy Source Readiness","type":"funnel","description":"Tracks the underlying strategic planning data sources from unread through to readable.","i":26},{"id":"v190-c1-121-28","title":"Strategy Metric Readiness","type":"lifecycle","description":"Follows strategic planning metrics from unavailable through to fully calculated and ready.","i":27}]},"criterion_2":{"overview":[{"id":"v190-c2-overview-01","title":"Corporate Administration Metric Profile","type":"bar","description":"Compares key corporate administration metrics side by side for this criterion.","i":0},{"id":"v190-c2-overview-02","title":"Live Source Availability","type":"donut","description":"Shows what share of the underlying DocTypes and fields are currently readable.","i":1},{"id":"v190-c2-overview-03","title":"Administration System Health","type":"funnel","description":"Tracks how administration records move from raised to fully resolved across the system.","i":2},{"id":"v190-c2-overview-04","title":"People-to-Feedback Lifecycle","type":"lifecycle","description":"Maps the stages a people record passes through on its way to feedback closure.","i":3},{"id":"v190-c2-overview-05","title":"Corporate Exception Funnel","type":"radar","description":"Highlights where corporate administration exceptions are concentrated across different areas.","i":4},{"id":"v190-c2-overview-06","title":"Evidence Readiness Matrix","type":"matrix","description":"Grids evidence completeness against each corporate administration control area.","i":5}],"2.1.1":[{"id":"v190-c2-211-01","title":"Staff Selection and Management Coverage","type":"bar","description":"Compares how many staff selection and management controls are covered across each area.","i":0},{"id":"v190-c2-211-02","title":"Staff Lifecycle Status","type":"donut","description":"Shows the current status mix of staff records, from onboarding to exit.","i":1},{"id":"v190-c2-211-04","title":"Workforce Control Readiness","type":"lifecycle","description":"Follows workforce controls from unverified through to fully in place and ready.","i":3}],"2.1.2":[{"id":"v190-c2-212-01","title":"Training and Development Coverage","type":"bar","description":"Compares how many staff have documented training and development coverage.","i":0},{"id":"v190-c2-212-02","title":"Training Status Distribution","type":"donut","description":"Shows the current status mix of staff training records, from planned to completed.","i":1},{"id":"v190-c2-212-11","title":"Development Action Completion","type":"funnel","description":"Tracks development actions from identified through to closed out.","i":10}],"2.2.1":[{"id":"v190-c2-221-01","title":"Communication Control Coverage","type":"bar","description":"Compares how many communication controls are documented across internal and external channels.","i":0},{"id":"v190-c2-221-02","title":"Communication Status Distribution","type":"donut","description":"Shows the current status mix of communication records, from draft to published.","i":1},{"id":"v190-c2-221-11","title":"Communication Record Completeness","type":"funnel","description":"Tracks what share of communication records are fully and correctly documented.","i":10}],"2.3.1":[{"id":"v190-c2-231-01","title":"Data Management Control Coverage","type":"bar","description":"Compares how many data management controls are in place across this area.","i":0},{"id":"v190-c2-231-02","title":"Data Control Status","type":"donut","description":"Shows the current status mix of data control records, from open to resolved.","i":1},{"id":"v190-c2-231-04","title":"Data Quality Readiness","type":"lifecycle","description":"Follows data quality checks from unverified through to confirmed clean.","i":3}],"2.3.2":[{"id":"v190-c2-232-01","title":"Knowledge Management Coverage","type":"bar","description":"Compares how many knowledge management controls are covered across this area.","i":0},{"id":"v190-c2-232-02","title":"Knowledge Asset Status","type":"donut","description":"Shows the current status mix of knowledge assets, from draft to published.","i":1},{"id":"v190-c2-232-04","title":"Knowledge Repository Readiness","type":"lifecycle","description":"Follows the knowledge repository from incomplete through to confirmed ready.","i":3}],"2.4.1":[{"id":"v190-c2-241-01","title":"Feedback Management Coverage","type":"bar","description":"Compares how many feedback management controls are covered across this area.","i":0},{"id":"v190-c2-241-02","title":"Feedback Status Distribution","type":"donut","description":"Shows the current status mix of feedback records, from received to closed.","i":1},{"id":"v190-c2-241-11","title":"Improvement Action Linkage","type":"funnel","description":"Tracks improvement actions raised from feedback through to implementation.","i":10}],"2.4.2":[{"id":"v190-c2-242-01","title":"Student Survey Coverage","type":"bar","description":"Compares how many student satisfaction surveys have documented coverage.","i":0},{"id":"v190-c2-242-02","title":"Student Survey Status","type":"donut","description":"Shows the current status mix of student surveys, from open to completed.","i":1},{"id":"v190-c2-242-04","title":"Student Satisfaction Readiness","type":"lifecycle","description":"Follows student satisfaction readiness from unverified through to confirmed complete.","i":3}],"2.4.3":[{"id":"v190-c2-243-01","title":"Staff Survey Coverage","type":"bar","description":"Compares how many staff satisfaction surveys have documented coverage.","i":0},{"id":"v190-c2-243-02","title":"Staff Survey Status","type":"donut","description":"Shows the current status mix of staff surveys, from open to completed.","i":1},{"id":"v190-c2-243-04","title":"Staff Satisfaction Readiness","type":"lifecycle","description":"Follows staff satisfaction readiness from unverified through to confirmed complete.","i":3}]},"criterion_3":{"overview":[{"id":"v190-c3-overview-01","title":"Agent Lifecycle Coverage","type":"bar","description":"Compares agent lifecycle stages side by side across all recruitment agents.","i":0},{"id":"v190-c3-overview-02","title":"Policy Control Coverage","type":"donut","description":"Shows what share of agent-related policy controls are currently in place.","i":1},{"id":"v190-c3-overview-05","title":"Open Exception Profile","type":"radar","description":"Highlights where open exceptions are concentrated across agent management areas.","i":4},{"id":"v190-c3-overview-06","title":"Source Readiness","type":"matrix","description":"Grids source readiness against each area this criterion covers.","i":5},{"id":"v190-c3-overview-07","title":"Agent Portfolio Status","type":"gauge","description":"Gauges how the current agent portfolio is distributed by status.","i":6},{"id":"v190-c3-overview-10","title":"Agent NDA Coverage","type":"donut","description":"Shows the share of agents with a completed NDA on file.","i":9},{"id":"v190-c3-overview-20","title":"Agent Evidence Completeness","type":"lifecycle","description":"Follows agent evidence records from incomplete through to fully documented.","i":19},{"id":"v190-c3-overview-28","title":"Agent Target Achievement","type":"lifecycle","description":"Tracks agents from recruitment target set through to achieved.","i":27}],"3.1.1":[{"id":"v190-c3-311-01","title":"Identification Pathways","type":"bar","description":"Compares how agent candidates were identified across each sourcing pathway.","i":0},{"id":"v190-c3-311-02","title":"Selection and Screening Funnel","type":"donut","description":"Tracks candidate agents from initial screening through to selection.","i":1},{"id":"v190-c3-311-05","title":"Approval and Background Check","type":"radar","description":"Follows candidate agents from approval through to a completed background check.","i":4},{"id":"v190-c3-311-06","title":"Contract and NDA Readiness","type":"matrix","description":"Gauges how ready contract and NDA documentation is for new agents.","i":5},{"id":"v190-c3-311-07","title":"Agent Listing and Status","type":"gauge","description":"Gauges how the current agent listing is distributed by status.","i":6},{"id":"v190-c3-311-12","title":"Due-Diligence Evidence","type":"lifecycle","description":"Follows due-diligence evidence from missing through to fully documented.","i":11},{"id":"v190-c3-311-15","title":"Selection Rating Completeness","type":"gauge","description":"Gauges what share of candidate agents have a completed selection rating.","i":14},{"id":"v190-c3-311-20","title":"Contract Signature Coverage","type":"lifecycle","description":"Gauges what share of agent contracts have a completed signature.","i":19},{"id":"v190-c3-311-22","title":"NDA Completion Status","type":"matrix","description":"Gauges what share of required agent NDAs have been completed.","i":21},{"id":"v190-c3-311-27","title":"Selection Source Readiness","type":"funnel","description":"Tracks the underlying selection data sources from unread through to readable.","i":26},{"id":"v190-c3-311-28","title":"Selection Metric Readiness","type":"lifecycle","description":"Follows selection metrics from unavailable through to fully calculated and ready.","i":27}],"3.2.1":[{"id":"v190-c3-321-01","title":"Agent Onboarding Funnel","type":"bar","description":"Tracks agents from onboarding start through to onboarding completion.","i":0},{"id":"v190-c3-321-02","title":"Training Coverage","type":"donut","description":"Shows what share of active agents have completed required training.","i":1},{"id":"v190-c3-321-03","title":"Service Delivery Controls","type":"funnel","description":"Gauges how many service delivery controls are in place for active agents.","i":2},{"id":"v190-c3-321-04","title":"Performance Evaluation Distribution","type":"lifecycle","description":"Shows how agent performance evaluations are distributed across ratings.","i":3},{"id":"v190-c3-321-06","title":"Complaints and Breaches","type":"matrix","description":"Grids complaints and breaches against each responsible agent.","i":5},{"id":"v190-c3-321-15","title":"Contract Renewal Coverage","type":"gauge","description":"Gauges what share of agent contracts have been renewed on time.","i":14},{"id":"v190-c3-321-17","title":"Provider Rating Outcomes","type":"bar","description":"Compares agent performance against their provider rating outcomes.","i":16},{"id":"v190-c3-321-22","title":"Monitoring Record Coverage","type":"matrix","description":"Grids monitoring record coverage against each active agent.","i":21},{"id":"v190-c3-321-26","title":"Offboarding Completion","type":"donut","description":"Shows what share of agent offboarding processes have been completed.","i":25},{"id":"v190-c3-321-27","title":"Evaluation Source Readiness","type":"funnel","description":"Tracks the underlying evaluation data sources from unread through to readable.","i":26},{"id":"v190-c3-321-28","title":"Evaluation Metric Readiness","type":"lifecycle","description":"Follows evaluation metrics from unavailable through to fully calculated and ready.","i":27}]},"criterion_6":{"overview":[{"id":"v190-c6-overview-02","title":"Policy Evidence Coverage","type":"donut","description":"Shows what share of quality policies have documented supporting evidence.","i":1},{"id":"v190-c6-overview-04","title":"Quality Calendar Completion","type":"lifecycle","description":"Gauges how much of the planned quality calendar has been completed.","i":3},{"id":"v190-c6-overview-06","title":"Source Readiness","type":"matrix","description":"Grids source readiness against each quality assurance area this criterion covers.","i":5},{"id":"v190-c6-overview-14","title":"Quality Evidence Completeness","type":"matrix","description":"Follows quality evidence records from incomplete through to fully documented.","i":13},{"id":"v190-c6-overview-16","title":"Overall Criterion Readiness","type":"trend","description":"Summarises how ready Criterion 6 is overall, from raw data through to verified evidence.","i":15}],"6.1.1":[{"id":"v190-c6-611-01","title":"Annual Audit Programme","type":"bar","description":"Compares planned audits against the annual audit programme.","i":0},{"id":"v190-c6-611-02","title":"Audit Scope Coverage","type":"donut","description":"Shows how audit scope is distributed across the areas covered.","i":1},{"id":"v190-c6-611-05","title":"Audit Findings by Severity","type":"radar","description":"Compares audit findings by severity across recent audits.","i":4},{"id":"v190-c6-611-06","title":"Corrective Action Closure","type":"matrix","description":"Grids corrective action closure against each audit finding raised.","i":5},{"id":"v190-c6-611-16","title":"Audit Source Readiness","type":"trend","description":"Tracks the underlying audit data sources from unread through to fully readable.","i":15}],"6.2.1":[{"id":"v190-c6-621-01","title":"THESIS Review Coverage","type":"bar","description":"Compares THESIS review inputs covered against the required agenda items.","i":0},{"id":"v190-c6-621-03","title":"Review Input Completeness","type":"funnel","description":"Follows management review input completeness from partial through to full.","i":2},{"id":"v190-c6-621-04","title":"Review Outputs","type":"lifecycle","description":"Follows management review outputs from raised through to implemented.","i":3},{"id":"v190-c6-621-07","title":"Review Status Distribution","type":"gauge","description":"Shows how management review meetings are distributed across their status.","i":6},{"id":"v190-c6-621-16","title":"Management Review Source Readiness","type":"trend","description":"Tracks the underlying management review data sources from unread through to readable.","i":15}],"6.3.1":[{"id":"v190-c6-631-01","title":"Innovation Type Mix","type":"bar","description":"Compares how innovation initiatives are distributed across their type.","i":0},{"id":"v190-c6-631-02","title":"Improvement Initiative Lifecycle","type":"donut","description":"Follows an improvement initiative from proposed through to implemented.","i":1},{"id":"v190-c6-631-06","title":"Improvement Action Status","type":"matrix","description":"Grids improvement action status against each initiative raised.","i":5},{"id":"v190-c6-631-08","title":"Implementation Progress","type":"trend","description":"Tracks how much implementation progress has been made across initiatives.","i":7},{"id":"v190-c6-631-16","title":"Innovation Source Readiness","type":"trend","description":"Tracks the underlying innovation data sources from unread through to readable.","i":15}],"6.4.1":[{"id":"v190-c6-641-01","title":"Provider Tier Profile","type":"bar","description":"Compares how providers are distributed across their accreditation tier.","i":0},{"id":"v190-c6-641-02","title":"Provider Accreditation Funnel","type":"donut","description":"Tracks providers from application through to accreditation approval.","i":1},{"id":"v190-c6-641-06","title":"Provider Evaluation Outcomes","type":"matrix","description":"Shows what share of provider evaluations resulted in a positive outcome.","i":5},{"id":"v190-c6-641-11","title":"Rating Completeness","type":"funnel","description":"Gauges what share of provider ratings have been fully completed.","i":10},{"id":"v190-c6-641-16","title":"Provider Source Readiness","type":"trend","description":"Tracks the underlying provider data sources from unread through to readable.","i":15}],"6.5.3":[{"id":"v190-c6-653-01","title":"Hazard Reporting Funnel","type":"bar","description":"Tracks hazards from reported through to fully assessed.","i":0},{"id":"v190-c6-653-02","title":"Risk Level Distribution","type":"donut","description":"Shows how identified risks are distributed across severity levels.","i":1},{"id":"v190-c6-653-03","title":"5×5 Risk Matrix","type":"funnel","description":"Grids likelihood against impact across the full 5x5 risk matrix.","i":2},{"id":"v190-c6-653-07","title":"Risk Assessment Coverage","type":"gauge","description":"Compares how many risk assessments have been completed across areas.","i":6},{"id":"v190-c6-653-16","title":"Risk Source Readiness","type":"trend","description":"Tracks the underlying risk data sources from unread through to fully readable.","i":15}]},"criterion_7":{"overview":[{"id":"v190-c7-overview-02","title":"Live Source Availability","type":"donut","description":"Shows what share of the underlying DocTypes and fields are currently readable.","i":1},{"id":"v190-c7-overview-06","title":"Outcome Evidence Readiness","type":"matrix","description":"Grids evidence completeness against each outcome area this criterion covers.","i":5},{"id":"v190-c7-overview-08","title":"Target Availability","type":"trend","description":"Tracks how many indicators have a defined target over recent periods.","i":7},{"id":"v190-c7-overview-09","title":"Actual Result Availability","type":"bar","description":"Compares how many indicators have an actual result recorded.","i":8},{"id":"v190-c7-overview-10","title":"Target Achievement","type":"donut","description":"Shows the share of indicators that have achieved their set target.","i":9},{"id":"v190-c7-overview-11","title":"Target Variance","type":"funnel","description":"Tracks the variance between target and actual results across indicators.","i":10},{"id":"v190-c7-overview-14","title":"Outcome Review Status","type":"matrix","description":"Grids outcome review status against each area being measured.","i":13},{"id":"v190-c7-overview-28","title":"Underperforming Indicators","type":"lifecycle","description":"Follows underperforming indicators from flagged through to addressed.","i":27},{"id":"v190-c7-overview-29","title":"Missing Measurements","type":"radar","description":"Compares where measurements are missing across tracked indicators.","i":28},{"id":"v190-c7-overview-34","title":"Outcome Action Status","type":"donut","description":"Shows the status mix of actions raised against underperforming outcomes.","i":33},{"id":"v190-c7-overview-35","title":"Outcome Source Readiness","type":"funnel","description":"Tracks the underlying outcome data sources from unread through to readable.","i":34},{"id":"v190-c7-overview-40","title":"Overall Criterion Readiness","type":"trend","description":"Summarises how ready Criterion 7 is overall, from raw data through to verified evidence.","i":39}],"7.1.1":[{"id":"v190-c7-711-01","title":"Measurement Control Coverage","type":"bar","description":"Compares how many measurement controls are documented across outcome areas.","i":0},{"id":"v190-c7-711-02","title":"Measurement Status Distribution","type":"donut","description":"Shows the current status mix of outcome measurements, from open to resolved.","i":1},{"id":"v190-c7-711-03","title":"Indicator Definition Coverage","type":"funnel","description":"Tracks how many indicators have a complete, documented definition.","i":2},{"id":"v190-c7-711-04","title":"Indicator Ownership Coverage","type":"lifecycle","description":"Compares how many indicators have a clearly assigned owner.","i":3},{"id":"v190-c7-711-05","title":"Target Definition Coverage","type":"radar","description":"Compares how many indicators have a documented target definition.","i":4},{"id":"v190-c7-711-06","title":"Actual Result Coverage","type":"matrix","description":"Grids actual result coverage against each defined indicator.","i":5},{"id":"v190-c7-711-08","title":"Target Achievement Gauge","type":"trend","description":"Gauges what share of indicators have achieved their set target.","i":7},{"id":"v190-c7-711-09","title":"Target Variance Profile","type":"bar","description":"Compares target-versus-actual variance across defined indicators.","i":8},{"id":"v190-c7-711-12","title":"Benchmark Readiness","type":"lifecycle","description":"Gauges how ready indicators are for benchmark comparison.","i":11},{"id":"v190-c7-711-14","title":"Underperformance Profile","type":"matrix","description":"Grids underperformance against each indicator falling short of target.","i":13},{"id":"v190-c7-711-15","title":"Missing Result Profile","type":"gauge","description":"Gauges what share of indicators are missing a recorded result.","i":14},{"id":"v190-c7-711-16","title":"Review Completion","type":"trend","description":"Gauges how many scheduled outcome reviews have been completed.","i":15},{"id":"v190-c7-711-17","title":"Improvement Action Coverage","type":"bar","description":"Compares how many underperforming outcomes have a linked improvement action.","i":16},{"id":"v190-c7-711-31","title":"Measurement Source Readiness","type":"gauge","description":"Gauges how readable the underlying measurement data sources currently are.","i":30},{"id":"v190-c7-711-32","title":"Measurement Metric Readiness","type":"trend","description":"Tracks how ready measurement metrics are, from unavailable to calculated.","i":31},{"id":"v190-c7-711-36","title":"Outcome Action Closure","type":"lifecycle","description":"Follows outcome actions from raised through to formally closed.","i":35},{"id":"v190-c7-711-37","title":"Evidence Completeness","type":"radar","description":"Tracks how complete supporting evidence is across measured outcomes.","i":36},{"id":"v190-c7-711-38","title":"Data Quality Profile","type":"matrix","description":"Grids data quality checks against each outcome measurement area.","i":37}]},"criterion_5":{"overview":[{"id":"c5-overview-readiness","title":"Academic System Readiness","type":"bar","description":"Compares the live academic-system metrics returned for the selected Criterion 5 area.","i":0},{"id":"c5-overview-availability","title":"Source Availability","type":"donut","description":"Shows readable sources, source issues, readable metrics and metric issues.","i":1},{"id":"c5-overview-health","title":"Criterion 5 System Health","type":"matrix","description":"Summarises available metrics, unavailable metrics, sources and exceptions.","i":2},{"id":"c5-overview-exceptions","title":"Criterion 5 Exception Profile","type":"funnel","description":"Highlights live exceptions that require academic or data-quality follow-up.","i":3}],"5.1.1":[{"id":"c5-511-coverage","title":"Course Design Control Coverage","type":"bar","description":"Compares course proposal, module design, programme mapping and assessment-plan evidence.","i":0},{"id":"c5-511-status","title":"Course Design Status Distribution","type":"donut","description":"Shows available design metrics, source readiness and exceptions.","i":1},{"id":"c5-511-readiness","title":"Course Design Evidence Readiness","type":"radar","description":"Compares readiness across the main course design and development controls.","i":2},{"id":"c5-511-gaps","title":"Course Design Gap Profile","type":"funnel","description":"Highlights course design controls that require follow-up.","i":3}],"5.1.2":[{"id":"c5-512-coverage","title":"Course Review Control Coverage","type":"bar","description":"Compares module review, course review, approval and recommendation evidence.","i":0},{"id":"c5-512-status","title":"Course Review Status Distribution","type":"donut","description":"Shows review source and metric readiness.","i":1},{"id":"c5-512-cycle","title":"Course Review Lifecycle","type":"lifecycle","description":"Follows review evidence from recorded through approval and recommendation follow-up.","i":2},{"id":"c5-512-gaps","title":"Review Exception Profile","type":"funnel","description":"Highlights overdue or incomplete review controls.","i":3}],"5.2.1":[{"id":"c5-521-coverage","title":"Course Planning Control Coverage","type":"bar","description":"Compares intake, module class, schedule and student-contract planning evidence.","i":0},{"id":"c5-521-status","title":"Course Planning Status Distribution","type":"donut","description":"Shows planning source and metric readiness.","i":1},{"id":"c5-521-flow","title":"Planning Readiness Flow","type":"lifecycle","description":"Follows planning evidence from intake through class, schedule and contract readiness.","i":2},{"id":"c5-521-gaps","title":"Planning Exception Profile","type":"funnel","description":"Highlights incomplete planning controls requiring follow-up.","i":3}],"5.2.2":[{"id":"c5-522-coverage","title":"Course Delivery Control Coverage","type":"bar","description":"Compares schedules, attendance, observations and sign-off evidence.","i":0},{"id":"c5-522-status","title":"Course Delivery Status Distribution","type":"donut","description":"Shows delivery source and metric readiness.","i":1},{"id":"c5-522-readiness","title":"Delivery Evidence Readiness","type":"radar","description":"Compares attendance, observation and sign-off evidence across delivery controls.","i":2},{"id":"c5-522-gaps","title":"Delivery Exception Profile","type":"funnel","description":"Highlights delivery controls requiring follow-up.","i":3}],"5.3.1":[{"id":"c5-531-coverage","title":"Partnership Control Coverage","type":"bar","description":"Compares agreement, monitoring, evaluation and provider-rating evidence.","i":0},{"id":"c5-531-status","title":"Partnership Status Distribution","type":"donut","description":"Shows partnership source and metric readiness.","i":1},{"id":"c5-531-risk","title":"Partnership Risk Profile","type":"funnel","description":"Highlights expiry, NDA and threshold risks requiring follow-up.","i":2},{"id":"c5-531-readiness","title":"Partnership Evidence Readiness","type":"matrix","description":"Grids readiness across partnership management controls.","i":3}],"5.4":[{"id":"c5-54-coverage","title":"Student Feedback Control Coverage","type":"bar","description":"Compares survey, score and attendance-risk evidence.","i":0},{"id":"c5-54-status","title":"Student Feedback Status Distribution","type":"donut","description":"Shows feedback source and metric readiness.","i":1},{"id":"c5-54-readiness","title":"Feedback Evidence Readiness","type":"radar","description":"Compares survey and learning-support evidence across key controls.","i":2},{"id":"c5-54-gaps","title":"Feedback Exception Profile","type":"funnel","description":"Highlights feedback controls requiring follow-up.","i":3}],"5.5":[{"id":"c5-55-coverage","title":"Assessment Control Coverage","type":"bar","description":"Compares assessment plans, control fields, results, grades and scores.","i":0},{"id":"c5-55-status","title":"Assessment Status Distribution","type":"donut","description":"Shows assessment source and metric readiness.","i":1},{"id":"c5-55-readiness","title":"Assessment Evidence Readiness","type":"radar","description":"Compares readiness across assessment planning and result controls.","i":2},{"id":"c5-55-gaps","title":"Assessment Exception Profile","type":"funnel","description":"Highlights assessment controls requiring correction or follow-up.","i":3}]}};
window.UCCLiveVisualDefinitions=LIVE_VISUAL_EXPANSION;
Object.keys(LIVE_VISUAL_EXPANSION).forEach(function(criterion){const config=CONFIG[criterion];if(!config)return;Object.keys(LIVE_VISUAL_EXPANSION[criterion]).forEach(function(section){config.sections[section]=config.sections[section]||{title:section,charts:[]};config.sections[section].charts=LIVE_VISUAL_EXPANSION[criterion][section];});});
function esc(value){return String(value==null?"":value).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;");}
function finiteNumber(value,fallback=0){const number=Number(value);return Number.isFinite(number)?number:fallback;}
function normaliseApiMessage(response){
let message=response&&response.message!==undefined?response.message:response;
for(let depth=0;depth<3;depth++){
if(typeof message==="string"){
try{message=JSON.parse(message);}catch(error){break;}
continue;
}
if(message&&typeof message==="object"&&!message.ok&&message.message&&typeof message.message==="object"){
message=message.message;
continue;
}
break;
}
return message;
}
function apiErrorMessage(error){
if(!error)return"Analytics request failed.";
if(typeof error==="string")return error;
if(error.message)return String(error.message);
if(error._server_messages){
try{
const messages=JSON.parse(error._server_messages);
if(Array.isArray(messages)&&messages.length){
const parsed=JSON.parse(messages[0]);
return parsed.message||String(messages[0]);
}
}catch(parseError){}
}
return error.exc_type||error.statusText||"Analytics request failed.";
}
function csvCell(value){const text=String(value==null?"":value);return/[",\n]/.test(text)?`"${text.replaceAll('"','""')}"`:text;}
function download(name,content,type="text/csv;charset=utf-8"){const blob=new Blob(["\ufeff",content],{type});const url=URL.createObjectURL(blob);const link=document.createElement("a");link.href=url;link.download=name;document.body.appendChild(link);link.click();link.remove();URL.revokeObjectURL(url);}
function statusBadge(status){const raw=String(status||"available"),label=raw.replaceAll("_"," ");const cls=/risk|error|denied|unavailable|failed/i.test(raw)?"risk":/warn|unsupported|partial|pending|overdue/i.test(raw)?"warning":"good";return`<span class="ucc-demo-status ${cls}">${esc(label)}</span>`;}
function activeSection(dashboard){return dashboard.dataset.demoActiveTab||"overview";}
function sectionDefinition(config,tab){const key=(config.panelMap&&config.panelMap[tab])||tab;return config.sections[tab]||config.sections[key]||config.sections.overview;}
function liveChartCardMarkup(chart){
return`<article class="panel ucc-shared-panel ucc-demo-visual-card ucc-live-generated-card" data-demo-card="${esc(chart.id)}"><div class="panel-head"><h2>${esc(chart.title)}<span class="ucc-card-desc-inline"> — ${esc(chart.description||"Permission-aware live metrics.")}</span></h2><div class="mini-toggle" data-demo-view-toggle="${esc(chart.id)}"><button type="button" class="active" data-demo-view="diagram">Diagram</button><button type="button" data-demo-view="table">Table</button></div></div><div class="chart ucc-demo-chart" data-demo-chart="${esc(chart.id)}" data-demo-chart-title="${esc(chart.title)}" data-demo-chart-type="${esc(chart.type||"bar")}"></div><div class="table-wrap hidden" data-demo-chart-table="${esc(chart.id)}"><table><thead><tr><th>Metric</th><th>Live value</th><th>Status</th></tr></thead><tbody data-demo-chart-table-body="${esc(chart.id)}"></tbody></table></div><button type="button" data-demo-drill="${esc(chart.id)}">View underlying records</button></article>`;
}
function panelInsertPoint(panel){
return Array.from(panel.children).find(function(child){return/Management Questions and Data-Based Answers/i.test(child.textContent||"");})||null;
}
function ensureLiveSectionCards(dashboard,config,sectionKey){
const definitions=LIVE_VISUAL_EXPANSION[dashboard.dataset.demoDashboard]||{};
if(!sectionKey||!definitions[sectionKey])return;
const panelKey=(config.panelMap&&config.panelMap[sectionKey])||sectionKey;
if(panelKey==="quality"||panelKey==="sources")return;
const panel=dashboard.querySelector(`[data-demo-panel="${CSS.escape(panelKey)}"]`);
if(!panel)return;
let grid=panel.querySelector(`:scope > .ucc-live-expanded-grid[data-live-section="${CSS.escape(sectionKey)}"]`);
if(!grid){
grid=document.createElement("div");
grid.className="grid2 ucc-live-expanded-grid";
grid.dataset.liveSection=sectionKey;
panel.insertBefore(grid,panelInsertPoint(panel));
}
if(!grid.dataset.liveCardsMounted){
grid.innerHTML=(definitions[sectionKey]||[]).filter(function(chart){return chart.enabled!==false;}).slice().sort((a,b)=>(a.title||"").localeCompare(b.title||"",undefined,{sensitivity:"base"})).map(liveChartCardMarkup).join("");
grid.dataset.liveCardsMounted="1";
}
}
function ensureLiveVisualCards(dashboard,config){
const definitions=LIVE_VISUAL_EXPANSION[dashboard.dataset.demoDashboard]||{};
dashboard.querySelectorAll(".ucc-demo-visual-card:not(.ucc-live-generated-card)").forEach(function(card){
card.hidden=true;
card.classList.add("ucc-live-base-card");
});
if(!dashboard.classList.contains("ucc-hidden"))ensureLiveSectionCards(dashboard,config,activeSection(dashboard));
}
function syncLiveSectionVisibility(dashboard,tab){
dashboard.querySelectorAll("[data-live-section]").forEach(function(grid){
grid.hidden=grid.dataset.liveSection!==tab;
});
}
function chartMax(rows){return Math.max.apply(null,rows.map(row=>finiteNumber(row[1],0)).concat([1]));}
function renderBars(node,rows){const max=chartMax(rows);node.innerHTML=`<div class="ucc-demo-bars">${rows.map(function(row){return`<div class="ucc-demo-bar"><label>${esc(row[0])}</label><div><i style="width:${Math.max(4,finiteNumber(row[1],0)/max*100)}%"></i></div><strong>${row[1]}${max<=100?"%":""}</strong></div>`;}).join("")}</div>`;}
function renderDonut(node,rows){const total=rows.reduce((sum,row)=>sum+finiteNumber(row[1],0),0)||1;let cursor=0;const stops=rows.map(function(row,index){const start=cursor/total*360;cursor+=finiteNumber(row[1],0);const end=cursor/total*360;return`var(--ucc-chart-${index%6}) ${start}deg ${end}deg`;}).join(",");node.innerHTML=`<div class="ucc-demo-donut-layout"><div class="ucc-demo-donut" style="background:conic-gradient(${stops})"><span>${total}</span><small>Total</small></div><div class="ucc-demo-legend">${rows.map(function(row,index){return`<div><i style="background:var(--ucc-chart-${index%6})"></i><span>${esc(row[0])}</span><strong>${row[1]}</strong></div>`;}).join("")}</div></div>`;}
function renderFunnel(node,rows){const max=chartMax(rows);node.innerHTML=`<div class="ucc-demo-funnel">${rows.map(function(row,index){const width=Math.max(38,finiteNumber(row[1],0)/max*100);return`<div class="ucc-demo-funnel-stage" style="width:${width}%"><span>${esc(row[0])}</span><strong>${row[1]}</strong></div>`;}).join("")}</div>`;}
function renderLifecycle(node,rows){node.innerHTML=`<div class="ucc-demo-lifecycle">${rows.map(function(row,index){return`<div class="ucc-demo-life-step"><i>${index+1}</i><span>${esc(row[0])}</span><strong>${row[1]}</strong></div>${index<rows.length-1?'<b aria-hidden="true">→</b>':""}`;}).join("")}</div>`;}
function renderMatrix(node,rows){const max=chartMax(rows);node.innerHTML=`<div class="ucc-demo-matrix">${rows.map(function(row){const level=Math.max(.18,finiteNumber(row[1],0)/max);return`<div style="--ucc-intensity:${level}"><span>${esc(row[0])}</span><strong>${row[1]}${max<=100?"%":""}</strong></div>`;}).join("")}</div>`;}
function renderRadar(node,rows){const size=320,cx=160,cy=160,radius=105,count=Math.max(rows.length,3),max=chartMax(rows);const points=rows.map(function(row,index){const angle=-Math.PI/2+index*2*Math.PI/count,r=radius*(finiteNumber(row[1],0)/max);return[cx+Math.cos(angle)*r,cy+Math.sin(angle)*r];});const axes=rows.map(function(row,index){const angle=-Math.PI/2+index*2*Math.PI/count,x=cx+Math.cos(angle)*radius,y=cy+Math.sin(angle)*radius,lx=cx+Math.cos(angle)*(radius+28),ly=cy+Math.sin(angle)*(radius+28);return`<line x1="${cx}" y1="${cy}" x2="${x}" y2="${y}"></line><text x="${lx}" y="${ly}" text-anchor="middle">${esc(row[0])}</text>`;}).join("");node.innerHTML=`<div class="ucc-demo-radar"><svg viewBox="0 0 ${size} ${size}" role="img" aria-label="Radar diagram"><circle cx="${cx}" cy="${cy}" r="${radius}"></circle><circle cx="${cx}" cy="${cy}" r="${radius*.66}"></circle><circle cx="${cx}" cy="${cy}" r="${radius*.33}"></circle>${axes}<polygon points="${points.map(point=>point.join(",")).join(" ")}"></polygon></svg><div class="ucc-demo-radar-values">${rows.map(row=>`<span>${esc(row[0])}: <strong>${row[1]}</strong></span>`).join("")}</div></div>`;}
function renderTrend(node,rows){const width=560,height=250,pad=38,max=chartMax(rows),step=(width-pad*2)/Math.max(1,rows.length-1);const points=rows.map(function(row,index){return[pad+index*step,height-pad-(finiteNumber(row[1],0)/max)*(height-pad*2)];});node.innerHTML=`<div class="ucc-demo-trend"><svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Trend diagram"><line class="axis" x1="${pad}" y1="${height-pad}" x2="${width-pad}" y2="${height-pad}"></line><polyline points="${points.map(p=>p.join(",")).join(" ")}"></polyline>${points.map(function(p,index){return`<circle cx="${p[0]}" cy="${p[1]}" r="5"></circle><text x="${p[0]}" y="${height-12}" text-anchor="middle">${esc(rows[index][0])}</text><text class="value" x="${p[0]}" y="${p[1]-10}" text-anchor="middle">${rows[index][1]}</text>`;}).join("")}</svg></div>`;}
function renderGauge(node,rows){const current=finiteNumber(rows[0]?.[1],0),reference=finiteNumber(rows[1]?.[1],current||1),percentage=reference?Math.max(0,Math.min(100,current/reference*100)):0;node.innerHTML=`<div class="ucc-demo-gauge-layout"><div class="ucc-demo-gauge" style="--ucc-gauge:${percentage*1.8}deg"><div><strong>${current}</strong><span>Current</span></div></div><div class="ucc-demo-gauge-copy"><span>Reference metric</span><strong>${reference}</strong><small>${current>=reference?"At or above reference":"Difference "+Math.max(0,reference-current)}</small></div></div>`;}
function renderRiskMatrix(node,chart){const values=chart.values||[],likelihood=["Rare","Remote","Occasional","Frequent","Almost Certain"],severity=["Catastrophic","Major","Moderate","Minor","Negligible"];node.innerHTML=`<div class="ucc-demo-risk-matrix"><div class="corner">Severity × Likelihood</div>${likelihood.map(x=>`<div class="head">${x}</div>`).join("")}${severity.map(function(label,row){return`<div class="side">${label}</div>${likelihood.map(function(_,col){const value=values[row*5+col]||0,level=value>=15?"high":value>=4?"medium":"low";return`<div class="${level}"><strong>${value}</strong></div>`;}).join("")}`;}).join("")}</div>`;}
function renderChart(node,chart,rows){const type=chart.type||"bar";if(type==="donut")return renderDonut(node,rows);if(type==="funnel")return renderFunnel(node,rows);if(type==="lifecycle"||type==="flow")return renderLifecycle(node,rows);if(type==="matrix")return renderMatrix(node,rows);if(type==="radar")return renderRadar(node,rows);if(type==="trend")return renderTrend(node,rows);if(type==="gauge")return renderGauge(node,rows);if(type==="risk-matrix")return renderRiskMatrix(node,chart);return renderBars(node,rows);}


const STATE=new Map();
const SAFE_COMPLEX_TYPES=new Set(["donut","funnel","trend"]);
function dashboardState(dashboard){if(!STATE.has(dashboard))STATE.set(dashboard,{loading:false,result:null,error:null,logs:[],lastSection:""});return STATE.get(dashboard);}
function logEvent(dashboard,level,event,detail){const state=dashboardState(dashboard);state.logs.push({time:new Date().toISOString(),level,event,detail:String(detail||"")});if(state.logs.length>500)state.logs.shift();const count=dashboard.querySelector("[data-demo-log-count]");if(count)count.textContent=String(state.logs.length);}
function selectedFilterObject(dashboard){const output={};dashboard.querySelectorAll("[data-demo-filter]").forEach(input=>{if(input.value)output[input.dataset.demoFilter]=input.value;});return output;}
function apiSection(config,dashboard,tab){const state=dashboardState(dashboard);if(tab==="quality"||tab==="sources")return state.lastSection||config.defaultSection;const mapped=config.apiSections&&config.apiSections[tab];if(mapped&&tab!=="overview")state.lastSection=mapped;return mapped||state.lastSection||config.defaultSection;}
function callApi(config,dashboard,action="summary",extra={}){
return new Promise((resolve,reject)=>{
if(!(window.frappe&&frappe.call)){reject(new Error("Frappe API client is unavailable."));return;}
const payload={action,subcriterion:apiSection(config,dashboard,activeSection(dashboard)),filters:selectedFilterObject(dashboard),page_size:100};
Object.keys(extra||{}).forEach(key=>payload[key]=extra[key]);
logEvent(dashboard,"INFO","api_request",`${config.apiMethod} · ${payload.subcriterion} · ${action}`);
frappe.call({
method:config.apiMethod,
args:{payload:JSON.stringify(payload)},
callback(response){
const message=normaliseApiMessage(response);
if(message&&message.ok){
logEvent(dashboard,"INFO","api_success",`${message.source_summary?.available||0}/${message.source_summary?.total||0} sources · ${message.metric_summary?.available||0}/${message.metric_summary?.total||0} metrics`);
resolve(message);
return;
}
const detail=message&&message.message?message.message:"Analytics response did not contain ok=true.";
logEvent(dashboard,"ERROR","api_invalid_response",detail);
reject(new Error(detail));
},
error(error){
const detail=apiErrorMessage(error);
logEvent(dashboard,"ERROR","api_error",detail);
reject(new Error(detail));
}
});
});
}
function setLoading(dashboard,active,progress=0,task="Loading live analytics"){const overlay=dashboard.querySelector("[data-demo-loading-overlay]");if(overlay)overlay.classList.toggle("hidden",!active);const title=dashboard.querySelector("[data-demo-loading-title]")||dashboard.querySelector("[data-demo-loading-overlay] strong");if(title)title.textContent=task;const fill=dashboard.querySelector("[data-demo-progress-fill]");if(fill)fill.style.width=Math.max(0,Math.min(100,progress))+"%";const value=dashboard.querySelector("[data-demo-progress-value]");if(value)value.textContent=Math.round(progress)+"%";const note=dashboard.querySelector("[data-demo-loading-overlay] .progress-text span:last-child");if(note)note.textContent="Permission-aware sources";}
function metricValue(metric){if(!metric||metric.status!=="available")return"—";const value=metric.value==null?0:metric.value;if(metric.unit==="SGD")return"SGD "+Number(value).toLocaleString();if(metric.unit==="rating")return String(value)+"/5";if(metric.unit==="percent")return String(value)+"%";return Number(value).toLocaleString();}
const DOCTYPE_DISPLAY_NAMES=Object.freeze({"Supplier Rating":"Provider Rating","Student Admission UCC":"Shortlisted Applicants","Student Group":"Module Class Details","Module Class Details":"Module Class Details","Student Batch Name":"Student Intake No","Student Intake No":"Student Intake No","Program":"Course","Course":"Module"});
function displayDoctypeName(doctype){return DOCTYPE_DISPLAY_NAMES[doctype]||doctype||"Source";}
function doctypeListRoute(doctype){return"/app/"+String(doctype||"").trim().toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"");}
function metricById(result,metricId){return(result?.metrics||[]).find(item=>item.id===metricId)||null;}
function sourceCalculation(question,metric){
if(question?.source_logic)return question.source_logic;
if(question?.source)return question.source;
if(!metric)return"Live API calculation";
const fields=(metric.resolved_fields||[]).filter(Boolean);
const source=metric.doctype||metric.source||"Live source";
return fields.length?`${source}.${fields.join(" / ")}`:`${source} · ${metric.unit||"records"} calculation`;
}
function extendedQuestionRows(result,tab){
const base=(result?.questions||[]).map(row=>({...row}));
const used=new Set(base.map(row=>row.metric_id).filter(Boolean));
(result?.metrics||[]).forEach(metric=>{
if(!metric?.id||used.has(metric.id))return;
const available=metric.status==="available";
const count=Number(metric.record_count??metric.total??0);
base.push({
id:"extended-"+metric.id,
criterion:result?.meta?.subcriterion||result?.policy?.criterion||tab,
question:`What is the current ${String(metric.label||"metric").toLowerCase()}?`,
answer:available?`${metricValue(metric)} from ${count.toLocaleString()} matching record(s).`:`Unavailable: ${metric.message||String(metric.status||"required source or field is unavailable").replaceAll("_"," ")}`,
metric_id:metric.id,
status:metric.status||"unavailable",
confidence:available?"Live":"Unavailable",
doctype:metric.doctype||"",
source_logic:sourceCalculation(null,metric),
record_count:count
});
});
return base;
}
function metricRows(result,chartIndex,chart){
const metrics=(result?.metrics||[]).filter(item=>item.status==="available");
const title=String(chart?.title||"").toLowerCase();
const first=metrics[0]||null;
if(/source availability|evidence readiness|source readiness/.test(title)){
const ss=result?.source_summary||{},ms=result?.metric_summary||{};
return[
["Available sources",finiteNumber(ss.available,0),first,true],
["Source issues",finiteNumber(ss.issues,0),first,true],
["Available metrics",finiteNumber(ms.available,0),first,true],
["Metric issues",finiteNumber(ms.issues,0),first,true]
];
}
if(/status distribution|system health|control health|readiness/.test(title)&&metrics.length){
const unavailable=(result?.metrics||[]).filter(item=>item.status!=="available").length;
return[
["Available",metrics.length,metrics[0],true],
["Unavailable",unavailable,metrics[0],true],
["Sources",finiteNumber(result?.source_summary?.available,0),metrics[0],true],
["Exceptions",(result?.exceptions||[]).length,metrics[0],true]
];
}
if(/exception|gap|risk profile/.test(title)){
const exceptionMetrics=(result?.exceptions||[]).filter(item=>item.status==="available");
if(exceptionMetrics.length)return exceptionMetrics.slice(0,5).map(item=>[item.label,finiteNumber(item.value,0),item]);
}
if(!metrics.length)return[];
const size=Math.min(5,metrics.length),start=(chartIndex*size)%metrics.length,rows=[];
for(let i=0;i<size;i++){const metric=metrics[(start+i)%metrics.length];rows.push([metric.label,finiteNumber(metric.value,0),metric]);}
return rows;
}
function chartForLive(node,chart,rows){
node.dataset.visualRenderAttempted="1";
if(!rows.length){node.innerHTML='<div class="ucc-live-empty"><strong>No live metric is readable for this section</strong><span>Open Source Mapping Report to see the exact DocType, permission or field issue.</span><button type="button" data-ucc-open-mapping>Source mapping report</button></div>';return;}
const pairs=rows.map(row=>[row[0],finiteNumber(row[1],0)]).filter(row=>Number.isFinite(row[1]));
if(!pairs.length){node.innerHTML='<div class="ucc-live-empty"><strong>The returned metrics are not numeric</strong><span>The visual was stopped before an invalid SVG path could be produced.</span><button type="button" data-ucc-open-mapping>Source mapping report</button></div>';return;}
const type=chart.type||"bar";
try{
if(type==="donut")return renderDonut(node,pairs);
if(type==="funnel")return renderFunnel(node,pairs);
if(type==="trend")return renderTrend(node,pairs);
if(type==="lifecycle"||type==="flow")return renderLifecycle(node,pairs);
if(type==="matrix")return renderMatrix(node,pairs);
if(type==="radar")return renderRadar(node,pairs);
if(type==="gauge")return renderGauge(node,pairs);
if(type==="risk-matrix"){
const seed=pairs.map(row=>Math.max(0,Math.round(row[1])));const values=[];
for(let i=0;i<25;i++)values.push(seed.length?seed[i%seed.length]:0);
return renderRiskMatrix(node,{...chart,values});
}
return renderBars(node,pairs);
}catch(error){
node.dataset.visualRenderError=error&&error.message?error.message:String(error);
node.innerHTML='<div class="ucc-visual-diagnostic"><strong>Visual data could not be rendered</strong><span>'+esc(node.dataset.visualRenderError)+' Open Source Mapping Report to check the mapped DocTypes and fields.</span><button type="button" data-ucc-open-mapping>Source mapping report</button></div>';
}
}
function renderLiveChartCard(dashboard,chart,index,result){
const chartNode=dashboard.querySelector(`[data-demo-chart="${CSS.escape(chart.id)}"]`);
const card=chartNode?.closest("[data-demo-card]");
const heading=card?.querySelector("h2");
if(heading)heading.innerHTML=esc(chart.title)+(chart.description?'<span class="ucc-card-desc-inline"> — '+esc(chart.description)+'</span>':'');
if(card){
card._liveCardPending={chart,index,result};
card.dataset.liveCardRendered="";
}
}
function renderLiveChartCardNow(card){
if(!card||!card._liveCardPending||card.dataset.liveCardRendered==="1")return;
const{chart,index,result}=card._liveCardPending;
const rows=metricRows(result,index,chart),chartNode=card.querySelector("[data-demo-chart]"),tableBody=card.querySelector("[data-demo-chart-table-body]");
if(chartNode){chartNode.dataset.demoChartTitle=chart.title;chartNode.dataset.demoChartType=chart.type||"bar";chartForLive(chartNode,chart,rows);}
if(tableBody){
tableBody.innerHTML=rows.length?rows.map(row=>{const metric=row[2],synthetic=row[3]===true,value=synthetic?Number(row[1]||0).toLocaleString():metric?metricValue(metric):Number(row[1]||0).toLocaleString(),status=metric?.status||"available";return`<tr><td>${esc(row[0])}</td><td>${esc(value)}</td><td>${statusBadge(status)}</td></tr>`;}).join(""):'<tr><td colspan="3">No available metric for this visual.</td></tr>';
}
card.dataset.liveCardRendered="1";
}
function renderKpis(dashboard,config,result){const mount=dashboard.querySelector("[data-demo-kpis]");if(!mount)return;const metrics=(result?.metrics||[]),rows=metrics.slice(0,6);while(rows.length<6)rows.push(null);mount.innerHTML=rows.map((metric,index)=>{if(metric)return`<article><span>${esc(metric.label)}</span><strong>${esc(metricValue(metric))}</strong><small>${esc(metric.doctype||metric.source||"Live metric")} · ${esc(metric.status.replaceAll("_"," "))}</small></article>`;const summary=index%2===0?result?.source_summary:result?.metric_summary;return`<article><span>${index%2===0?"Sources available":"Metrics available"}</span><strong>${summary?summary.available+"/"+summary.total:"—"}</strong><small>Permission-aware readiness</small></article>`;}).join("");}
function renderQa(dashboard,result,tab){
const target=dashboard.querySelector(`[data-demo-qa="${CSS.escape(dashboard.dataset.demoDashboard+":"+((dashboardState(dashboard).lastPanel)||tab))}"]`)||dashboard.querySelector("[data-demo-panel]:not(.hidden) [data-demo-qa]");
if(!target)return;
const rows=extendedQuestionRows(result,tab);
target.innerHTML=rows.length?rows.map(row=>{
const metric=metricById(result,row.metric_id);
const available=(metric?.status||row.status)==="available";
const count=Number(metric?.record_count??metric?.total??row.record_count??0);
const doctype=metric?.doctype||row.doctype||"";
const answerAction=available&&row.metric_id
?`<button type="button" class="record-link ucc-qa-action" data-live-qa-records="${esc(row.metric_id)}" data-live-qa-title="${esc(row.question||metric?.label||"Matching records")}">View ${count.toLocaleString()} matching record${count===1?"":"s"} ↗</button>`
:"";
const sourceAction=doctype
?`<button type="button" class="source-doctype-link ucc-qa-action" data-live-source-doctype="${esc(doctype)}">Open ${esc(displayDoctypeName(doctype))} list ↗</button>`
:'<span class="source-unavailable">No readable source list</span>';
return`<tr><td>${esc(row.criterion||result?.meta?.subcriterion||result?.policy?.policy||tab)}</td><td>${esc(row.question)}</td><td><div>${esc(row.answer)}</div>${answerAction}</td><td><div>${esc(sourceCalculation(row,metric))}</div>${sourceAction}</td><td>${statusBadge(row.status)}</td></tr>`;
}).join(""):'<tr><td colspan="5">No management questions are configured for this section.</td></tr>';
}
function renderSources(dashboard,result){
const target=dashboard.querySelector(`[data-demo-sources="${CSS.escape(dashboard.dataset.demoDashboard)}"]`);
if(!target)return;
const rows=result?.sources||[];
target.innerHTML=rows.length?rows.map(row=>{
const doctype=row.doctype||"";
const sourceName=doctype||row.candidates?.join(" / ")||row.key;
const action=doctype?`<button type="button" class="source-doctype-link ucc-qa-action" data-live-source-doctype="${esc(doctype)}">Open ${esc(displayDoctypeName(doctype))} list ↗</button>`:"";
return`<tr><td><div>${esc(sourceName)}</div>${action}</td><td>${esc(row.key||"Source")}</td><td>${statusBadge(row.status)} ${esc(row.message||"")}</td><td>${Number(row.count||0).toLocaleString()}</td></tr>`;
}).join(""):'<tr><td colspan="4">No source definitions returned.</td></tr>';
}
function renderQuality(dashboard,result){const target=dashboard.querySelector(`[data-demo-quality="${CSS.escape(dashboard.dataset.demoDashboard)}"]`);if(!target)return;const rows=result?.data_quality||[];target.innerHTML=rows.length?rows.map(row=>`<tr><td>${esc(row.check)}</td><td>${esc(row.source)}</td><td>${statusBadge(row.status)}</td><td>${esc(row.detail)}</td></tr>`).join(""):'<tr><td>Live source and metric checks</td><td>0</td><td>'+statusBadge("available")+'</td><td>No readiness issue returned.</td></tr>';}
function renderReadiness(dashboard,config,result){const title=dashboard.querySelector("[data-demo-readiness-title]"),copy=dashboard.querySelector("[data-demo-readiness-copy]");if(!result){if(title)title.textContent=`Criterion ${config.number} live analytics active.`;if(copy)copy.textContent="Waiting for the live data connection.";return;}const ss=result.source_summary||{},ms=result.metric_summary||{},sA=ss.available||0,sT=ss.total||0,mA=ms.available||0,mT=ms.total||0,issues=Math.max(0,sT-sA)+Math.max(0,mT-mA);if(title)title.textContent=`Criterion ${config.number} live analytics active${issues?" with limitations":""}.`;if(copy)copy.textContent=`Live data connected · ${sA} of ${sT} sources available · ${mA} of ${mT} metrics available${issues?` · ${issues} item${issues===1?"":"s"} need review`:""}`;}
function renderError(dashboard,config,error){const title=dashboard.querySelector("[data-demo-readiness-title]"),copy=dashboard.querySelector("[data-demo-readiness-copy]");if(title)title.textContent=`Criterion ${config.number} live API unavailable.`;if(copy)copy.textContent=error.message||String(error);const mount=dashboard.querySelector("[data-demo-kpis]");if(mount)mount.innerHTML=`<article><span>API status</span><strong>Unavailable</strong><small>${esc(error.message||error)}</small></article>`;}
function renderDashboard(dashboard){const config=CONFIG[dashboard.dataset.demoDashboard],state=dashboardState(dashboard),result=state.result;if(!config)return;if(state.error&&!result){renderError(dashboard,config,state.error);return;}const tab=activeSection(dashboard),section=sectionDefinition(config,tab);renderKpis(dashboard,config,result);(section?.charts||[]).forEach((chart,index)=>renderLiveChartCard(dashboard,chart,chart.i??index,result));dashboard.querySelectorAll(`[data-live-section="${CSS.escape(tab)}"] [data-demo-card]`).forEach(renderLiveChartCardNow);renderQa(dashboard,result,tab);renderSources(dashboard,result);renderQuality(dashboard,result);renderReadiness(dashboard,config,result);}
async function loadLive(dashboard,force=false){const config=CONFIG[dashboard.dataset.demoDashboard],state=dashboardState(dashboard),section=apiSection(config,dashboard,activeSection(dashboard));ensureLiveSectionCards(dashboard,config,activeSection(dashboard));if(state.loading)return;if(!force&&state.result&&state.result.meta?.subcriterion===section){renderDashboard(dashboard);return;}state.loading=true;state.error=null;setLoading(dashboard,true,15,`Loading ${section}`);try{const result=await callApi(config,dashboard,"summary");setLoading(dashboard,true,80,"Rendering live analytics");state.result=result;state.error=null;renderDashboard(dashboard);setLoading(dashboard,true,100,"Live analytics ready");setTimeout(()=>setLoading(dashboard,false),150);}catch(error){state.error=error;logEvent(dashboard,"ERROR","api_failure",error.message||error);renderDashboard(dashboard);setLoading(dashboard,false);}finally{state.loading=false;}}
function showTab(dashboard,tab){const config=CONFIG[dashboard.dataset.demoDashboard];dashboard.dataset.demoActiveTab=tab;dashboard.querySelectorAll("[data-demo-tab]").forEach(button=>button.classList.toggle("active",button.dataset.demoTab===tab));const panelKey=(config.panelMap&&config.panelMap[tab])||tab;dashboardState(dashboard).lastPanel=panelKey;dashboard.querySelectorAll("[data-demo-panel]").forEach(panel=>panel.classList.toggle("hidden",panel.dataset.demoPanel!==panelKey));ensureLiveSectionCards(dashboard,config,tab);syncLiveSectionVisibility(dashboard,tab);if(tab!=="quality"&&tab!=="sources")loadLive(dashboard);else renderDashboard(dashboard);}
function allQaRows(result){return extendedQuestionRows(result,result?.meta?.subcriterion||"section").map(row=>[row.criterion,row.question,row.answer,sourceCalculation(row,metricById(result,row.metric_id)),row.status]);}
function allExceptionRows(result){return(result?.exceptions||[]).map(row=>[row.id,row.label,metricValue(row),row.status,row.doctype||row.source]);}
function ensureModal(){let modal=platform.querySelector("[data-demo-modal]");if(modal)return modal;modal=document.createElement("div");modal.className="ucc-demo-modal";modal.dataset.demoModal="1";modal.hidden=true;modal.innerHTML=`<div class="ucc-demo-modal-card"><header><div><strong data-demo-modal-title>Analytics details</strong><span>Permission-aware live data</span></div><button type="button" data-demo-modal-close aria-label="Close">×</button></header><div class="ucc-demo-modal-body" data-demo-modal-body></div></div>`;platform.appendChild(modal);modal.querySelector("[data-demo-modal-close]").addEventListener("click",()=>modal.hidden=true);modal.addEventListener("click",event=>{if(event.target===modal)modal.hidden=true;});return modal;}
function openModal(title,body){const modal=ensureModal();modal.querySelector("[data-demo-modal-title]").textContent=title;modal.querySelector("[data-demo-modal-body]").innerHTML=body;modal.hidden=false;}
function tableFromRows(rows){if(!rows||!rows.length)return'<div class="ucc-live-empty"><strong>No matching records</strong><span>The source is readable but no records matched the current filter.</span></div>';const columns=Array.from(new Set(rows.flatMap(row=>Object.keys(row))));return`<div class="table-wrap"><table><thead><tr>${columns.map(col=>`<th>${esc(col)}</th>`).join("")}</tr></thead><tbody>${rows.map(row=>`<tr>${columns.map(col=>`<td>${esc(row[col])}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;}
async function openMetricRecords(config,dashboard,metric,title){
if(!metric){openModal("Live records","No available metric is mapped to this result.");return;}
openModal("Loading live records",`<div class="ucc-demo-modal-note">${esc(title||metric.label)}</div>`);
try{
const response=await callApi(config,dashboard,"drilldown",{metric_id:metric.id,page:1,page_size:100});
openModal(title||metric.label,`<div class="ucc-demo-modal-note"><strong>${esc(response.drilldown?.total||0)} matching record(s)</strong><br>${esc(response.drilldown?.doctype||metric.doctype||"")}</div>${tableFromRows(response.drilldown?.rows||[])}`);
}catch(error){openModal("Drill-down unavailable",esc(error.message||error));}
}
async function openRecords(config,chartId,dashboard){
const result=dashboardState(dashboard).result,section=sectionDefinition(config,activeSection(dashboard)),index=Math.max(0,(section?.charts||[]).findIndex(item=>item.id===chartId)),chart=(section?.charts||[])[index];
if(/readiness|source availability|status distribution|system health|control health/i.test(chart?.title||"")){openReadiness(config,dashboard);return;}
const rows=metricRows(result,index,chart),metric=rows.find(row=>row[2])?.[2];
return openMetricRecords(config,dashboard,metric,metric?.label||chart?.title||"Live records");
}
function openReadiness(config,dashboard){
const result=dashboardState(dashboard).result;
if(!result){openModal("Readiness","The live API has not returned a result.");return;}
const policy=result.policy||{},sources=result.sources||[],metrics=result.metrics||[];
openModal(`Criterion ${config.number} readiness`,`<div class="ucc-demo-modal-note"><strong>Criterion ${config.number} data readiness</strong><br>Source and metric status reflects the current user's permissions.</div><div class="grid2"><section><h3>Sources</h3><div class="table-wrap"><table><thead><tr><th>Source</th><th>Records</th><th>Status</th></tr></thead><tbody>${sources.map(row=>{const doctype=row.doctype||"";const action=doctype?`<button type="button" class="source-doctype-link ucc-qa-action" data-live-source-doctype="${esc(doctype)}">Open ${esc(displayDoctypeName(doctype))} list ↗</button>`:"";return`<tr><td><div>${esc(doctype||row.candidates?.join(" / ")||row.key)}</div>${action}</td><td>${row.count||0}</td><td>${statusBadge(row.status)}</td></tr>`;}).join("")}</tbody></table></div></section><section><h3>Metrics</h3><div class="table-wrap"><table><thead><tr><th>Metric</th><th>Value</th><th>Status</th></tr></thead><tbody>${metrics.map(item=>`<tr><td>${esc(item.label)}</td><td>${esc(metricValue(item))}</td><td>${statusBadge(item.status)}</td></tr>`).join("")}</tbody></table></div></section></div>`);
}
function showDiagnostics(config,dashboard){const state=dashboardState(dashboard),result=state.result,logs=state.logs;openModal(`Criterion ${config.number} diagnostics`,`<div class="table-wrap"><table><thead><tr><th>Time</th><th>Level</th><th>Event</th><th>Detail</th></tr></thead><tbody>${logs.map(row=>`<tr><td>${esc(row.time)}</td><td>${statusBadge(row.level)}</td><td>${esc(row.event)}</td><td>${esc(row.detail)}</td></tr>`).join("")||'<tr><td colspan="4">No diagnostic events.</td></tr>'}</tbody></table></div><div class="ucc-demo-modal-note">API: ${esc(config.apiMethod)} · Section: ${esc(result?.meta?.subcriterion||apiSection(config,dashboard,activeSection(dashboard)))}</div>`);}
async function handleAction(dashboard,action){const config=CONFIG[dashboard.dataset.demoDashboard],state=dashboardState(dashboard),result=state.result;if(action==="refresh")await loadLive(dashboard,true);if(action==="export-qa"){const rows=[["Section","Question","Answer","Source","Status"],...allQaRows(result)];download(`criterion_${config.number}_live_qa.csv`,rows.map(row=>row.map(csvCell).join(",")).join("\n"));}if(action==="export-exceptions"){const rows=[["Metric","Label","Value","Status","Source"],...allExceptionRows(result)];download(`criterion_${config.number}_live_exceptions.csv`,rows.map(row=>row.map(csvCell).join(",")).join("\n"));}if(action==="export-table"){const rows=[["Metric","Value","Unit","Status","Source"],...(result?.metrics||[]).map(item=>[item.label,item.value,item.unit,item.status,item.doctype||item.source])];download(`criterion_${config.number}_${result?.meta?.subcriterion||"section"}_live_metrics.csv`,rows.map(row=>row.map(csvCell).join(",")).join("\n"));}if(action==="copy-link"){const url=new URL(location.href);url.searchParams.set("dashboard",dashboard.dataset.demoDashboard);url.searchParams.set("live_tab",activeSection(dashboard));navigator.clipboard?.writeText(url.toString()).catch(()=>{});}if(action==="diagnostics")showDiagnostics(config,dashboard);if(action==="readiness")openReadiness(config,dashboard);}
platform.querySelectorAll("[data-demo-dashboard]").forEach(function(dashboard){const config=CONFIG[dashboard.dataset.demoDashboard];if(!config)return;if(window.__uccMergeSourcesQuality)window.__uccMergeSourcesQuality(dashboard,"data-demo-tab","data-demo-panel");ensureLiveVisualCards(dashboard,config);syncLiveSectionVisibility(dashboard,"overview");dashboard.dataset.liveApi="1";dashboard.querySelectorAll("[data-demo-tab]").forEach(button=>button.addEventListener("click",()=>showTab(dashboard,button.dataset.demoTab)));dashboard.querySelectorAll("[data-demo-filter]").forEach(input=>input.addEventListener("change",()=>loadLive(dashboard,true)));dashboard.addEventListener("ucc:live-tool-action",function(event){const action=event.detail&&event.detail.action;const mapped=action==="export-current"?"export-table":action;if(mapped)handleAction(dashboard,mapped);});dashboard.addEventListener("click",function(event){
const sourceButton=event.target.closest("[data-live-source-doctype]");
if(sourceButton){
event.preventDefault();
event.stopPropagation();
const doctype=sourceButton.dataset.liveSourceDoctype;
if(doctype)window.open(doctypeListRoute(doctype),"_blank","noopener");
return;
}
const questionButton=event.target.closest("[data-live-qa-records]");
if(questionButton){
event.preventDefault();
event.stopPropagation();
const metric=metricById(dashboardState(dashboard).result,questionButton.dataset.liveQaRecords);
openMetricRecords(config,dashboard,metric,questionButton.dataset.liveQaTitle||metric?.label||"Matching records");
return;
}
const actionButton=event.target.closest("[data-demo-action]");
if(actionButton){event.preventDefault();event.stopPropagation();handleAction(dashboard,actionButton.dataset.demoAction);return;}
const drill=event.target.closest("[data-demo-drill]");
if(drill){event.preventDefault();openRecords(config,drill.dataset.demoDrill,dashboard);return;}
const viewButton=event.target.closest("[data-demo-view]");
if(viewButton){const card=viewButton.closest("[data-demo-card]");if(!card)return;renderLiveChartCardNow(card);card.querySelectorAll("[data-demo-view]").forEach(button=>button.classList.toggle("active",button===viewButton));const diagram=card.querySelector("[data-demo-chart]"),table=card.querySelector("[data-demo-chart-table]");if(diagram)diagram.classList.toggle("hidden",viewButton.dataset.demoView!=="diagram");if(table)table.classList.toggle("hidden",viewButton.dataset.demoView!=="table");}
});dashboard.dataset.demoActiveTab="overview";dashboard.querySelectorAll("[data-demo-panel]").forEach(panel=>panel.classList.toggle("hidden",panel.dataset.demoPanel!=="overview"));if(!dashboard.classList.contains("ucc-hidden"))loadLive(dashboard);else renderReadiness(dashboard,config,null);});platform.addEventListener("ucc:dashboard-change",event=>{const id=event.detail&&event.detail.dashboard;if(!id)return;const dashboard=platform.querySelector(`[data-demo-dashboard="${CSS.escape(id)}"]`);if(dashboard)loadLive(dashboard);});
platform.addEventListener("click",function(event){
const sourceButton=event.target.closest("[data-live-source-doctype]");
if(!sourceButton||sourceButton.closest("[data-demo-dashboard]"))return;
event.preventDefault();
const doctype=sourceButton.dataset.liveSourceDoctype;
if(doctype)window.open(doctypeListRoute(doctype),"_blank","noopener");
});
window.UCCLiveAnalytics=Object.freeze({config:CONFIG,refresh:function(criterion){const dashboard=platform.querySelector(`[data-demo-dashboard="${CSS.escape(criterion)}"]`);if(dashboard)return loadLive(dashboard,true);},showTab:function(criterion,tab){const dashboard=platform.querySelector(`[data-demo-dashboard="${CSS.escape(criterion)}"]`);if(dashboard)showTab(dashboard,tab);}});
})();
/* UCC DIAGRAM EXPLORER v1.9.11 */
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

const parentTabMap = Object.freeze({});

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
c511Panel: "",
localPanel: node.closest("[data-local-panel]")?.dataset.localPanel || "",
type: kind === "demo" ? node.dataset.demoChartType || "live-foundation" : inferType(id, title),
source: kind === "demo" ? "Permission-aware live API foundation" : sourceHint(node),
description: ""
};
entry.section = sectionLabel(entry);
return entry;
}

function buildRegistry() {
const registry = new Map();

Object.entries(global.UCCC4VisualDefinitions || {}).forEach(([panel, definitions]) => {
(definitions || []).forEach(definition => {
if (definition.enabled === false) return;
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
source: "Permission-aware Criterion 4 API metrics",
description: text(definition.description || "")
};
entry.section = sectionLabel(entry);
if (!registry.has(entry.key)) registry.set(entry.key, entry);
});
});

Object.entries(global.UCCLiveVisualDefinitions || {}).forEach(([dashboard, sections]) => {
Object.entries(sections || {}).forEach(([panel, definitions]) => {
(definitions || []).forEach(definition => {
if (definition.enabled === false) return;
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
source: "Permission-aware live API metrics",
description: text(definition.description || "")
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
${entry.description ? `<small>${entry.description}</small>` : ""}
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

function resolveEntryNode(entry) {
if (entry.node && entry.node.isConnected) return entry.node;
if (entry.kind === "c4-expanded") {
entry.node = platformRoot.querySelector(`[data-c4-expanded-chart="${CSS.escape(entry.id)}"]`);
} else if (entry.kind === "demo") {
entry.node = platformRoot.querySelector(`[data-demo-chart="${CSS.escape(entry.id)}"]`);
}
return entry.node || null;
}

function revealNestedViews(entry) {
const node = resolveEntryNode(entry);
if (entry.kind === "demo") {
window.UCCLiveAnalytics?.showTab(entry.dashboard, entry.panel || "overview");
node?.closest("[data-demo-card]")?.querySelector('[data-demo-view="diagram"]')?.click();
return;
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
window.UCCLiveAnalytics?.showTab(entry.dashboard, entry.panel || "overview");
setTimeout(finish, 120);
} else if (entry.dashboard === "criterion_4") {
const tab = platformRoot.querySelector(
`[data-dashboard-panel="criterion_4"] [data-c4-tab="${CSS.escape(entry.panel || "overview")}"]`
);
if (tab) tab.click();
setTimeout(finish, 180);
} else {
setTimeout(finish, 120);
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
/* UCC universal visual navigation and diagnostics v1.9.11 */
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
'[data-dashboard-panel="criterion_5"] nav.tabs > button[data-tab]'
));
}

const menu = document.createElement("section");
menu.className = "ucc-visual-hover-menu";
menu.hidden = true;
menu.setAttribute("role", "region");
menu.setAttribute("aria-label", "Section visual menu");
menu.innerHTML = '<header><div><strong data-visual-menu-title>Section visuals</strong><br><span data-visual-menu-count>0 visuals</span></div></header><div class="ucc-visual-hover-menu-list" data-visual-menu-list></div>';
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
trigger.removeAttribute("aria-haspopup");
trigger.removeAttribute("aria-expanded");
}
function bindTabs() {
directTabTriggers().forEach(trigger => {
addCountBadge(trigger);
trigger.dataset.visualHoverReady = "1";
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
if (event.target.closest("[data-ucc-open-mapping]")) {
event.preventDefault();
event.stopPropagation();
const dashboard = activeDashboard;
closeMenu();
openSourceMapping(dashboard);
return;
}
});
// Section tabs now navigate directly. Escape still closes diagnostics and any legacy hidden visual panel.
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
platform_version: "1.9.11",
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
function deferredUnrendered(node) {
// Click-to-render charts are intentionally empty until the user opens the Diagram view. Don't flag them as failed renders.
const demoCard = node.closest("[data-demo-card]");
if (demoCard) return demoCard.dataset.liveCardRendered !== "1";
const c4Card = node.closest("[data-c4-expanded-card]");
if (c4Card) return c4Card.dataset.c4CardRendered !== "1";
return node.dataset.c5Deferred === "1";
}
function scanVisuals() {
const now = Date.now();
platform.querySelectorAll("[data-c4-visual],[data-c4-expanded-chart],[data-chart],[data-demo-chart]").forEach(node => {
if (!node.isConnected || node.getClientRects().length === 0 || isLoading(node) || deferredUnrendered(node)) return;
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
