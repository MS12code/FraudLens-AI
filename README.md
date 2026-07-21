<div align="center">

# 🕵️‍♂️ FraudLens AI

### Agentic Credit Card Fraud Investigation Assistant

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Streamlit_Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://fraudlens-ai-ak89vufd3rvoe94xlaapdu.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.2-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![Groq](https://img.shields.io/badge/Groq-Llama_3.3-F55036?style=for-the-badge)](https://groq.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

<br/>

**FraudLens AI** is a multi-agent fraud investigation system powered by LangGraph and Groq's Llama 3.3. It simulates a professional fraud analyst desk — seven specialized AI agents collaborate sequentially to evaluate a transaction and produce an executive-ready investigation report.

<br/>

👉 **[🌐 Launch Live Application](https://fraudlens-ai-ak89vufd3rvoe94xlaapdu.streamlit.app/)** 👈

</div>

---

## 🧠 What is FraudLens AI?

Traditional fraud systems rely on rigid rule-based logic — they lack the contextual reasoning a human fraud analyst applies. FraudLens AI bridges that gap by orchestrating a team of specialized LLM agents, each responsible for a specific domain of fraud detection:

- **Is the transaction amount unusual for this customer?**
- **Was this transaction physically possible given the customer's location?**
- **Does the merchant have a high-risk profile?**
- **What is the overall fraud probability?**

All findings are synthesized into a structured investigation report with a fraud score, risk level, and clear recommendation.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 **7-Agent Pipeline** | Planner → Transaction → Customer → Location → Merchant → Decision → Report |
| 📊 **Fraud Scoring** | Composite 0–100 fraud risk score with confidence percentage |
| 🎭 **3 Quick Presets** | Load "Low-Risk Dining", "High-Risk Crypto", or "Impossible Travel" in one click |
| ⚡ **Live Agent Feed** | Watch each LangGraph node complete in real time |
| 📄 **Investigation Report** | Executive-ready markdown dossier with case file table and findings |
| 🎨 **Premium Dark UI** | Custom dark slate theme with glassmorphism cards and color-coded risk levels |
| 🔑 **Flexible API Key** | Works with `.env`, Streamlit sidebar input, or Streamlit Cloud secrets |

---

## 🏗️ Architecture

```
                        ┌─────────────────────┐
                        │    User Input        │
                        │  (Streamlit UI)      │
                        └──────────┬──────────┘
                                   │
                              ┌────▼────┐
                              │ START   │
                              └────┬────┘
                                   │
                     ┌─────────────▼─────────────┐
                     │       Planner Agent        │
                     │  Maps the investigation    │
                     └─────────────┬─────────────┘
                                   │
                     ┌─────────────▼─────────────┐
                     │  Transaction Analysis      │
                     │  Amount · Time · Method    │
                     └─────────────┬─────────────┘
                                   │
                     ┌─────────────▼─────────────┐
                     │  Customer Behavior         │
                     │  Spending · History        │
                     └─────────────┬─────────────┘
                                   │
                     ┌─────────────▼─────────────┐
                     │  Location Analysis         │
                     │  Country · Travel Check    │
                     └─────────────┬─────────────┘
                                   │
                     ┌─────────────▼─────────────┐
                     │  Merchant Risk             │
                     │  Category · Reputation     │
                     └─────────────┬─────────────┘
                                   │
                     ┌─────────────▼─────────────┐
                     │  Fraud Decision Engine     │
                     │  Score · Level · Action    │
                     └─────────────┬─────────────┘
                                   │
                     ┌─────────────▼─────────────┐
                     │  Report Generator          │
                     │  Executive Dossier         │
                     └─────────────┬─────────────┘
                                   │
                              ┌────▼────┐
                              │  END    │
                              └─────────┘
```

### Agent Responsibilities

| Agent | Role |
|---|---|
| **Planner** | Parses inputs, drafts the investigation checklist |
| **Transaction Analyst** | Flags amount anomalies, risky hours, suspicious payment methods |
| **Customer Behavior** | Compares spend vs. average, checks fraud history |
| **Location Analyst** | Detects impossible travel, foreign card-present transactions |
| **Merchant Risk** | Evaluates high-risk categories (crypto, luxury, gambling) |
| **Decision Engine** | Synthesizes all findings → Fraud Score + Action |
| **Report Generator** | Produces structured markdown case file |

---

## 🛠️ Tech Stack

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.12+ | Core language |
| Streamlit | 1.59 | Web dashboard UI |
| LangGraph | 1.2 | Agent orchestration (StateGraph) |
| LangChain | 1.3 | LLM integration layer |
| langchain-groq | 1.1 | Groq API client |
| Groq / Llama 3.3 | 70B | LLM backbone |
| Pydantic | 2.x | State & schema validation |
| python-dotenv | 1.x | Local environment config |

---

## 📁 Project Structure

```
FraudLens-AI/
│
├── app.py                    # Streamlit dashboard (main entry point)
│
├── agents/                   # Individual agent node implementations
│   ├── planner_agent.py
│   ├── transaction_agent.py
│   ├── customer_agent.py
│   ├── location_agent.py
│   ├── merchant_agent.py
│   ├── decision_agent.py
│   └── report_agent.py
│
├── graph/
│   └── workflow.py           # LangGraph StateGraph construction
│
├── schemas/
│   └── state.py              # TypedDict state + Pydantic models
│
├── prompts/
│   └── prompts.py            # System prompts for all 7 agents
│
├── utils/
│   └── helper.py             # ChatGroq factory + JSON parser
│
├── requirements.txt
├── .env.example              # Template — copy to .env and add your key
└── README.md
```

---

## ⚡ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/MS12code/FraudLens-AI.git
cd FraudLens-AI
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Copy the example and add your Groq key:

```bash
cp .env.example .env
```

Edit `.env`:

```env
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

> Get a free API key at [console.groq.com](https://console.groq.com)

### 5. Run the app

```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## 🎮 Usage

### Sidebar Inputs
Configure the transaction parameters — or use one of the **Quick Presets**:

| Preset | Scenario | Expected Result |
|---|---|---|
| 🟢 Low-Risk Dining | Starbucks, local, chip card, $32 | Score ~20 → **Approve** |
| 🔴 High-Risk Crypto | CryptoWorld, Russia, 3 AM, online, $4500 | Score ~85 → **Decline** |
| 🟡 Impossible Travel | Berlin shop, card present, home: India, fraud history | Score ~75 → **Escalate** |

### Click "Investigate Transaction"
Watch the live agent feed as each of the 7 nodes completes, then view:
- **Risk Score** (0–100) and **Risk Level** (Low / Medium / High)
- **Confidence** percentage and **Recommended Action**
- **Agent-by-Agent Findings** tab with each agent's observations
- **Full Investigation Report** in formatted markdown

---

## ☁️ Deployment (Streamlit Cloud)

🌐 **Live App URL**: [https://fraudlens-ai-ak89vufd3rvoe94xlaapdu.streamlit.app/](https://fraudlens-ai-ak89vufd3rvoe94xlaapdu.streamlit.app/)

The application is deployed on Streamlit Cloud with automatic GitHub integration.

### Deployment Steps (Reference)
1. Repository: `MS12code/FraudLens-AI` (branch: `main`)
2. Entry point: `app.py`
3. Advanced Settings → Secrets configured with `GROQ_API_KEY` and `GROQ_MODEL`.

---

## 🔮 Future Improvements

- **Parallel Agent Execution** — Run Transaction, Customer, Location & Merchant agents concurrently with LangGraph fan-out to cut latency by ~60%
- **Human-in-the-Loop** — Add LangGraph interrupt states to pause for analyst approval when "Escalate" is recommended
- **Case History** — SQLite persistence for previously investigated transactions
- **Risk Trend Charts** — Visualize fraud patterns across multiple investigations



## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

Built with ❤️ using LangGraph · Groq · Streamlit

⭐ Star this repo if you found it useful!

</div>
