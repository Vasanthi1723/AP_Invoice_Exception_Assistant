"""
Line-item matcher: fuzzy-matches invoice lines to PO lines.

Uses item_code (exact match priority) and description (fuzzy match fallback)
to pair each invoice line with the best matching PO line.
"""

from __future__ import annotations

from dataclasses import dataclass

from thefuzz import fuzz

from backend.models.schemas import InvoiceLineItem, POLineItem


@dataclass
class MatchResult:
    """Result of matching a single invoice line to a PO line."""
    po_line: POLineItem
    invoice_line: InvoiceLineItem
    confidence: float  # 0.0 - 1.0
    matched_by: str  # 'item_code' | 'description' | 'none'


def _code_match_score(po_code: str, inv_code: str | None) -> float:
    """Exact item-code match returns 1.0, otherwise 0.0."""
    if not inv_code:
        return 0.0
    return 1.0 if po_code.strip().upper() == inv_code.strip().upper() else 0.0


def _description_match_score(po_desc: str, inv_desc: str) -> float:
    """
    Fuzzy description match using token-sort ratio.
    Returns a score between 0.0 and 1.0.
    """
    score = fuzz.token_sort_ratio(po_desc.lower(), inv_desc.lower())
    return score / 100.0


def match_line_items(
    po_lines: list[POLineItem],
    invoice_lines: list[InvoiceLineItem],
    code_match_threshold: float = 1.0,
    description_match_threshold: float = 0.55,
) -> tuple[list[MatchResult], list[POLineItem], list[InvoiceLineItem]]:
    """
    Match invoice lines to PO lines.

    Strategy:
      1. First pass: match by exact item_code
      2. Second pass: match remaining by fuzzy description
      3. Return unmatched lines on both sides

    Args:
        po_lines: List of PO line items
        invoice_lines: List of invoice line items
        code_match_threshold: Minimum score for code match (default 1.0 = exact)
        description_match_threshold: Minimum fuzzy score for description match

    Returns:
        Tuple of (matched pairs, unmatched PO lines, unmatched invoice lines)
    """
    matches: list[MatchResult] = []
    remaining_po = list(po_lines)
    remaining_inv = list(invoice_lines)

    # --- Pass 1: exact item-code matching ---
    matched_po_indices = set()
    matched_inv_indices = set()

    for i, inv_line in enumerate(remaining_inv):
        if not inv_line.item_code:
            continue
        for j, po_line in enumerate(remaining_po):
            if j in matched_po_indices:
                continue
            score = _code_match_score(po_line.item_code, inv_line.item_code)
            if score >= code_match_threshold:
                matches.append(MatchResult(
                    po_line=po_line,
                    invoice_line=inv_line,
                    confidence=score,
                    matched_by="item_code",
                ))
                matched_po_indices.add(j)
                matched_inv_indices.add(i)
                break

    # Remove matched items
    remaining_po = [l for i, l in enumerate(remaining_po) if i not in matched_po_indices]
    remaining_inv = [l for i, l in enumerate(remaining_inv) if i not in matched_inv_indices]

    # --- Pass 2: fuzzy description matching ---
    matched_po_indices = set()
    matched_inv_indices = set()

    for i, inv_line in enumerate(remaining_inv):
        best_score = 0.0
        best_j = -1
        for j, po_line in enumerate(remaining_po):
            if j in matched_po_indices:
                continue
            score = _description_match_score(po_line.description, inv_line.description)
            if score > best_score:
                best_score = score
                best_j = j

        if best_j >= 0 and best_score >= description_match_threshold:
            matches.append(MatchResult(
                po_line=remaining_po[best_j],
                invoice_line=inv_line,
                confidence=best_score,
                matched_by="description",
            ))
            matched_po_indices.add(best_j)
            matched_inv_indices.add(i)

    unmatched_po = [l for i, l in enumerate(remaining_po) if i not in matched_po_indices]
    unmatched_inv = [l for i, l in enumerate(remaining_inv) if i not in matched_inv_indices]

    return matches, unmatched_po, unmatched_inv
