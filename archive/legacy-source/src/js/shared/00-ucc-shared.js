/* Shared frontend helpers for Criteria 1–7.
   Existing v1.7.0 behavior remains in preserved modules.
   Future criterion code must use UCCShared rather than adding duplicates. */
(function (global) {
  "use strict";

  if (global.UCCShared) return;

  function escapeHtml(value) {
    const div = document.createElement("div");
    div.textContent = value == null ? "" : String(value);
    return div.innerHTML;
  }

  function downloadText(filename, text, mimeType) {
    const blob = new Blob([text], { type: mimeType || "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = filename;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    URL.revokeObjectURL(url);
  }

  function toCsv(rows, columns) {
    const quote = value => `"${String(value == null ? "" : value).replace(/"/g, '""')}"`;
    const header = columns.map(column => quote(column.label)).join(",");
    const body = rows.map(row =>
      columns.map(column => quote(row[column.key])).join(",")
    );
    return [header].concat(body).join("\n");
  }

  function doctypeRoute(doctype) {
    if (!doctype) return "#";
    let slug = "";
    if (global.frappe && frappe.router && typeof frappe.router.slug === "function") {
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
    downloadText,
    toCsv,
    doctypeRoute,
    openDoctype,
    readStorage,
    writeStorage
  });
})(window);
