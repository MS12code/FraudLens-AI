from prompts.prompts import TRANSACTION_PROMPT
from utils.helper import get_llm, parse_json_response
from schemas.state import InvestigationState

def run_transaction_agent(state: InvestigationState) -> dict:
    """
    Analyzes transaction amount, payment method, time, and merchant category for risk flags.
    """
    transaction_details = state.get("transaction_details", {})
    planner_notes = state.get("planner_notes", "")
    
    # Format and call LLM
    prompt = TRANSACTION_PROMPT.format(
        transaction_details=transaction_details,
        planner_notes=planner_notes
    )
    
    llm = get_llm()
    response = llm.invoke(prompt)
    
    # Parse json output
    parsed_response = parse_json_response(response.content)
    
    # Ensure correct keys
    analysis = {
        "observations": parsed_response.get("observations", []),
        "risks_identified": parsed_response.get("risks_identified", []),
        "risk_level": parsed_response.get("risk_level", "Low")
    }
    
    return {
        "transaction_analysis": analysis,
        "current_step": "Customer Behavior Analysis"
    }
