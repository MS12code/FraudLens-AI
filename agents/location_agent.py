from prompts.prompts import LOCATION_PROMPT
from utils.helper import get_llm, parse_json_response
from schemas.state import InvestigationState

def run_location_agent(state: InvestigationState) -> dict:
    """
    Analyzes transaction country vs. home country and looks for impossible travel flags.
    """
    transaction_details = state.get("transaction_details", {})
    planner_notes = state.get("planner_notes", "")
    transaction_analysis = state.get("transaction_analysis", {})
    customer_analysis = state.get("customer_analysis", {})
    
    # Format and call LLM
    prompt = LOCATION_PROMPT.format(
        transaction_details=transaction_details,
        planner_notes=planner_notes,
        transaction_analysis=transaction_analysis,
        customer_analysis=customer_analysis
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
        "location_analysis": analysis,
        "current_step": "Merchant Risk Analysis"
    }
