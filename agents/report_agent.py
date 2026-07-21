from prompts.prompts import REPORT_PROMPT
from utils.helper import get_llm
from schemas.state import InvestigationState

def run_report_agent(state: InvestigationState) -> dict:
    """
    Generates a professional markdown report summarizing findings from all agents.
    """
    transaction_details = state.get("transaction_details", {})
    planner_notes = state.get("planner_notes", "")
    transaction_analysis = state.get("transaction_analysis", {})
    customer_analysis = state.get("customer_analysis", {})
    location_analysis = state.get("location_analysis", {})
    merchant_analysis = state.get("merchant_analysis", {})
    fraud_decision = state.get("fraud_decision", {})
    
    # Format and call LLM
    prompt = REPORT_PROMPT.format(
        transaction_details=transaction_details,
        planner_notes=planner_notes,
        transaction_analysis=transaction_analysis,
        customer_analysis=customer_analysis,
        location_analysis=location_analysis,
        merchant_analysis=merchant_analysis,
        fraud_decision=fraud_decision
    )
    
    llm = get_llm()
    response = llm.invoke(prompt)
    
    return {
        "final_report": response.content.strip(),
        "current_step": "Complete"
    }
