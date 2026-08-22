"""
Comparator service: detects mismatches between matched PO and invoice lines.

Generates structured exceptions with template-based explanations that
cite exact source fields and values — NOT LLM-generated.
"""

from __future__ import annotations

import uuid
from typing import Optional

from backend.models.schemas import (
    ComparisonResult,
    ComparisonSummary,
    ExceptionType,
    ExtractedInvoice,
    LineException,
    MatchedLine,
    OverallStatus,
    PurchaseOrder,
    Severity,
)
from backend.services.matcher import match_line_items


def _make_id() -> str:
    return f"EXC-{uuid.uuid4().hex[:6].upper()}"


def _severity_from_pct(pct: float) -> Severity:
    """Classify severity based on absolute percentage deviation."""
    abs_pct = abs(pct)
    if abs_pct > 5.0:
        return Severity.HIGH
    elif abs_pct > 1.0:
        return Severity.MEDIUM
    return Severity.LOW


def _check_price(
    po_price: float,
    inv_price: float,
    po_line_num: int,
    inv_line_num: int,
    tolerance: float = 0.005,
) -> Optional[LineException]:
    """Check for unit-price mismatch."""
    diff = inv_price - po_price
    if abs(diff) <= tolerance:
        return None

    pct = (diff / po_price * 100) if po_price != 0 else 100.0
    direction = "exceeds" if diff > 0 else "is less than"

    return LineException(
        exception_id=_make_id(),
        type=ExceptionType.PRICE_MISMATCH,
        field="unit_price",
        po_value=po_price,
        invoice_value=inv_price,
        difference=round(diff, 4),
        difference_pct=round(pct, 2),
        severity=_severity_from_pct(pct),
        explanation=(
            f"Invoice unit price (${inv_price:.2f}) {direction} PO unit price "
            f"(${po_price:.2f}) by ${abs(diff):.2f} ({abs(pct):.2f}%). "
            f"Source: PO line {po_line_num} field 'unit_price' = {po_price}, "
            f"Invoice line {inv_line_num} field 'unit_price' = {inv_price}."
        ),
    )


def _check_quantity(
    po_qty: float,
    inv_qty: float,
    po_line_num: int,
    inv_line_num: int,
    tolerance: float = 0.0,
) -> Optional[LineException]:
    """Check for quantity mismatch."""
    diff = inv_qty - po_qty
    if abs(diff) <= tolerance:
        return None

    pct = (diff / po_qty * 100) if po_qty != 0 else 100.0
    direction = "more than" if diff > 0 else "less than"

    return LineException(
        exception_id=_make_id(),
        type=ExceptionType.QUANTITY_MISMATCH,
        field="quantity",
        po_value=po_qty,
        invoice_value=inv_qty,
        difference=round(diff, 4),
        difference_pct=round(pct, 2),
        severity=_severity_from_pct(pct),
        explanation=(
            f"Invoice quantity ({inv_qty}) is {direction} PO quantity "
            f"({po_qty}) by {abs(diff)} units ({abs(pct):.2f}%). "
            f"Source: PO line {po_line_num} field 'quantity' = {po_qty}, "
            f"Invoice line {inv_line_num} field 'quantity' = {inv_qty}."
        ),
    )


def _check_document_tax(
    po: PurchaseOrder,
    invoice: ExtractedInvoice,
    tolerance: float = 0.01,
) -> Optional[LineException]:
    """Check for document-level tax mismatch."""
    # Calculate expected tax from PO
    expected_tax = po.tax
    actual_tax = invoice.tax
    diff = actual_tax - expected_tax

    if abs(diff) <= tolerance:
        return None

    pct = (diff / expected_tax * 100) if expected_tax != 0 else 100.0
    direction = "exceeds" if diff > 0 else "is less than"

    return LineException(
        exception_id=_make_id(),
        type=ExceptionType.TAX_MISMATCH,
        field="tax",
        po_value=expected_tax,
        invoice_value=actual_tax,
        difference=round(diff, 4),
        difference_pct=round(pct, 2),
        severity=_severity_from_pct(pct),
        explanation=(
            f"Invoice total tax (${actual_tax:.2f}) {direction} expected PO tax "
            f"(${expected_tax:.2f}) by ${abs(diff):.2f} ({abs(pct):.2f}%). "
            f"Source: PO field 'tax' = {expected_tax}, "
            f"Invoice field 'tax' = {actual_tax}. "
            f"Note: PO tax rate is {po.tax_rate * 100:.1f}%."
        ),
    )


def compare(
    po: PurchaseOrder,
    invoice: ExtractedInvoice,
    price_tolerance: float = 0.005,
    qty_tolerance: float = 0.0,
    tax_tolerance: float = 0.01,
) -> ComparisonResult:
    """
    Compare an extracted invoice against a purchase order.

    Performs:
      1. Fuzzy line-item matching
      2. Price / quantity comparison on each matched pair
      3. Document-level tax comparison
      4. Flags unmatched lines on both sides

    Returns a fully populated ComparisonResult with exceptions and explanations.
    """

    # Step 1: Match line items
    match_results, unmatched_po, unmatched_inv = match_line_items(
        po.line_items, invoice.line_items
    )

    # Step 2: Check each matched pair for mismatches
    matched_lines: list[MatchedLine] = []

    for mr in match_results:
        exceptions: list[LineException] = []

        # Price check
        price_exc = _check_price(
            mr.po_line.unit_price,
            mr.invoice_line.unit_price,
            mr.po_line.line_number,
            mr.invoice_line.line_number,
            price_tolerance,
        )
        if price_exc:
            exceptions.append(price_exc)

        # Quantity check
        qty_exc = _check_quantity(
            mr.po_line.quantity,
            mr.invoice_line.quantity,
            mr.po_line.line_number,
            mr.invoice_line.line_number,
            qty_tolerance,
        )
        if qty_exc:
            exceptions.append(qty_exc)

        matched_lines.append(MatchedLine(
            po_line=mr.po_line,
            invoice_line=mr.invoice_line,
            match_confidence=mr.confidence,
            exceptions=exceptions,
        ))

    # Step 3: Document-level tax check
    tax_exc = _check_document_tax(po, invoice, tax_tolerance)

    # Step 4: Build summary
    all_exceptions: list[LineException] = []
    for ml in matched_lines:
        all_exceptions.extend(ml.exceptions)
    if tax_exc:
        all_exceptions.append(tax_exc)

    # Add exceptions for unmatched lines
    for po_line in unmatched_po:
        exc = LineException(
            exception_id=_make_id(),
            type=ExceptionType.MISSING_ON_INVOICE,
            field="line_item",
            po_value=po_line.description,
            invoice_value=None,
            severity=Severity.HIGH,
            explanation=(
                f"PO line {po_line.line_number} ('{po_line.description}', "
                f"item code '{po_line.item_code}') has no matching line on the invoice. "
                f"Expected {po_line.quantity} {po_line.unit} at ${po_line.unit_price:.2f} each."
            ),
        )
        all_exceptions.append(exc)

    for inv_line in unmatched_inv:
        exc = LineException(
            exception_id=_make_id(),
            type=ExceptionType.EXTRA_ON_INVOICE,
            field="line_item",
            po_value=None,
            invoice_value=inv_line.description,
            severity=Severity.MEDIUM,
            explanation=(
                f"Invoice line {inv_line.line_number} ('{inv_line.description}') "
                f"has no matching line on the PO. This is an extra charge of "
                f"{inv_line.quantity} {inv_line.unit} at ${inv_line.unit_price:.2f} each "
                f"(total ${inv_line.total:.2f})."
            ),
        )
        all_exceptions.append(exc)

    by_type: dict[str, int] = {}
    for exc in all_exceptions:
        by_type[exc.type.value] = by_type.get(exc.type.value, 0) + 1

    lines_with_exceptions = sum(1 for ml in matched_lines if ml.exceptions)

    summary = ComparisonSummary(
        total_lines_compared=len(matched_lines),
        lines_with_exceptions=lines_with_exceptions,
        total_exceptions=len(all_exceptions),
        by_type=by_type,
    )

    overall_status = (
        OverallStatus.MATCH if len(all_exceptions) == 0
        else OverallStatus.EXCEPTIONS_FOUND
    )

    return ComparisonResult(
        invoice_number=invoice.invoice_number,
        po_number=po.po_number,
        overall_status=overall_status,
        invoice_data=invoice,
        po_data=po,
        matched_lines=matched_lines,
        unmatched_po_lines=unmatched_po,
        unmatched_invoice_lines=unmatched_inv,
        tax_exception=tax_exc,
        summary=summary,
    )
