/**
 * AP Invoice Exception Assistant — Frontend Application
 *
 * Single-file JS application handling:
 *  - File upload (drag-and-drop + file picker)
 *  - PO selection and preview
 *  - Comparison API calls
 *  - Results rendering (summary, comparison table, exception cards)
 *  - Chat interface with streaming-like experience
 */

// ============================================================
// Constants & State
// ============================================================

const API_BASE = '';  // Same origin — served by FastAPI
const MAX_FILE_SIZE = 20 * 1024 * 1024; // 20MB

const state = {
  invoiceFile: null,
  invoicePreviewUrl: null,
  selectedPO: null,
  selectedPOData: null,
  comparisonResult: null,
  chatHistory: [],
  chatOpen: false,
  loading: false,
  samplePOs: [],
  sampleInvoices: [],
  geminiConfigured: false,
};

// ============================================================
// DOM References
// ============================================================

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

const dom = {
  apiStatus: $('#api-status'),
  apiKeyWarning: $('#api-key-warning'),
  invoiceUploadZone: $('#invoice-upload-zone'),
  invoiceFileInput: $('#invoice-file-input'),
  invoiceFilename: $('#invoice-filename'),
  sampleInvoicesContainer: $('#sample-invoices-container'),
  poSelect: $('#po-select'),
  poPreview: $('#po-preview'),
  poPreviewBody: $('#po-preview-body'),
  poSummaryText: $('#po-summary-text'),
  compareBtn: $('#compare-btn'),
  resultsSection: $('#results-section'),
  statusBadge: $('#status-badge'),
  summaryStrip: $('#summary-strip'),
  confidenceBadge: $('#confidence-badge'),
  originalInvoicePreview: $('#original-invoice-preview'),
  extractedDataPreview: $('#extracted-data-preview'),
  comparisonTableBody: $('#comparison-table-body'),
  exceptionList: $('#exception-list'),
  exceptionCountLabel: $('#exception-count-label'),
  loadingOverlay: $('#loading-overlay'),
  loadingStep: $('#loading-step'),
  mainContent: $('#main-content'),
  chatPanel: $('#chat-panel'),
  chatMessages: $('#chat-messages'),
  chatSuggestions: $('#chat-suggestions'),
  chatInput: $('#chat-input'),
  chatSendBtn: $('#chat-send-btn'),
  chatCloseBtn: $('#chat-close-btn'),
  chatToggleFab: $('#chat-toggle-fab'),
  newComparisonBtn: $('#new-comparison-btn'),
};

// ============================================================
// API Helpers
// ============================================================

async function apiFetch(path, options = {}) {
  const url = `${API_BASE}${path}`;
  try {
    const response = await fetch(url, options);
    if (!response.ok) {
      const err = await response.json().catch(() => ({ detail: response.statusText }));
      throw new Error(err.detail || `HTTP ${response.status}`);
    }
    return response.json();
  } catch (e) {
    if (e.message.includes('Failed to fetch')) {
      throw new Error('Cannot connect to the server. Is it running?');
    }
    throw e;
  }
}

// ============================================================
// Initialization
// ============================================================

async function init() {
  setupEventListeners();
  await checkHealth();
  await loadSampleData();
}

async function checkHealth() {
  try {
    const data = await apiFetch('/api/health');
    dom.apiStatus.textContent = 'System Online';
    state.geminiConfigured = data.gemini_configured;
    if (!data.gemini_configured) {
      dom.apiKeyWarning.classList.remove('hidden');
    }
  } catch {
    dom.apiStatus.textContent = 'Offline';
    dom.apiStatus.style.color = 'var(--severity-high)';
  }
}

async function loadSampleData() {
  try {
    // Load sample POs
    const posData = await apiFetch('/api/sample-pos');
    state.samplePOs = posData.purchase_orders;
    renderPOSelector();

    // Load sample invoices
    const invoicesData = await apiFetch('/api/sample-invoices');
    state.sampleInvoices = invoicesData.invoices;
    renderSampleInvoices();
  } catch (e) {
    console.warn('Could not load sample data:', e);
  }
}

// ============================================================
// Event Listeners
// ============================================================

function setupEventListeners() {
  // Invoice upload — drag and drop
  dom.invoiceUploadZone.addEventListener('click', () => dom.invoiceFileInput.click());
  dom.invoiceUploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dom.invoiceUploadZone.classList.add('active');
  });
  dom.invoiceUploadZone.addEventListener('dragleave', () => {
    dom.invoiceUploadZone.classList.remove('active');
  });
  dom.invoiceUploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dom.invoiceUploadZone.classList.remove('active');
    if (e.dataTransfer.files.length > 0) {
      handleInvoiceFile(e.dataTransfer.files[0]);
    }
  });
  dom.invoiceFileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
      handleInvoiceFile(e.target.files[0]);
    }
  });

  // PO selector
  dom.poSelect.addEventListener('change', handlePOSelect);

  // Compare button
  dom.compareBtn.addEventListener('click', runComparison);

  // New comparison
  dom.newComparisonBtn.addEventListener('click', resetToUpload);

  // Chat
  dom.chatInput.addEventListener('input', () => {
    dom.chatSendBtn.disabled = !dom.chatInput.value.trim();
  });
  dom.chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey && dom.chatInput.value.trim()) {
      e.preventDefault();
      sendChatMessage();
    }
  });
  dom.chatSendBtn.addEventListener('click', sendChatMessage);
  dom.chatCloseBtn.addEventListener('click', toggleChat);
  dom.chatToggleFab.addEventListener('click', toggleChat);
}

// ============================================================
// Invoice Handling
// ============================================================

function handleInvoiceFile(file) {
  // Validate file type
  const validTypes = ['application/pdf', 'image/png', 'image/jpeg', 'image/webp'];
  if (!validTypes.includes(file.type)) {
    alert('Please upload a PDF, PNG, JPG, or WebP file.');
    return;
  }
  if (file.size > MAX_FILE_SIZE) {
    alert('File too large. Maximum 20MB.');
    return;
  }

  state.invoiceFile = file;

  // Create preview URL for images
  if (file.type.startsWith('image/')) {
    state.invoicePreviewUrl = URL.createObjectURL(file);
  } else {
    state.invoicePreviewUrl = null;  // PDFs can't be previewed as easily
  }

  // Update UI
  dom.invoiceUploadZone.classList.add('has-file');
  dom.invoiceFilename.textContent = `✓ ${file.name}`;
  dom.invoiceFilename.classList.remove('hidden');

  updateCompareButton();
}

function handleSampleInvoiceClick(filename) {
  // For sample invoices, we'll fetch the file and store it
  fetch(`/api/sample-invoices/${filename}`)
    .then(res => res.blob())
    .then(blob => {
      const file = new File([blob], filename, { type: blob.type });
      handleInvoiceFile(file);
    })
    .catch(e => console.error('Error loading sample invoice:', e));
}

// ============================================================
// PO Handling
// ============================================================

function renderPOSelector() {
  state.samplePOs.forEach(po => {
    const option = document.createElement('option');
    option.value = po.filename;
    option.textContent = `${po.po_number} — ${po.vendor} ($${po.total.toLocaleString()}, ${po.line_count} items)`;
    dom.poSelect.appendChild(option);
  });
}

async function handlePOSelect() {
  const filename = dom.poSelect.value;
  if (!filename) {
    state.selectedPO = null;
    state.selectedPOData = null;
    dom.poPreview.style.display = 'none';
    updateCompareButton();
    return;
  }

  try {
    const data = await apiFetch(`/api/sample-pos/${filename}`);
    state.selectedPO = filename;
    state.selectedPOData = data;
    renderPOPreview(data);
    dom.poPreview.style.display = 'block';
  } catch (e) {
    console.error('Error loading PO:', e);
  }

  updateCompareButton();
}

function renderPOPreview(po) {
  dom.poPreviewBody.innerHTML = po.line_items.map(item => `
    <tr>
      <td>${item.line_number}</td>
      <td style="font-size:0.7rem;">${item.item_code}</td>
      <td>${item.description}</td>
      <td>${item.quantity}</td>
      <td>$${item.unit_price.toFixed(2)}</td>
      <td>$${item.total.toFixed(2)}</td>
    </tr>
  `).join('');
  dom.poSummaryText.textContent = `Subtotal: $${po.subtotal.toFixed(2)} | Tax (${(po.tax_rate * 100).toFixed(1)}%): $${po.tax.toFixed(2)} | Total: $${po.total.toFixed(2)}`;
}

function renderSampleInvoices() {
  if (state.sampleInvoices.length === 0) return;
  dom.sampleInvoicesContainer.innerHTML = state.sampleInvoices.map(inv => `
    <button class="btn btn--ghost btn--sm" onclick="handleSampleInvoiceClick('${inv.filename}')">
      📎 ${inv.filename}
    </button>
  `).join(' ');
}

// ============================================================
// Compare Button State
// ============================================================

function updateCompareButton() {
  const ready = state.invoiceFile && state.selectedPO;
  dom.compareBtn.disabled = !ready;
}

// ============================================================
// Run Comparison
// ============================================================

async function runComparison() {
  if (!state.invoiceFile || !state.selectedPO) return;

  showLoading(true);

  try {
    // Build form data
    const formData = new FormData();
    formData.append('invoice_file', state.invoiceFile);
    formData.append('po_filename', state.selectedPO);

    // Update loading steps
    setLoadingStep('Uploading invoice…');
    await delay(300);
    setLoadingStep('Extracting line items with Gemini Vision…');

    const result = await apiFetch('/api/compare', {
      method: 'POST',
      body: formData,
    });

    state.comparisonResult = result;
    renderResults(result);
    showResults(true);

    // Reset chat
    state.chatHistory = [];
    dom.chatMessages.innerHTML = `
      <div class="chat-message chat-message--system">
        Ask me anything about the ${result.summary.total_exceptions} exception(s) found.
        I'll cite the exact source fields in my answers.
      </div>
    `;
    renderChatSuggestions(result);

  } catch (e) {
    alert(`Comparison failed: ${e.message}`);
    console.error(e);
  } finally {
    showLoading(false);
  }
}

// ============================================================
// Results Rendering
// ============================================================

function renderResults(result) {
  // Status badge
  if (result.overall_status === 'MATCH') {
    dom.statusBadge.innerHTML = `<span class="status-badge status-badge--match">✓ All Clear</span>`;
  } else {
    dom.statusBadge.innerHTML = `<span class="status-badge status-badge--exceptions">⚠ ${result.summary.total_exceptions} Exception${result.summary.total_exceptions !== 1 ? 's' : ''}</span>`;
  }

  // Summary strip
  renderSummaryStrip(result.summary, result);

  // Invoice preview
  renderInvoicePreview(result);

  // Comparison table
  renderComparisonTable(result);

  // Exception cards
  renderExceptions(result);

  // Confidence badge
  const conf = result.invoice_data.extraction_confidence;
  if (conf != null) {
    const confClass = conf >= 0.9 ? 'high' : conf >= 0.7 ? 'medium' : 'low';
    dom.confidenceBadge.className = `confidence-badge confidence-badge--${confClass}`;
    dom.confidenceBadge.textContent = `${(conf * 100).toFixed(0)}% confidence`;
  }
}

function renderSummaryStrip(summary, result) {
  const icons = {
    total: 'alert-triangle',
    price: 'dollar-sign',
    qty: 'package',
    tax: 'percent',
    match: 'check-circle',
  };
  const cards = [
    { cls: 'total', value: summary.total_exceptions, label: 'Total Exceptions' },
    { cls: 'price', value: summary.by_type.PRICE_MISMATCH || 0, label: 'Price Mismatches' },
    { cls: 'qty', value: summary.by_type.QUANTITY_MISMATCH || 0, label: 'Quantity Mismatches' },
    { cls: 'tax', value: (summary.by_type.TAX_MISMATCH || 0), label: 'Tax Issues' },
    { cls: 'match', value: summary.total_lines_compared - summary.lines_with_exceptions, label: 'Lines OK' },
  ];

  dom.summaryStrip.innerHTML = cards.map((c, i) => `
    <div class="summary-card summary-card--${c.cls}" style="animation-delay:${i * 0.07}s">
      <div class="summary-card__icon-row">
        <div class="summary-card__icon">
          <i data-lucide="${icons[c.cls]}"></i>
        </div>
      </div>
      <div class="summary-card__value">${c.value}</div>
      <div class="summary-card__label">${c.label}</div>
    </div>
  `).join('');

  // Re-init Lucide icons for dynamically injected content
  if (window.lucide) lucide.createIcons();

  // Render risk panel
  renderRiskPanel(summary, result);
}

function renderRiskPanel(summary, result) {
  const riskPanel = document.getElementById('risk-panel');
  if (!riskPanel) return;

  const total = summary.total_lines_compared || 1;
  const priceIssues = summary.by_type.PRICE_MISMATCH || 0;
  const qtyIssues = summary.by_type.QUANTITY_MISMATCH || 0;
  const taxIssues = summary.by_type.TAX_MISMATCH || 0;
  const matchedOk = total - (summary.lines_with_exceptions || 0);

  const pricePct = Math.min(Math.round((priceIssues / total) * 100), 100);
  const qtyPct   = Math.min(Math.round((qtyIssues   / total) * 100), 100);
  const taxPct   = Math.min(Math.round((taxIssues   / total) * 100), 100);
  const matchPct = Math.min(Math.round((matchedOk   / total) * 100), 100);

  // Animate bars
  setTimeout(() => {
    const setBar = (id, pctId, pct) => {
      const bar = document.getElementById(id);
      const pctEl = document.getElementById(pctId);
      if (bar) bar.style.width = pct + '%';
      if (pctEl) pctEl.textContent = pct + '%';
    };
    setBar('risk-bar-price', 'risk-pct-price', pricePct);
    setBar('risk-bar-qty',   'risk-pct-qty',   qtyPct);
    setBar('risk-bar-tax',   'risk-pct-tax',   taxPct);
    setBar('risk-bar-match', 'risk-pct-match', matchPct);
  }, 300);

  // Set overall risk level badge
  const badge = document.getElementById('risk-level-badge');
  if (badge) {
    const highCount = summary.by_severity?.HIGH || 0;
    const medCount  = summary.by_severity?.MEDIUM || 0;
    if (highCount >= 2 || summary.total_exceptions > 4) {
      badge.textContent = 'High Risk'; badge.className = 'risk-level-badge high';
    } else if (highCount >= 1 || medCount >= 2) {
      badge.textContent = 'Medium Risk'; badge.className = 'risk-level-badge medium';
    } else if (summary.total_exceptions === 0) {
      badge.textContent = 'Low Risk'; badge.className = 'risk-level-badge low';
    } else {
      badge.textContent = 'Low Risk'; badge.className = 'risk-level-badge low';
    }
  }

  riskPanel.style.display = 'flex';
  riskPanel.style.flexDirection = 'column';
}

function renderInvoicePreview(result) {
  // Original invoice
  if (state.invoicePreviewUrl) {
    dom.originalInvoicePreview.innerHTML = `<img src="${state.invoicePreviewUrl}" alt="Original invoice">`;
  } else {
    dom.originalInvoicePreview.innerHTML = `
      <div style="padding:40px; text-align:center;">
        <div style="font-size:2rem; margin-bottom:8px;">📄</div>
        <div class="text-muted">PDF preview not available</div>
        <div class="text-muted" style="font-size:0.75rem;">Invoice: ${result.invoice_data.invoice_number}</div>
      </div>
    `;
  }

  // Extracted data table
  const inv = result.invoice_data;
  dom.extractedDataPreview.innerHTML = `
    <div style="margin-bottom:12px; font-size:0.8rem;">
      <div><strong>Invoice #:</strong> <span class="mono">${inv.invoice_number}</span></div>
      ${inv.vendor ? `<div><strong>Vendor:</strong> ${inv.vendor}</div>` : ''}
      ${inv.date ? `<div><strong>Date:</strong> ${inv.date}</div>` : ''}
      ${inv.po_reference ? `<div><strong>PO Ref:</strong> <span class="mono">${inv.po_reference}</span></div>` : ''}
    </div>
    <table class="extracted-data-table">
      <thead>
        <tr>
          <th>#</th>
          <th>Description</th>
          <th>Qty</th>
          <th>Price</th>
          <th>Total</th>
        </tr>
      </thead>
      <tbody>
        ${inv.line_items.map(item => `
          <tr>
            <td>${item.line_number}</td>
            <td style="font-family:var(--font-sans); font-size:0.78rem;">${item.description}</td>
            <td>${item.quantity}</td>
            <td>$${item.unit_price.toFixed(2)}</td>
            <td>$${item.total.toFixed(2)}</td>
          </tr>
        `).join('')}
      </tbody>
    </table>
    <div style="margin-top:8px; font-size:0.75rem; text-align:right; color:var(--text-tertiary);">
      Subtotal: $${inv.subtotal.toFixed(2)} | Tax: $${inv.tax.toFixed(2)} | Total: $${inv.total.toFixed(2)}
    </div>
  `;
}

function renderComparisonTable(result) {
  let rows = '';

  result.matched_lines.forEach(ml => {
    const hasExceptions = ml.exceptions.length > 0;
    const qtyMatch = ml.po_line.quantity === ml.invoice_line.quantity;
    const priceMatch = Math.abs(ml.po_line.unit_price - ml.invoice_line.unit_price) < 0.006;
    const totalMatch = Math.abs(ml.po_line.total - ml.invoice_line.total) < 0.01;

    rows += `<tr>
      <td>
        <span class="confidence-badge confidence-badge--${ml.match_confidence >= 0.9 ? 'high' : 'medium'}">
          ${(ml.match_confidence * 100).toFixed(0)}%
        </span>
      </td>
      <td>
        <div>${ml.po_line.description}</div>
        ${ml.po_line.description !== ml.invoice_line.description ? `<div style="font-size:0.7rem; color:var(--text-tertiary);">Invoice: "${ml.invoice_line.description}"</div>` : ''}
      </td>
      <td>${ml.po_line.quantity}</td>
      <td class="${qtyMatch ? 'cell-match' : 'cell-mismatch'}">
        ${ml.invoice_line.quantity}
        ${!qtyMatch ? `<span class="cell-diff cell-diff--${ml.invoice_line.quantity > ml.po_line.quantity ? 'over' : 'under'}">
          ${ml.invoice_line.quantity > ml.po_line.quantity ? '+' : ''}${ml.invoice_line.quantity - ml.po_line.quantity}
        </span>` : ''}
      </td>
      <td class="col-divider">$${ml.po_line.unit_price.toFixed(2)}</td>
      <td class="${priceMatch ? 'cell-match' : 'cell-mismatch'}">
        $${ml.invoice_line.unit_price.toFixed(2)}
        ${!priceMatch ? `<span class="cell-diff cell-diff--${ml.invoice_line.unit_price > ml.po_line.unit_price ? 'over' : 'under'}">
          ${ml.invoice_line.unit_price > ml.po_line.unit_price ? '+' : ''}$${(ml.invoice_line.unit_price - ml.po_line.unit_price).toFixed(2)}
        </span>` : ''}
      </td>
      <td class="col-divider">$${ml.po_line.total.toFixed(2)}</td>
      <td class="${totalMatch ? 'cell-match' : 'cell-mismatch'}">$${ml.invoice_line.total.toFixed(2)}</td>
      <td>${ml.exceptions.length > 0 ? `<span style="color:var(--severity-high);">🚩 ${ml.exceptions.length}</span>` : '<span style="color:var(--accent-emerald);">✓</span>'}</td>
    </tr>`;
  });

  // Unmatched PO lines
  result.unmatched_po_lines.forEach(pl => {
    rows += `<tr style="background:var(--severity-high-bg);">
      <td><span class="severity-badge severity-badge--high">MISSING</span></td>
      <td>${pl.description}</td>
      <td>${pl.quantity}</td>
      <td class="cell-mismatch">—</td>
      <td class="col-divider">$${pl.unit_price.toFixed(2)}</td>
      <td class="cell-mismatch">—</td>
      <td class="col-divider">$${pl.total.toFixed(2)}</td>
      <td class="cell-mismatch">—</td>
      <td><span style="color:var(--severity-high);">🚩</span></td>
    </tr>`;
  });

  // Unmatched invoice lines
  result.unmatched_invoice_lines.forEach(il => {
    rows += `<tr style="background:var(--severity-medium-bg);">
      <td><span class="severity-badge severity-badge--medium">EXTRA</span></td>
      <td>${il.description}</td>
      <td>—</td>
      <td>${il.quantity}</td>
      <td class="col-divider">—</td>
      <td>$${il.unit_price.toFixed(2)}</td>
      <td class="col-divider">—</td>
      <td>$${il.total.toFixed(2)}</td>
      <td><span style="color:var(--severity-medium);">🚩</span></td>
    </tr>`;
  });

  dom.comparisonTableBody.innerHTML = rows;
}

function renderExceptions(result) {
  // Collect all exceptions
  const allExceptions = [];

  result.matched_lines.forEach(ml => {
    ml.exceptions.forEach(exc => {
      allExceptions.push({ ...exc, context: `Line: ${ml.po_line.description}` });
    });
  });

  if (result.tax_exception) {
    allExceptions.push({ ...result.tax_exception, context: 'Document-level' });
  }

  // Add unmatched line exceptions
  result.unmatched_po_lines.forEach(pl => {
    allExceptions.push({
      exception_id: `MISS-${pl.line_number}`,
      type: 'MISSING_ON_INVOICE',
      field: 'line_item',
      severity: 'HIGH',
      explanation: `PO line ${pl.line_number} ("${pl.description}", item code "${pl.item_code}") has no matching line on the invoice. Expected ${pl.quantity} ${pl.unit} at $${pl.unit_price.toFixed(2)} each.`,
      context: pl.description,
    });
  });

  result.unmatched_invoice_lines.forEach(il => {
    allExceptions.push({
      exception_id: `EXTRA-${il.line_number}`,
      type: 'EXTRA_ON_INVOICE',
      field: 'line_item',
      severity: 'MEDIUM',
      explanation: `Invoice line ${il.line_number} ("${il.description}") has no matching PO line. Extra charge of ${il.quantity} ${il.unit} at $${il.unit_price.toFixed(2)} each (total $${il.total.toFixed(2)}).`,
      context: il.description,
    });
  });

  dom.exceptionCountLabel.textContent = `${allExceptions.length} exception${allExceptions.length !== 1 ? 's' : ''} found`;

  if (allExceptions.length === 0) {
    dom.exceptionList.innerHTML = `
      <div class="card" style="text-align:center; padding:40px;">
        <div style="font-size:2rem; margin-bottom:8px;">✅</div>
        <div style="font-size:1rem; font-weight:600; color:var(--accent-emerald);">No Exceptions Found</div>
        <div class="text-muted mt-sm">Invoice matches the Purchase Order perfectly.</div>
      </div>
    `;
    return;
  }

  const typeIcons = {
    PRICE_MISMATCH: '💰',
    QUANTITY_MISMATCH: '📦',
    TAX_MISMATCH: '🧾',
    MISSING_ON_INVOICE: '❌',
    EXTRA_ON_INVOICE: '➕',
    DESCRIPTION_MISMATCH: '📝',
  };

  const typeLabels = {
    PRICE_MISMATCH: 'Price Mismatch',
    QUANTITY_MISMATCH: 'Quantity Mismatch',
    TAX_MISMATCH: 'Tax Mismatch',
    MISSING_ON_INVOICE: 'Missing on Invoice',
    EXTRA_ON_INVOICE: 'Extra on Invoice',
    DESCRIPTION_MISMATCH: 'Description Mismatch',
  };

  dom.exceptionList.innerHTML = allExceptions.map(exc => {
    const severityLower = (exc.severity || 'medium').toLowerCase();

    // Split explanation into main text and source citation
    const parts = exc.explanation.split('Source:');
    const mainText = parts[0].trim();
    const sourceText = parts.length > 1 ? 'Source:' + parts[1] : null;

    return `
      <div class="exception-card exception-card--${severityLower}">
        <div class="exception-card__header">
          <div class="exception-card__type">
            <span class="exception-card__type-icon">${typeIcons[exc.type] || '🚩'}</span>
            ${typeLabels[exc.type] || exc.type}
            <span class="exception-card__id">${exc.exception_id}</span>
          </div>
          <span class="severity-badge severity-badge--${severityLower}">${exc.severity}</span>
        </div>
        <div class="exception-card__explanation">${mainText}</div>
        ${sourceText ? `<div class="exception-card__source">${sourceText}</div>` : ''}
        ${exc.po_value != null && exc.invoice_value != null && exc.difference != null ? `
          <div class="exception-card__values">
            <div class="value-block">
              <div class="value-block__label">PO Value</div>
              <div class="value-block__value value-block__value--po">${formatValue(exc.po_value, exc.field)}</div>
            </div>
            <div class="value-block">
              <div class="value-block__label">Invoice Value</div>
              <div class="value-block__value value-block__value--invoice">${formatValue(exc.invoice_value, exc.field)}</div>
            </div>
            <div class="value-block">
              <div class="value-block__label">Difference</div>
              <div class="value-block__value value-block__value--diff">
                ${exc.difference > 0 ? '+' : ''}${formatValue(exc.difference, exc.field)}
                ${exc.difference_pct != null ? ` (${exc.difference_pct > 0 ? '+' : ''}${exc.difference_pct.toFixed(1)}%)` : ''}
              </div>
            </div>
          </div>
        ` : ''}
      </div>
    `;
  }).join('');
}

function formatValue(val, field) {
  if (typeof val === 'string') return val;
  if (field === 'unit_price' || field === 'tax') return `$${val.toFixed(2)}`;
  if (field === 'quantity') return val.toString();
  if (typeof val === 'number') {
    return Math.abs(val) < 1 ? `$${val.toFixed(2)}` : val.toLocaleString();
  }
  return String(val);
}

// ============================================================
// Chat
// ============================================================

function toggleChat() {
  state.chatOpen = !state.chatOpen;

  if (state.chatOpen) {
    // Open chatbot
    dom.chatPanel.classList.add('active');

    // Hide floating chatbot icon
    dom.chatToggleFab.classList.add('hidden');

    // Focus input
    setTimeout(() => {
      dom.chatInput.focus();
    }, 200);

  } else {
    // Close chatbot
    dom.chatPanel.classList.remove('active');

    // Show floating chatbot icon again
    dom.chatToggleFab.classList.remove('hidden');
  }
}

function renderChatSuggestions(result) {
  const suggestions = [
    `Why was invoice ${result.invoice_number} flagged?`,
    `What is the total financial impact of these exceptions?`,
    `Which lines matched correctly?`,
    `Summarize all price discrepancies.`,
  ];

  const existingTitle = dom.chatSuggestions.querySelector('.chat-suggestions__title');
  dom.chatSuggestions.innerHTML = '';
  if (existingTitle) dom.chatSuggestions.appendChild(existingTitle);
  else {
    const title = document.createElement('div');
    title.className = 'chat-suggestions__title';
    title.textContent = 'Suggested questions';
    dom.chatSuggestions.appendChild(title);
  }

  suggestions.forEach(q => {
    const btn = document.createElement('button');
    btn.className = 'chat-suggestion-btn';
    btn.textContent = q;
    btn.addEventListener('click', () => {
      dom.chatInput.value = q;
      dom.chatSendBtn.disabled = false;
      sendChatMessage();
    });
    dom.chatSuggestions.appendChild(btn);
  });
}

async function sendChatMessage() {
  const message = dom.chatInput.value.trim();
  if (!message || !state.comparisonResult) return;

  // Add user message
  addChatMessage('user', message);
  dom.chatInput.value = '';
  dom.chatSendBtn.disabled = true;

  // Hide suggestions after first message
  dom.chatSuggestions.style.display = 'none';

  // Show typing indicator
  const typingId = addChatMessage('assistant', '<span class="loading-step">Thinking…</span>');

  try {
    const response = await apiFetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message,
        history: state.chatHistory,
      }),
    });

    // Remove typing indicator and add real response
    removeChatMessage(typingId);
    addChatMessage('assistant', formatChatResponse(response.reply));

    // Update history
    state.chatHistory.push(
      { role: 'user', content: message },
      { role: 'assistant', content: response.reply },
    );

  } catch (e) {
    removeChatMessage(typingId);
    addChatMessage('assistant', `<span style="color:var(--severity-high);">Error: ${e.message}</span>`);
  }
}

function addChatMessage(role, content) {
  const id = `msg-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`;
  const div = document.createElement('div');
  div.className = `chat-message chat-message--${role}`;
  div.id = id;
  div.innerHTML = content;
  dom.chatMessages.appendChild(div);
  dom.chatMessages.scrollTop = dom.chatMessages.scrollHeight;
  return id;
}

function removeChatMessage(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

function formatChatResponse(text) {
  // Convert markdown-style formatting to HTML
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/`(.*?)`/g, '<code style="background:var(--bg-glass);padding:1px 4px;border-radius:3px;font-family:var(--font-mono);font-size:0.8rem;">$1</code>')
    .replace(/\n/g, '<br>');
}

// ============================================================
// UI State Management
// ============================================================

function showLoading(show) {
  state.loading = show;
  dom.loadingOverlay.classList.toggle('active', show);
}

function setLoadingStep(text) {
  dom.loadingStep.textContent = text;
}

function showResults(show) {
  dom.resultsSection.classList.toggle('active', show);
  if (show) {
    dom.chatToggleFab.classList.add('visible');
    // Scroll to results
    dom.resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

function resetToUpload() {
  state.comparisonResult = null;
  state.chatHistory = [];
  state.chatOpen = false;

  dom.resultsSection.classList.remove('active');
  dom.chatPanel.classList.remove('active');
  dom.mainContent.classList.remove('chat-open');
  dom.chatToggleFab.classList.remove('visible');
  dom.chatSuggestions.style.display = '';

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// ============================================================
// Bootstrap
// ============================================================

// Expose sample invoice handler globally for onclick
window.handleSampleInvoiceClick = handleSampleInvoiceClick;

document.addEventListener('DOMContentLoaded', init);
