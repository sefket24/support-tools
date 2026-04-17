import streamlit as st
import json
import os
import re
from datetime import datetime, timezone

# ── Config ────────────────────────────────────────────────────────────────────
VISITS_FILE = "visits.json"

# ── Session State Persistence ───────────────────────────────────────────────
if "debugger_res" not in st.session_state:
    st.session_state.debugger_res = None
if "gatekeeper_res" not in st.session_state:
    st.session_state.gatekeeper_res = None

# ── Logic functions (DO NOT MODIFY PARSING LOGIC as per user request) ───────
def analyze_deployment(text: str):
    t = text.lower()
    if "$port" in t or ("port" in t and ("listen" in t or "bind" in t or "process" in t)):
        return {
            "issue": "Port binding failure",
            "root_cause": "The app is not binding to the required $PORT environment variable assigned by the platform.",
            "pattern": "Common runtime port error",
            "fix_time": "2–5 minutes",
            "suggested_response": "Looks like your app isn’t listening on the required port. Make sure your server is running on $PORT and try redeploying.",
            "fix": "Set your server to listen on `process.env.PORT` (Node) or `int(os.environ['PORT'])` (Python)."
        }
    if "oomkilled" in t or ("memory" in t and "limit" in t):
        return {
            "issue": "Memory limit exceeded (OOMKilled)",
            "root_cause": "Container hit its memory ceiling during runtime dependency load or memory leak.",
            "pattern": "Recurring deployment memory issue",
            "fix_time": "5–10 minutes",
            "suggested_response": "Your app hit a memory limit during startup. Try increasing the memory allowance in your config or lazy-loading heavy libs.",
            "fix": "Increase the container memory limit or optimize dependency loading."
        }
    if "timeout" in t or "timed out" in t:
        return {
            "issue": "Deployment timeout",
            "root_cause": "Startup exceeded the platform window. App likely doing blocking work before server bind.",
            "pattern": "Startup timeout pattern",
            "fix_time": "Requires deeper investigation",
            "suggested_response": "The deployment timed out because the app took too long to start. Try starting the server before loading heavy assets.",
            "fix": "Start the HTTP server first, then initialise resources asynchronously."
        }
    return None

def classify_ticket(text: str):
    t = text.lower()
    if any(w in t for w in ["enterprise", "billing", "refund", "breach", "outage"]):
        return {
            "tag_class": "tag-esc", "classification": "Escalate",
            "pattern": "High-priority business risk",
            "next_step": "Route to Tier 2 Engineering queue (Linear).",
            "agent_response": "Got it — I’m escalating this to our engineering team and will follow up.",
            "esc_details": {"team": "Engineering", "tool": "Linear", "priority": "High", "note": "Priority issue detected in support triage."}
        }
    if any(w in t for w in ["how to", "where is", "forgot password", "reset"]):
        return {
            "tag_class": "tag-dup", "classification": "Self-serve / Doc link",
            "pattern": "Common account access question",
            "next_step": "Auto-populate with help center article link.",
            "agent_response": "You can do this here: [help.replit.com] — let me know if you run into any issues.",
            "esc_details": None
        }
    return {
        "tag_class": "tag-self", "classification": "Standard Support",
        "pattern": "General technical query",
        "next_step": "Review logs and provide structured response.",
        "agent_response": "Hey — that shouldn't happen. Can you share a bit more detail so I can help figure this out?",
        "esc_details": None
    }

# ── Rendering helpers ─────────────────────────────────────────────────────────
def render_debugger_res(res):
    if not res:
        st.error("No patterns matched. Please check the logs manually.")
        return
    st.markdown(f"""
    <div class="result-box">
        <div style="display:flex; justify-content:space-between; align-items:start;">
            <div><div class="result-label">Issue</div><div style="font-size:14px;font-weight:600;color:#e8e9f0;">{res['issue']}</div></div>
            <div style="text-align:right;"><div class="result-label">Resolution</div><div style="font-size:11px;color:#fb923c;font-weight:700;">{res['fix_time']}</div></div>
        </div>
        <div style="margin-top:10px;"><div class="result-label">Pattern</div><div style="font-size:12px;color:#c4c6d6;">{res['pattern']}</div></div>
        <div style="margin-top:10px;"><div class="result-label">Suggested Response</div><div style="font-size:13px;color:#f7f9f9;font-style:italic;">"{res['suggested_response']}"</div></div>
    </div>
    """, unsafe_allow_html=True)

def render_gatekeeper_res(cls):
    if not cls: return
    st.markdown(f"""
    <div class="result-box">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div><div class="result-label">Classification</div><span class="tag {cls['tag_class']}">{cls['classification']}</span></div>
            <div style="text-align:right;"><div class="result-label">Pattern</div><div style="font-size:11px;color:#c4c6d6;">{cls['pattern']}</div></div>
        </div>
        <div style="margin-top:12px;"><div class="result-label">Next step</div><div style="font-size:13px;color:#c4c6d6;">{cls['next_step']}</div></div>
        <div style="margin-top:12px;"><div class="result-label">Agent response</div><div style="font-size:13px;color:#f7f9f9;font-style:italic;">"{cls['agent_response']}"</div></div>
    """, unsafe_allow_html=True)

    if cls['esc_details']:
        st.markdown(f"""
        <div class="escalation-grid">
            <div class="esc-stat"><div class="esc-label">Team</div><div class="esc-val">{cls['esc_details']['team']}</div></div>
            <div class="esc-stat"><div class="esc-label">Tool</div><div class="esc-val">{cls['esc_details']['tool']}</div></div>
            <div class="esc-stat"><div class="esc-label">Priority</div><div class="esc-val" style="color:#f87171;">{cls['esc_details']['priority']}</div></div>
        </div>
        <div style="margin-top:10px;"><div class="result-label">Internal Note</div><div style="font-size:11px;color:#8b8fa8;font-style:italic;">{cls['esc_details']['note']}</div></div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Main UI ───────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Support Tools", page_icon="🛠", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Outfit:wght@500;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
h1, h2, h3, h4 { font-family: 'Outfit', sans-serif; }
.contact-links { font-size: 13px; color: #8b8fa8; display: flex; gap: 12px; margin-bottom: 12px; }
.contact-links a { color: #6c63ff; text-decoration: none; border-bottom: 1px solid rgba(108,99,255,0.3); padding-bottom: 1px; }
.badge { display: inline-block; font-size: 10px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: #6c63ff; background: rgba(108,99,255,.12); border: 1px solid rgba(108,99,255,.25); border-radius: 20px; padding: 4px 12px; margin-bottom: 16px; }
.result-box { background: rgba(108,99,255,.08); border: 1px solid rgba(108,99,255,.25); border-radius: 10px; padding: 16px 18px; margin-top: 12px; }
.result-label { font-size: 10px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: #6c63ff; margin-bottom: 6px; }
.tag { font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 4px; text-transform: uppercase; letter-spacing: .05em; }
.tag-esc { background: rgba(239,68,68,.12); color: #f87171; }
.tag-dup { background: rgba(251,146,60,.12); color: #fb923c; }
.tag-self { background: rgba(34,197,94,.12); color: #4ade80; }
.tag-vague { background: rgba(108,99,255,.12); color: #a78bfa; }
.escalation-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 10px; }
.esc-stat { background: rgba(0,0,0,0.2); padding: 8px; border-radius: 6px; text-align: center; }
.esc-label { font-size: 8px; color: #8b8fa8; text-transform: uppercase; }
.esc-val { font-size: 11px; font-weight: 700; color: #e8e9f0; }
.pos-line { font-size: 12px; color: #a0a4c0; font-style: italic; border-left: 2px solid #6c63ff; padding-left: 10px; margin: 20px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom:20px;line-height:1.4;">
    <div style="font-size:22px;font-weight:700;color:#e8e9f0;margin-bottom:6px;">Sefket Nouri</div>
    <div class="contact-links">
        <a href="mailto:me@sefketnouri.com">me@sefketnouri.com</a>
        <a href="https://www.linkedin.com/in/sefketnouri/" target="_blank">LinkedIn</a>
    </div>
    <div class="badge">Support Operations Debugger</div>
</div>
""", unsafe_allow_html=True)

# ── Deployment Debugger ───────────────────────────────────────────────────────
st.markdown("#### 🔍 Deployment Debugger")
debugger_input = st.text_area("Paste error/log", key="debugger_input_area", height=70)

if st.button("Run Debugger"):
    if not debugger_input.strip():
        st.warning("Please paste a log first.")
    else:
        st.session_state.debugger_res = analyze_deployment(debugger_input)
        st.write("RAW RESULT:", st.session_state.debugger_res)

if st.session_state.debugger_res is not None:
    render_debugger_res(st.session_state.debugger_res)

st.markdown("<br>", unsafe_allow_html=True)

# ── Support Gatekeeper ────────────────────────────────────────────────────────
st.markdown("#### 🛡 Support Gatekeeper")
gatekeeper_input = st.text_area("Paste support message", key="gatekeeper_input_area", height=70)

if st.button("Run Gatekeeper"):
    if not gatekeeper_input.strip():
        st.warning("Please paste a message first.")
    else:
        st.session_state.gatekeeper_res = classify_ticket(gatekeeper_input)
        st.write("RAW RESULT:", st.session_state.gatekeeper_res)

if st.session_state.gatekeeper_res is not None:
    render_gatekeeper_res(st.session_state.gatekeeper_res)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br><hr><center style='font-size:11px;color:#555;'>Diagnostics Engine v1.5</center>", unsafe_allow_html=True)
