from langgraph.graph import StateGraph, START, END
from schemas.state import InvestigationState
from agents.planner_agent import run_planner_agent
from agents.transaction_agent import run_transaction_agent
from agents.customer_agent import run_customer_agent
from agents.location_agent import run_location_agent
from agents.merchant_agent import run_merchant_agent
from agents.decision_agent import run_decision_agent
from agents.report_agent import run_report_agent

def create_workflow():
    """
    Constructs the sequential Agentic AI workflow for fraud investigation.
    """
    # Initialize the graph with the state schema
    workflow = StateGraph(InvestigationState)
    
    # Add Nodes
    workflow.add_node("planner", run_planner_agent)
    workflow.add_node("transaction", run_transaction_agent)
    workflow.add_node("customer", run_customer_agent)
    workflow.add_node("location", run_location_agent)
    workflow.add_node("merchant", run_merchant_agent)
    workflow.add_node("decision", run_decision_agent)
    workflow.add_node("report", run_report_agent)
    
    # Define sequential edges
    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "transaction")
    workflow.add_edge("transaction", "customer")
    workflow.add_edge("customer", "location")
    workflow.add_edge("location", "merchant")
    workflow.add_edge("merchant", "decision")
    workflow.add_edge("decision", "report")
    workflow.add_edge("report", END)
    
    return workflow.compile()
