"""
╔══════════════════════════════════════════════════════════════════╗
║         ResearchMind · Multi-Agent AI Research System            ║
║         UI: Streamlit  |  LLM: Groq  |  Search: Tavily          ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ─────────────────────────────────────────────────────────────────
# PAGE CONFIG — must be the very first Streamlit call
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #e8e4dc;
}

.stApp {
    background: #0a0a0f;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(255,140,50,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(255,80,30,0.08) 0%, transparent 55%);
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1200px; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
    position: relative;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #ff8c32;
    margin-bottom: 1rem;
    opacity: 0.9;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 6vw, 5rem);
    font-weight: 800;
    line-height: 1.0;
    letter-spacing: -0.03em;
    color: #f0ebe0;
    margin: 0 0 1rem;
}
.hero h1 span { color: #ff8c32; }
.hero-sub {
    font-size: 1.05rem;
    font-weight: 300;
    color: #a09890;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.65;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,140,50,0.3), transparent);
    margin: 2rem 0;
}

/* ── Input card ── */
.input-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,140,50,0.15);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    backdrop-filter: blur(8px);
}

/* ── Text input — normal state ── */
.stTextInput > div > div > input {
    background: #13131a !important;
    border: 1px solid rgba(255,140,50,0.25) !important;
    border-radius: 10px !important;
    color: #f0ebe0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    caret-color: #f0ebe0 !important;
    /* Prevent any light background leaking through */
    filter: none !important;
}
.stTextInput > div > div > input:focus {
    background: #13131a !important;
    border-color: #ff8c32 !important;
    box-shadow: 0 0 0 3px rgba(255,140,50,0.12) !important;
    color: #f0ebe0 !important;
}
.stTextInput > div > div > input::placeholder {
    color: #4a4540 !important;
    opacity: 1 !important;
}

/* ── Streamlit input wrapper background ── */
.stTextInput > div > div {
    background: #13131a !important;
    border-radius: 10px !important;
}
[data-baseweb="input"] {
    background: #13131a !important;
}
[data-baseweb="base-input"] {
    background: #13131a !important;
}

/* ── BULLETPROOF autofill fix — Chrome/Edge/Safari ── */
/* Chrome uses -webkit-autofill; the inset shadow is the only reliable override */
.stTextInput input:-webkit-autofill,
.stTextInput input:-webkit-autofill:hover,
.stTextInput input:-webkit-autofill:focus,
.stTextInput input:-webkit-autofill:active {
    -webkit-text-fill-color: #f0ebe0 !important;
    -webkit-box-shadow: 0 0 0px 9999px #13131a inset !important;
    box-shadow: 0 0 0px 9999px #13131a inset !important;
    background-color: #13131a !important;
    caret-color: #f0ebe0 !important;
    transition: background-color 86400s ease 0s, color 86400s ease 0s !important;
}
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
input:-webkit-autofill:active,
input:-internal-autofill-selected {
    -webkit-text-fill-color: #f0ebe0 !important;
    -webkit-box-shadow: 0 0 0px 9999px #13131a inset !important;
    box-shadow: 0 0 0px 9999px #13131a inset !important;
    background-color: #13131a !important;
    caret-color: #f0ebe0 !important;
    transition: background-color 86400s ease 0s, color 86400s ease 0s !important;
}

/* ── Label ── */
.stTextInput > label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #ff8c32 !important;
    font-weight: 500 !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #ff8c32 0%, #ff5a1a 100%) !important;
    color: #0a0a0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 2.2rem !important;
    cursor: pointer !important;
    transition: transform 0.15s, box-shadow 0.15s, opacity 0.15s !important;
    box-shadow: 0 4px 20px rgba(255,140,50,0.3) !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(255,140,50,0.4) !important;
    opacity: 0.95 !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Download button (subtle variant) ── */
.stDownloadButton > button {
    background: rgba(255,140,50,0.1) !important;
    color: #ff8c32 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.08em !important;
    border: 1px solid rgba(255,140,50,0.3) !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.2rem !important;
    box-shadow: none !important;
    transition: background 0.2s, border-color 0.2s !important;
    width: auto !important;
}
.stDownloadButton > button:hover {
    background: rgba(255,140,50,0.18) !important;
    border-color: rgba(255,140,50,0.5) !important;
    transform: none !important;
}

/* ── Pipeline step cards ── */
.step-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
.step-card.active {
    border-color: rgba(255,140,50,0.4);
    background: rgba(255,140,50,0.04);
}
.step-card.done {
    border-color: rgba(80,200,120,0.3);
    background: rgba(80,200,120,0.03);
}
.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    border-radius: 14px 0 0 14px;
    background: rgba(255,255,255,0.05);
    transition: background 0.3s;
}
.step-card.active::before { background: #ff8c32; }
.step-card.done::before   { background: #50c878; }

.step-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 0.3rem;
}
.step-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    color: #ff8c32;
    opacity: 0.7;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: #f0ebe0;
}
.step-status { margin-left: auto; font-family: 'DM Mono', monospace; font-size: 0.68rem; letter-spacing: 0.1em; }
.status-waiting { color: #555; }
.status-running { color: #ff8c32; }
.status-done    { color: #50c878; }

/* ── Result panels ── */
.result-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.8rem 2rem;
    margin-top: 1rem;
    margin-bottom: 1.5rem;
}
.result-panel-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #ff8c32;
    margin-bottom: 1rem;
    padding-bottom: 0.7rem;
    border-bottom: 1px solid rgba(255,140,50,0.15);
}
.result-content {
    font-size: 0.92rem;
    line-height: 1.8;
    color: #f0ebe0;
    white-space: pre-wrap;
    font-family: 'DM Sans', sans-serif;
}

/* ── Report & feedback panels ── */
.report-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,140,50,0.2);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-top: 1rem;
}
.feedback-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(80,200,120,0.2);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-top: 1rem;
}
.panel-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    padding-bottom: 0.7rem;
}
.panel-label.orange { color: #ff8c32; border-bottom: 1px solid rgba(255,140,50,0.15); }
.panel-label.green  { color: #50c878; border-bottom: 1px solid rgba(80,200,120,0.15); }

/* ── Report markdown typography ── */
.report-panel h1, .report-panel h2, .report-panel h3 {
    font-family: 'Syne', sans-serif !important;
    color: #f0ebe0 !important;
}
.report-panel p, .report-panel li {
    color: #f0ebe0 !important;
    line-height: 1.8 !important;
}
.feedback-panel p, .feedback-panel li,
.feedback-panel strong, .feedback-panel em,
.feedback-panel h1, .feedback-panel h2, .feedback-panel h3 {
    color: #f0ebe0 !important;
    line-height: 1.8 !important;
}
.feedback-panel h1, .feedback-panel h2, .feedback-panel h3 {
    color: #ffffff !important;
    font-family: 'Syne', sans-serif !important;
}

/* ── Streamlit markdown global — catches output rendered outside custom divs ── */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span,
[data-testid="stMarkdownContainer"] td,
[data-testid="stMarkdownContainer"] th,
[data-testid="stMarkdownContainer"] blockquote,
[data-testid="stMarkdownContainer"] em {
    color: #f0ebe0 !important;
    line-height: 1.8 !important;
}
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4 {
    color: #ffffff !important;
    font-family: 'Syne', sans-serif !important;
}
[data-testid="stMarkdownContainer"] strong {
    color: #ffffff !important;
    font-weight: 700 !important;
}
[data-testid="stMarkdownContainer"] code {
    color: #ff8c32 !important;
    background: rgba(255,140,50,0.1) !important;
    border-radius: 4px !important;
    padding: 1px 5px !important;
}

/* ── Spinner ── */
.stSpinner > div { color: #ff8c32 !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    color: #a09890 !important;
    letter-spacing: 0.1em !important;
    background: rgba(255,255,255,0.03) !important;
    border-radius: 8px !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
}

/* ── Section heading ── */
.section-heading {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #f0ebe0;
    margin: 2rem 0 1rem;
}

/* ── Footer ── */
.notice {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #605850;
    text-align: center;
    margin-top: 3rem;
    letter-spacing: 0.08em;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #2a2520; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #ff8c3244; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# HELPER: render a pipeline step card
# ─────────────────────────────────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING",    "status-waiting"),
        "running": ("● RUNNING",  "status-running"),
        "done":    ("✓ DONE",     "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    desc_html = (
        f"<div style='font-size:0.82rem;color:#706860;margin-top:0.3rem;'>{desc}</div>"
        if desc else ""
    )
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {desc_html}
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────────────────────────
for key, default in [("results", {}), ("running", False), ("done", False), ("current_step", 0)]:
    if key not in st.session_state:
        st.session_state[key] = default


# ─────────────────────────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent AI System · LangGraph + Groq + Tavily</div>
    <h1>Research<span>Mind</span></h1>
    <p class="hero-sub">
        Four specialised AI agents collaborate — searching, scraping, writing,
        and critiquing — to deliver a polished research report on any topic.
    </p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# LAYOUT: input (left) | pipeline status (right)
# ─────────────────────────────────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
        label_visibility="visible",
    )

    run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Example chip row ──
    st.markdown("""
    <div style="display:flex;align-items:center;gap:0.5rem;flex-wrap:wrap;margin-bottom:1.5rem;">
        <span style="font-family:'DM Mono',monospace;font-size:0.68rem;
            color:#605850;letter-spacing:0.1em;">TRY →</span>
        <span style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
            border-radius:6px;padding:0.25rem 0.7rem;font-size:0.75rem;
            color:#a09890;font-family:'DM Sans',sans-serif;">LLM agents 2025</span>
        <span style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
            border-radius:6px;padding:0.25rem 0.7rem;font-size:0.75rem;
            color:#a09890;font-family:'DM Sans',sans-serif;">CRISPR gene editing</span>
        <span style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
            border-radius:6px;padding:0.25rem 0.7rem;font-size:0.75rem;
            color:#a09890;font-family:'DM Sans',sans-serif;">Fusion energy progress</span>
    </div>
    """, unsafe_allow_html=True)

with col_pipeline:
    st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)

    r = st.session_state.results

    # Determine each step's display state using explicit current_step tracker
    step_order = ["search", "reader", "writer", "critic"]
    def get_state(step: str) -> str:
        if step in r:
            return "done"
        if st.session_state.running:
            idx = step_order.index(step)
            if idx == st.session_state.current_step:
                return "running"
        return "waiting"

    step_card("01", "Search Agent",  get_state("search"), "Gathers recent web information via Tavily")
    step_card("02", "Reader Agent",  get_state("reader"), "Scrapes & extracts deep content from top URL")
    step_card("03", "Writer Chain",  get_state("writer"), "Drafts the full structured research report")
    step_card("04", "Critic Chain",  get_state("critic"), "Reviews accuracy, depth & scores the report")


# ─────────────────────────────────────────────────────────────────
# TRIGGER: button press → reset state and rerun into pipeline block
# ─────────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("⚠️  Please enter a research topic first.")
    else:
        st.session_state.results      = {}
        st.session_state.running      = True
        st.session_state.done         = False
        st.session_state.current_step = 0   # reset step pointer
        st.rerun()


# ─────────────────────────────────────────────────────────────────
# PIPELINE EXECUTION
# Each step sets current_step, saves its result, then calls st.rerun()
# so the pipeline column re-renders and shows the correct RUNNING card.
# On next rerun, current_step is already advanced → next step runs.
# ─────────────────────────────────────────────────────────────────
if st.session_state.running and not st.session_state.done:

    topic_val    = st.session_state.topic_input
    results      = dict(st.session_state.results)   # carry over completed steps
    current_step = st.session_state.current_step

    # ── Step 0 → Search Agent ────────────────────────────────────
    if current_step == 0 and "search" not in results:
        with st.spinner("🔍  Search Agent is scanning the web…"):
            search_agent = build_search_agent()
            sr = search_agent.invoke({
                "messages": [("user",
                    f"Find recent, reliable and detailed information about: {topic_val}"
                )]
            })
            results["search"] = sr["messages"][-1].content
        st.session_state.results      = results
        st.session_state.current_step = 1          # advance → Reader is now RUNNING
        st.rerun()

    # ── Step 1 → Reader Agent ────────────────────────────────────
    elif current_step == 1 and "reader" not in results:
        with st.spinner("📄  Reader Agent is scraping top resources…"):
            reader_agent = build_reader_agent()
            rr = reader_agent.invoke({
                "messages": [("user",
                    f"Based on the following search results about '{topic_val}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{results['search'][:800]}"
                )]
            })
            results["reader"] = rr["messages"][-1].content
        st.session_state.results      = results
        st.session_state.current_step = 2          # advance → Writer is now RUNNING
        st.rerun()

    # ── Step 2 → Writer Chain ────────────────────────────────────
    elif current_step == 2 and "writer" not in results:
        with st.spinner("✍️  Writer is drafting the research report…"):
            research_combined = (
                f"SEARCH RESULTS:\n{results['search']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
            )
            results["writer"] = writer_chain.invoke({
                "topic":    topic_val,
                "research": research_combined,
            })
        st.session_state.results      = results
        st.session_state.current_step = 3          # advance → Critic is now RUNNING
        st.rerun()

    # ── Step 3 → Critic Chain ────────────────────────────────────
    elif current_step == 3 and "critic" not in results:
        with st.spinner("🧐  Critic is reviewing and scoring the report…"):
            results["critic"] = critic_chain.invoke({
                "report": results["writer"]
            })
        st.session_state.results      = results
        st.session_state.current_step = 4          # all done
        st.session_state.running      = False
        st.session_state.done         = True
        st.rerun()



# ─────────────────────────────────────────────────────────────────
# RESULTS DISPLAY
# ─────────────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    # ── Raw outputs in collapsible expanders ──
    if "search" in r:
        with st.expander("🔍  Search Results (raw output)", expanded=False):
            st.markdown(
                f'<div class="result-panel">'
                f'<div class="result-panel-title">Search Agent Output</div>'
                f'<div class="result-content">{r["search"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    if "reader" in r:
        with st.expander("📄  Scraped Content (raw output)", expanded=False):
            st.markdown(
                f'<div class="result-panel">'
                f'<div class="result-panel-title">Reader Agent Output</div>'
                f'<div class="result-content">{r["reader"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # ── Final report ──
    if "writer" in r:
        st.markdown(
            '<div class="report-panel">'
            '<div class="panel-label orange">📝  Final Research Report</div>',
            unsafe_allow_html=True,
        )
        st.markdown(r["writer"])   # render as native Markdown
        st.markdown("</div>", unsafe_allow_html=True)

        # Download button
        st.download_button(
            label="⬇  Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    # ── Critic feedback ──
    if "critic" in r:
        st.markdown(
            '<div class="feedback-panel">'
            '<div class="panel-label green">🧐  Critic Feedback</div>',
            unsafe_allow_html=True,
        )
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    ResearchMind · Powered by LangGraph multi-agent pipeline · LangChain · Groq · Tavily · Streamlit
</div>
""", unsafe_allow_html=True)
