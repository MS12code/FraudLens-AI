"""
utils/helper.py
---------------
Utility functions for FraudLens AI:
  - get_llm()           : Creates and returns a ChatGroq LLM instance.
  - parse_json_response(): Cleans and parses JSON from raw LLM text.

API key resolution order:
  1. Directly passed api_key argument
  2. Streamlit session_state (entered in sidebar)
  3. Streamlit secrets (for Streamlit Cloud deployment)
  4. Environment variable GROQ_API_KEY (from .env file)
"""

import os
import re
import json
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load .env file if present (for local development)
load_dotenv()


def get_llm(api_key: str = None, model_name: str = None) -> ChatGroq:
    """
    Initializes and returns a configured ChatGroq LLM client.

    Searches for the API key in the following order:
    1. Passed argument
    2. Streamlit session_state (sidebar input)
    3. Streamlit secrets (Streamlit Cloud)
    4. Environment variable (local .env file)
    """
    groq_api_key = api_key

    # Check Streamlit session state (sidebar key input)
    if not groq_api_key:
        try:
            import streamlit as st
            if "groq_api_key" in st.session_state and st.session_state["groq_api_key"]:
                groq_api_key = st.session_state["groq_api_key"]
        except Exception:
            pass

    # Check Streamlit secrets (Streamlit Cloud deployment)
    if not groq_api_key:
        try:
            import streamlit as st
            groq_api_key = st.secrets.get("GROQ_API_KEY", None)
        except Exception:
            pass

    # Fall back to environment variable
    if not groq_api_key:
        groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        raise ValueError(
            "Groq API Key not found. Please provide it via:\n"
            "  • Streamlit sidebar input\n"
            "  • Streamlit Cloud secrets (GROQ_API_KEY)\n"
            "  • A local .env file"
        )

    # Resolve model: argument > env var > default
    selected_model = (
        model_name
        or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    )

    return ChatGroq(
        groq_api_key=groq_api_key,
        model=selected_model,
        temperature=0.0
    )


def parse_json_response(raw_text: str) -> Dict[str, Any]:
    """
    Robustly cleans and parses JSON from raw LLM output.

    Handles:
      - Markdown code fences (```json ... ```)
      - Leading/trailing text around the JSON object
      - Malformed JSON with a best-effort extraction
    """
    cleaned = raw_text.strip()

    # Strip markdown code fences if present
    if cleaned.startswith("```"):
        match = re.search(r"```(?:json)?\s*(.*?)\s*```", cleaned, re.DOTALL)
        if match:
            cleaned = match.group(1).strip()

    # Try direct parse
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Try extracting the first complete JSON object
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(cleaned[start : end + 1])
        except json.JSONDecodeError:
            pass

    # If all parsing fails, log and return empty dict to avoid pipeline crash
    print(f"[FraudLens Warning] Failed to parse JSON from LLM response:\n{raw_text[:300]}")
    return {}
