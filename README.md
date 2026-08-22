# AP Invoice Exception Assistant

An AI-powered tool that ingests vendor invoices (PDF/image) and purchase orders, extracts line items using Gemini Vision, identifies mismatches in price, quantity, and tax, and provides a chat interface for reviewers to ask questions and receive **source-grounded** explanations.

## Demo Video / Screenshots

> Run the app locally and navigate to `http://localhost:8000` to see the full demo.

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│  Frontend (Vanilla HTML/CSS/JS served by FastAPI)            │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  Upload   │  │   Results    │  │  Chat Panel  │           │
│  │  Panel    │  │  Dashboard   │  │  (Sidebar)   │           │
│  └──────────┘  └──────────────┘  └──────────────┘           │
└──────────────────────┬───────────────────────────────────────┘
                       │ REST API
┌──────────────────────┴───────────────────────────────────────┐
│  Backend (Python / FastAPI)                                   │
│  ┌───────────┐  ┌──────────┐  ┌────────────┐  ┌───────────┐ │
│  │  Invoice   │  │  Fuzzy   │  │  Mismatch  │  │   Chat    │ │
│  │ Extractor  │  │ Matcher  │  │ Comparator │  │  Engine   │ │
│  │(Gemini API)│  │(thefuzz) │  │ (rules)    │  │(Gemini)   │ │
│  └───────────┘  └──────────┘  └────────────┘  └───────────┘ │
└──────────────────────────────────────────────────────────────┘
```

### Key Design Decisions

1. **Gemini Vision for extraction** — Invoice images are sent directly to Gemini's multimodal API with a structured prompt specifying the exact JSON schema. This avoids building an OCR pipeline while producing high-quality results.

2. **Deterministic comparison engine** — Mismatch detection is pure Python business logic (no LLM). Price, quantity, and tax comparisons use configurable tolerances. This means exceptions are **never hallucinated**.

3. **Template-based explanations** — Every exception explanation is generated from a template that cites exact field names and values (e.g., "PO line 1 field 'unit_price' = 0.45"). The LLM is only used for extraction and natural-language chat.

4. **Grounded chat** — The entire ComparisonResult JSON is injected into the chat system prompt. The LLM is instructed to cite specific fields in every answer, ensuring source-grounded responses.

5. **Two-pass line matching** — Lines are matched first by exact item code, then by fuzzy description similarity. This handles real-world cases where item descriptions vary between PO and invoice.

## Assumptions

| # | What was ambiguous | Assumption made |
|---|-------------------|-----------------|
| A1 | PO format not specified | PO is structured JSON — keeps focus on the hard problem (unstructured invoice extraction) |
| A2 | Scope of OCR robustness | Gemini Vision handles extraction — no separate OCR pipeline needed |
| A3 | Chat depth | Scoped to current comparison. Full data injected as context for grounding |
| A4 | Multi-invoice support | One comparison at a time (no database). Can upload new pairs freely |
| A5 | Tax mismatch definition | Flagged when invoice tax differs from PO tax by > $0.01 |
| A6 | Line matching strategy | Item code (exact) → description (fuzzy, threshold 55%) → unmatched |

## Quick Start

### Prerequisites
- Python 3.11+
- A Google Gemini API key (for invoice extraction and chat)

### Setup

```bash
# 1. Install dependencies
pip install -r backend/requirements.txt

# 2. Set your Gemini API key
# Edit backend/.env and add your key:
#   GEMINI_API_KEY=your_key_here

# 3. Generate sample invoice images
python backend/generate_invoices.py

# 4. Run the server
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# 5. Open http://localhost:8000 in your browser
```

### Running Tests

```bash
python -m pytest backend/tests/ -v
```

## Tech Stack

| Layer | Tech | Why |
|-------|------|-----|
| Frontend | HTML + CSS + JS | No build step, instant dev cycle, served by FastAPI |
| Backend | FastAPI | Async-native, auto-generated Swagger docs |
| AI | Google Gemini (multimodal + text) | Vision API for extraction, text API for chat |
| PDF | PyMuPDF | PDF→image conversion for Gemini Vision |
| Matching | thefuzz | Fuzzy string matching for line-item descriptions |
| Validation | Pydantic | Schema enforcement on all data models |

## Project Structure

```
├── backend/
│   ├── main.py                 # FastAPI app + all endpoints
│   ├── requirements.txt
│   ├── .env                    # GEMINI_API_KEY goes here
│   ├── generate_invoices.py    # Creates sample invoice PDFs/PNGs
│   ├── models/
│   │   └── schemas.py          # Pydantic data models
│   ├── services/
│   │   ├── extractor.py        # Gemini Vision invoice extraction
│   │   ├── matcher.py          # Fuzzy line-item matching
│   │   ├── comparator.py       # Mismatch detection + explanations
│   │   └── chat_engine.py      # Grounded chat with Gemini
│   ├── sample_data/
│   │   ├── po_001.json         # Sample PO (industrial supplies)
│   │   ├── po_002.json         # Sample PO (office supplies)
│   │   ├── invoice_001.png/pdf # Sample invoice with mismatches
│   │   └── invoice_002.png/pdf # Sample invoice with mismatches
│   └── tests/
│       └── test_comparator.py  # 9 unit tests
├── frontend/
│   ├── index.html              # Single-page app
│   ├── styles.css              # Design system (dark theme)
│   └── app.js                  # Frontend logic
└── README.md
```

## API Documentation

Once running, visit `http://localhost:8000/docs` for auto-generated Swagger UI.

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Health check + Gemini config status |
| GET | `/api/sample-pos` | List sample purchase orders |
| GET | `/api/sample-pos/{filename}` | Get a specific PO |
| GET | `/api/sample-invoices` | List sample invoice files |
| GET | `/api/sample-invoices/{filename}` | Serve invoice image/PDF |
| POST | `/api/compare` | Compare invoice vs PO |
| POST | `/api/chat` | Ask about exceptions |

## How It Satisfies Each Evaluation Criterion

### 1. "Quality and robustness of document extraction"
- Side-by-side view: original invoice image + extracted structured table
- Confidence scores displayed as color-coded badges
- Two different invoice layouts demonstrate extraction robustness
- Handles both PDF and image formats

### 2. "Clarity and accuracy of the reasoning behind each flag"
- Exception cards show plain-English explanations with exact field citations
- Color-coded severity badges (High/Medium/Low) based on deviation magnitude
- Three value blocks per exception: PO value, Invoice value, Difference (with %)

### 3. "Whether the explanation cites actual source fields"
- Every exception explanation follows the format: `"Source: PO line X field 'Y' = Z, Invoice line X field 'Y' = W"`
- These are template-generated (deterministic), not LLM-generated
- Chat answers include inline field citations, grounded by the full comparison context injected into the system prompt
