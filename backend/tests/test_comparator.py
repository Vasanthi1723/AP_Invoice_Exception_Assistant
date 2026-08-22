"""
Unit tests for the comparator service.

Tests the core mismatch detection logic with deterministic inputs.
"""

import pytest

from backend.models.schemas import (
    ExceptionType,
    ExtractedInvoice,
    InvoiceLineItem,
    OverallStatus,
    POLineItem,
    PurchaseOrder,
    Severity,
)
from backend.services.comparator import compare


def _make_po(
    line_items: list[dict] | None = None,
    tax_rate: float = 0.08,
) -> PurchaseOrder:
    """Helper to create a test PO."""
    items = line_items or [
        {
            "line_number": 1,
            "item_code": "ITEM-001",
            "description": "Widget Alpha",
            "quantity": 100,
            "unit_price": 10.00,
            "unit": "EA",
            "total": 1000.00,
        },
        {
            "line_number": 2,
            "item_code": "ITEM-002",
            "description": "Widget Beta",
            "quantity": 50,
            "unit_price": 25.00,
            "unit": "EA",
            "total": 1250.00,
        },
    ]
    po_items = [POLineItem(**item) for item in items]
    subtotal = sum(i.total for i in po_items)
    tax = round(subtotal * tax_rate, 2)
    return PurchaseOrder(
        po_number="PO-TEST-001",
        vendor="Test Vendor",
        date="2024-01-01",
        currency="USD",
        tax_rate=tax_rate,
        line_items=po_items,
        subtotal=subtotal,
        tax=tax,
        total=round(subtotal + tax, 2),
    )


def _make_invoice(
    line_items: list[dict] | None = None,
    tax: float | None = None,
) -> ExtractedInvoice:
    """Helper to create a test extracted invoice."""
    items = line_items or [
        {
            "line_number": 1,
            "item_code": "ITEM-001",
            "description": "Widget Alpha",
            "quantity": 100,
            "unit_price": 10.00,
            "unit": "EA",
            "total": 1000.00,
        },
        {
            "line_number": 2,
            "item_code": "ITEM-002",
            "description": "Widget Beta",
            "quantity": 50,
            "unit_price": 25.00,
            "unit": "EA",
            "total": 1250.00,
        },
    ]
    inv_items = [InvoiceLineItem(**item) for item in items]
    subtotal = sum(i.total for i in inv_items)
    if tax is None:
        tax = round(subtotal * 0.08, 2)
    return ExtractedInvoice(
        invoice_number="INV-TEST-001",
        vendor="Test Vendor",
        line_items=inv_items,
        subtotal=subtotal,
        tax=tax,
        total=round(subtotal + tax, 2),
    )


class TestPerfectMatch:
    """When invoice exactly matches PO, no exceptions should be flagged."""

    def test_no_exceptions_on_exact_match(self):
        po = _make_po()
        inv = _make_invoice()
        result = compare(po, inv)

        assert result.overall_status == OverallStatus.MATCH
        assert result.summary.total_exceptions == 0
        assert len(result.matched_lines) == 2
        for ml in result.matched_lines:
            assert len(ml.exceptions) == 0


class TestPriceMismatch:
    """Price mismatches should be detected and explained."""

    def test_price_increase_flagged(self):
        po = _make_po()
        inv = _make_invoice(line_items=[
            {
                "line_number": 1,
                "item_code": "ITEM-001",
                "description": "Widget Alpha",
                "quantity": 100,
                "unit_price": 12.00,  # $2 more than PO
                "unit": "EA",
                "total": 1200.00,
            },
            {
                "line_number": 2,
                "item_code": "ITEM-002",
                "description": "Widget Beta",
                "quantity": 50,
                "unit_price": 25.00,
                "unit": "EA",
                "total": 1250.00,
            },
        ])
        result = compare(po, inv)

        assert result.overall_status == OverallStatus.EXCEPTIONS_FOUND
        # Find the price exception
        price_excs = [
            exc
            for ml in result.matched_lines
            for exc in ml.exceptions
            if exc.type == ExceptionType.PRICE_MISMATCH
        ]
        assert len(price_excs) == 1
        exc = price_excs[0]
        assert exc.po_value == 10.00
        assert exc.invoice_value == 12.00
        assert exc.difference == 2.0
        assert exc.severity == Severity.HIGH  # 20% difference
        assert "unit_price" in exc.explanation
        assert "$10.00" in exc.explanation
        assert "$12.00" in exc.explanation

    def test_small_price_within_tolerance(self):
        po = _make_po()
        inv = _make_invoice(line_items=[
            {
                "line_number": 1,
                "item_code": "ITEM-001",
                "description": "Widget Alpha",
                "quantity": 100,
                "unit_price": 10.004,  # Within default tolerance of 0.005
                "unit": "EA",
                "total": 1000.40,
            },
            {
                "line_number": 2,
                "item_code": "ITEM-002",
                "description": "Widget Beta",
                "quantity": 50,
                "unit_price": 25.00,
                "unit": "EA",
                "total": 1250.00,
            },
        ])
        result = compare(po, inv)

        price_excs = [
            exc
            for ml in result.matched_lines
            for exc in ml.exceptions
            if exc.type == ExceptionType.PRICE_MISMATCH
        ]
        assert len(price_excs) == 0


class TestQuantityMismatch:
    """Quantity mismatches should be detected and explained."""

    def test_quantity_decrease_flagged(self):
        po = _make_po()
        inv = _make_invoice(line_items=[
            {
                "line_number": 1,
                "item_code": "ITEM-001",
                "description": "Widget Alpha",
                "quantity": 80,  # 20 less than PO
                "unit_price": 10.00,
                "unit": "EA",
                "total": 800.00,
            },
            {
                "line_number": 2,
                "item_code": "ITEM-002",
                "description": "Widget Beta",
                "quantity": 50,
                "unit_price": 25.00,
                "unit": "EA",
                "total": 1250.00,
            },
        ])
        result = compare(po, inv)

        qty_excs = [
            exc
            for ml in result.matched_lines
            for exc in ml.exceptions
            if exc.type == ExceptionType.QUANTITY_MISMATCH
        ]
        assert len(qty_excs) == 1
        exc = qty_excs[0]
        assert exc.po_value == 100
        assert exc.invoice_value == 80
        assert exc.difference == -20
        assert "quantity" in exc.explanation


class TestTaxMismatch:
    """Document-level tax mismatches should be detected."""

    def test_tax_overcharge_flagged(self):
        po = _make_po()
        inv = _make_invoice(tax=200.00)  # Way more than expected
        result = compare(po, inv)

        assert result.tax_exception is not None
        assert result.tax_exception.type == ExceptionType.TAX_MISMATCH
        assert "tax" in result.tax_exception.explanation.lower()


class TestUnmatchedLines:
    """Missing and extra lines should be detected."""

    def test_missing_po_line_flagged(self):
        po = _make_po()
        inv = _make_invoice(line_items=[
            {
                "line_number": 1,
                "item_code": "ITEM-001",
                "description": "Widget Alpha",
                "quantity": 100,
                "unit_price": 10.00,
                "unit": "EA",
                "total": 1000.00,
            },
            # ITEM-002 is missing from invoice
        ])
        result = compare(po, inv)

        assert len(result.unmatched_po_lines) == 1
        assert result.unmatched_po_lines[0].item_code == "ITEM-002"
        assert result.summary.by_type.get("MISSING_ON_INVOICE", 0) == 1

    def test_extra_invoice_line_flagged(self):
        po = _make_po()
        inv = _make_invoice(line_items=[
            {
                "line_number": 1,
                "item_code": "ITEM-001",
                "description": "Widget Alpha",
                "quantity": 100,
                "unit_price": 10.00,
                "unit": "EA",
                "total": 1000.00,
            },
            {
                "line_number": 2,
                "item_code": "ITEM-002",
                "description": "Widget Beta",
                "quantity": 50,
                "unit_price": 25.00,
                "unit": "EA",
                "total": 1250.00,
            },
            {
                "line_number": 3,
                "item_code": "ITEM-999",
                "description": "Mysterious Extra Charge",
                "quantity": 1,
                "unit_price": 500.00,
                "unit": "EA",
                "total": 500.00,
            },
        ])
        result = compare(po, inv)

        assert len(result.unmatched_invoice_lines) == 1
        assert result.summary.by_type.get("EXTRA_ON_INVOICE", 0) == 1


class TestFuzzyDescriptionMatching:
    """Lines should match even when descriptions differ slightly."""

    def test_fuzzy_description_match(self):
        po = _make_po()
        inv = _make_invoice(line_items=[
            {
                "line_number": 1,
                "item_code": None,  # No item code
                "description": "Alpha Widget",  # Reworded
                "quantity": 100,
                "unit_price": 10.00,
                "unit": "EA",
                "total": 1000.00,
            },
            {
                "line_number": 2,
                "item_code": None,
                "description": "Beta Widget",
                "quantity": 50,
                "unit_price": 25.00,
                "unit": "EA",
                "total": 1250.00,
            },
        ])
        result = compare(po, inv)

        # Should still match by fuzzy description
        assert len(result.matched_lines) == 2
        assert len(result.unmatched_po_lines) == 0


class TestExplanationQuality:
    """Explanations should cite actual source fields and values."""

    def test_explanation_cites_source_fields(self):
        po = _make_po()
        inv = _make_invoice(line_items=[
            {
                "line_number": 1,
                "item_code": "ITEM-001",
                "description": "Widget Alpha",
                "quantity": 100,
                "unit_price": 15.00,  # Different
                "unit": "EA",
                "total": 1500.00,
            },
            {
                "line_number": 2,
                "item_code": "ITEM-002",
                "description": "Widget Beta",
                "quantity": 50,
                "unit_price": 25.00,
                "unit": "EA",
                "total": 1250.00,
            },
        ])
        result = compare(po, inv)

        price_excs = [
            exc
            for ml in result.matched_lines
            for exc in ml.exceptions
            if exc.type == ExceptionType.PRICE_MISMATCH
        ]
        assert len(price_excs) == 1
        explanation = price_excs[0].explanation

        # Must cite the field name
        assert "unit_price" in explanation
        # Must cite PO value
        assert "10.00" in explanation
        # Must cite invoice value
        assert "15.00" in explanation
        # Must reference source location
        assert "PO line" in explanation
        assert "Invoice line" in explanation
