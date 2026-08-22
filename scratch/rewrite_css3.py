import os

css_content = """/* ============================================================
   AP Invoice Exception Assistant — Soft Minimal Enterprise
   ============================================================ */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Open+Sans:wght@400;500;600;700&family=Poppins:wght@500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  /* Soft Neutral Theme */
  --bg-page: #F5F3EF;
  --bg-card: #FCFBF8;
  --bg-secondary: #EBE8E3;
  
  --border-subtle: #DEDAD3;
  
  --text-primary: #2F3437;
  --text-secondary: #6B7280;
  --text-inverse: #FFFFFF;
  
  --accent-primary: #6F7F6B;
  --accent-hover: #5a6857;
  --accent-bg: #EAECE8;
  
  --severity-high: #B85C5C;
  --severity-high-bg: rgba(184, 92, 92, 0.08);
  --severity-medium: #D99036;
  --severity-medium-bg: rgba(217, 144, 54, 0.08);
  --severity-low: #8A8175;
  --severity-low-bg: rgba(138, 129, 117, 0.08);
  
  --success: #5C7F62;
  --success-bg: rgba(92, 127, 98, 0.08);
  
  /* Typography */
  --font-sans: 'Inter', 'Open Sans', -apple-system, sans-serif;
  --font-heading: 'Poppins', -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
  
  /* Spacing Scale (Swiss-inspired) */
  --space-xs: 8px;
  --space-sm: 12px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  
  /* Borders */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  
  /* Shadows */
  --shadow-subtle: 0 2px 4px rgba(47, 52, 55, 0.03);
  --shadow-float: 0 8px 24px rgba(47, 52, 55, 0.1);
  
  /* Transitions */
  --transition-base: 250ms cubic-bezier(0.4, 0, 0.2, 1);
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
  margin: 0;
}

/* --- Split-Screen Layout (Crucial for Chatbot) --- */
#app {
  width: 100%;
}

.app-layout {
  display: flex;
  width: 100%;
  max-width: 1600px;
  margin: 0 auto;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  min-width: 0; /* Prevents flex children from overflowing */
  padding: 0 var(--space-xl);
  display: flex;
  flex-direction: column;
  transition: padding var(--transition-base);
  margin: 0 auto;
  max-width: 1200px; /* Constrain main content nicely */
  width: 100%;
}

/* --- Header --- */
.app-header {
  padding: var(--space-xl) 0 var(--space-md);
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border-subtle);
  margin-bottom: var(--space-xl);
}

.app-header__left {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.app-header__icon {
  font-size: 1.75rem;
  color: var(--accent-primary);
}

.app-header__text {
  display: flex;
  flex-direction: column;
}

.app-header__title {
  font-family: var(--font-heading);
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
}

.app-header__subtitle {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.app-header__status {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  font-size: 0.85rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--success);
}

/* --- Typography Utilities --- */
h1, h2, h3, h4 {
  font-family: var(--font-heading);
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.2;
}

.section-title { font-size: 1.25rem; }
.card__title { font-size: 1.1rem; }

.mono { font-family: var(--font-mono); }
.text-muted { color: var(--text-secondary); }
.text-right { text-align: right; }
.text-center { text-align: center; }
.text-warning { color: var(--severity-medium); }

.mt-sm { margin-top: var(--space-sm); }
.mt-md { margin-top: var(--space-md); }
.mt-lg { margin-top: var(--space-lg); }
.mt-xl { margin-top: var(--space-xl); }
.mb-sm { margin-bottom: var(--space-sm); }
.mb-md { margin-bottom: var(--space-md); }
.mb-lg { margin-bottom: var(--space-lg); }
.mb-xl { margin-bottom: var(--space-xl); }

/* --- Info Strip --- */
.info-strip {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: var(--space-md) var(--space-lg);
  margin-bottom: var(--space-xl);
  display: flex;
  align-items: flex-start;
  gap: var(--space-md);
  font-size: 0.9rem;
  color: var(--text-primary);
  box-shadow: var(--shadow-subtle);
}

.info-strip__icon {
  font-size: 1.1rem;
  margin-top: 2px;
}
.info-strip__desc {
  color: var(--text-secondary);
  margin-left: var(--space-xs);
}

/* --- Workspace Grid (2 Columns) --- */
.workspace-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-lg);
  margin-bottom: var(--space-xl);
  align-items: stretch;
}

@media (max-width: 900px) {
  .workspace-grid {
    grid-template-columns: 1fr;
  }
}

/* --- Cards --- */
.card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: var(--space-lg);
  box-shadow: var(--shadow-subtle);
  display: flex;
  flex-direction: column;
}

.card__header {
  margin-bottom: var(--space-lg);
}

/* --- Upload Zone --- */
.upload-zone {
  border: 1px dashed var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: var(--space-xl) var(--space-lg);
  text-align: center;
  cursor: pointer;
  background: var(--bg-secondary);
  transition: all var(--transition-base);
}

.upload-zone:hover, .upload-zone.active {
  border-color: var(--accent-primary);
  background: var(--accent-bg);
}

.upload-zone.has-file {
  border-color: var(--success);
  border-style: solid;
  background: var(--success-bg);
  padding: var(--space-lg);
}

.upload-zone__icon {
  font-size: 1.5rem;
  margin-bottom: var(--space-sm);
}

.upload-zone__text {
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--text-primary);
}

.upload-zone__hint {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-top: var(--space-xs);
}

.upload-zone__filename {
  font-size: 0.9rem;
  color: var(--text-primary);
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
.upload-zone__filename::before {
  content: '✓';
  color: var(--success);
}

.sample-invoices-section {
  text-align: center;
}
.section-label {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.sample-invoices {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-sm);
  justify-content: center;
}
.sample-invoice-btn {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 6px 12px;
  font-size: 0.85rem;
  color: var(--text-primary);
  cursor: pointer;
  transition: all var(--transition-base);
}
.sample-invoice-btn:hover {
  background: var(--bg-secondary);
  border-color: var(--text-secondary);
}

/* --- PO Selector --- */
.po-selector__label {
  display: block;
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin-bottom: var(--space-xs);
}

.po-selector select {
  width: 100%;
  padding: 12px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  font-family: var(--font-sans);
  font-size: 0.95rem;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%236B7280' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 16px center;
}

.po-selector select:focus {
  outline: none;
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 1px var(--accent-primary);
}

.table-wrapper {
  overflow-x: auto;
}

.po-table, .comparison-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}
.po-table th, .comparison-table th {
  background: var(--bg-secondary);
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border-subtle);
  white-space: nowrap;
}
.po-table td, .comparison-table td {
  padding: 14px 16px;
  border-bottom: 1px solid var(--border-subtle);
  color: var(--text-primary);
  vertical-align: top;
}
.po-table tr:last-child td, .comparison-table tr:last-child td {
  border-bottom: none;
}

.po-totals {
  text-align: right;
  font-size: 0.95rem;
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
  gap: var(--space-xs);
  font-family: var(--font-sans);
  font-size: 0.95rem;
  font-weight: 500;
  border: 1px solid transparent;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: background var(--transition-base), opacity var(--transition-base);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn--primary {
  background: var(--accent-primary);
  color: var(--text-inverse);
  padding: 16px 32px;
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
  padding: 6px 12px;
  font-size: 0.85rem;
}

.compare-action {
  display: flex;
  justify-content: center;
  margin-bottom: var(--space-2xl);
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

/* Summary Grid */
.summary-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: var(--space-lg);
}
@media (max-width: 1024px) {
  .summary-grid {
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  }
}

.summary-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: var(--space-lg);
  display: flex;
  flex-direction: column;
}
.summary-card__label {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: var(--space-xs);
}
.summary-card__value {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--text-primary);
}

/* Specific colors for summary cards only on value */
.summary-card--total .summary-card__value { color: var(--severity-high); }
.summary-card--price .summary-card__value { color: var(--severity-medium); }
.summary-card--qty .summary-card__value { color: var(--severity-medium); }
.summary-card--tax .summary-card__value { color: var(--severity-high); }
.summary-card--match .summary-card__value { color: var(--success); }

/* Badges */
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: var(--radius-sm);
  font-size: 0.85rem;
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

/* --- Extraction Preview --- */
.section-title-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.confidence-badge {
  font-size: 0.85rem;
  color: var(--text-secondary);
  background: var(--bg-secondary);
  padding: 6px 12px;
  border-radius: var(--radius-sm);
}

.preview-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-lg);
}
@media (max-width: 768px) {
  .preview-container {
    grid-template-columns: 1fr;
  }
}

.preview-pane {
  padding: 0;
}
.preview-pane__header {
  padding: var(--space-md) var(--space-lg);
  border-bottom: 1px solid var(--border-subtle);
  font-weight: 600;
  font-size: 1rem;
  background: var(--bg-card); /* Ensure consistency */
}
.preview-pane__content {
  padding: var(--space-lg);
  max-height: 500px;
  overflow-y: auto;
}
.empty-state {
  text-align: center;
  color: var(--text-secondary);
  padding: var(--space-2xl) 0;
}
.empty-state__icon {
  font-size: 2.5rem;
  margin-bottom: var(--space-sm);
}

/* --- Comparison Table Specifics --- */
.table-card {
  padding: 0;
}

.cell-mismatch {
  font-weight: 500;
}
.cell-match {
  color: var(--text-secondary);
}
.cell-diff {
  display: block;
  font-size: 0.8rem;
  font-family: var(--font-mono);
  margin-top: 4px;
}
.cell-diff--over { color: var(--severity-high); }
.cell-diff--under { color: var(--severity-medium); }

.match-badge {
  padding: 4px 8px;
  border-radius: var(--radius-sm);
  font-size: 0.8rem;
  font-weight: 600;
  display: inline-block;
}
.match-badge--matched { background: var(--success-bg); color: var(--success); }
.match-badge--missing { background: var(--severity-high-bg); color: var(--severity-high); }
.match-badge--extra { background: var(--severity-medium-bg); color: var(--severity-medium); }
.match-badge--mismatch { background: var(--severity-high-bg); color: var(--severity-high); }

/* --- Exception Cards --- */
.exception-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}
.exception-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: var(--space-lg);
  border-left: 4px solid transparent;
}
.exception-card--high { border-left-color: var(--severity-high); }
.exception-card--medium { border-left-color: var(--severity-medium); }
.exception-card--low { border-left-color: var(--severity-low); }

.exception-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-sm);
}
.exception-card__type {
  font-family: var(--font-heading);
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
}
.exception-card__explanation {
  font-size: 0.95rem;
  color: var(--text-secondary);
  margin-bottom: var(--space-md);
}
.severity-badge {
  padding: 4px 12px;
  border-radius: var(--radius-sm);
  font-size: 0.8rem;
  font-weight: 600;
}
.severity-badge--high { background: var(--severity-high-bg); color: var(--severity-high); }
.severity-badge--medium { background: var(--severity-medium-bg); color: var(--severity-medium); }
.severity-badge--low { background: var(--severity-low-bg); color: var(--severity-low); }

.exception-card__source {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  color: var(--text-secondary);
  background: var(--bg-secondary);
  padding: 12px 16px;
  border-radius: var(--radius-sm);
  margin-bottom: var(--space-md);
}

.exception-card__values {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: var(--space-lg);
  padding-top: var(--space-md);
  border-top: 1px solid var(--border-subtle);
}
.value-block {
  display: flex;
  flex-direction: column;
}
.value-block__label {
  font-size: 0.8rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 4px;
}
.value-block__value {
  font-family: var(--font-mono);
  font-size: 1rem;
  font-weight: 500;
}
.value-block__value--diff { color: var(--severity-high); }

/* --- Chatbot Floating Panel (SPLIT SCREEN) --- */
.chat-toggle-fab {
  position: fixed;
  bottom: var(--space-xl);
  right: var(--space-xl);
  width: 56px;
  height: 56px;
  background: var(--accent-primary);
  color: var(--text-inverse);
  border: none;
  border-radius: 50%;
  font-size: 1.5rem;
  cursor: pointer;
  box-shadow: var(--shadow-float);
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform var(--transition-base);
}
.chat-toggle-fab:hover {
  transform: translateY(-2px);
  background: var(--accent-hover);
}
.chat-toggle-fab.hidden {
  display: none !important;
}

.chat-panel {
  display: none; /* Hidden by default */
  width: 400px;
  flex-shrink: 0;
  height: 100vh;
  position: sticky;
  top: 0;
  background: var(--bg-card);
  border-left: 1px solid var(--border-subtle);
  box-shadow: -4px 0 24px rgba(47, 52, 55, 0.05);
}
.chat-panel.active {
  display: flex;
  flex-direction: column;
}

@media (max-width: 1200px) {
  .chat-panel.active {
    position: fixed;
    right: 0;
    top: 0;
    z-index: 100;
  }
}
@media (max-width: 600px) {
  .chat-panel.active {
    width: 100%;
  }
}

.chat-panel__header {
  padding: var(--space-lg);
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.chat-panel__title {
  font-family: var(--font-heading);
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--text-primary);
}
.chat-panel__close {
  background: transparent;
  border: none;
  font-size: 1.25rem;
  color: var(--text-secondary);
  cursor: pointer;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-lg);
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}
.chat-message {
  padding: 12px 16px;
  border-radius: var(--radius-md);
  font-size: 0.95rem;
  max-width: 90%;
  line-height: 1.5;
}
.chat-message--user {
  background: var(--bg-secondary);
  color: var(--text-primary);
  align-self: flex-end;
  border-bottom-right-radius: 4px;
}
.chat-message--assistant {
  background: var(--accent-bg);
  color: var(--text-primary);
  align-self: flex-start;
  border-bottom-left-radius: 4px;
}
.chat-message--system {
  background: transparent;
  color: var(--text-secondary);
  align-self: center;
  text-align: center;
  font-size: 0.9rem;
}

.chat-suggestions {
  padding: 0 var(--space-lg) var(--space-md);
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-xs);
}
.chat-suggestion-btn {
  background: var(--bg-page);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 8px 12px;
  font-size: 0.85rem;
  color: var(--text-primary);
  cursor: pointer;
  transition: background var(--transition-base);
}
.chat-suggestion-btn:hover {
  background: var(--bg-secondary);
}

.chat-input-area {
  padding: var(--space-md) var(--space-lg) var(--space-lg);
  border-top: 1px solid var(--border-subtle);
  background: var(--bg-card);
}
.chat-input-wrapper {
  display: flex;
  gap: var(--space-xs);
}
.chat-input {
  flex: 1;
  padding: 14px 16px;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  background: var(--bg-page);
  font-family: var(--font-sans);
  font-size: 0.95rem;
}
.chat-input:focus {
  outline: none;
  border-color: var(--accent-primary);
}
.chat-send-btn {
  width: 48px;
  border-radius: var(--radius-sm);
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

/* --- Loading Overlay --- */
.loading-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(245, 243, 239, 0.9);
  z-index: 200;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-md);
}
.loading-overlay.active { display: flex; }
.loading-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid var(--border-subtle);
  border-top-color: var(--accent-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.loading-text {
  font-weight: 500;
  font-size: 1.1rem;
  color: var(--text-primary);
}
.loading-step {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

/* Utilities */
.hidden { display: none !important; }
"""

with open(r'c:\Users\VASANTHI\OneDrive\Desktop\AP Invoice\frontend\styles.css', 'w', encoding='utf-8') as f:
    f.write(css_content)

print("Overwrote styles.css successfully.")
