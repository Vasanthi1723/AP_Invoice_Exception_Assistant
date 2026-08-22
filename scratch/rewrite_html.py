import os

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="AP Invoice Exception Assistant — AI-powered invoice mismatch detection with grounded explanations">
  <title>AP Invoice Exception Assistant</title>
  <link rel="stylesheet" href="/static/styles.css">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📋</text></svg>">
</head>
<body>
  <div id="app">
    <div class="app-container">
      <!-- Header -->
      <header class="app-header" id="app-header">
        <div class="app-header__brand">
          <div class="app-header__title">AP Invoice Exception Assistant</div>
          <div class="app-header__subtitle">AI-powered invoice and purchase order verification</div>
        </div>
        <div class="app-header__status">
          <span class="status-dot"></span>
          <span id="api-status">Connecting…</span>
        </div>
      </header>

      <!-- Main Content Area -->
      <div class="main-content" id="main-content">
        
        <!-- Demo Banner -->
        <div class="demo-banner" id="demo-banner">
          <span class="demo-banner__icon">💡</span>
          <div>
            <strong>Demo Mode:</strong> Upload an invoice and select a PO to compare. 
            <span id="api-key-warning" class="hidden" style="color: var(--severity-medium);">
              ⚠️ No Gemini API key configured — using demo data only.
            </span>
          </div>
        </div>

        <!-- Top Workspace (3 Columns) -->
        <div class="workspace-grid">
          
          <!-- Column 1: Invoice Upload -->
          <div class="card invoice-card">
            <div class="card__header">
              <div class="card__title">Invoice Document</div>
            </div>
            <div class="upload-zone" id="invoice-upload-zone">
              <div class="upload-zone__icon">📤</div>
              <div class="upload-zone__title">Drop invoice here or click to browse</div>
              <div class="upload-zone__hint">Supports PDF, PNG, JPG, WebP</div>
              <div class="upload-zone__filename hidden" id="invoice-filename"></div>
              <input type="file" id="invoice-file-input" accept=".pdf,.png,.jpg,.jpeg,.webp" style="display:none">
            </div>
            <div class="mt-md text-center">
              <span class="text-muted" style="font-size:0.8rem;">Sample invoices</span>
            </div>
            <div class="mt-sm sample-invoices" id="sample-invoices-container"></div>
          </div>

          <!-- Column 2: PO Selection -->
          <div class="card po-card">
            <div class="card__header">
              <div class="card__title">Purchase Order</div>
            </div>
            <div class="po-selector">
              <label class="po-selector__label" for="po-select">Select a Purchase Order</label>
              <select id="po-select">
                <option value="">— Choose a PO —</option>
              </select>
            </div>
            <div id="po-preview" class="mt-md" style="display:none;">
              <table class="extracted-data-table">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Item Code</th>
                    <th>Description</th>
                    <th class="text-right">Qty</th>
                    <th class="text-right">Unit Price</th>
                    <th class="text-right">Total</th>
                  </tr>
                </thead>
                <tbody id="po-preview-body"></tbody>
              </table>
              <div class="po-totals mt-sm">
                <span id="po-summary-text"></span>
              </div>
            </div>
          </div>

          <!-- Column 3: AI Assistant -->
          <aside class="card chat-panel active" id="chat-panel">
            <div class="chat-panel__header">
              <div class="chat-panel__title">Exception Assistant</div>
              <button class="chat-panel__close hidden" id="chat-close-btn" title="Close chat">✕</button>
            </div>
            <div class="chat-messages" id="chat-messages">
              <div class="chat-message chat-message--system" id="chat-empty-state">
                Analyze an invoice to ask questions about detected exceptions.
              </div>
            </div>
            <div class="chat-suggestions" id="chat-suggestions">
              <div class="chat-suggestions__title hidden">Suggested questions</div>
            </div>
            <div class="chat-input-area">
              <div class="chat-input-wrapper">
                <input type="text" class="chat-input" id="chat-input" placeholder="Ask about an exception…" autocomplete="off">
                <button class="chat-send-btn" id="chat-send-btn" disabled title="Send message">➤</button>
              </div>
            </div>
          </aside>
          
        </div>

        <!-- Compare Button -->
        <div class="compare-action" id="compare-action">
          <button class="btn btn--primary btn--lg" id="compare-btn" disabled>
            Analyze Invoice
          </button>
        </div>

        <!-- Results Section (hidden until comparison runs) -->
        <section class="results-section" id="results-section">
          <!-- Overall Status -->
          <div class="results-header mb-lg">
            <h2>
              Comparison Results
              <span id="status-badge"></span>
            </h2>
            <button class="btn btn--secondary btn--sm" id="new-comparison-btn">
              New Comparison
            </button>
          </div>

          <!-- Summary Strip -->
          <div class="summary-strip" id="summary-strip"></div>

          <!-- Side-by-Side Preview -->
          <div class="invoice-preview mb-lg">
            <div class="section-title-wrapper mb-sm">
              <h3 class="section-title">Extraction Preview</h3>
              <span class="confidence-badge" id="confidence-badge"></span>
            </div>
            <div class="preview-container">
              <div class="preview-pane card">
                <div class="preview-pane__header">Original Invoice</div>
                <div class="preview-pane__content" id="original-invoice-preview">
                  <p class="text-muted text-center" style="padding:40px 0;">Invoice image will appear here</p>
                </div>
              </div>
              <div class="preview-pane card">
                <div class="preview-pane__header">Extracted Data</div>
                <div class="preview-pane__content" id="extracted-data-preview">
                  <p class="text-muted text-center" style="padding:40px 0;">Extracted data will appear here</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Comparison Table -->
          <div class="comparison-section mb-lg card" id="comparison-table-section">
            <div class="card__header">
              <div class="card__title">Line-by-Line Comparison</div>
            </div>
            <div class="comparison-table-wrapper">
              <table class="comparison-table" id="comparison-table">
                <thead>
                  <tr>
                    <th>Match</th>
                    <th style="width: 30%;">Description</th>
                    <th class="text-right">PO Qty</th>
                    <th class="text-right">Inv Qty</th>
                    <th class="text-right">PO Price</th>
                    <th class="text-right">Inv Price</th>
                    <th class="text-right">PO Total</th>
                    <th class="text-right">Inv Total</th>
                    <th>Flags</th>
                  </tr>
                </thead>
                <tbody id="comparison-table-body"></tbody>
              </table>
            </div>
          </div>

          <!-- Exception Cards -->
          <div class="exceptions-section card" id="exceptions-section">
            <div class="card__header">
              <div class="card__title">Exception Details</div>
              <div class="text-muted" style="font-size:0.8rem;" id="exception-count-label"></div>
            </div>
            <div class="exception-list" id="exception-list"></div>
          </div>
        </section>
      </div>
    </div>
  </div>

  <!-- Chat Toggle FAB (hidden in new layout but kept for JS compatibility if needed) -->
  <button class="chat-toggle-fab hidden" id="chat-toggle-fab" title="Open assistant chat">💬</button>

  <!-- Loading Overlay -->
  <div class="loading-overlay" id="loading-overlay">
    <div class="loading-spinner"></div>
    <div class="loading-text">Analyzing invoice…</div>
    <div class="loading-step" id="loading-step">Extracting line items with Gemini Vision</div>
  </div>

  <script src="/static/app.js"></script>
</body>
</html>
"""

with open(r'c:\Users\VASANTHI\OneDrive\Desktop\AP Invoice\frontend\index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Overwrote index.html successfully.")
