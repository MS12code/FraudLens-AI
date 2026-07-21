from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

class TransactionDetails(BaseModel):
    amount: float = Field(description="Transaction amount in USD")
    merchant_name: str = Field(description="Name of the merchant")
    merchant_category: str = Field(description="Merchant category code or descriptor (e.g., Electronics, Travel, Dining)")
    transaction_country: str = Field(description="Country where the transaction is initiated")
    customer_home_country: str = Field(description="Billing or home country of the customer")
    transaction_time: str = Field(description="Time of day in HH:MM format")
    payment_method: str = Field(description="Payment mechanism used (e.g., Online, In-Store Credit Card, Digital Wallet)")
    average_spending: float = Field(description="The customer's average historical transaction amount in USD")
    previous_fraud_history: str = Field(description="Whether the customer has history of fraud: 'Yes' or 'No'")
    card_present: str = Field(description="Whether the physical card was present for the transaction: 'Yes' or 'No'")

class AgentAnalysis(BaseModel):
    observations: List[str] = Field(default_factory=list, description="Key notes and observations identified during analysis")
    risks_identified: List[str] = Field(default_factory=list, description="Specific risk indicators or red flags identified")
    risk_level: str = Field(default="Low", description="Overall risk level assessed by this agent: Low, Medium, High")

class FraudDecision(BaseModel):
    fraud_score: int = Field(description="Final fraud risk score from 0 to 100")
    risk_level: str = Field(description="Final risk level classification: Low, Medium, or High")
    confidence: int = Field(description="Confidence level in the decision from 0 to 100")
    recommended_action: str = Field(description="Recommended resolution: Approve, Decline, or Escalate for Manual Review")
    reasoning: List[str] = Field(default_factory=list, description="Bullet points explaining the final determination")

class InvestigationState(TypedDict):
    transaction_details: Dict[str, Any]
    planner_notes: str
    transaction_analysis: Dict[str, Any]
    customer_analysis: Dict[str, Any]
    location_analysis: Dict[str, Any]
    merchant_analysis: Dict[str, Any]
    fraud_decision: Dict[str, Any]
    final_report: str
    current_step: str
