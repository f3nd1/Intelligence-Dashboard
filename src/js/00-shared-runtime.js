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
