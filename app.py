import streamlit as st
import json
import os
import re
from datetime import datetime

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Support Tools | Traceable Mode", page_icon="🛠", layout="centered")

# ── Session State Init (Step 7) ──────────────────────────────────────────────
if "dbg_result" not in st.session_state:
    st.session_state.dbg_result = None
if "gate_result" not in st.session_state:
    st.session_state.gate_result = None

# ── Styles ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Outfit:wght@500;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
h1, h2, h3, h4 { font-family: 'Outfit', sans-serif; }
.result-box {
    background: rgba(108,99,255,.08);
    border: 1px solid rgba(108,99,255,.25);
    border-radius: 10px; padding: 16px 18px; margin-top: 12px;
}
.debug-log {
    background: #1e1e1e; color: #00ff00; font-family: monospace; 
    font-size: 11px; padding: 10px; border-radius: 5px; margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ── Logic ─────────────────────────────────────────────────────────────────────

def analyze_deployment(text: str):
    t = text.lower()
    # Pattern matching
    if re.search(r"EADDRINUSE|listen.*:(3000|8080|8000|4000|5000)|hardcoded.*port", text, re.I):
        return {
            "issue": "Port binding failure",
            "cause": "Another process is using the port or the app is not using $PORT.",
            "fix": "Use process.env.PORT and bind to 0.0.0.0.",
        }
    return {
        "issue": "Unrecognized Log Pattern",
        "cause": "Manual review required.",
        "fix": "Check for application-level logic errors.",
    }

def classify_ticket(text: str):
    t = text.lower()
    if any(w in t for w in ["enterprise", "billing", "billed", "charge", "refund", "breach", "outage"]):
        return {
            "classification": "Escalate (High Priority)",
            "type": "Billing / Business Risk",
            "next_step": "Route to Tier 2 Engineering.",
        }
    return {
        "classification": "Standard Support",
        "type": "General Inquiry",
        "next_step": "Provide structured response.",
    }

def run_analysis(tool_type, input_text):
    # Step 4: Standardize output contract
    if input_text == "debug_test":
        return {
            "status": "success",
            "data": {"message": "State Management Working", "timestamp": datetime.now().isoformat()},
            "message": "Debug test executed"
        }

    # Step 6: Remove try/except to let errors surface
    if tool_type == "debugger":
        res_data = analyze_deployment(input_text)
        status = "success" if "Unrecognized" not in res_data["issue"] else "fallback"
    else:
        res_data = classify_ticket(input_text)
        status = "success"

    return {
        "status": status,
        "data": res_data,
        "message": f"Analysis complete at {datetime.now().strftime('%H:%M:%S')}"
    }

def render_result(tool_type, result):
    # Step 5: Fix render_result() to handle all statuses and always display
    if not result:
        st.warning("DEBUG: render_result called with empty result")
        return

    st.write("### Analysis Results")
    st.write(f"**Status:** {result['status'].upper()}")
    
    with st.container():
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        
        # Always display something (Step 5)
        data = result.get("data", {})
        if not data:
            st.write("No detailed data returned.")
        else:
            for key, val in data.items():
                st.write(f"**{key.replace('_', ' ').title()}:** {val}")
        
        if result.get("message"):
            st.caption(result["message"])
            
        st.markdown("</div>", unsafe_allow_html=True)

# ── Main UI ───────────────────────────────────────────────────────────────────

st.title("TRACE MODE V2 - April 16")
st.markdown("## Replit Support Tools")

# 1. Debugger Section
st.subheader("🔍 Deployment Debugger")
dbg_input = st.text_area("Deployment logs", key="dbg_input", height=100, 
                         value="Error: listen EADDRINUSE: address already in use :::3000")

if st.button("Diagnose Error", key="debugger_btn"):
    # Step 1: Confirm execution path
    st.markdown('<div class="debug-log">DEBUG: Debugger Button clicked</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="debug-log">DEBUG INPUT: {dbg_input[:50]}...</div>', unsafe_allow_html=True)
    
    # Step 2: Force render test (visual confirmation)
    st.success("Test: run_analysis() triggered")
    
    # Run and save to session state (Step 7)
    st.session_state.dbg_result = run_analysis("debugger", dbg_input)
    
    # Step 3: Print raw output
    st.write("**RAW RESULT:**", st.session_state.dbg_result)

if st.session_state.dbg_result:
    render_result("debugger", st.session_state.dbg_result)

st.divider()

# 2. Gatekeeper Section
st.subheader("🛡 Support Gatekeeper")
gate_input = st.text_area("Support message", key="gate_input", height=100, 
                          value="Enterprise customer here — I'm being double charged for my seat and need a refund.")

if st.button("Triage Ticket", key="gatekeeper_btn"):
    # Step 1: Confirm execution path
    st.markdown('<div class="debug-log">DEBUG: Gatekeeper Button clicked</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="debug-log">DEBUG INPUT: {gate_input[:50]}...</div>', unsafe_allow_html=True)
    
    st.success("Test: run_analysis() triggered")
    
    st.session_state.gate_result = run_analysis("gatekeeper", gate_input)
    
    # Step 3: Print raw output
    st.write("**RAW RESULT:**", st.session_state.gate_result)

if st.session_state.gate_result:
    render_result("gatekeeper", st.session_state.gate_result)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br><hr><center style='font-size:11px;color:#555;'>System Trace Mode v1.4</center>", unsafe_allow_html=True)
