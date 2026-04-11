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
h1 { font-size: 38px !important; font-weight: 700 !important; letter-spacing: -.02em; line-height: 1.15 !important; }
.hero-desc { font-size: 16px; color: #8b8fa8; line-height: 1.7; margin-bottom: 8px; }
.section-label {
    font-size: 11px; font-weight: 700; letter-spacing: .1em;
    text-transform: uppercase; color: #8b8fa8; margin-bottom: 4px;
}
.tool-card {
    background: #1a1d27; border: 1px solid #2a2d3e;
    border-radius: 16px; padding: 28px; margin-bottom: 20px;
    transition: border-color .2s;
}
.tool-title { font-size: 18px; font-weight: 700; display: flex; align-items: center; gap: 10px; }
.tool-desc  { font-size: 14px; color: #8b8fa8; margin: 8px 0 18px; }
.status-pill {
    font-size: 11px; font-weight: 600; letter-spacing: .06em;
    text-transform: uppercase; color: #22c55e;
    background: rgba(34,197,94,.1); border: 1px solid rgba(34,197,94,.2);
    border-radius: 20px; padding: 3px 10px;
}
.demo-frame { border: 1px solid #2a2d3e; border-radius: 10px; overflow: hidden; background: #0f1117; }
.demo-bar {
    display: flex; align-items: center; gap: 6px;
    padding: 8px 14px; background: rgba(255,255,255,.03);
    border-bottom: 1px solid #2a2d3e;
}
.demo-url { font-size: 11px; color: #8b8fa8; margin-left: 6px; font-family: monospace; }
.demo-body { padding: 20px; }
.log { font-family: monospace; font-size: 12px; padding: 6px 10px; border-radius: 6px; margin-bottom: 6px; }
.log-err  { background: rgba(239,68,68,.08); color: #f87171; }
.log-warn { background: rgba(251,146,60,.08); color: #fb923c; }
.log-ok   { background: rgba(34,197,94,.08);  color: #4ade80; }
.analysis {
    margin-top: 14px; background: rgba(108,99,255,.12);
    border: 1px solid rgba(108,99,255,.25); border-radius: 8px; padding: 12px 14px;
}
.analysis-label { font-size: 10px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: #6c63ff; margin-bottom: 6px; }
.ticket { border: 1px solid #2a2d3e; border-radius: 8px; padding: 14px; margin-bottom: 12px; }
.ticket-id { font-size: 11px; color: #8b8fa8; font-family: monospace; }
.ticket-body { font-size: 13px; color: #8b8fa8; margin: 6px 0; }
.ticket-route { font-size: 12px; color: #e8e9f0; }
.tag { font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 4px; text-transform: uppercase; letter-spacing: .05em; }
.tag-esc  { background: rgba(239,68,68,.12); color: #f87171; }
.tag-dup  { background: rgba(251,146,60,.12); color: #fb923c; }
.tag-self { background: rgba(34,197,94,.12);  color: #4ade80; }
.benefit { display: flex; gap: 10px; font-size: 15px; margin-bottom: 10px; }
.arrow { color: #6c63ff; font-weight: 700; }
hr-custom { border: none; border-top: 1px solid #2a2d3e; margin: 32px 0; }
</style>
""", unsafe_allow_html=True)

# Hero
st.markdown('<div class="badge">⬤ &nbsp;Internal Tooling</div>', unsafe_allow_html=True)
st.markdown("# Reducing **repeated** support issues")
st.markdown('<p class="hero-desc">Two lightweight tools built to surface failure patterns faster, route tickets with confidence, and stop the same issues from burning support time every week.</p>', unsafe_allow_html=True)

st.markdown("---")

# Benefits
st.markdown('<p class="section-label">How this helps support teams</p>', unsafe_allow_html=True)
st.markdown("""
<div class="benefit"><span class="arrow">→</span> <span><b>Faster triage</b> — pattern detection surfaces root causes in seconds, not hours</span></div>
<div class="benefit"><span class="arrow">→</span> <span><b>Fewer repeated issues</b> — known patterns are flagged before a ticket queue builds</span></div>
<div class="benefit"><span class="arrow">→</span> <span><b>Clearer escalation paths</b> — routing logic removes guesswork on who handles what</span></div>
""", unsafe_allow_html=True)

st.markdown("---")

# Tools
st.markdown('<p class="section-label">Live tools</p>', unsafe_allow_html=True)

# Deployment Debugger
st.markdown("""
<div class="tool-card">
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;flex-wrap:wrap;gap:8px;">
    <div class="tool-title">🔍 &nbsp;Deployment Debugger</div>
    <span class="status-pill">Live</span>
  </div>
  <p class="tool-desc">Scans deployment logs for error patterns and summarizes the most likely root cause.</p>
  <div class="demo-frame">
    <div class="demo-bar">
      <span style="width:8px;height:8px;border-radius:50%;background:#ff5f57;display:inline-block;"></span>
      <span style="width:8px;height:8px;border-radius:50%;background:#febc2e;display:inline-block;margin:0 4px;"></span>
      <span style="width:8px;height:8px;border-radius:50%;background:#28c840;display:inline-block;"></span>
      <span class="demo-url">deploy-debugger / run #4821</span>
    </div>
    <div class="demo-body">
      <div class="log log-err">14:02:31 &nbsp; OOMKilled — container exceeded memory limit (512Mi)</div>
      <div class="log log-warn">14:02:29 &nbsp; Heap allocation spike detected (+340MB in 4s)</div>
      <div class="log log-ok">14:01:58 &nbsp; Deploy started — image sha256:a3f9…</div>
      <div class="analysis">
        <div class="analysis-label">Root cause summary</div>
        <div style="font-size:13px;color:#e8e9f0;line-height:1.5;">
          Memory limit hit during startup. Likely cause: uncached dependency load on cold start.
          Seen 3× in the last 7 days. Recommended fix: increase limit to 768Mi or lazy-load heavy deps.
        </div>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# Support Gatekeeper
st.markdown("""
<div class="tool-card">
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;flex-wrap:wrap;gap:8px;">
    <div class="tool-title">🛡 &nbsp;Support Gatekeeper</div>
    <span class="status-pill">Live</span>
  </div>
  <p class="tool-desc">Classifies incoming tickets — duplicate, self-serve, or escalate — and routes them to the right queue automatically.</p>
  <div class="demo-frame">
    <div class="demo-bar">
      <span style="width:8px;height:8px;border-radius:50%;background:#ff5f57;display:inline-block;"></span>
      <span style="width:8px;height:8px;border-radius:50%;background:#febc2e;display:inline-block;margin:0 4px;"></span>
      <span style="width:8px;height:8px;border-radius:50%;background:#28c840;display:inline-block;"></span>
      <span class="demo-url">gatekeeper / queue</span>
    </div>
    <div class="demo-body">
      <div class="ticket">
        <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:6px;margin-bottom:6px;">
          <span class="ticket-id">#TKT-1094</span><span class="tag tag-esc">Escalate</span>
        </div>
        <div class="ticket-body">"Auth tokens expiring mid-session for enterprise accounts on SSO."</div>
        <div class="ticket-route">→ Route to: <strong style="color:#6c63ff;">Infra-Security</strong></div>
      </div>
      <div class="ticket">
        <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:6px;margin-bottom:6px;">
          <span class="ticket-id">#TKT-1095</span><span class="tag tag-dup">Duplicate</span>
        </div>
        <div class="ticket-body">"How do I reset my password?"</div>
        <div class="ticket-route">→ Auto-close + link: <strong style="color:#6c63ff;">docs/reset-password</strong></div>
      </div>
      <div class="ticket">
        <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:6px;margin-bottom:6px;">
          <span class="ticket-id">#TKT-1096</span><span class="tag tag-self">Self-serve</span>
        </div>
        <div class="ticket-body">"Can I export my data as CSV?"</div>
        <div class="ticket-route">→ Bot reply sent: <strong style="color:#6c63ff;">docs/data-export</strong></div>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<p style="text-align:center;font-size:12px;color:#8b8fa8;margin-top:32px;">Internal tooling demo · Not for external distribution</p>', unsafe_allow_html=True)
