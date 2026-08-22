"""
Generate synthetic invoice images for demo purposes.
Creates styled HTML invoices and renders them to PNG using a simple approach.
Since we don't have a browser-based renderer, we'll create invoices as
well-formatted text-based PNGs using Pillow or as HTML files that can be
screenshot'd.

For this demo, we generate PDF invoices using reportlab-like approach with
PyMuPDF (fitz) which can create PDFs from scratch.
"""

import json
import sys
from pathlib import Path

# We'll use PyMuPDF to create simple PDF invoices
import fitz  # PyMuPDF


def create_invoice_pdf(output_path: str, invoice_data: dict):
    """Create a professional-looking invoice PDF."""

    doc = fitz.open()
    page = doc.new_page(width=595, height=842)  # A4

    # Colors
    dark_blue = (0.1, 0.15, 0.3)
    medium_blue = (0.25, 0.35, 0.55)
    light_gray = (0.6, 0.6, 0.65)
    black = (0, 0, 0)
    white = (1, 1, 1)
    accent = (0.38, 0.4, 0.94)  # Indigo-ish

    # Header background
    rect = fitz.Rect(0, 0, 595, 100)
    page.draw_rect(rect, color=None, fill=dark_blue)

    # Company name
    page.insert_text(
        fitz.Point(40, 45),
        invoice_data.get("vendor", "Vendor"),
        fontsize=20,
        fontname="helv",
        color=white,
    )

    # INVOICE label
    page.insert_text(
        fitz.Point(420, 45),
        "INVOICE",
        fontsize=24,
        fontname="helv",
        color=accent,
    )

    # Invoice details
    y = 130
    details = [
        ("Invoice #:", invoice_data["invoice_number"]),
        ("Date:", invoice_data["date"]),
        ("PO Reference:", invoice_data.get("po_reference", "N/A")),
        ("Currency:", invoice_data.get("currency", "USD")),
    ]

    for label, value in details:
        page.insert_text(fitz.Point(40, y), label, fontsize=9, fontname="helv", color=light_gray)
        page.insert_text(fitz.Point(130, y), str(value), fontsize=9, fontname="helv", color=black)
        y += 18

    # Bill To (right side)
    page.insert_text(fitz.Point(380, 130), "Bill To:", fontsize=9, fontname="helv", color=light_gray)
    page.insert_text(fitz.Point(380, 148), "Client Corporation", fontsize=9, fontname="helv", color=black)
    page.insert_text(fitz.Point(380, 163), "123 Business Ave, Suite 400", fontsize=8, fontname="helv", color=light_gray)
    page.insert_text(fitz.Point(380, 176), "New York, NY 10001", fontsize=8, fontname="helv", color=light_gray)

    # Table header
    y = 240
    table_header_rect = fitz.Rect(30, y - 15, 565, y + 8)
    page.draw_rect(table_header_rect, color=None, fill=dark_blue)

    headers = [
        (35, "#"),
        (55, "Item Code"),
        (140, "Description"),
        (340, "Qty"),
        (390, "Unit Price"),
        (465, "Total"),
    ]

    for x, text in headers:
        page.insert_text(fitz.Point(x, y), text, fontsize=8, fontname="helv", color=white)

    y += 20

    # Line items
    for item in invoice_data["line_items"]:
        # Alternate row shading
        if item["line_number"] % 2 == 0:
            row_rect = fitz.Rect(30, y - 12, 565, y + 8)
            page.draw_rect(row_rect, color=None, fill=(0.97, 0.97, 0.98))

        page.insert_text(fitz.Point(38, y), str(item["line_number"]), fontsize=8, fontname="helv", color=black)
        page.insert_text(fitz.Point(55, y), str(item.get("item_code", "")), fontsize=7, fontname="helv", color=light_gray)
        page.insert_text(fitz.Point(140, y), item["description"][:35], fontsize=8, fontname="helv", color=black)
        page.insert_text(fitz.Point(340, y), str(item["quantity"]), fontsize=8, fontname="helv", color=black)
        page.insert_text(fitz.Point(390, y), f"${item['unit_price']:.2f}", fontsize=8, fontname="helv", color=black)
        page.insert_text(fitz.Point(465, y), f"${item['total']:.2f}", fontsize=8, fontname="helv", color=black)
        y += 22

    # Separator line
    y += 10
    page.draw_line(fitz.Point(350, y), fitz.Point(565, y), color=light_gray, width=0.5)
    y += 18

    # Totals
    totals = [
        ("Subtotal:", f"${invoice_data['subtotal']:.2f}"),
        ("Tax:", f"${invoice_data['tax']:.2f}"),
    ]

    for label, value in totals:
        page.insert_text(fitz.Point(390, y), label, fontsize=9, fontname="helv", color=light_gray)
        page.insert_text(fitz.Point(480, y), value, fontsize=9, fontname="helv", color=black)
        y += 18

    # Total (bold)
    total_rect = fitz.Rect(380, y - 12, 565, y + 8)
    page.draw_rect(total_rect, color=None, fill=dark_blue)
    page.insert_text(fitz.Point(390, y), "TOTAL:", fontsize=10, fontname="helv", color=white)
    page.insert_text(fitz.Point(470, y), f"${invoice_data['total']:.2f}", fontsize=11, fontname="helv", color=accent)

    # Footer
    y = 780
    page.insert_text(
        fitz.Point(40, y),
        "Payment Terms: Net 30 | Thank you for your business",
        fontsize=7,
        fontname="helv",
        color=light_gray,
    )

    doc.save(output_path)
    doc.close()
    print(f"Created: {output_path}")


def main():
    output_dir = Path(__file__).parent / "sample_data"
    output_dir.mkdir(exist_ok=True)

    # Invoice 1: Matches PO-2024-0042 with deliberate mismatches
    # - Price increase on bolts ($0.45 -> $0.48)
    # - Quantity decrease on bolts (500 -> 480)
    # - Tax overcharge ($31.60 -> $35.95)
    invoice_001 = {
        "invoice_number": "INV-88321",
        "vendor": "Acme Industrial Supplies",
        "date": "2024-12-02",
        "po_reference": "PO-2024-0042",
        "currency": "USD",
        "line_items": [
            {
                "line_number": 1,
                "item_code": "AIS-304-BOLT",
                "description": "SS Hex Bolt M10x50mm",
                "quantity": 480,
                "unit_price": 0.48,
                "unit": "EA",
                "total": 230.40,
            },
            {
                "line_number": 2,
                "item_code": "AIS-WASHER-10",
                "description": "Flat Washer M10 Zinc Plated",
                "quantity": 500,
                "unit_price": 0.12,
                "unit": "EA",
                "total": 60.00,
            },
            {
                "line_number": 3,
                "item_code": "AIS-NUT-M10",
                "description": "M10 Hex Nut Stainless",
                "quantity": 500,
                "unit_price": 0.22,
                "unit": "EA",
                "total": 110.00,
            },
        ],
        "subtotal": 400.40,
        "tax": 35.95,
        "total": 436.35,
    }

    # Invoice 2: Matches PO-2024-0087 with different mismatches
    # - Paper quantity over (50 -> 55 boxes)
    # - Toner price increase ($89.50 -> $94.99)
    # - Chair missing from invoice
    # - Extra line: "Delivery Surcharge"
    invoice_002 = {
        "invoice_number": "INV-90044",
        "vendor": "Global Office Solutions",
        "date": "2024-11-18",
        "po_reference": "PO-2024-0087",
        "currency": "USD",
        "line_items": [
            {
                "line_number": 1,
                "item_code": "GOS-PAPER-A4",
                "description": "A4 Copy Paper Premium 80gsm 5-Ream",
                "quantity": 55,
                "unit_price": 24.99,
                "unit": "BOX",
                "total": 1374.45,
            },
            {
                "line_number": 2,
                "item_code": "GOS-TONER-HP26A",
                "description": "HP 26A Black Toner CF226A",
                "quantity": 10,
                "unit_price": 94.99,
                "unit": "EA",
                "total": 949.90,
            },
            {
                "line_number": 3,
                "item_code": "GOS-DESK-SIT",
                "description": "Sit-Stand Adjustable Desk 60x30",
                "quantity": 5,
                "unit_price": 499.00,
                "unit": "EA",
                "total": 2495.00,
            },
            {
                "line_number": 4,
                "item_code": "GOS-DLVRY",
                "description": "Delivery and Setup Surcharge",
                "quantity": 1,
                "unit_price": 150.00,
                "unit": "EA",
                "total": 150.00,
            },
        ],
        "subtotal": 4969.35,
        "tax": 322.01,
        "total": 5291.36,
    }

    create_invoice_pdf(str(output_dir / "invoice_001.pdf"), invoice_001)
    create_invoice_pdf(str(output_dir / "invoice_002.pdf"), invoice_002)

    # Also save as PNG (render first page)
    for name in ["invoice_001", "invoice_002"]:
        pdf_path = output_dir / f"{name}.pdf"
        doc = fitz.open(str(pdf_path))
        page = doc[0]
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        pix.save(str(output_dir / f"{name}.png"))
        doc.close()
        print(f"Created: {output_dir / f'{name}.png'}")

    print("\nDone! Created invoice PDFs and PNGs in", output_dir)


if __name__ == "__main__":
    main()
