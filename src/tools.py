"""Toolbelt assembly for agents.

Collects third-party tools and local tools (like RAG) into a single list that
graphs can bind to their language models.
"""
from __future__ import annotations
from typing import List
from langchain_tavily import TavilySearch


def get_tool_belt() -> List:
    """Return the list of tools available to agents (Tavily, GoogleMaps."""
    tavily_tool = TavilySearch(
            tavily_api_key=settings.tavily_api_key,
            max_results=settings.tavily_max_results,
            search_depth=settings.tavily_search_depth,
            include_domains=settings.tavily_include_domains # ["akc.org", "breedmap.com"]
        )

    # google_maps_tool = TODO

    return [tavily_tool] # TODO add google maps tool
