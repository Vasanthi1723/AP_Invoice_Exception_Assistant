"""
Pydantic data models for the AP Invoice Exception Assistant.

Defines the schemas for:
- Purchase Orders (PO)
- Extracted Invoices
- Comparison Results with Exceptions
- Chat messages
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ExceptionType(str, Enum):
    PRICE_MISMATCH = "PRICE_MISMATCH"
    QUANTITY_MISMATCH = "QUANTITY_MISMATCH"
    TAX_MISMATCH = "TAX_MISMATCH"
    MISSING_ON_INVOICE = "MISSING_ON_INVOICE"
    EXTRA_ON_INVOICE = "EXTRA_ON_INVOICE"
    DESCRIPTION_MISMATCH = "DESCRIPTION_MISMATCH"


class Severity(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class OverallStatus(str, Enum):
    MATCH = "MATCH"
    EXCEPTIONS_FOUND = "EXCEPTIONS_FOUND"
    EXTRACTION_FAILED = "EXTRACTION_FAILED"


# ---------------------------------------------------------------------------
# Purchase Order Models
# ---------------------------------------------------------------------------

class POLineItem(BaseModel):
    line_number: int
    item_code: str
    description: str
    quantity: float
    unit_price: float
    unit: str = "EA"
    total: float


class PurchaseOrder(BaseModel):
    po_number: str
    vendor: str
    date: str
    currency: str = "USD"
    tax_rate: float = Field(default=0.0, description="Tax rate as a decimal, e.g. 0.08 for 8%")
    line_items: list[POLineItem]
    subtotal: float
    tax: float
    total: float


# ---------------------------------------------------------------------------
# Invoice Models (extracted from document)
# ---------------------------------------------------------------------------

class InvoiceLineItem(BaseModel):
    line_number: int
    item_code: Optional[str] = None
    description: str
    quantity: float
    unit_price: float
    unit: str = "EA"
    total: float


class ExtractedInvoice(BaseModel):
    invoice_number: str
    vendor: Optional[str] = None
    date: Optional[str] = None
    po_reference: Optional[str] = None
    currency: str = "USD"
    line_items: list[InvoiceLineItem]
    subtotal: float
    tax: float
    total: float
    extraction_confidence: Optional[float] = Field(
        default=None,
        description="Overall confidence score for extraction (0-1)"
    )
    raw_text_snippet: Optional[str] = Field(
        default=None,
        description="Raw text extracted from the invoice for reference"
    )


# ---------------------------------------------------------------------------
# Comparison / Exception Models
# ---------------------------------------------------------------------------

class LineException(BaseModel):
    exception_id: str
    type: ExceptionType
    field: str
    po_value: Optional[float | str] = None
    invoice_value: Optional[float | str] = None
    difference: Optional[float] = None
    difference_pct: Optional[float] = None
    severity: Severity
    explanation: str = Field(
        description="Plain-English explanation citing exact source fields and values"
    )


class MatchedLine(BaseModel):
    po_line: POLineItem
    invoice_line: InvoiceLineItem
    match_confidence: float = Field(description="Fuzzy match confidence 0-1")
    exceptions: list[LineException] = Field(default_factory=list)


class ComparisonSummary(BaseModel):
    total_lines_compared: int
    lines_with_exceptions: int
    total_exceptions: int
    by_type: dict[str, int] = Field(default_factory=dict)


class ComparisonResult(BaseModel):
    invoice_number: str
    po_number: str
    overall_status: OverallStatus
    invoice_data: ExtractedInvoice
    po_data: PurchaseOrder
    matched_lines: list[MatchedLine] = Field(default_factory=list)
    unmatched_po_lines: list[POLineItem] = Field(default_factory=list)
    unmatched_invoice_lines: list[InvoiceLineItem] = Field(default_factory=list)
    tax_exception: Optional[LineException] = Field(
        default=None,
        description="Document-level tax mismatch if any"
    )
    summary: ComparisonSummary


# ---------------------------------------------------------------------------
# Chat Models
# ---------------------------------------------------------------------------

class ChatMessage(BaseModel):
    role: str = Field(description="'user' or 'assistant'")
    content: str


class ChatRequest(BaseModel):
    message: str
    comparison_context: Optional[ComparisonResult] = None
    history: list[ChatMessage] = Field(default_factory=list)


class ChatResponse(BaseModel):
    reply: str
    citations: list[str] = Field(
        default_factory=list,
        description="List of source field citations used in the reply"
    )
