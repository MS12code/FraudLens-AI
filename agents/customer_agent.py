from prompts.prompts import CUSTOMER_PROMPT
from utils.helper import get_llm, parse_json_response
from schemas.state import InvestigationState

def run_customer_agent(state: InvestigationState) -> dict:
    """
    Analyzes transaction against customer spending averages, deviation, and history.
    """
    transaction_details = state.get("transaction_details", {})
    planner_notes = state.get("planner_notes", "")
    transaction_analysis = state.get("transaction_analysis", {})
    
    # Format and call LLM
    prompt = CUSTOMER_PROMPT.format(
        transaction_details=transaction_details,
        planner_notes=planner_notes,
        transaction_analysis=transaction_analysis
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
        "customer_analysis": analysis,
        "current_step": "Location Analysis"
    }
