from prompts.prompts import MERCHANT_PROMPT
from utils.helper import get_llm, parse_json_response
from schemas.state import InvestigationState

def run_merchant_agent(state: InvestigationState) -> dict:
    """
    Analyzes merchant category, reputation, and online risk indicators.
    """
    transaction_details = state.get("transaction_details", {})
    planner_notes = state.get("planner_notes", "")
    location_analysis = state.get("location_analysis", {})
    
    # Format and call LLM
    prompt = MERCHANT_PROMPT.format(
        transaction_details=transaction_details,
        planner_notes=planner_notes,
        location_analysis=location_analysis
    )
    
    llm = get_llm()
    response = llm.invoke(prompt)
    
    # Parse JSON
    parsed_response = parse_json_response(response.content)
    
    analysis = {
        "observations": parsed_response.get("observations", []),
        "risks_identified": parsed_response.get("risks_identified", []),
        "risk_level": parsed_response.get("risk_level", "Low")
    }
    
    return {
        "merchant_analysis": analysis,
        "current_step": "Fraud Decision"
    }
