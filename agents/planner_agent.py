from prompts.prompts import PLANNER_PROMPT
from utils.helper import get_llm
from schemas.state import InvestigationState

def run_planner_agent(state: InvestigationState) -> dict:
    """
    Formulates an initial investigation checklist based on input transaction parameters.
    """
    transaction_details = state.get("transaction_details", {})
    
    # Prepare the prompt
    prompt = PLANNER_PROMPT.format(transaction_details=transaction_details)
    
    # Execute LLM call
    llm = get_llm()
    response = llm.invoke(prompt)
    
    return {
        "planner_notes": response.content.strip(),
        "current_step": "Transaction Analysis"
    }
