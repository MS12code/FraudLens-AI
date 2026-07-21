import os
import streamlit as st
import datetime
from datetime import datetime as dt
import time
from dotenv import load_dotenv

# Set page configuration first
st.set_page_config(
    page_title="FraudLens AI - Credit Card Fraud Assistant",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import graph module (lazy import to ensure sys path handles it)
from graph.workflow import create_workflow

# Apply premium custom CSS for styling
st.markdown("""
<style>
    /* Premium Styling */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    .main-title {
        background: linear-gradient(135deg, #6366f1 0%, #3b82f6 50%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        margin-bottom: 2rem;
    }
    .badge {
        background: rgba(99, 102, 241, 0.15);
        color: #818cf8;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid rgba(99, 102, 241, 0.3);
        display: inline-block;
        margin-bottom: 1rem;
    }
    /* Card Styles */
    .metric-card {
        background-color: #1e293b;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        text-align: center;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        margin-top: 0.5rem;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    /* Risk Levels Cards */
    .risk-low {
        background-color: rgba(16, 185, 129, 0.1);
        border: 1px solid #10b981;
        color: #10b981 !important;
        padding: 1rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.2rem;
        text-align: center;
    }
    .risk-medium {
        background-color: rgba(245, 158, 11, 0.1);
        border: 1px solid #f59e0b;
        color: #f59e0b !important;
        padding: 1rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.2rem;
        text-align: center;
    }
    .risk-high {
        background-color: rgba(239, 68, 68, 0.1);
        border: 1px solid #ef4444;
        color: #ef4444 !important;
        padding: 1rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.2rem;
        text-align: center;
    }
    .section-card {
        background-color: #111827;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #1f2937;
        margin-bottom: 1rem;
    }
    .agent-header {
        font-weight: 700;
        color: #38bdf8;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    /* Sidebar customization */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SESSION STATE & DEFAULTS -----------------
defaults = {
    "amount": 250.00,
    "merchant_name": "Electronics Depot",
    "merchant_category": "Electronics",
    "transaction_country": "United States",
    "customer_home_country": "United States",
    "transaction_time": datetime.time(12, 0),
    "payment_method": "Online Credit Card",
    "average_spending": 100.00,
    "previous_fraud_history": "No",
    "card_present": "No",
    "groq_api_key": "",
    "model_name": "llama-3.3-70b-versatile"
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Callback to load preset values
def apply_preset():
    preset = st.session_state.selected_preset
    if preset == "Low-Risk Dining":
        st.session_state.amount = 32.50
        st.session_state.merchant_name = "Starbucks Coffee"
        st.session_state.merchant_category = "Dining"
        st.session_state.transaction_country = "United States"
        st.session_state.customer_home_country = "United States"
        st.session_state.transaction_time = datetime.time(8, 45)
        st.session_state.payment_method = "Digital Wallet"
        st.session_state.average_spending = 25.00
        st.session_state.previous_fraud_history = "No"
        st.session_state.card_present = "Yes"
    elif preset == "High-Risk Crypto":
        st.session_state.amount = 4500.00
        st.session_state.merchant_name = "CryptoWorld Exchange"
        st.session_state.merchant_category = "Electronics"
        st.session_state.transaction_country = "Russia"
        st.session_state.customer_home_country = "United States"
        st.session_state.transaction_time = datetime.time(3, 15)
        st.session_state.payment_method = "Online Credit Card"
        st.session_state.average_spending = 45.00
        st.session_state.previous_fraud_history = "No"
        st.session_state.card_present = "No"
    elif preset == "Impossible Travel":
        st.session_state.amount = 850.00
        st.session_state.merchant_name = "Berlin Tech Shop"
        st.session_state.merchant_category = "Electronics"
        st.session_state.transaction_country = "Germany"
        st.session_state.customer_home_country = "India"
        st.session_state.transaction_time = datetime.time(14, 20)
        st.session_state.payment_method = "In-Store Card (Swipe/Chip)"
        st.session_state.average_spending = 120.00
        st.session_state.previous_fraud_history = "Yes"
        st.session_state.card_present = "Yes"

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/shield.png", width=64)
    st.markdown("### FraudLens AI Settings")
    st.markdown("Configure the transaction metrics and agent attributes below.")
    
    # API Configurations
    st.markdown("---")
    st.markdown("**AI Agent Configuration**")
    
    # Check if a server-side secret / env key is configured
    has_server_key = bool(os.getenv("GROQ_API_KEY") or (hasattr(st, "secrets") and st.secrets.get("GROQ_API_KEY")))
    
    if has_server_key:
        st.caption("🔒 **API Key Status**: Loaded securely from Server Secrets")
        st.text_input("Override Groq API Key (Optional)", type="password", key="groq_api_key", help="Leave blank to use pre-configured server secrets.")
    else:
        st.text_input("Groq API Key", type="password", key="groq_api_key", help="Enter your Groq API Key (console.groq.com)")

    st.selectbox("LLM Model Selection", [
        "llama-3.3-70b-versatile",
        "llama-3.1-70b-versatile",
        "llama-3.3-70b-specdec",
        "llama3-8b-8192",
        "mixtral-8x7b-32768"
    ], key="model_name")
    
    # Presets Selector
    st.markdown("---")
    st.markdown("**Scenario Quick Presets**")
    st.selectbox("Load Sample Scenario", [
        "Custom Configuration",
        "Low-Risk Dining",
        "High-Risk Crypto",
        "Impossible Travel"
    ], key="selected_preset", on_change=apply_preset)

    st.markdown("---")
    st.markdown("**Transaction Parameters**")
    st.number_input("Transaction Amount ($)", min_value=0.01, step=10.0, key="amount")
    st.text_input("Merchant Name", key="merchant_name")
    st.selectbox("Merchant Category", ["Electronics", "Luxury Goods", "Travel", "Dining", "Online Retail", "Gambling/Casino", "Other"], key="merchant_category")
    
    countries_list = ["United States", "India", "Germany", "United Kingdom", "Canada", "Brazil", "Russia", "China", "Ukraine", "Romania"]
    st.selectbox("Transaction Country", countries_list, key="transaction_country")
    st.selectbox("Customer Home Country", countries_list, key="customer_home_country")
    st.time_input("Transaction Time", key="transaction_time")
    st.selectbox("Payment Method", ["Online Credit Card", "In-Store Card (Swipe/Chip)", "Digital Wallet", "Contactless"], key="payment_method")
    
    st.markdown("---")
    st.markdown("**Customer History**")
    st.number_input("Average Monthly Spending ($)", min_value=0.01, step=50.0, key="average_spending")
    st.radio("Previous Fraud History?", ["No", "Yes"], key="previous_fraud_history")
    st.radio("Card Physical Present?", ["Yes", "No"], key="card_present")

# ----------------- MAIN PAGE -----------------
st.markdown('<span class="badge">AGENTIC ORCHESTRATION</span>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">🕵️‍♂️ FraudLens AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">FraudLens AI - Agentic Credit Card Fraud Investigation Assistant powered by LangGraph & Groq LLMs</p>', unsafe_allow_html=True)

# Overview Columns
col_desc, col_graphic = st.columns([2, 1])
with col_desc:
    st.markdown("""
    ### How It Works
    FraudLens AI models a professional **Multi-Agent Fraud Desk** workflow. When you trigger an investigation:
    1. **Planner Agent** designs a tailored investigation blueprint.
    2. **Transaction Analysis Agent** searches the payment attributes for direct anomalies.
    3. **Customer Behavior Agent** validates the purchase against historical customer trends.
    4. **Location Agent** runs travel feasibility checks.
    5. **Merchant Agent** evaluates vendor category risks.
    6. **Fraud Decision Agent** synthesizes all observations to calculate scores and recommendations.
    7. **Report Generator Agent** compiles a structured markdown dossier.
    """)

with col_graphic:
    st.markdown("""
    <div style="background-color: #1e293b; padding: 1.5rem; border-radius: 12px; border: 1px solid #334155;">
        <h5 style="color: #38bdf8; margin-top:0;">Workflow Topology</h5>
        <div style="font-size: 0.85rem; color: #94a3b8; font-family: monospace;">
            START &rarr; Planner Agent<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&rarr; Transaction Analyst<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&rarr; Customer Behavior Analyst<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&rarr; Location Analyst<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&rarr; Merchant Risk Analyst<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&rarr; Decision Engine<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&rarr; Report Generator &rarr; END
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Main action button
btn_col1, btn_col2 = st.columns([1, 4])
with btn_col1:
    investigate = st.button("🔍 Investigate Transaction", type="primary", use_container_width=True)

if investigate:
    # Set env var dynamically if input in sidebar
    if st.session_state.groq_api_key:
        os.environ["GROQ_API_KEY"] = st.session_state.groq_api_key
        
    # Check key before running
    has_key = bool(st.session_state.groq_api_key or os.getenv("GROQ_API_KEY") or (hasattr(st, "secrets") and st.secrets.get("GROQ_API_KEY")))
    if not has_key:
        st.error("⚠️ Groq API Key is missing. Please paste it in the sidebar configuration to continue.")
    else:
        # Save configured model name to env for helper
        os.environ["GROQ_MODEL"] = st.session_state.model_name
        
        # Build inputs dict
        inputs = {
            "amount": st.session_state.amount,
            "merchant_name": st.session_state.merchant_name,
            "merchant_category": st.session_state.merchant_category,
            "transaction_country": st.session_state.transaction_country,
            "customer_home_country": st.session_state.customer_home_country,
            "transaction_time": st.session_state.transaction_time.strftime("%H:%M"),
            "payment_method": st.session_state.payment_method,
            "average_spending": st.session_state.average_spending,
            "previous_fraud_history": st.session_state.previous_fraud_history,
            "card_present": st.session_state.card_present
        }
        
        st.markdown("### ⚙️ Orchestration Live Execution")
        
        # Setup workflow and stream
        workflow = create_workflow()
        
        initial_state = {
            "transaction_details": inputs,
            "planner_notes": "",
            "transaction_analysis": {},
            "customer_analysis": {},
            "location_analysis": {},
            "merchant_analysis": {},
            "fraud_decision": {},
            "final_report": "",
            "current_step": "Planner"
        }
        
        # Status box container
        status_box = st.status("Initializing Investigation Graph...", expanded=True)
        
        accumulated_state = initial_state.copy()
        
        # Visual timelines mapping
        agent_names = {
            "planner": "📋 Planner Agent",
            "transaction": "💳 Transaction Analysis Agent",
            "customer": "👤 Customer Behavior Agent",
            "location": "🗺️ Location Analysis Agent",
            "merchant": "🏪 Merchant Risk Agent",
            "decision": "⚖️ Fraud Decision Agent",
            "report": "📄 Report Generation Agent"
        }
        
        try:
            # Execute LangGraph and update state dynamically
            for event in workflow.stream(initial_state):
                for node_name, output_dict in event.items():
                    accumulated_state.update(output_dict)
                    display_name = agent_names.get(node_name, node_name.capitalize())
                    status_box.write(f"✔️ **{display_name}** complete. Updated Graph state.")
                    time.sleep(0.5) # subtle animation lag
            
            status_box.update(label="Graph Execution Finished Successfully!", state="complete", expanded=False)
            
            # ----------------- DISPLAY METRICS -----------------
            decision = accumulated_state.get("fraud_decision", {})
            score = decision.get("fraud_score", 0)
            level = decision.get("risk_level", "Low")
            conf = decision.get("confidence", 0)
            action = decision.get("recommended_action", "Approve")
            
            st.markdown("## 📊 Investigation Metrics")
            
            m_col1, m_col2, m_col3, m_col4 = st.columns(4)
            
            with m_col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Fraud Risk Score</div>
                    <div class="metric-value" style="color: #3b82f6;">{score}/100</div>
                </div>
                """, unsafe_allow_html=True)
                
            with m_col2:
                # Highlight level card
                style_cls = "risk-low" if level == "Low" else ("risk-medium" if level == "Medium" else "risk-high")
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Risk Level Classification</div>
                    <div style="margin-top:0.75rem;" class="{style_cls}">{level.upper()} RISK</div>
                </div>
                """, unsafe_allow_html=True)
                
            with m_col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Orchestrator Confidence</div>
                    <div class="metric-value" style="color: #10b981;">{conf}%</div>
                </div>
                """, unsafe_allow_html=True)
                
            with m_col4:
                # Color recommendations
                rec_color = "#10b981" if action == "Approve" else ("#f59e0b" if action == "Escalate for Manual Review" else "#ef4444")
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Recommended Action</div>
                    <div class="metric-value" style="color: {rec_color}; font-size:1.8rem; margin-top:0.9rem;">{action}</div>
                </div>
                """, unsafe_allow_html=True)
                
            # ----------------- DISPLAY TABS -----------------
            st.markdown("---")
            st.markdown("## 🔎 Detailed Case File & Dossier")
            
            tab_report, tab_findings, tab_planner = st.tabs([
                "📄 Investigation Report", 
                "🕵️ Agent-by-Agent Findings", 
                "📋 Planner Blueprint"
            ])
            
            with tab_report:
                st.markdown(accumulated_state.get("final_report", "No report generated."))
                
            with tab_findings:
                st.markdown("### Intermediate Analysis Outputs")
                
                f_col1, f_col2 = st.columns(2)
                
                with f_col1:
                    # Transaction Analyst
                    t_analysis = accumulated_state.get("transaction_analysis", {})
                    st.markdown(f"""
                    <div class="section-card">
                        <div class="agent-header">💳 Transaction Analysis Agent (Risk: {t_analysis.get('risk_level', 'Low')})</div>
                        <b>Key Observations:</b>
                        <ul>
                            {"".join([f"<li>{obs}</li>" for obs in t_analysis.get('observations', [])])}
                        </ul>
                        <b>Risks Identified:</b>
                        <ul>
                            {"".join([f"<li>{r}</li>" for r in t_analysis.get('risks_identified', [])])}
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Location Analyst
                    l_analysis = accumulated_state.get("location_analysis", {})
                    st.markdown(f"""
                    <div class="section-card">
                        <div class="agent-header">🗺️ Location Analysis Agent (Risk: {l_analysis.get('risk_level', 'Low')})</div>
                        <b>Key Observations:</b>
                        <ul>
                            {"".join([f"<li>{obs}</li>" for obs in l_analysis.get('observations', [])])}
                        </ul>
                        <b>Risks Identified:</b>
                        <ul>
                            {"".join([f"<li>{r}</li>" for r in l_analysis.get('risks_identified', [])])}
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with f_col2:
                    # Customer Analyst
                    c_analysis = accumulated_state.get("customer_analysis", {})
                    st.markdown(f"""
                    <div class="section-card">
                        <div class="agent-header">👤 Customer Behavior Agent (Risk: {c_analysis.get('risk_level', 'Low')})</div>
                        <b>Key Observations:</b>
                        <ul>
                            {"".join([f"<li>{obs}</li>" for obs in c_analysis.get('observations', [])])}
                        </ul>
                        <b>Risks Identified:</b>
                        <ul>
                            {"".join([f"<li>{r}</li>" for r in c_analysis.get('risks_identified', [])])}
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Merchant Analyst
                    m_analysis = accumulated_state.get("merchant_analysis", {})
                    st.markdown(f"""
                    <div class="section-card">
                        <div class="agent-header">🏪 Merchant Risk Agent (Risk: {m_analysis.get('risk_level', 'Low')})</div>
                        <b>Key Observations:</b>
                        <ul>
                            {"".join([f"<li>{obs}</li>" for obs in m_analysis.get('observations', [])])}
                        </ul>
                        <b>Risks Identified:</b>
                        <ul>
                            {"".join([f"<li>{r}</li>" for r in m_analysis.get('risks_identified', [])])}
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
            
            with tab_planner:
                st.markdown("### Investigation Planner Blueprint")
                st.markdown(accumulated_state.get("planner_notes", "No blueprint generated."))
                
        except Exception as e:
            st.error(f"An error occurred during workflow execution: {e}")
            st.info("Check your API key validity, internet connection, and available models.")
