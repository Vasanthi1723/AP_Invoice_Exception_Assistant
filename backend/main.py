"""
AP Invoice Exception Assistant — FastAPI Application

Main entry point. Serves:
  - REST API endpoints for comparison and chat
  - Static frontend files
  - Sample data for demo
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.models.schemas import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    ComparisonResult,
    ExtractedInvoice,
    PurchaseOrder,
)
from backend.services.chat_engine import chat
from backend.services.comparator import compare
from backend.services.extractor import extract_invoice

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
SAMPLE_DATA_DIR = Path(__file__).parent / "sample_data"
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"

app = FastAPI(
    title="AP Invoice Exception Assistant",
    description="AI-powered invoice mismatch detection with grounded explanations",
    version="1.0.0",
)

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for the latest comparison (simple single-session demo)
_latest_comparison: Optional[ComparisonResult] = None


# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "gemini_configured": bool(GEMINI_API_KEY),
    }


@app.get("/api/sample-pos")
async def list_sample_pos():
    """Return list of available sample Purchase Orders."""
    pos = []
    for f in sorted(SAMPLE_DATA_DIR.glob("po_*.json")):
        with open(f) as fh:
            data = json.load(fh)
            pos.append({
                "filename": f.name,
                "po_number": data["po_number"],
                "vendor": data["vendor"],
                "total": data["total"],
                "line_count": len(data["line_items"]),
            })
    return {"purchase_orders": pos}


@app.get("/api/sample-pos/{filename}")
async def get_sample_po(filename: str):
    """Return a specific sample PO by filename."""
    filepath = SAMPLE_DATA_DIR / filename
    if not filepath.exists() or not filepath.name.startswith("po_"):
        raise HTTPException(status_code=404, detail="PO not found")
    with open(filepath) as f:
        return json.load(f)


@app.get("/api/sample-invoices")
async def list_sample_invoices():
    """Return list of available sample invoice images."""
    invoices = []
    for ext in ["*.png", "*.jpg", "*.jpeg", "*.pdf", "*.webp"]:
        for f in sorted(SAMPLE_DATA_DIR.glob(ext)):
            if f.stem.startswith("invoice_"):
                invoices.append({
                    "filename": f.name,
                    "url": f"/api/sample-invoices/{f.name}",
                })
    return {"invoices": invoices}


@app.get("/api/sample-invoices/{filename}")
async def get_sample_invoice_file(filename: str):
    """Serve a sample invoice image file."""
    filepath = SAMPLE_DATA_DIR / filename
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="Invoice file not found")
    return FileResponse(filepath)


@app.post("/api/compare")
async def compare_invoice(
    invoice_file: Optional[UploadFile] = File(None),
    po_file: Optional[UploadFile] = File(None),
    po_filename: Optional[str] = Form(None),
    invoice_json: Optional[str] = Form(None),
):
    """
    Compare an invoice against a purchase order.

    Accepts either:
      - invoice_file (image/PDF) + po_file or po_filename (sample PO)
      - invoice_json (pre-extracted JSON) + po_file or po_filename

    Returns a full ComparisonResult with exceptions and explanations.
    """
    global _latest_comparison

    if not GEMINI_API_KEY and not invoice_json:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY not configured. Set it in the .env file. "
                   "Alternatively, use the demo mode with pre-extracted invoice data.",
        )

    # --- Load Purchase Order ---
    po: PurchaseOrder
    if po_file:
        po_data = json.loads(await po_file.read())
        po = PurchaseOrder(**po_data)
    elif po_filename:
        filepath = SAMPLE_DATA_DIR / po_filename
        if not filepath.exists():
            raise HTTPException(status_code=404, detail=f"Sample PO '{po_filename}' not found")
        with open(filepath) as f:
            po = PurchaseOrder(**json.load(f))
    else:
        raise HTTPException(status_code=400, detail="Must provide either po_file or po_filename")

    # --- Extract Invoice ---
    invoice: ExtractedInvoice
    if invoice_json:
        # Pre-extracted JSON (demo mode or manual input)
        invoice = ExtractedInvoice(**json.loads(invoice_json))
    elif invoice_file:
        # Extract from uploaded file using Gemini Vision
        file_bytes = await invoice_file.read()
        try:
            invoice = await extract_invoice(
                file_bytes=file_bytes,
                filename=invoice_file.filename or "invoice.png",
                api_key=GEMINI_API_KEY,
            )
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))
    else:
        raise HTTPException(
            status_code=400,
            detail="Must provide either invoice_file or invoice_json",
        )

    # --- Compare ---
    result = compare(po, invoice)
    _latest_comparison = result

    logger.info(
        f"Comparison complete: {result.summary.total_exceptions} exceptions found "
        f"for invoice {result.invoice_number} vs PO {result.po_number}"
    )

    return result.model_dump()


@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Chat about the current comparison results.

    Injects the full comparison context into the Gemini prompt so answers
    are always grounded in actual source fields.
    """
    global _latest_comparison

    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY not configured. Set it in the .env file.",
        )

    # Use provided context or fall back to the latest comparison
    comparison = request.comparison_context or _latest_comparison
    if not comparison:
        raise HTTPException(
            status_code=400,
            detail="No comparison context available. Run a comparison first.",
        )

    try:
        response = await chat(
            message=request.message,
            comparison=comparison,
            history=request.history,
            api_key=GEMINI_API_KEY,
        )
        return response.model_dump()
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


# ---------------------------------------------------------------------------
# Static Frontend
# ---------------------------------------------------------------------------

# Serve the frontend's index.html at the root
@app.get("/")
async def serve_frontend():
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return JSONResponse(
        content={"message": "Frontend not found. API is running at /docs"},
        status_code=200,
    )


# Mount static files (CSS, JS, etc.)
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
