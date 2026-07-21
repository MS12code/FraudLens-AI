from prompts.prompts import DECISION_PROMPT
from utils.helper import get_llm, parse_json_response
from schemas.state import InvestigationState

def run_decision_agent(state: InvestigationState) -> dict:
    """
    Synthesizes analysis from all specialists and makes a final decision on the transaction risk.
    """
    transaction_analysis = state.get("transaction_analysis", {})
    customer_analysis = state.get("customer_analysis", {})
    location_analysis = state.get("location_analysis", {})
    merchant_analysis = state.get("merchant_analysis", {})
    
    # Format and call LLM
    prompt = DECISION_PROMPT.format(
        transaction_analysis=transaction_analysis,
        customer_analysis=customer_analysis,
        location_analysis=location_analysis,
        merchant_analysis=merchant_analysis
    )
    
    llm = get_llm()
    response = llm.invoke(prompt)
    
    # Parse JSON
    parsed_response = parse_json_response(response.content)
    
    decision = {
        "fraud_score": parsed_response.get("fraud_score", 0),
        "risk_level": parsed_response.get("risk_level", "Low"),
        "confidence": parsed_response.get("confidence", 0),
        "recommended_action": parsed_response.get("recommended_action", "Approve"),
        "reasoning": parsed_response.get("reasoning", [])
    }
    
    return {
        "fraud_decision": decision,
        "current_step": "Report Generation"
    }
