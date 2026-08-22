import os

css_content = """/* ============================================================
   AP Invoice Exception Assistant — Invoicer Theme
   ============================================================ */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  /* Invoicer Color Palette */
  --bg-page: #E6F7ED;
  --bg-card: #FFFFFF;
  --bg-header: #5dd08f;
  --bg-input: #F3F4F6;
  
  --border-subtle: #E5E7EB;
  --border-medium: #D1D5DB;
  --border-focus: #5dd08f;
  
  --text-primary: #111827;
  --text-secondary: #4B5563;
  --text-tertiary: #9CA3AF;
  --text-inverse: #FFFFFF;
  
  --accent-primary: #5dd08f;
  --accent-primary-hover: #4bc07f;
  
  --severity-high: #EF4444;
  --severity-high-bg: rgba(239, 68, 68, 0.1);
  --severity-medium: #F97316;
  --severity-medium-bg: rgba(249, 115, 22, 0.1);
  --severity-low: #3B82F6;
  --severity-low-bg: rgba(59, 130, 246, 0.1);
  
  --success: #10B981;
  --success-bg: rgba(16, 185, 129, 0.1);
  
  /* Typography */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-heading: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
  
  /* Spacing */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  
  /* Borders */
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 24px;
  --radius-full: 9999px;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  --shadow-lg: 0 10px 30px rgba(0, 0, 0, 0.05);
  
  /* Transitions */
  --transition-fast: 150ms ease;
  --transition-base: 250ms ease;
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
  line-height: 1.6;
  min-height: 100vh;
  padding: var(--space-xl);
  display: flex;
  justify-content: center;
}

#app {
  width: 100%;
  max-width: 1200px;
}

/* --- Layout --- */
.app-container {
  background: var(--bg-card);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* --- Header --- */
.app-header {
  background: var(--bg-header);
  padding: 20px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: var(--text-primary);
}

.app-header__brand {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.app-header__icon {
  font-size: 1.5rem;
}

.app-header__title {
  font-size: 1.25rem;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.app-header__subtitle {
  display: none; /* Hide subtitle for cleaner look */
}

.app-header__status {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: 0.85rem;
  font-weight: 500;
  background: rgba(255, 255, 255, 0.3);
  padding: 6px 16px;
  border-radius: var(--radius-full);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--text-primary);
}

/* --- Typography --- */
h1, h2, h3, h4 {
  font-family: var(--font-heading);
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--text-primary);
  line-height: 1.2;
}

h2 { font-size: 1.5rem; }
h3 { font-size: 1.125rem; }
.mono { font-family: var(--font-mono); }

/* --- Main Content --- */
.main-content {
  padding: var(--space-xl) var(--space-xl);
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-xl);
  transition: grid-template-columns var(--transition-base);
}

.main-content.chat-open {
  grid-template-columns: 1fr 380px;
}

/* --- Cards --- */
.card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  box-shadow: var(--shadow-sm);
}

.card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-md);
}

.card__title {
  font-size: 1.1rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.card__title-icon {
  display: none; /* Hide icons in card titles for cleaner look */
}

/* --- Buttons --- */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-sm);
  padding: 10px 24px;
  font-family: var(--font-sans);
  font-size: 0.875rem;
  font-weight: 600;
  border: none;
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: all var(--transition-fast);
  white-space: nowrap;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn--primary {
  background: var(--accent-primary);
  color: var(--bg-card);
}

.btn--primary:hover:not(:disabled) {
  background: var(--accent-primary-hover);
  transform: translateY(-1px);
}

.btn--secondary {
  background: var(--bg-input);
  color: var(--text-primary);
}

.btn--secondary:hover:not(:disabled) {
  background: var(--border-medium);
}

.btn--sm {
  padding: 6px 16px;
  font-size: 0.8rem;
}

.btn--lg {
  padding: 12px 32px;
  font-size: 1rem;
}

/* --- Upload Section --- */
.upload-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-lg);
  margin-bottom: var(--space-xl);
}

.upload-zone {
  border: 2px dashed var(--border-medium);
  border-radius: var(--radius-md);
  padding: var(--space-xl) var(--space-lg);
  text-align: center;
  cursor: pointer;
  background: var(--bg-input);
  transition: all var(--transition-base);
}

.upload-zone:hover, .upload-zone.active {
  border-color: var(--accent-primary);
  background: #f0fdf4;
}

.upload-zone.has-file {
  border-color: var(--accent-primary);
  border-style: solid;
  background: #f0fdf4;
}

.upload-zone__icon {
  font-size: 2rem;
  margin-bottom: var(--space-sm);
}

.upload-zone__title {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-primary);
}

.upload-zone__hint {
  font-size: 0.8rem;
  color: var(--text-secondary);
  margin-top: 4px;
}

.upload-zone__filename {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  color: var(--success);
  margin-top: var(--space-sm);
  font-weight: 500;
}

/* PO Selector */
.po-selector__label {
  display: block;
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: var(--space-xs);
  font-weight: 500;
}

.po-selector select {
  width: 100%;
  padding: 12px 16px;
  background: var(--bg-input);
  border: 1px solid transparent;
  border-radius: var(--radius-md);
  color: var(--text-primary);
  font-family: var(--font-sans);
  font-size: 0.9rem;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%234B5563' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 16px center;
}

.po-selector select:focus {
  outline: none;
  border-color: var(--accent-primary);
  background-color: var(--bg-card);
}

/* Compare Action */
.compare-action {
  display: flex;
  justify-content: center;
  margin-bottom: var(--space-xl);
}

/* --- Results Section --- */
.results-section {
  display: none;
  animation: fade-in 0.4s ease-out;
}
.results-section.active { display: block; }

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Summary Strip */
.summary-strip {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-md);
  margin-bottom: var(--space-xl);
}

.summary-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  display: flex;
  flex-direction: column;
}

.summary-card__label {
  font-size: 0.8rem;
  color: var(--text-secondary);
  font-weight: 500;
  margin-bottom: var(--space-xs);
}

.summary-card__value {
  font-size: 1.8rem;
  font-weight: 700;
  line-height: 1.2;
  color: var(--text-primary);
}

/* Badges */
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.02em;
}

.status-badge--exceptions {
  background: var(--severity-high-bg);
  color: var(--severity-high);
}

.status-badge--match {
  background: var(--success-bg);
  color: var(--success);
}

/* --- Data Tables --- */
.comparison-table-wrapper, .preview-pane {
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
}

th {
  background: var(--bg-input);
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

.cell-mismatch {
  color: var(--severity-high);
  font-weight: 600;
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

/* --- Exception Cards --- */
.exception-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.exception-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
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
  font-weight: 700;
  font-size: 1rem;
  color: var(--text-primary);
}

.exception-card__explanation {
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.6;
}

.severity-badge {
  padding: 4px 10px;
  border-radius: var(--radius-full);
  font-size: 0.7rem;
  font-weight: 700;
}
.severity-badge--high { background: var(--severity-high-bg); color: var(--severity-high); }
.severity-badge--medium { background: var(--severity-medium-bg); color: var(--severity-medium); }
.severity-badge--low { background: var(--severity-low-bg); color: var(--severity-low); }

/* --- Chat Panel --- */
.chat-panel {
  display: none;
  position: sticky;
  top: var(--space-xl);
  height: calc(100vh - 2 * var(--space-xl) - 100px); /* Adjust height */
  flex-direction: column;
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-md);
}
.chat-panel.active { display: flex; }

.chat-panel__header {
  padding: 16px;
  background: var(--bg-input);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  border-bottom: 1px solid var(--border-subtle);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.chat-message {
  padding: 12px 16px;
  border-radius: var(--radius-md);
  font-size: 0.9rem;
  max-width: 90%;
}

.chat-message--user {
  background: var(--accent-primary);
  color: var(--bg-card);
  align-self: flex-end;
  border-bottom-right-radius: 4px;
}

.chat-message--assistant {
  background: var(--bg-input);
  color: var(--text-primary);
  align-self: flex-start;
  border-bottom-left-radius: 4px;
}

.chat-message--system {
  background: transparent;
  color: var(--text-tertiary);
  font-size: 0.8rem;
  align-self: center;
  text-align: center;
}

.chat-input-area {
  padding: 16px;
  border-top: 1px solid var(--border-subtle);
}

.chat-input-wrapper {
  display: flex;
  gap: 8px;
}

.chat-input {
  flex: 1;
  padding: 10px 16px;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-full);
  background: var(--bg-input);
  font-family: var(--font-sans);
  font-size: 0.9rem;
}

.chat-input:focus {
  outline: none;
  border-color: var(--accent-primary);
}

.chat-send-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--accent-primary);
  color: white;
  border: none;
  cursor: pointer;
}

/* Chat toggle FAB */
.chat-toggle-fab {
  position: fixed;
  bottom: 32px;
  right: 32px;
  width: 56px;
  height: 56px;
  background: var(--accent-primary);
  border: none;
  border-radius: 50%;
  color: white;
  font-size: 1.4rem;
  cursor: pointer;
  box-shadow: var(--shadow-lg);
  display: none;
  z-index: 50;
}
.chat-toggle-fab.visible { display: flex; align-items: center; justify-content: center; }

/* Loading overlay */
.loading-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(255, 255, 255, 0.9);
  z-index: 100;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 16px;
}
.loading-overlay.active { display: flex; }

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--border-subtle);
  border-top-color: var(--accent-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Utility */
.hidden { display: none !important; }
.text-center { text-align: center; }
.text-muted { color: var(--text-tertiary); }
.mt-sm { margin-top: 8px; }
.mt-md { margin-top: 16px; }
.mt-lg { margin-top: 24px; }
.mb-lg { margin-bottom: 24px; }
"""

with open(r'c:\Users\VASANTHI\OneDrive\Desktop\AP Invoice\frontend\styles.css', 'w', encoding='utf-8') as f:
    f.write(css_content)
    
print("Overwrote styles.css successfully.")
