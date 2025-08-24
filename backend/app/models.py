"""Model utilities for constructing chat LLM clients.

Centralizes configuration of the default chat model and temperature so graphs can
import a single helper without repeating provider-specific wiring.
"""
from __future__ import annotations

import os
from typing import Any
from langchain_openai import ChatOpenAI


def get_chat_model(model_name: str | None = None, *, temperature: float = 0) -> Any:
    """Return a configured LangChain ChatOpenAI client.

    - model_name: optional override. If not provided, uses OPENAI_MODEL env var,
      falling back to "gpt-4.1-nano".
    - temperature: sampling temperature for the chat model (ignored for gpt-4.1-nano).

    Returns: a LangChain-compatible chat model instance.
    """
    name = model_name or os.environ.get("OPENAI_MODEL", "gpt-4.1-nano")

    # o4-mini doesn't support temperature parameter
    if name == "o4-mini":
        return ChatOpenAI(
            model=name,
            timeout=30,  # 30 second timeout to prevent hanging
            max_retries=2  # Retry failed requests
        )
    else:
        return ChatOpenAI(
            model=name,
            temperature=temperature,
            timeout=30,  # 30 second timeout to prevent hanging
            max_retries=2  # Retry failed requests
        )
