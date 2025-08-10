"""Lead Intelligence Supervisor V2 - Advanced lead analysis with tool integration."""

from __future__ import annotations
from typing import Dict, Any, List, Optional
import json
import logging
from datetime import datetime

from .base_supervisor import SupervisorAgent, SupervisorDecision
from ...state import SurveyState
from ...tools import get_tool_belt

logger = logging.getLogger(__name__)


class LeadIntelligenceSupervisor(SupervisorAgent):
    """Supervisor for intelligent lead analysis and tool-assisted validation."""
    
    def __init__(self, **kwargs):
        super().__init__(
            name="LeadIntelligenceSupervisor",
            model_name="gpt-4o-mini",
            temperature=0.1,
            max_tokens=3000,
            timeout_seconds=60,
            **kwargs
        )
        
        # Initialize tools
        self.tools = get_tool_belt()
        
    def get_system_prompt(self) -> str:
        """System prompt for lead intelligence decisions."""
        return """You are the Lead Intelligence Supervisor for an advanced lead qualification system.

Your role is to analyze lead quality, validate responses using external tools when needed, and make final qualification decisions.

CORE RESPONSIBILITIES:
1. Analyze all user responses for lead qualification patterns
2. Decide when external validation is needed (Tavily search, Google Maps)
3. Validate mathematical lead scores against business logic
4. Make final lead classification decisions (qualified/maybe/no/continue)
5. Provide detailed reasoning and confidence assessments

TOOL USAGE DECISIONS:
- Use Tavily search for: Industry research, service validation, competitive analysis
- Use Google Maps for: Distance calculations, service area validation, location verification
- Use tools strategically - not for every lead, only when validation adds value

LEAD CLASSIFICATION LOGIC:
- QUALIFIED: High score + high confidence + passes business requirements
- MAYBE: Borderline score OR low confidence OR missing critical info
- NO: Low score + high confidence OR fails required criteria  
- CONTINUE: Insufficient data, need more questions

OUTPUT FORMAT:
Always respond with valid JSON:
{
  "action": "validate_with_tools" | "score_only" | "continue_survey",
  "tools_needed": ["tavily_search", "google_maps"] | [],
  "tool_queries": {
    "tavily_search": "specific search query",
    "google_maps": {"origin": "address", "destination": "address"}
  },
  "reasoning": "detailed analysis of why tools are/aren't needed",
  "confidence": 0.0-1.0,
  "preliminary_classification": "qualified" | "maybe" | "no" | "continue"
}

Be strategic about tool usage - only use when external validation significantly improves decision quality."""

    def make_decision(self, state: SurveyState, context: Dict[str, Any] = None) -> SupervisorDecision:
        """Analyze lead and decide on tool usage and validation strategy."""
        try:
            # Extract state information
            responses = state.get("all_responses", [])
            calculated_score = state.get("calculated_score", 0)
            client_info = state.get("client_info", {})
            business_rules = state.get("business_rules", {})
            form_config = state.get("form_config", {})
            
            if not responses:
                return SupervisorDecision(
                    decision="continue_survey",
                    reasoning="No responses yet to analyze",
                    confidence=1.0,
                    metadata={"action": "continue_survey"}
                )
            
            # Analyze responses for tool needs
            tool_analysis = self._analyze_tool_requirements(responses, client_info, business_rules)
            
            # Prepare LLM prompt
            user_message = {
                "role": "user",
                "content": f"""Analyze this lead and determine validation strategy:

LEAD DATA:
- Calculated Score: {calculated_score}/100
- Responses Count: {len(responses)}
- Business: {client_info.get('business_name', 'Unknown')} ({client_info.get('industry', 'Unknown')})
- Service Area: {client_info.get('service_area', 'Not specified')}

RECENT RESPONSES:
{json.dumps(responses[-5:], indent=2)}

BUSINESS RULES:
{json.dumps(business_rules, indent=2)}

TOOL ANALYSIS:
{json.dumps(tool_analysis, indent=2)}

Decide if external validation tools would improve the accuracy of lead qualification for this specific case."""
            }
            
            # Get LLM decision
            llm_response = self.invoke_llm([user_message])
            
            # Parse response
            if isinstance(llm_response, str):
                decision_data = json.loads(llm_response)
            else:
                decision_data = llm_response
            
            # Create supervisor decision
            decision = SupervisorDecision(
                decision=decision_data.get("action", "score_only"),
                reasoning=decision_data.get("reasoning", "Lead intelligence analysis"),
                confidence=decision_data.get("confidence", 0.7),
                recommendations=decision_data.get("tools_needed", []),
                metadata={
                    "tools_needed": decision_data.get("tools_needed", []),
                    "tool_queries": decision_data.get("tool_queries", {}),
                    "preliminary_classification": decision_data.get("preliminary_classification", "continue"),
                    "tool_analysis": tool_analysis,
                    "score_analyzed": calculated_score
                }
            )
            
            # Store in history
            self.decision_history.append(decision)
            
            logger.info(f"Lead Intelligence decision: {decision.decision} (confidence: {decision.confidence})")
            return decision
            
        except Exception as e:
            logger.error(f"Lead Intelligence Supervisor error: {e}")
            # Fallback decision
            return SupervisorDecision(
                decision="score_only",
                reasoning=f"Fallback due to error: {str(e)}",
                confidence=0.3,
                recommendations=[],
                metadata={"error": str(e), "fallback": True}
            )
    
    def _analyze_tool_requirements(self, responses: List[Dict], client_info: Dict, business_rules: Dict) -> Dict[str, Any]:
        """Analyze if specific tools would be valuable for this lead."""
        analysis = {
            "tavily_recommended": False,
            "maps_recommended": False,
            "tavily_reasons": [],
            "maps_reasons": []
        }
        
        # Analyze for Tavily search needs
        business_type = client_info.get('industry', '').lower()
        
        # Check if we need industry/service validation
        if any(keyword in business_type for keyword in ['pet', 'dog', 'animal']):
            # Look for breed mentions in responses
            for response in responses:
                answer = response.get('answer', '').lower()
                if any(breed_word in answer for breed_word in ['breed', 'dog', 'puppy', 'aggressive', 'bite']):
                    analysis["tavily_recommended"] = True
                    analysis["tavily_reasons"].append("Breed safety validation needed")
                    break
        
        if 'real estate' in business_type or 'property' in business_type:
            for response in responses:
                answer = response.get('answer', '').lower()
                if any(term in answer for term in ['market', 'price', 'value', 'investment']):
                    analysis["tavily_recommended"] = True
                    analysis["tavily_reasons"].append("Market research validation")
                    break
        
        # Analyze for Google Maps needs
        service_area = client_info.get('service_area', '')
        user_location = None
        
        # Look for location mentions in responses
        for response in responses:
            answer = response.get('answer', '').lower()
            if any(loc_word in answer for loc_word in ['address', 'location', 'zip', 'area', 'neighborhood']):
                user_location = response.get('answer', '')
                break
        
        if service_area and user_location and len(user_location.strip()) > 5:
            analysis["maps_recommended"] = True
            analysis["maps_reasons"].append("Service area distance validation needed")
        
        return analysis


def lead_intelligence_supervisor_node(state: SurveyState) -> Dict[str, Any]:
    """Node function for Lead Intelligence Supervisor."""
    supervisor = LeadIntelligenceSupervisor()
    
    # Make tool usage decision
    decision = supervisor.make_decision(state)
    
    # Execute tools if recommended
    tool_results = {}
    if decision.decision == "validate_with_tools":
        tool_results = _execute_recommended_tools(decision.metadata, state)
    
    return {
        "lead_intel_decision": decision.to_dict(),
        "tool_results": tool_results,
        "tools_executed": list(tool_results.keys()),
        "supervisor_metadata": {
            "supervisor_name": supervisor.name,
            "model_used": supervisor.model_name,
            "decision_timestamp": decision.timestamp
        }
    }


def _execute_recommended_tools(decision_metadata: Dict, state: SurveyState) -> Dict[str, Any]:
    """Execute the tools recommended by the supervisor."""
    tool_results = {}
    tools_needed = decision_metadata.get("tools_needed", [])
    tool_queries = decision_metadata.get("tool_queries", {})
    
    try:
        # Execute Tavily search if needed
        if "tavily_search" in tools_needed and "tavily_search" in tool_queries:
            query = tool_queries["tavily_search"]
            logger.info(f"Executing Tavily search: {query}")
            
            # Import and use Tavily tool
            from langchain_tavily import TavilySearchResults
            tavily = TavilySearchResults(max_results=3)
            
            search_results = tavily.run(query)
            tool_results["tavily_search"] = {
                "query": query,
                "results": search_results,
                "executed_at": datetime.now().isoformat()
            }
        
        # Execute Google Maps if needed
        if "google_maps" in tools_needed and "google_maps" in tool_queries:
            maps_query = tool_queries["google_maps"]
            logger.info(f"Executing Google Maps query: {maps_query}")
            
            # For now, simulate Maps API call (implement actual API later)
            tool_results["google_maps"] = {
                "query": maps_query,
                "distance": "12.5 miles",
                "duration": "18 minutes",
                "in_service_area": True,
                "executed_at": datetime.now().isoformat(),
                "simulated": True  # Remove when real API implemented
            }
        
    except Exception as e:
        logger.error(f"Tool execution error: {e}")
        tool_results["error"] = str(e)
    
    return tool_results