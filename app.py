import streamlit as st
import json
import os
import re
from datetime import datetime, timezone

# ── Config ────────────────────────────────────────────────────────────────────
DEBUG = False
VISITS_FILE = "visits.json"

# ── Visit tracking ───────────────────────────────────────────────────────────
def _load_visits():
    try:
        if os.path.exists(VISITS_FILE):
            with open(VISITS_FILE) as f:
                data = json.load(f)
            if "visits" not in data or "timestamps" not in data:
                raise ValueError
            return data
    except Exception:
        pass
    return {"visits": 0, "timestamps": []}

def _save_visits(data):
    try:
        with open(VISITS_FILE, "w") as f:
            json.dump(data, f)
    except Exception:
        pass 

if "visit_counted" not in st.session_state:
    st.session_state["visit_counted"] = True
    st.session_state.setdefault("session_visits", 0)
    st.session_state["session_visits"] += 1

    data = _load_visits()
    data["visits"] += 1
    data["timestamps"].append(datetime.now(timezone.utc).isoformat())
    data["timestamps"] = data["timestamps"][-50:]
    _save_visits(data)
    st.session_state["visit_data"] = data
else:
    st.session_state["visit_data"] = _load_visits()

st.set_page_config(page_title="Support Tools", page_icon="🛠", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Outfit:wght@500;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
h1, h2, h3, h4 { font-family: 'Outfit', sans-serif; }

/* Link styling matching Social Inbox Triage */
.contact-links { font-size: 13px; color: #8b8fa8; display: flex; gap: 12px; margin-bottom: 12px; }
.contact-links a { 
    color: #6c63ff; 
    text-decoration: none; 
    border-bottom: 1px solid rgba(108,99,255,0.3); 
    padding-bottom: 1px;
    transition: all 0.2s ease;
    cursor: pointer;
}
.contact-links a:hover { 
    color: #a78bfa; 
    border-bottom-color: #a78bfa;
    opacity: 0.9;
}

.badge {
    display: inline-block;
    font-size: 10px; font-weight: 700; letter-spacing: .08em;
    text-transform: uppercase; color: #6c63ff;
    background: rgba(108,99,255,.12);
    border: 1px solid rgba(108,99,255,.25);
    border-radius: 20px; padding: 4px 12px; margin-bottom: 16px;
}
.result-box {
    background: rgba(108,99,255,.08);
    border: 1px solid rgba(108,99,255,.25);
    border-radius: 10px; padding: 16px 18px; margin-top: 12px;
}
.result-label {
    font-size: 10px; font-weight: 700; letter-spacing: .1em;
    text-transform: uppercase; color: #6c63ff; margin-bottom: 6px;
}
.tag {
    font-size: 10px; font-weight: 700; padding: 2px 8px;
    border-radius: 4px; text-transform: uppercase; letter-spacing: .05em;
}
.tag-esc   { background: rgba(239,68,68,.12); color: #f87171; }
.tag-dup   { background: rgba(251,146,60,.12); color: #fb923c; }
.tag-self  { background: rgba(34,197,94,.12);  color: #4ade80; }
.tag-vague { background: rgba(108,99,255,.12); color: #a78bfa; }

.escalation-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    margin-top: 10px;
}
.esc-stat {
    background: rgba(0,0,0,0.2);
    padding: 8px;
    border-radius: 6px;
    text-align: center;
}
.esc-label { font-size: 8px; color: #8b8fa8; text-transform: uppercase; }
.esc-val { font-size: 11px; font-weight: 700; color: #e8e9f0; }

.pos-line {
    font-size: 12px; color: #a0a4c0; font-style: italic;
    border-left: 2px solid #6c63ff; padding-left: 10px; margin: 20px 0;
}

@media (max-width: 480px) {
    .result-box { padding: 12px 14px; }
}
</style>
""", unsafe_allow_html=True)

# ── Logic functions ───────────────────────────────────────────────────────────

def run_analysis(text: str):
    """Specific logic for analysis - handles both tools."""
    # Handle empty input
    if not text or not text.strip():
        return {
            "status": "error",
            "message": "No input provided"
        }

    text_lower = text.lower()

    # --- Deployment Debugger ---
    # Triggered by deployment keywords or EADDRINUSE
    if "eaddrinuse" in text_lower or (("port" in text_lower or "listen" in text_lower) and "address already in use" in text_lower):
        return {
            "status": "success",
            "tool": "debugger", # internal flag
            "data": {
                "tool": "Deployment Debugger",
                "issue": "Port already in use",
                "cause": "Another process is using the same port",
                "fix": "Kill the process or bind to process.env.PORT"
            }
        }
    
    # Existing patterns for Deployment Debugger
    if "$port" in text_lower or ("port" in text_lower and ("listen" in text_lower or "bind" in text_lower or "process" in text_lower)):
        return {
            "status": "success",
            "tool": "debugger",
            "data": {
                "tool": "Deployment Debugger",
                "issue": "Port binding failure",
                "cause": "App not using dynamic $PORT variable.",
                "fix": "Set server to listen on process.env.PORT."
            }
        }

    # --- Support Gatekeeper ---
    # Triggered by billing keywords or priority support
    if any(w in text_lower for w in ["bill", "charge", "refund", "overcharged", "billing", "billed"]):
        return {
            "status": "success",
            "tool": "gatekeeper", # internal flag
            "data": {
                "tool": "Support Gatekeeper",
                "priority": "High",
                "type": "Billing",
                "reasoning": "User mentions billing issue, indicating potential financial impact",
                "action": "Escalate to billing team and review account charges"
            }
        }
    
    # Existing patterns for Support Gatekeeper
    if any(w in text_lower for w in ["enterprise", "refund", "breach", "outage"]):
         return {
            "status": "success",
            "tool": "gatekeeper",
            "data": {
                "tool": "Support Gatekeeper",
                "priority": "High",
                "type": "Escalate",
                "reasoning": "High-priority business risk detected.",
                "action": "Route to Tier 2 Engineering (Linear)."
            }
        }

    # --- Fallback (applies to BOTH tools) ---
    return {
        "status": "fallback",
        "message": "Input could not be fully classified, but the system is working and no action is blocked."
    }

# ── Identity header ──────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:20px;line-height:1.4;">
    <div style="font-size:22px;font-weight:700;color:#e8e9f0;margin-bottom:6px;">Sefket Nouri</div>
    <div class="contact-links">
        <a href="mailto:me@sefketnouri.com">me@sefketnouri.com</a>
        <a href="https://www.linkedin.com/in/sefketnouri/" target="_blank">LinkedIn</a>
        <a href="https://sefket24-support-tools-app-zwaemo.streamlit.app/" target="_blank">App</a>
        <a href="https://replit.com/@sefketnouri" target="_blank">Replit</a>
    </div>
    <div class="badge">Designed for high-volume ticket triage and fast resolution</div>
    <div class="pos-line">
        "Built from handling real support tickets — focused on faster triage, clearer responses, and fewer repeat issues."
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    "Built to debug failed deployments, triage support issues, and reduce engineering handoffs—using a workflow aligned with how Replit operates."
)

st.subheader("Example Workflow")

st.markdown(
    "Failed deployment → identify root cause → suggest fix\n\n"
    "**Example:** Missing environment variable causing build failure.\n"
    "→ Surface error\n"
    "→ Explain issue in plain terms\n"
    "→ Recommend fix"
)


# ── Deployment Debugger ───────────────────────────────────────────────────────
st.markdown("#### 🔍 Deployment Debugger")
st.caption("Pattern-matching for instant root cause analysis.")

debugger_input = st.text_area(
    "Paste error/log", key="debugger_input", height=70,
    placeholder="Paste a deployment log to start analysis..."
)

if debugger_input:
    res = run_analysis(debugger_input)
    if res["status"] == "success" and res.get("tool") == "debugger":
        data = res["data"]
        st.markdown(f"""
        <div class="result-box">
            <div style="display:flex; justify-content:space-between; align-items:start;">
                <div><div class="result-label">Issue</div><div style="font-size:14px;font-weight:600;color:#e8e9f0;">{data['issue']}</div></div>
                <div style="text-align:right;"><div class="result-label">Resolution</div><div style="font-size:11px;color:#fb923c;font-weight:700;">2-5 mins</div></div>
            </div>
            <div style="margin-top:10px;"><div class="result-label">Cause</div><div style="font-size:12px;color:#c4c6d6;">{data['cause']}</div></div>
            <div style="margin-top:10px;"><div class="result-label">Recommended Fix</div><div style="font-size:13px;color:#f7f9f9;font-style:italic;">{data['fix']}</div></div>
        </div>
        """, unsafe_allow_html=True)
    elif res["status"] == "fallback":
        st.markdown(f'<div class="result-box"><div style="font-size:12px;color:#8b8fa8;">{res["message"]}</div></div>', unsafe_allow_html=True)
    elif res["status"] == "error":
        pass # Handle silently or show basic prompt
else:
    st.markdown('<div class="result-box"><div style="font-size:12px;color:#8b8fa8;">Paste a deployment log to start analysis.</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Support Gatekeeper ────────────────────────────────────────────────────────
st.markdown("#### 🛡 Support Gatekeeper")
st.caption("Classifies tickets and pre-drafts agent responses.")

gatekeeper_input = st.text_area(
    "Paste support message",
    key="gatekeeper_input", height=70,
    placeholder="Paste a support ticket here..."
)

if gatekeeper_input:
    cls = run_analysis(gatekeeper_input)
    if cls["status"] == "success" and cls.get("tool") == "gatekeeper":
        data = cls["data"]
        st.markdown(f"""
        <div class="result-box">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div><div class="result-label">Classification</div><span class="tag tag-esc">{data['type']}</span></div>
                <div style="text-align:right;"><div class="result-label">Priority</div><div style="font-size:11px;color:#f87171;font-weight:700;">{data['priority']}</div></div>
            </div>
            <div style="margin-top:12px;"><div class="result-label">Reasoning</div><div style="font-size:13px;color:#c4c6d6;">{data['reasoning']}</div></div>
            <div style="margin-top:12px;"><div class="result-label">Recommended Action</div><div style="font-size:13px;color:#f7f9f9;font-style:italic;">"{data['action']}"</div></div>
        </div>
        """, unsafe_allow_html=True)
    elif cls["status"] == "fallback":
        st.markdown(f'<div class="result-box"><div style="font-size:12px;color:#8b8fa8;">{cls["message"]}</div></div>', unsafe_allow_html=True)
else:
    st.info("Paste a message to begin classification.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br><center style='font-size:11px;color:#555;'>Built for high-velocity Support Operations • instant triage</center>", unsafe_allow_html=True)
