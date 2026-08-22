import os

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="AP Invoice Exception Assistant — AI-powered invoice validation and exception detection">
  <title>AP Invoice Exception Assistant</title>
  <link rel="stylesheet" href="/static/styles.css">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📄</text></svg>">
</head>
<body>
  <div id="app">
    <div class="app-container">
      
      <!-- Header -->
      <header class="app-header" id="app-header">
        <div class="app-header__left">
          <div class="app-header__icon">📄</div>
          <div class="app-header__text">
            <h1 class="app-header__title">AP Invoice Exception Assistant</h1>
            <div class="app-header__subtitle">AI-powered invoice validation and exception detection</div>
          </div>
        </div>
        <div class="app-header__status">
          <span class="status-dot"></span>
          <span id="api-status">System Online</span>
        </div>
      </header>

      <!-- Main Content Area -->
      <div class="main-content" id="main-content">
        
        <!-- Info Strip (Demo Banner) -->
        <div class="info-strip" id="demo-banner">
          <div class="info-strip__icon">💡</div>
          <div class="info-strip__text">
            <strong>Demo Mode</strong>
            <span>Upload an invoice and select a purchase order to automatically extract invoice data, compare line items, and identify exceptions.</span>
            <span id="api-key-warning" class="hidden text-warning">
              ⚠️ No Gemini API key configured — using demo data only.
            </span>
          </div>
        </div>

        <!-- Top Workspace (2 Columns) -->
        <div class="workspace-grid">
          
          <!-- Column 1: Invoice Upload -->
          <div class="card invoice-card">
            <div class="card__header">
              <h2 class="card__title">Invoice Document</h2>
            </div>
            <div class="upload-zone" id="invoice-upload-zone">
              <div class="upload-zone__icon">📤</div>
              <div class="upload-zone__text">Drop invoice here or click to browse</div>
              <div class="upload-zone__hint">Supports PDF, PNG, JPG, WebP</div>
              <div class="upload-zone__filename hidden" id="invoice-filename"></div>
              <input type="file" id="invoice-file-input" accept=".pdf,.png,.jpg,.jpeg,.webp" style="display:none">
            </div>
            <div class="sample-invoices-section mt-lg">
              <span class="section-label">Sample invoices:</span>
              <div class="sample-invoices mt-sm" id="sample-invoices-container"></div>
            </div>
          </div>

          <!-- Column 2: PO Selection -->
          <div class="card po-card">
            <div class="card__header">
              <h2 class="card__title">Purchase Order</h2>
            </div>
            <div class="po-selector">
              <label class="po-selector__label" for="po-select">Select a Purchase Order</label>
              <select id="po-select">
                <option value="">— Choose a PO —</option>
              </select>
            </div>
            <div id="po-preview" class="po-preview-container mt-lg" style="display:none;">
              <div class="table-wrapper">
                <table class="po-table">
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
              </div>
              <div class="po-totals mt-md">
                <span id="po-summary-text"></span>
              </div>
            </div>
          </div>
          
        </div>

        <!-- Compare Button -->
        <div class="compare-action" id="compare-action">
          <button class="btn btn--primary" id="compare-btn" disabled>
            Analyze Invoice
          </button>
        </div>

        <!-- Results Section (hidden until comparison runs) -->
        <section class="results-section mt-xl" id="results-section">
          
          <div class="results-header mb-lg">
            <h2>
              Comparison Results
              <span id="status-badge"></span>
            </h2>
            <button class="btn btn--secondary btn--sm" id="new-comparison-btn">
              New Comparison
            </button>
          </div>

          <!-- Summary Cards -->
          <div class="summary-grid" id="summary-strip"></div>

          <!-- Extraction Preview -->
          <div class="extraction-preview mb-xl">
            <div class="section-title-wrapper mb-md">
              <h2 class="section-title">Extraction Preview</h2>
              <span class="confidence-badge" id="confidence-badge"></span>
            </div>
            <div class="preview-container">
              <div class="preview-pane card">
                <div class="preview-pane__header">Original Invoice</div>
                <div class="preview-pane__content" id="original-invoice-preview">
                  <div class="empty-state">
                    <div class="empty-state__icon">📄</div>
                    <div class="empty-state__text">Preview unavailable</div>
                  </div>
                </div>
              </div>
              <div class="preview-pane card">
                <div class="preview-pane__header">Extracted Data</div>
                <div class="preview-pane__content" id="extracted-data-preview">
                  <div class="empty-state">
                    <div class="empty-state__text">Extracted data will appear here</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Line-by-Line Comparison -->
          <div class="comparison-section mb-xl" id="comparison-table-section">
            <h2 class="section-title mb-md">Line-by-Line Comparison</h2>
            <div class="card table-card">
              <div class="table-responsive">
                <table class="comparison-table" id="comparison-table">
                  <thead>
                    <tr>
                      <th>Match</th>
                      <th style="width: 25%;">Description</th>
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
          </div>

          <!-- Exception Details -->
          <div class="exceptions-section" id="exceptions-section">
            <div class="section-title-wrapper mb-md">
              <h2 class="section-title">Exception Details</h2>
              <div class="text-muted" id="exception-count-label"></div>
            </div>
            <div class="exception-list" id="exception-list"></div>
          </div>

        </section>
      </div>
    </div>
  </div>

  <!-- Chat Toggle FAB -->
  <button class="chat-toggle-fab" id="chat-toggle-fab" title="Open exception assistant">
    💬
  </button>

  <!-- Chatbot Panel (Sliding Side Panel) -->
  <aside class="chat-panel" id="chat-panel">
    <div class="chat-panel__header">
      <div class="chat-panel__title">Exception Assistant</div>
      <button class="chat-panel__close" id="chat-close-btn" title="Close chat">✕</button>
    </div>
    
    <div class="chat-messages" id="chat-messages">
      <div class="chat-message chat-message--system" id="chat-empty-state">
        Ask questions about the invoice analysis.
      </div>
    </div>
    
    <div class="chat-suggestions" id="chat-suggestions">
      <div class="chat-suggestions__title hidden">Suggested Questions</div>
    </div>
    
    <div class="chat-input-area">
      <div class="chat-input-wrapper">
        <input type="text" class="chat-input" id="chat-input" placeholder="Ask a question..." autocomplete="off">
        <button class="chat-send-btn" id="chat-send-btn" disabled title="Send message">➤</button>
      </div>
    </div>
  </aside>

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
