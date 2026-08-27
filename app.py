import time
import streamlit as st
from Agents import build_reader_agent, build_search_agent, critic_chain, writer_chain

# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind // Autonomous Agent Swarm",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Dark Amber & Cyberpunk Aesthetic ─────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

:root {
    --bg: #07090e;
    --surface: rgba(18, 22, 34, 0.65);
    --border: rgba(255, 140, 50, 0.2);
    --border-glow: rgba(255, 140, 50, 0.55);
    --amber: #ff8c32;
    --amber-bright: #ffa756;
    --emerald: #10b981;
    --text-high: #f8fafc;
    --text-mid: #94a3b8;
    --text-muted: #64748b;
}

* { font-family: 'Plus Jakarta Sans', sans-serif; }
h1, h2, h3, .brand-title { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -0.02em; }
code, pre, .mono { font-family: 'JetBrains Mono', monospace !important; }

.stApp {
    background-color: var(--bg) !important;
    color: var(--text-high) !important;
}

/* Ambient Radial Lighting */
.stApp::before {
    content: '';
    position: fixed;
    top: -50%; left: -50%; width: 200%; height: 200%;
    background: radial-gradient(circle at 80% 15%, rgba(255, 140, 50, 0.12) 0%, transparent 45%),
                radial-gradient(circle at 15% 85%, rgba(239, 68, 68, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 50% 50%, rgba(16, 185, 129, 0.04) 0%, transparent 50%);
    pointer-events: none; z-index: 0;
}

/* Glassmorphism Card */
.glass-card {
    background: var(--surface);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 12px 36px 0 rgba(0, 0, 0, 0.45);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.glass-card:hover {
    border-color: var(--border-glow);
    box-shadow: 0 14px 40px -10px rgba(255, 140, 50, 0.22);
}

.hero-title {
    background: linear-gradient(135deg, #ffffff 0%, #fed7aa 40%, var(--amber) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: clamp(2.4rem, 4.5vw, 3.6rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    margin-bottom: 0.3rem;
}

.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--amber);
    margin-bottom: 0.5rem;
}

/* Custom Step Card */
.step-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 14px;
    padding: 1.1rem 1.4rem;
    margin-bottom: 0.85rem;
    position: relative;
    transition: all 0.3s ease;
}
.step-card.active {
    border-color: var(--border-glow);
    background: rgba(255, 140, 50, 0.06);
    box-shadow: 0 0 20px rgba(255, 140, 50, 0.15);
}
.step-card.done {
    border-color: rgba(16, 185, 129, 0.4);
    background: rgba(16, 185, 129, 0.04);
}
.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3.5px;
    border-radius: 14px 0 0 14px;
    background: rgba(255, 255, 255, 0.08);
}
.step-card.active::before { background: var(--amber); }
.step-card.done::before   { background: var(--emerald); }

.step-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.step-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: var(--amber);
    font-weight: 700;
}
.step-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.92rem;
    font-weight: 700;
    color: var(--text-high);
}
.step-status {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.08em;
}

/* Interactive Action Buttons */
.stButton > button {
    background: linear-gradient(135deg, #ff8c32 0%, #ea580c 100%) !important;
    color: #000000 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 800 !important;
    font-size: 0.95rem !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 0.75rem 2rem !important;
    letter-spacing: 0.04em !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 20px rgba(255, 140, 50, 0.35) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) scale(1.01) !important;
    box-shadow: 0 8px 30px rgba(255, 140, 50, 0.55) !important;
}

/* Metric Display Strip */
.stat-pill {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.75rem 1.2rem;
    text-align: center;
}
.stat-value {
    font-size: 1.35rem;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    color: #ffffff;
}
.stat-label {
    font-size: 0.7rem;
    color: var(--text-mid);
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
</style>
""",
    unsafe_allow_html=True,
)


# ─── Helper Functions & Callbacks ─────────────────────────────────────────────
def render_step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING", "#52525b"),
        "running": ("● RUNNING", "#ff8c32"),
        "done": ("✓ COMPLETED", "#10b981"),
    }
    label, color = status_map.get(state, ("WAITING", "#52525b"))
    st.markdown(
        f"""
    <div class="step-card {state}">
        <div class="step-header">
            <div>
                <span class="step-num">{num}</span>&nbsp;&nbsp;
                <span class="step-title">{title}</span>
            </div>
            <span class="step-status" style="color:{color};">{label}</span>
        </div>
        {"<div style='font-size:0.78rem; color:#808b96; margin-top:0.35rem;'>"+desc+"</div>" if desc else ""}
    </div>
    """,
        unsafe_allow_html=True,
    )


def select_suggested_topic(topic_text: str):
    st.session_state["topic_field"] = topic_text


# ─── Session State Initialization ─────────────────────────────────────────────
if "topic_field" not in st.session_state:
    st.session_state["topic_field"] = ""
if "results" not in st.session_state:
    st.session_state.results = None
if "active_step" not in st.session_state:
    st.session_state.active_step = "waiting"

# ─── Hero Banner ──────────────────────────────────────────────────────────────
st.markdown('<div class="hero-eyebrow">⚡ MULTI-AGENT INTELLIGENCE MATRIX</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">ResearchMind OS</div>', unsafe_allow_html=True)
st.markdown(
    '<div style="color:var(--text-mid); font-size:1rem; max-width:650px; margin-bottom:2rem; line-height:1.6;">'
    "Four specialized autonomous agents collaborate in a sequential cognitive pipeline to discover, scrape, "
    "synthesize, and rigorously peer-review technical research."
    "</div>",
    unsafe_allow_html=True,
)

# ─── Main Interface Grid ──────────────────────────────────────────────────────
col_input, col_pipeline = st.columns([5, 4], gap="large")

with col_input:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Directive or Technical Query",
        placeholder="e.g. Post-Quantum Cryptography implementations & NIST standards",
        key="topic_field",
    )

    st.write("")
    run_btn = st.button("🚀 EXECUTE AUTONOMOUS AGENT SWARM", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Example Topics via safe on_click callbacks
    st.markdown(
        """
    <div style="font-size:0.72rem; color:var(--text-muted); font-family:JetBrains Mono; margin-bottom:0.6rem; letter-spacing:0.1em;">
        SUGGESTED VECTORS:
    </div>
    """,
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        st.button(
            "⚛️ Quantum Computing 2026",
            use_container_width=True,
            on_click=select_suggested_topic,
            args=("Quantum Computing breakthrough implementations 2026",),
        )
    with c2:
        st.button(
            "🧬 CRISPR Gene Therapies",
            use_container_width=True,
            on_click=select_suggested_topic,
            args=("Recent CRISPR Cas-9 clinical trial results and breakthroughs",),
        )
    with c3:
        st.button(
            "⚡ Nuclear Fusion Net Gain",
            use_container_width=True,
            on_click=select_suggested_topic,
            args=("Magnetic confinement fusion energy milestones",),
        )

with col_pipeline:
    st.markdown(
        '<div style="font-family:Space Grotesk; font-size:1.1rem; font-weight:700; color:white; margin-bottom:1rem;">Agent Pipeline Status</div>',
        unsafe_allow_html=True,
    )

    current_state = st.session_state.active_step
    render_step_card("01", "Discovery Agent", "done" if current_state in ["reader", "writer", "critic", "complete"] else ("running" if current_state == "search" else "waiting"), "Queries Tavily Web API for authoritative sources")
    render_step_card("02", "DOM Extractor Agent", "done" if current_state in ["writer", "critic", "complete"] else ("running" if current_state == "reader" else "waiting"), "Scrapes & parses full-length technical content")
    render_step_card("03", "Synthesis Writer", "done" if current_state in ["critic", "complete"] else ("running" if current_state == "writer" else "waiting"), "Compiles exhaustive markdown report with citations")
    render_step_card("04", "Peer Review Critic", "done" if current_state == "complete" else ("running" if current_state == "critic" else "waiting"), "Evaluates factual density, scoring from 1-10")

# ─── Pipeline Execution Coordinator ───────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please provide a research directive before launching agents.")
    else:
        status_box = st.status("⚡ Agents initialized. Processing...", expanded=True)
        try:
            t0 = time.time()

            # Step 1: Search Discovery
            with status_box:
                st.session_state.active_step = "search"
                st.write("🔍 **Agent 01 (Discovery)** querying Tavily API for technical literature...")
                search_agent = build_search_agent()
                sr = search_agent.invoke({
                    "messages": [("user", f"Find recent, reliable, and detailed technical information and URLs on: {topic}")]
                })
                search_out = sr["messages"][-1].content

                # Step 2: DOM Reader
                st.session_state.active_step = "reader"
                st.write("📄 **Agent 02 (DOM Extractor)** scraping primary technical sources...")
                reader_agent = build_reader_agent()
                rr = reader_agent.invoke({
                    "messages": [(
                        "user",
                        f"From these search results on '{topic}', select the most authoritative technical URL and scrape it for full context:\n\n{search_out[:1200]}",
                    )]
                })
                reader_out = rr["messages"][-1].content

                # Step 3: Synthesis Writer
                st.session_state.active_step = "writer"
                st.write("✍️ **Agent 03 (Synthesis Writer)** drafting exhaustive research brief...")
                research_combined = f"SEARCH DISCOVERY:\n{search_out}\n\nSCRAPED DOCUMENTATION:\n{reader_out}"
                report_out = writer_chain.invoke({"topic": topic, "research": research_combined})

                # Step 4: Critic Chain
                st.session_state.active_step = "critic"
                st.write("🧐 **Agent 04 (Critic)** conducting blind peer review & rubric scoring...")
                critic_out = critic_chain.invoke({"report": report_out})

                elapsed = round(time.time() - t0, 2)
                st.session_state.active_step = "complete"
                status_box.update(label=f"✅ Multi-Agent Pipeline Completed in {elapsed}s!", state="complete", expanded=False)

                st.session_state.results = {
                    "topic": topic,
                    "search": search_out,
                    "reader": reader_out,
                    "report": report_out,
                    "critic": critic_out,
                    "word_count": len(report_out.split()),
                    "elapsed": elapsed,
                }
                st.rerun()

        except Exception as e:
            st.session_state.active_step = "waiting"
            status_box.update(label=f"❌ Execution Error: {e}", state="error", expanded=True)
            st.error(str(e))

# ─── Results & Intelligence Dashboard ─────────────────────────────────────────
if st.session_state.results:
    res = st.session_state.results
    st.markdown("---")

    # Real-Time Telemetry Ribbon
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="stat-pill"><div class="stat-value">{res["word_count"]}</div><div class="stat-label">Words Generated</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="stat-pill"><div class="stat-value">{res["elapsed"]}s</div><div class="stat-label">Pipeline Latency</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="stat-pill"><div class="stat-value" style="color:var(--amber);">4/4</div><div class="stat-label">Agents Coordinated</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown('<div class="stat-pill"><div class="stat-value" style="color:var(--emerald);">REVIEWED</div><div class="stat-label">Critic Verdict</div></div>', unsafe_allow_html=True)

    st.write("")

    tab_report, tab_critic, tab_scraped, tab_search = st.tabs([
        "📝 Executive Technical Report",
        "🧐 Critic Peer Review",
        "📄 Extracted Web Context",
        "🔍 Discovery Raw Stream",
    ])

    with tab_report:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(res["report"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            label="⬇ Export Master Markdown Brief (.md)",
            data=res["report"],
            file_name=f"research_mind_{int(time.time())}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with tab_critic:
        st.markdown('<div class="glass-card" style="border-left: 3px solid #10b981;">', unsafe_allow_html=True)
        st.markdown(res["critic"])
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_scraped:
        st.text_area("DOM Content (Cleaned & De-noised)", value=res["reader"], height=350, disabled=True)

    with tab_search:
        st.text_area("Tavily Search Snippets", value=res["search"], height=350, disabled=True)
