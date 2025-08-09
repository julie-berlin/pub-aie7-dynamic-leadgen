"""Toolbelt assembly for agents.

Collects third-party tools and local tools (like RAG) into a single list that
graphs can bind to their language models.
"""
from __future__ import annotations
from typing import List
import os
from langchain_tavily import TavilySearch


def get_tool_belt() -> List:
    """Return the list of tools available to agents (Tavily, GoogleMaps."""
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        # Return empty list if Tavily is not configured
        return []
    
    tavily_tool = TavilySearch(
        tavily_api_key=tavily_api_key,
        max_results=5,  # Hard-coded default
        search_depth="basic",  # Hard-coded default
        include_domains=["akc.org", "breedmap.com"]  # Hard-coded defaults
    )

    # google_maps_tool = TODO

    return [tavily_tool] # TODO add google maps tool
