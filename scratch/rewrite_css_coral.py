import os

css_content = """/* ============================================================
   AP Invoice Exception Assistant — Warm Coral Enterprise SaaS
   ============================================================ */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Open+Sans:wght@400;500;600;700&family=Poppins:wght@500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  /* BACKGROUNDS */
  --bg-primary: #F5F2ED;
  --bg-secondary: #EEEAE3;
  --surface: #FFFFFF;

  /* PRIMARY BRAND */
  --primary: #E85D3F;
  --primary-hover: #D94F32;
  --primary-soft: #FCE8E2;

  /* ACCENT */
  --accent-orange: #F47A4A;
  --accent-peach: #F7B39B;

  /* TEXT */
  --text-primary: #2B2D31;
  --text-secondary: #6B6B6B;
  --text-muted: #8A8A8A;
  --text-inverse: #FFFFFF;

  /* BORDERS */
  --border: #DEDAD3;
  --border-light: #EAE6E0;

  /* SUCCESS */
  --success: #5E8B6B;
  --success-soft: #E7F1E9;

  /* WARNING */
  --warning: #D99A3D;
  --warning-soft: #FFF3DD;

  /* ERROR */
  --error: #C95A5A;
  --error-soft: #FBE8E8;

  /* TYPOGRAPHY */
  --font-sans: 'Inter', 'Open Sans', -apple-system, sans-serif;
  --font-heading: 'Poppins', -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* SPACING SCALE */
  --space-xs: 8px;
  --space-sm: 12px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 40px;

  /* BORDER RADIUS */
  --radius-sm: 6px; /* controls */
  --radius-md: 8px; /* buttons */
  --radius-lg: 12px; /* cards */

  /* SHADOW */
  --shadow-subtle: 0 4px 16px rgba(45, 40, 35, 0.06);
  --shadow-float: 0 8px 24px rgba(45, 40, 35, 0.12);

  /* TRANSITIONS */
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
  background: var(--bg-primary);
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
  max-width: 1600px; /* Allows room for chatbot side-by-side */
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
  border-bottom: 1px solid var(--border);
  margin-bottom: var(--space-xl);
  background: transparent;
}

.app-header__left {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.app-header__icon {
  font-size: 1.5rem;
  color: var(--primary);
}

.app-header__text {
  display: flex;
  flex-direction: column;
}

.app-header__title {
  font-family: var(--font-heading);
  font-size: 1.75rem; /* 28px */
  font-weight: 700;
  color: var(--text-primary);
}

.app-header__subtitle {
  font-size: 0.95rem;
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
  color: var(--text-primary);
  line-height: 1.2;
}

.section-title { 
  font-size: 1.375rem; /* ~22px */
  font-weight: 600;
}
.card__title { 
  font-size: 1.125rem; /* 18px */
  font-weight: 600;
}

.mono { font-family: var(--font-mono); }
.text-muted { color: var(--text-secondary); }
.text-right { text-align: right; }
.text-center { text-align: center; }
.text-warning { color: var(--warning); }

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
  background: var(--primary-soft);
  border: 1px solid var(--accent-peach);
  border-radius: var(--radius-md);
  padding: var(--space-md) var(--space-lg);
  margin-bottom: var(--space-xl);
  display: flex;
  align-items: flex-start;
  gap: var(--space-md);
  font-size: 0.95rem;
  color: var(--text-primary);
}

.info-strip__icon {
  font-size: 1.1rem;
  color: var(--primary);
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
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
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
  border: 1px dashed var(--border);
  border-radius: var(--radius-sm);
  padding: var(--space-xl) var(--space-lg);
  text-align: center;
  cursor: pointer;
  background: var(--bg-secondary);
  transition: all var(--transition-base);
}

.upload-zone:hover, .upload-zone.active {
  border-color: var(--primary);
  background: var(--primary-soft);
}

.upload-zone.has-file {
  border-color: var(--success);
  border-style: solid;
  background: var(--success-soft);
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
  color: var(--text-muted);
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
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 6px 12px;
  font-size: 0.85rem;
  color: var(--text-primary);
  cursor: pointer;
  transition: all var(--transition-base);
}
.sample-invoice-btn:hover {
  background: var(--primary-soft);
  border-color: var(--accent-peach);
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
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  font-family: var(--font-sans);
  font-size: 0.95rem;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%236B6B6B' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 16px center;
  transition: all var(--transition-base);
}

.po-selector select:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 2px var(--primary-soft);
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
  font-size: 0.8rem;
  border-bottom: 1px solid var(--border);
  white-space: nowrap;
}
.po-table td, .comparison-table td {
  padding: 14px 16px;
  border-bottom: 1px solid var(--border-light);
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
  border-top: 1px solid var(--border);
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
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn--primary {
  background: var(--primary);
  color: var(--text-inverse);
  padding: 16px 32px;
  box-shadow: 0 2px 8px rgba(232, 93, 63, 0.2);
}

.btn--primary:hover:not(:disabled) {
  background: var(--primary-hover);
}

.btn--secondary {
  background: var(--bg-secondary);
  border-color: var(--border);
  color: var(--text-primary);
  padding: 8px 16px;
}

.btn--secondary:hover:not(:disabled) {
  background: var(--border);
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
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
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
  font-size: 2rem;
  font-weight: 600;
  color: var(--text-primary);
}

/* Specific colors for summary cards only on value */
.summary-card--total .summary-card__value { color: var(--error); }
.summary-card--price .summary-card__value { color: var(--accent-orange); }
.summary-card--qty .summary-card__value { color: var(--warning); }
.summary-card--tax .summary-card__value { color: var(--error); }
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
  background: var(--error-soft);
  color: var(--error);
}
.status-badge--match {
  background: var(--success-soft);
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
  border-bottom: 1px solid var(--border);
  font-weight: 600;
  font-size: 1rem;
  background: var(--surface);
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
}
.preview-pane__content {
  padding: var(--space-lg);
  max-height: 500px;
  overflow-y: auto;
}
.empty-state {
  text-align: center;
  color: var(--text-muted);
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
  color: var(--text-muted);
}
.cell-diff {
  display: block;
  font-size: 0.8rem;
  font-family: var(--font-mono);
  margin-top: 4px;
}
.cell-diff--over { color: var(--error); }
.cell-diff--under { color: var(--warning); }

.match-badge {
  padding: 4px 8px;
  border-radius: var(--radius-sm);
  font-size: 0.8rem;
  font-weight: 600;
  display: inline-block;
}
.match-badge--matched { background: var(--success-soft); color: var(--success); }
.match-badge--missing { background: var(--error-soft); color: var(--error); }
.match-badge--extra { background: var(--warning-soft); color: var(--warning); }
.match-badge--mismatch { background: var(--primary-soft); color: var(--primary); }

/* --- Exception Cards --- */
.exception-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}
.exception-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
}

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
.severity-badge--high { background: var(--error-soft); color: var(--error); }
.severity-badge--medium { background: var(--warning-soft); color: var(--warning); }
.severity-badge--low { background: var(--bg-secondary); color: var(--text-secondary); }

.exception-card__source {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  color: var(--text-secondary);
  background: var(--bg-primary);
  padding: 12px 16px;
  border-radius: var(--radius-sm);
  margin-bottom: var(--space-md);
  border: 1px solid var(--border-light);
}

.exception-card__values {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: var(--space-lg);
  padding-top: var(--space-md);
  border-top: 1px solid var(--border-light);
}
.value-block {
  display: flex;
  flex-direction: column;
}
.value-block__label {
  font-size: 0.8rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 4px;
}
.value-block__value {
  font-family: var(--font-mono);
  font-size: 1rem;
  font-weight: 500;
}
.value-block__value--diff { color: var(--error); }

/* --- Chatbot Floating Panel (SPLIT SCREEN) --- */
.chat-toggle-fab {
  position: fixed;
  bottom: var(--space-xl);
  right: var(--space-xl);
  width: 56px;
  height: 56px;
  background: var(--primary);
  color: var(--text-inverse);
  border: none;
  border-radius: 50%;
  font-size: 1.5rem;
  cursor: pointer;
  box-shadow: var(--shadow-float);
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform var(--transition-base), opacity var(--transition-base);
}
.chat-toggle-fab:hover {
  transform: translateY(-2px);
  background: var(--primary-hover);
}
.chat-toggle-fab.hidden {
  display: none !important;
}

.chat-panel {
  display: none; /* Hidden by default */
  width: 400px;
  min-width: 400px;
  flex-shrink: 0;
  height: 100vh;
  position: sticky;
  top: 0;
  background: var(--surface);
  border-left: 1px solid var(--border);
  box-shadow: -4px 0 24px rgba(45, 40, 35, 0.05);
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
    z-index: 200;
  }
}
@media (max-width: 600px) {
  .chat-panel.active {
    width: 100%;
    min-width: 100%;
  }
}

.chat-panel__header {
  padding: var(--space-lg);
  border-bottom: 1px solid var(--border);
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
  border-bottom-right-radius: 2px;
}
.chat-message--assistant {
  background: var(--primary-soft);
  color: var(--text-primary);
  align-self: flex-start;
  border-bottom-left-radius: 2px;
}
.chat-message--system {
  background: transparent;
  color: var(--text-muted);
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
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 8px 12px;
  font-size: 0.85rem;
  color: var(--text-primary);
  cursor: pointer;
  transition: all var(--transition-base);
}
.chat-suggestion-btn:hover {
  border-color: var(--primary);
  background: var(--primary-soft);
}

.chat-input-area {
  padding: var(--space-md) var(--space-lg) var(--space-lg);
  border-top: 1px solid var(--border);
  background: var(--surface);
}
.chat-input-wrapper {
  display: flex;
  gap: var(--space-xs);
}
.chat-input {
  flex: 1;
  padding: 14px 16px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: var(--bg-primary);
  font-family: var(--font-sans);
  font-size: 0.95rem;
}
.chat-input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 2px var(--primary-soft);
}
.chat-send-btn {
  width: 48px;
  border-radius: var(--radius-sm);
  background: var(--primary);
  color: var(--text-inverse);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background var(--transition-base);
}
.chat-send-btn:hover:not(:disabled) {
  background: var(--primary-hover);
}
.chat-send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* --- Loading Overlay --- */
.loading-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(245, 242, 237, 0.9);
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
  border: 3px solid var(--border);
  border-top-color: var(--primary);
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
