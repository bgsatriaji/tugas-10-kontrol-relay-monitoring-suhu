/** Konfigurasi Node-RED khusus Codespaces (port 1880). */
module.exports = {
  uiPort: process.env.PORT || 1880,
  uiHost: "0.0.0.0",
  flowFilePretty: true,
  diagnostics: { enabled: false },
  logging: { console: { level: "info", metrics: false, audit: false } },
  editorTheme: { page: { title: "Pertemuan 10 | Node-RED" } }
};
