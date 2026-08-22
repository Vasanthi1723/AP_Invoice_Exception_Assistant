"""
Chat Engine: Provides grounded, source-cited answers about invoice exceptions.

The key design decision: the entire ComparisonResult JSON is injected into the
system prompt, so the LLM always has access to exact field values. The system
prompt explicitly instructs the LLM to cite specific source fields in every answer.
"""

from __future__ import annotations

import json
import logging

from google import genai
from google.genai import types

from backend.models.schemas import ChatMessage, ChatResponse, ComparisonResult

logger = logging.getLogger(__name__)


def _build_system_prompt(comparison: ComparisonResult) -> str:
    """
    Build a system prompt that injects the full comparison context.

    This is the grounding mechanism: by providing all raw data in the system
    prompt, we ensure the LLM can always cite specific fields and values.
    """
    # Serialize comparison to a clean JSON representation
    context_json = comparison.model_dump_json(indent=2)

    return f"""You are an AP (Accounts Payable) Invoice Exception Assistant. You help
invoice reviewers understand why invoices were flagged with exceptions.

You have access to the complete comparison data between an invoice and its
corresponding purchase order. This data is your ONLY source of truth.

CRITICAL RULES:
1. ALWAYS cite specific source fields and values in your answers.
   Example: "The unit price on Invoice line 1 is $0.48 (field: unit_price),
   while PO line 1 specifies $0.45 (field: unit_price), a difference of $0.03."
2. NEVER make up or assume data that isn't in the comparison context below.
3. When discussing exceptions, reference the exception_id (e.g., EXC-A1B2C3).
4. Format monetary values with $ and 2 decimal places.
5. Be concise but thorough. A reviewer should be able to act on your answer.
6. If asked about something not in the data, say so explicitly.
7. When explaining WHY something was flagged, trace the logic:
   "This was flagged because [field] on the invoice ([value]) differs from
   the PO ([value]) by [amount] ([percentage]%)."

COMPARISON DATA:
{context_json}

Answer the reviewer's questions based solely on this data."""


async def chat(
    message: str,
    comparison: ComparisonResult,
    history: list[ChatMessage],
    api_key: str,
) -> ChatResponse:
    """
    Process a chat message with grounded context from the comparison result.

    Args:
        message: The user's question
        comparison: Full comparison result for context grounding
        history: Previous chat messages in this conversation
        api_key: Google Gemini API key

    Returns:
        ChatResponse with the grounded answer and source citations
    """
    system_prompt = _build_system_prompt(comparison)

    # Build conversation history
    contents = []
    for msg in history:
        contents.append(types.Content(
            role="user" if msg.role == "user" else "model",
            parts=[types.Part.from_text(text=msg.content)],
        ))

    # Add current message
    contents.append(types.Content(
        role="user",
        parts=[types.Part.from_text(text=message)],
    ))

    # Call Gemini
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.3,
            max_output_tokens=2048,
        ),
    )

    reply_text = response.text.strip()

    # Extract citations from the reply (field references in the format field: value)
    citations = []
    # Look for patterns like "field 'X' = Y" or "field: X"
    import re
    citation_patterns = re.findall(
        r"(?:field[:\s]+['\"]?(\w+)['\"]?\s*[=:]\s*[\$]?[\d.]+)|"
        r"(?:PO line \d+|Invoice line \d+|PO field|Invoice field)",
        reply_text,
    )
    citations = list(set(citation_patterns))

    return ChatResponse(
        reply=reply_text,
        citations=citations,
    )
