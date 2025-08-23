"""LLM model configuration for standalone testing."""

import os
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import logging

logger = logging.getLogger(__name__)

def get_chat_model(
    model_name: str = "o4-mini",
    temperature: float = 0.3,
    max_tokens: Optional[int] = None
):
    """Get configured chat model instance."""

    # Check for API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    if "gpt" in model_name.lower() and openai_key:
        return ChatOpenAI(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=openai_key
        )
    elif "claude" in model_name.lower() and anthropic_key:
        return ChatAnthropic(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=anthropic_key
        )
    else:
        # Default to GPT-3.5 if available
        if openai_key:
            logger.info(f"Model {model_name} not available, defaulting to gpt-3.5-turbo")
            return ChatOpenAI(
                model="o4-mini",
                temperature=temperature,
                max_tokens=max_tokens,
                api_key=openai_key
            )
        else:
            raise ValueError("No API keys found. Please set OPENAI_API_KEY or ANTHROPIC_API_KEY")
