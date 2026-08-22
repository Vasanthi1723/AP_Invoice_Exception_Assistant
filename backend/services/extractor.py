"""
Invoice Extractor: Uses Google Gemini's multimodal API to extract
structured line-item data from invoice images and PDFs.

This is the core "document extraction" component. It sends the invoice
image directly to Gemini Vision with a carefully engineered prompt that
specifies the exact JSON schema we expect back.
"""

from __future__ import annotations

import base64
import io
import json
import logging
import re
from pathlib import Path

from google import genai
from google.genai import types

from backend.models.schemas import ExtractedInvoice, InvoiceLineItem

logger = logging.getLogger(__name__)

# The extraction prompt is the most critical piece of the system.
# It must be precise about the JSON schema and include instructions
# for handling edge cases.
EXTRACTION_PROMPT = """You are an expert accounts payable document processor.
Analyze the attached invoice image and extract ALL line items and header information
into the exact JSON format specified below.

IMPORTANT RULES:
1. Extract EVERY line item visible on the invoice — do not skip any
2. If a field is not visible or unclear, use null
3. For numeric fields, extract the raw number (no currency symbols)
4. If item codes are present, extract them exactly as shown
5. Calculate totals if they are not explicitly shown
6. Look for tax amounts — they may be labeled as "Tax", "GST", "VAT", "Sales Tax", etc.
7. Report your overall confidence in the extraction as a decimal 0-1

Return ONLY valid JSON in this exact format (no markdown fences, no commentary):

{
  "invoice_number": "string",
  "vendor": "string or null",
  "date": "string (YYYY-MM-DD) or null",
  "po_reference": "string or null — look for PO#, Purchase Order, Reference fields",
  "currency": "USD",
  "line_items": [
    {
      "line_number": 1,
      "item_code": "string or null",
      "description": "string — full item description",
      "quantity": 0.0,
      "unit_price": 0.0,
      "unit": "EA",
      "total": 0.0
    }
  ],
  "subtotal": 0.0,
  "tax": 0.0,
  "total": 0.0,
  "extraction_confidence": 0.95,
  "raw_text_snippet": "first 200 chars of visible text on the invoice"
}
"""


def _pdf_to_images(pdf_bytes: bytes) -> list[bytes]:
    """Convert PDF pages to PNG images using PyMuPDF."""
    try:
        import fitz  # PyMuPDF

        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        images = []
        for page_num in range(min(len(doc), 3)):  # Max 3 pages
            page = doc[page_num]
            # Render at 2x resolution for better OCR
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            images.append(pix.tobytes("png"))
        doc.close()
        return images
    except ImportError:
        logger.warning("PyMuPDF not installed — PDF support disabled")
        raise ValueError(
            "PDF processing requires PyMuPDF. Install with: pip install PyMuPDF"
        )


def _detect_mime_type(file_bytes: bytes, filename: str) -> str:
    """Detect the MIME type from file extension or magic bytes."""
    ext = Path(filename).suffix.lower()
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
        ".pdf": "application/pdf",
    }
    return mime_map.get(ext, "image/png")


async def extract_invoice(
    file_bytes: bytes,
    filename: str,
    api_key: str,
) -> ExtractedInvoice:
    """
    Extract structured data from an invoice image or PDF.

    Args:
        file_bytes: Raw bytes of the uploaded file
        filename: Original filename (used for MIME type detection)
        api_key: Google Gemini API key

    Returns:
        ExtractedInvoice with all extracted line items and metadata
    """
    mime_type = _detect_mime_type(file_bytes, filename)

    # Convert PDF to images if needed
    if mime_type == "application/pdf":
        image_bytes_list = _pdf_to_images(file_bytes)
        mime_type = "image/png"
    else:
        image_bytes_list = [file_bytes]

    # Build the multimodal parts
    parts = []
    parts.append(types.Part.from_text(text=EXTRACTION_PROMPT))
    for img_bytes in image_bytes_list:
        parts.append(types.Part.from_bytes(data=img_bytes, mime_type=mime_type))

    # Call Gemini
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[types.Content(role="user", parts=parts)],
        config=types.GenerateContentConfig(
            temperature=0.1,  # Low temperature for factual extraction
            max_output_tokens=4096,
        ),
    )

    # Parse the response
    raw_text = response.text.strip()

    # Clean potential markdown fences
    if raw_text.startswith("```"):
        raw_text = re.sub(r"^```(?:json)?\s*", "", raw_text)
        raw_text = re.sub(r"\s*```$", "", raw_text)

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Gemini response as JSON: {e}")
        logger.error(f"Raw response: {raw_text[:500]}")
        raise ValueError(
            f"Gemini returned invalid JSON. This may indicate a complex or "
            f"unusual invoice layout. Raw response preview: {raw_text[:200]}"
        )

    # Validate and construct the model
    try:
        # Ensure line_items have proper line_numbers
        for i, item in enumerate(data.get("line_items", [])):
            if "line_number" not in item:
                item["line_number"] = i + 1

        invoice = ExtractedInvoice(**data)
        logger.info(
            f"Extracted invoice {invoice.invoice_number} with "
            f"{len(invoice.line_items)} line items "
            f"(confidence: {invoice.extraction_confidence})"
        )
        return invoice

    except Exception as e:
        logger.error(f"Failed to validate extracted data: {e}")
        raise ValueError(f"Extracted data failed validation: {e}")
