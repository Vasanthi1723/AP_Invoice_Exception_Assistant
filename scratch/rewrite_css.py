import os

css_content = """/* ============================================================
   AP Invoice Exception Assistant — Enterprise Finance Theme
   ============================================================ */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  /* Enterprise Finance Color Palette */
  --bg-page: #F6F4EF;
  --bg-card: #FFFFFF;
  --bg-secondary: #EFEDE7;
  --bg-accent-light: #E6EFE8;
  
  --border-subtle: #DEDCD6;
  --border-focus: #8FAF9A;
  
  --text-primary: #2F3A32;
  --text-secondary: #73786F;
  --text-inverse: #FFFFFF;
  
  --accent-primary: #4F7C65;
  --accent-secondary: #8FAF9A;
  --accent-hover: #3d6351;
  
  --severity-high: #B85C5C;
  --severity-high-bg: rgba(184, 92, 92, 0.08);
  --severity-medium: #C28A3A;
  --severity-medium-bg: rgba(194, 138, 58, 0.08);
  --severity-low: #7A8F7D;
  --severity-low-bg: rgba(122, 143, 125, 0.08);
  
  --success: #4F8A65;
  --success-bg: rgba(79, 138, 101, 0.08);
  
  /* Typography */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-heading: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
  
  /* Spacing */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 12px;
  --space-lg: 16px;
  --space-xl: 24px;
  --space-2xl: 32px;
  --space-3xl: 40px;
  
  /* Borders */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  
  /* Shadows */
  --shadow-subtle: 0 2px 4px rgba(47, 58, 50, 0.03), 0 1px 2px rgba(47, 58, 50, 0.02);
  
  /* Transitions */
  --transition-base: 200ms ease;
}

*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  font-size: 16px;
  scroll-behavior: smooth;
}

body {
  font-family: var(--font-sans);
  background: var(--bg-page);
  color: var(--text-primary);
  line-height: 1.5;
  min-height: 100vh;
  display: flex;
  justify-content: center;
}

#app {
  width: 100%;
  max-width: 1400px;
  padding: 0 var(--space-xl);
}

/* --- Layout --- */
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* --- Header --- */
.app-header {
  padding: var(--space-xl) 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border-subtle);
  margin-bottom: var(--space-2xl);
}

.app-header__brand {
  display: flex;
  flex-direction: column;
}

.app-header__title {
  font-family: var(--font-heading);
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--text-primary);
}

.app-header__subtitle {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin-top: var(--space-xs);
}

.app-header__status {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--success);
}

/* --- Typography --- */
h1, h2, h3, h4 {
  font-family: var(--font-heading);
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.2;
}

h2 { font-size: 1.25rem; }
h3 { font-size: 1.1rem; }
.mono { font-family: var(--font-mono); }
.text-muted { color: var(--text-secondary); }
.text-right { text-align: right; }
.text-center { text-align: center; }

.mt-sm { margin-top: var(--space-sm); }
.mt-md { margin-top: var(--space-md); }
.mt-lg { margin-top: var(--space-lg); }
.mt-xl { margin-top: var(--space-xl); }
.mb-sm { margin-bottom: var(--space-sm); }
.mb-md { margin-bottom: var(--space-md); }
.mb-lg { margin-bottom: var(--space-lg); }
.mb-xl { margin-bottom: var(--space-xl); }

/* --- Demo Banner --- */
.demo-banner {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: var(--space-lg) var(--space-xl);
  margin-bottom: var(--space-2xl);
  display: flex;
  align-items: center;
  gap: var(--space-lg);
  font-size: 0.9rem;
  color: var(--text-primary);
  box-shadow: var(--shadow-subtle);
}

/* --- Workspace Grid --- */
.workspace-grid {
  display: grid;
  grid-template-columns: 1fr 1.2fr 0.9fr;
  gap: var(--space-xl);
  margin-bottom: var(--space-2xl);
  align-items: stretch;
}

@media (max-width: 1024px) {
  .workspace-grid {
    grid-template-columns: 1fr 1fr;
  }
  .chat-panel {
    grid-column: 1 / -1;
  }
}
@media (max-width: 768px) {
  .workspace-grid {
    grid-template-columns: 1fr;
  }
}

/* --- Cards --- */
.card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: var(--space-xl);
  box-shadow: var(--shadow-subtle);
  display: flex;
  flex-direction: column;
}

.card__header {
  margin-bottom: var(--space-lg);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card__title {
  font-family: var(--font-heading);
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
}

/* --- Upload Zone --- */
.upload-zone {
  border: 1px dashed var(--border-subtle);
  border-radius: var(--radius-md);
  padding: var(--space-xl) var(--space-lg);
  text-align: center;
  cursor: pointer;
  background: var(--bg-page);
  transition: all var(--transition-base);
}

.upload-zone:hover, .upload-zone.active {
  border-color: var(--accent-primary);
  background: var(--bg-accent-light);
}

.upload-zone.has-file {
  border-color: var(--border-subtle);
  border-style: solid;
  background: var(--bg-card);
  padding: var(--space-lg);
}

.upload-zone__icon {
  font-size: 1.5rem;
  margin-bottom: var(--space-sm);
}

.upload-zone__title {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-primary);
}

.upload-zone__hint {
  font-size: 0.8rem;
  color: var(--text-secondary);
  margin-top: var(--space-xs);
}

.upload-zone__filename {
  font-size: 0.85rem;
  color: var(--text-primary);
  font-weight: 500;
}

.sample-invoices {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-sm);
  justify-content: center;
}
.sample-invoice-btn {
  background: var(--bg-secondary);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 4px 10px;
  font-size: 0.75rem;
  color: var(--text-primary);
  cursor: pointer;
  transition: background var(--transition-base);
}
.sample-invoice-btn:hover {
  background: var(--border-subtle);
}

/* --- PO Selector --- */
.po-selector__label {
  display: block;
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: var(--space-sm);
}

.po-selector select {
  width: 100%;
  padding: 10px 14px;
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  font-family: var(--font-sans);
  font-size: 0.9rem;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%2373786F' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 14px center;
}

.po-selector select:focus {
  outline: none;
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 1px var(--accent-primary);
}

.po-totals {
  text-align: right;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-primary);
  padding-top: var(--space-md);
  border-top: 1px solid var(--border-subtle);
}

/* --- Buttons --- */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-sm);
  font-family: var(--font-sans);
  font-size: 0.9rem;
  font-weight: 500;
  border: 1px solid transparent;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn--primary {
  background: var(--accent-primary);
  color: var(--text-inverse);
  padding: 16px 28px;
}

.btn--primary:hover:not(:disabled) {
  background: var(--accent-hover);
}

.btn--secondary {
  background: var(--bg-secondary);
  border-color: var(--border-subtle);
  color: var(--text-primary);
  padding: 8px 16px;
}

.btn--secondary:hover:not(:disabled) {
  background: var(--border-subtle);
}

.btn--sm {
  padding: 8px 16px;
  font-size: 0.85rem;
}
.btn--lg {
  padding: 16px 32px;
  font-size: 1rem;
}

.compare-action {
  display: flex;
  justify-content: center;
  margin-bottom: var(--space-3xl);
}

/* --- Chat Assistant --- */
.chat-panel {
  padding: 0;
  height: 100%;
}
.chat-panel__header {
  padding: var(--space-lg) var(--space-xl);
  border-bottom: 1px solid var(--border-subtle);
  background: var(--bg-card);
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
}
.chat-panel__title {
  font-family: var(--font-heading);
  font-size: 1rem;
  font-weight: 600;
}
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-xl);
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
  min-height: 200px;
}
.chat-message {
  padding: 12px 16px;
  border-radius: var(--radius-md);
  font-size: 0.9rem;
  max-width: 90%;
  line-height: 1.5;
}
.chat-message--user {
  background: var(--bg-secondary);
  color: var(--text-primary);
  align-self: flex-end;
}
.chat-message--assistant {
  background: var(--bg-accent-light);
  color: var(--text-primary);
  align-self: flex-start;
}
.chat-message--system {
  background: transparent;
  color: var(--text-secondary);
  align-self: center;
  text-align: center;
  font-size: 0.85rem;
}
.chat-suggestions {
  padding: 0 var(--space-xl) var(--space-lg);
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-sm);
}
.chat-suggestion-btn {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 6px 12px;
  font-size: 0.8rem;
  color: var(--text-primary);
  cursor: pointer;
}
.chat-suggestion-btn:hover {
  background: var(--bg-secondary);
}
.chat-input-area {
  padding: var(--space-lg) var(--space-xl);
  border-top: 1px solid var(--border-subtle);
  background: var(--bg-card);
  border-radius: 0 0 var(--radius-lg) var(--radius-lg);
}
.chat-input-wrapper {
  display: flex;
  gap: var(--space-sm);
}
.chat-input {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  background: var(--bg-card);
  font-family: var(--font-sans);
  font-size: 0.9rem;
}
.chat-input:focus {
  outline: none;
  border-color: var(--accent-primary);
}
.chat-send-btn {
  width: 40px;
  border-radius: var(--radius-md);
  background: var(--accent-primary);
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
.chat-send-btn:disabled {
  opacity: 0.5;
}

/* --- Results Section --- */
.results-section {
  display: none;
}
.results-section.active {
  display: block;
}
.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Summary Strip */
.summary-strip {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: var(--space-lg);
  margin-bottom: var(--space-2xl);
}
.summary-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: var(--space-xl);
}
.summary-card__label {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: var(--space-xs);
}
.summary-card__value {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
}

/* Badges */
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  font-weight: 600;
  margin-left: var(--space-md);
}
.status-badge--exceptions {
  background: var(--severity-high-bg);
  color: var(--severity-high);
}
.status-badge--match {
  background: var(--success-bg);
  color: var(--success);
}
.confidence-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  font-weight: 500;
  background: var(--bg-secondary);
  color: var(--text-secondary);
}

/* --- Tables --- */
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
}
th {
  background: var(--bg-page);
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  color: var(--text-secondary);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  border-bottom: 1px solid var(--border-subtle);
}
td {
  padding: 16px;
  border-bottom: 1px solid var(--border-subtle);
  color: var(--text-primary);
  vertical-align: top;
}
tr:last-child td {
  border-bottom: none;
}
.comparison-table-wrapper {
  overflow-x: auto;
}
.cell-mismatch {
  font-weight: 500;
}
.cell-match {
  color: var(--text-secondary);
}
.cell-diff {
  display: block;
  font-size: 0.75rem;
  font-family: var(--font-mono);
  margin-top: 4px;
}
.cell-diff--over { color: var(--severity-high); }
.cell-diff--under { color: var(--severity-medium); }

/* --- Preview Section --- */
.section-title-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.preview-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-lg);
}
.preview-pane {
  padding: 0;
}
.preview-pane__header {
  padding: var(--space-lg) var(--space-xl);
  border-bottom: 1px solid var(--border-subtle);
  font-weight: 600;
  font-size: 0.95rem;
  background: var(--bg-card);
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
}
.preview-pane__content {
  padding: var(--space-xl);
  max-height: 500px;
  overflow-y: auto;
}

/* --- Exceptions --- */
.exception-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}
.exception-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: var(--space-xl);
  border-left: 3px solid transparent;
}
.exception-card--high { border-left-color: var(--severity-high); }
.exception-card--medium { border-left-color: var(--severity-medium); }
.exception-card--low { border-left-color: var(--severity-low); }

.exception-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-md);
}
.exception-card__type {
  font-family: var(--font-heading);
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--text-primary);
}
.exception-card__explanation {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin-bottom: var(--space-lg);
}
.severity-badge {
  padding: 4px 10px;
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  font-weight: 500;
}
.severity-badge--high { background: var(--severity-high-bg); color: var(--severity-high); }
.severity-badge--medium { background: var(--severity-medium-bg); color: var(--severity-medium); }
.severity-badge--low { background: var(--severity-low-bg); color: var(--severity-low); }

.exception-card__values {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: var(--space-lg);
  padding-top: var(--space-lg);
  border-top: 1px solid var(--border-subtle);
}
.value-block {
  display: flex;
  flex-direction: column;
}
.value-block__label {
  font-size: 0.75rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 4px;
}
.value-block__value {
  font-family: var(--font-mono);
  font-size: 0.95rem;
  font-weight: 500;
}
.value-block__value--diff { color: var(--severity-high); }

/* --- Loading Overlay --- */
.loading-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(246, 244, 239, 0.9);
  z-index: 100;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-md);
}
.loading-overlay.active { display: flex; }
.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border-subtle);
  border-top-color: var(--accent-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.loading-text {
  font-weight: 500;
  color: var(--text-primary);
}
.loading-step {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

/* Utilities */
.hidden { display: none !important; }
"""

with open(r'c:\Users\VASANTHI\OneDrive\Desktop\AP Invoice\frontend\styles.css', 'w', encoding='utf-8') as f:
    f.write(css_content)

print("Overwrote styles.css successfully.")
