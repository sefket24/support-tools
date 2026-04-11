import streamlit as st

st.set_page_config(page_title="Support Tools", page_icon="🛠", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.badge {
    display: inline-block;
    font-size: 11px; font-weight: 700; letter-spacing: .08em;
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
    font-size: 11px; font-weight: 600; padding: 3px 10px;
    border-radius: 4px; text-transform: uppercase; letter-spacing: .05em;
}
.tag-esc  { background: rgba(239,68,68,.12); color: #f87171; }
.tag-dup  { background: rgba(251,146,60,.12); color: #fb923c; }
.tag-self { background: rgba(34,197,94,.12);  color: #4ade80; }
.tag-vague { background: rgba(108,99,255,.12); color: #a78bfa; }
.footer { text-align: center; font-size: 13px; color: #8b8fa8; margin-top: 40px; line-height: 1.8; }
@media (max-width: 480px) {
    .result-box { padding: 12px 14px; }
    h2 { font-size: 22px !important; }
}
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────────────────────
st.markdown('<div class="badge">⬤ &nbsp;Support Tooling Demo</div>', unsafe_allow_html=True)
st.markdown("## Reducing **repeated** support issues")
st.markdown(
    "Tools I built to stop handling the same support issues twice — "
    "pattern detection, root cause analysis, and ticket routing."
)

st.markdown("---")

# ── Try it instantly ────────────────────────────────────────────────────────
st.markdown("### Try it instantly")
st.markdown("Both tools are pre-filled. Edit the input to test your own.")

# ── Deployment Debugger ─────────────────────────────────────────────────────
st.markdown("#### 🔍 Deployment Debugger")
st.caption("Scans deployment errors for known failure patterns and surfaces the root cause.")
st.markdown('<p style="font-size:12px;color:#8b8fa8;margin:-8px 0 8px;">Best with real error messages or logs</p>', unsafe_allow_html=True)

debug_input = st.text_area(
    "Paste a specific error or log message",
    value="Deployment fails: no process listening on $PORT",
    placeholder="Example: Deployment fails: no process listening on $PORT",
    height=80,
    key="debug_input",
)

_VAGUE_PHRASES = [
    "not working", "broken", "doesn't work", "it's not working", "isnt working",
    "my app is broken", "won't work", "nothing works", "app is down",
    "something is wrong", "not loading", "help", "it broke",
]
_TECHNICAL_SIGNALS = [
    "error", "fail", "exception", "port", "memory", "timeout", "module",
    "import", "crash", "exit", "kill", "log", "stack", "trace", "deploy",
    "build", "npm", "pip", "docker", "process", "listen", "bind", "oom",
    "sigterm", "sigkill", "exit code", "enoent", "econnrefused",
]

def _is_vague(text: str) -> bool:
    t = text.strip().lower()
    if len(t) < 15:
        return True
    if any(sig in t for sig in _TECHNICAL_SIGNALS):
        return False
    return any(phrase in t for phrase in _VAGUE_PHRASES)

def analyze_deployment(text: str):
    t = text.lower()
    if "$port" in t or ("port" in t and ("listen" in t or "bind" in t or "process" in t)):
        return {
            "issue": "Port binding failure",
            "root_cause": "The app is not binding to the PORT environment variable. Most platforms (Heroku, Render, Railway) assign a dynamic port at runtime — hardcoding a port or not reading $PORT will cause this.",
            "fix": "Set your server to listen on `process.env.PORT` (Node) or `int(os.environ['PORT'])` (Python). Do not hardcode a port number.",
        }
    if "oomkilled" in t or ("memory" in t and "limit" in t):
        return {
            "issue": "Memory limit exceeded (OOMKilled)",
            "root_cause": "Container hit its memory ceiling during runtime. Often caused by a cold-start dependency load or memory leak.",
            "fix": "Increase the container memory limit or lazy-load heavy dependencies to reduce peak usage at startup.",
        }
    if "timeout" in t or "timed out" in t:
        return {
            "issue": "Deployment timeout",
            "root_cause": "The deploy process exceeded the platform's allowed startup window. App may be doing heavy work before binding to a port.",
            "fix": "Start the HTTP server first, then initialise heavy resources asynchronously.",
        }
    if "cannot find module" in t or "module not found" in t or "importerror" in t:
        return {
            "issue": "Missing dependency",
            "root_cause": "A required package is not installed in the deployment environment.",
            "fix": "Ensure the package is listed in requirements.txt / package.json and re-deploy.",
        }
    return None

if debug_input.strip():
    if _is_vague(debug_input):
        st.markdown("""
        <div class="result-box">
            <div style="font-size:14px;color:#c4c6d6;line-height:1.8;">
                Could not identify a specific error.<br>
                <span style="font-size:13px;color:#8b8fa8;">Try pasting:</span>
                <ul style="font-size:13px;color:#8b8fa8;margin:4px 0 0 16px;padding:0;">
                    <li>a log line</li>
                    <li>an error message</li>
                    <li>or a deployment failure output</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        result = analyze_deployment(debug_input)
        if result:
            st.markdown(f"""
            <div class="result-box">
                <div class="result-label">Detected issue</div>
                <div style="font-size:15px;font-weight:600;color:#e8e9f0;margin-bottom:12px;">{result['issue']}</div>
                <div class="result-label">Root cause</div>
                <div style="font-size:14px;color:#c4c6d6;margin-bottom:12px;line-height:1.6;">{result['root_cause']}</div>
                <div class="result-label">Suggested fix</div>
                <div style="font-size:14px;color:#c4c6d6;line-height:1.6;">{result['fix']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="result-box">
                <div style="font-size:14px;color:#c4c6d6;line-height:1.8;">
                    Could not identify a specific error.<br>
                    <span style="font-size:13px;color:#8b8fa8;">Try pasting:</span>
                    <ul style="font-size:13px;color:#8b8fa8;margin:4px 0 0 16px;padding:0;">
                        <li>a log line</li>
                        <li>an error message</li>
                        <li>or a deployment failure output</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")

# ── Support Gatekeeper ──────────────────────────────────────────────────────
st.markdown("#### 🛡 Support Gatekeeper")
st.caption("Classifies incoming tickets and recommends the right next step.")

gate_input = st.text_area(
    "Paste a support message:",
    value="My app isn't working",
    height=80,
    key="gate_input",
    label_visibility="collapsed",
)

def classify_ticket(text: str):
    t = text.lower()
    # Duplicate / docs-answerable
    docs_triggers = [
        "reset my password", "forgot password", "change password",
        "export", "download my data", "cancel my subscription", "how do i",
        "how to", "where can i find", "what is",
    ]
    # Escalation signals
    esc_triggers = [
        "enterprise", "sso", "saml", "billing error", "charge", "refund",
        "data breach", "security", "outage", "down for everyone", "not working for all",
        "auth token", "session expired",
    ]
    # Vague / needs info
    vague_triggers = [
        "not working", "broken", "doesn't work", "it's broken", "won't load",
        "nothing works", "help", "issue",
    ]

    for trigger in esc_triggers:
        if trigger in t:
            return {
                "tag": "escalate",
                "tag_class": "tag-esc",
                "classification": "Escalate",
                "next_step": "Route to Tier 2 or the relevant specialist team. Requires human review.",
            }
    for trigger in docs_triggers:
        if trigger in t:
            return {
                "tag": "duplicate",
                "tag_class": "tag-dup",
                "classification": "Duplicate / Self-serve",
                "next_step": "Auto-reply with the relevant docs link. No human response needed.",
            }
    for trigger in vague_triggers:
        if trigger in t:
            return {
                "tag": "vague",
                "tag_class": "tag-vague",
                "classification": "Needs clarification",
                "next_step": "Send a structured follow-up: ask what app, what error message, and what they expected to happen. Do not assign to a queue yet.",
            }
    return {
        "tag": "self-serve",
        "tag_class": "tag-self",
        "classification": "Self-serve",
        "next_step": "Likely answerable from docs or a macro. Review and route to the relevant help article.",
    }

if gate_input.strip():
    cls = classify_ticket(gate_input)
    st.markdown(f"""
    <div class="result-box">
        <div class="result-label">Classification &nbsp;<span class="tag {cls['tag_class']}">{cls['classification']}</span></div>
        <div style="margin-top:10px;" class="result-label">Recommended next step</div>
        <div style="font-size:14px;color:#c4c6d6;line-height:1.6;margin-top:4px;">{cls['next_step']}</div>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div class="footer">
    <strong style="color:#e8e9f0;">Sefket Nouri</strong> — Support Specialist<br>
    Focused on reducing repeat support issues through tooling and systems thinking<br>
    <span style="font-size:12px;">
        <a href="https://www.linkedin.com/in/sefketnouri" style="color:#6c63ff;text-decoration:none;">LinkedIn</a>
        &nbsp;·&nbsp;
        <a href="https://replit.com/@sefket24" style="color:#6c63ff;text-decoration:none;">View implementation on Replit</a>
    </span>
</div>
""", unsafe_allow_html=True)
