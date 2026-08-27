# ResearchMind: Multi-Agent Deep Research & Synthesis Engine

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/Orchestration-LangChain-green.svg)](https://python.langchain.com/)
[![LLM: Mistral AI](https://img.shields.io/badge/LLM-Mistral%20AI-orange.svg)](https://mistral.ai/)
[![Search: Tavily](https://img.shields.io/badge/Search-Tavily%20API-lightblue.svg)](https://tavily.com/)
[![UI: Streamlit](https://img.shields.io/badge/Interface-Streamlit-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An autonomous multi-agent research architecture built with **LangChain**, **Mistral AI**, **Tavily API**, and **Streamlit**. Orchestrates specialized, decoupled AI agents to discover, extract, synthesize, and rigorously peer-review technical research reports on complex directives.

---

## 🏛️ System Architecture

```text
                   [ User Research Directive ]
                                │
                                ▼
   ┌──────────────────────────────────────────────────────────┐
   │                Agent 01: Web Discovery                  │
   │  • Query refinement & targeted entity extraction         │
   │  • Tavily Web Search API (Snippets, Titles, URLs)        │
   └────────────────────────────┬─────────────────────────────┘
                                │
                                ▼
   ┌──────────────────────────────────────────────────────────┐
   │                Agent 02: DOM Extractor                   │
   │  • Evaluates top authoritative technical URL             │
   │  • HTML tag decomposition (`script`, `style`, `nav`, etc) │
   │  • Fallback to Tavily Extract for JS-heavy SPAs          │
   └────────────────────────────┬─────────────────────────────┘
                                │
                                ▼
   ┌──────────────────────────────────────────────────────────┐
   │               Agent 03: Synthesis Writer                 │
   │  • Context synthesis across discovery snippets & DOM     │
   │  • Generates structured markdown report + citations      │
   └────────────────────────────┬─────────────────────────────┘
                                │
                                ▼
   ┌──────────────────────────────────────────────────────────┐
   │                Agent 04: Evaluator Critic                │
   │  • Blind peer review scoring rubric (1–10)               │
   │  • Strengths, technical gaps, and verdict extraction     │
   └──────────────────────────────────────────────────────────┘
```

---

## ⚡ Key Architectural Capabilities

* **Staged Multi-Agent Pipeline:** Divides research tasks into specialized, single-responsibility agents (Search, Extraction, Synthesis, Evaluation) to prevent prompt clutter and hallucination loops.
* **Deterministic Noise Reduction:** Automatically decomposes boilerplate DOM elements (`script`, `style`, `nav`, `footer`, `header`, `noscript`, `aside`) to maximize LLM context density.
* **Dual-Tier Web Extraction:** Direct HTTP request parsing with automatic fallback to headless Tavily extraction for protected or SPA pages.
* **Unbiased Critic Chain:** Decouples synthesis from evaluation into an independent LLM prompt chain to prevent self-concurrence bias.
* **Resilient LLMOps Setup:** Configured with exponential backoff retries (`max_retries=6`) and HTTP timeout protections.
* **Cybernetic Glassmorphism HUD:** Real-time telemetry dashboard featuring token synthesis counts, latency monitoring, and multi-view execution tabs.

---

## 📂 Repository Structure

```text
├── docs/
|   └── DECISIONS.md    # Architectural Decisions & Technical Trade-Offs
|
├── .env.example        # Template for API keys (MISTRAL_API_KEY, TAVILY_API_KEY)
├── .gitignore          # Git exclusion rules for virtual environments & credentials
├── Agents.py           # Multi-agent definitions, chains, and LLM orchestration
├── app.py              # Streamlit dashboard interface & interactive execution flow
├── LICENSE             # Project distribution license (MIT)
├── pipeline.py         # Headless CLI research execution harness
├── requirements.txt    # Production Python dependencies
├── tools.py            # Tavily Web Search and DOM text extraction tools
├── DECISIONS.md        # Architecture decisions, failure modes & future reflection scope
└── README.md           # System documentation & quickstart
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Aditya-C-Patil/Multi-Agent.git
cd Multi-Agent
```

### 2. Set Up Virtual Environment

```bash
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On Linux/macOS
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Keys

Create a `.env` file in the root directory:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 5. Launch the Application

**Streamlit Web UI:**

```bash
streamlit run app.py
```

**CLI Pipeline Mode:**

```bash
python pipeline.py
```

---

## 📊 Evaluation & Output Structure

Each research cycle generates:

1. **Executive Technical Brief:** In-depth overview, key architectural findings, critical implications, and verified source references.
2. **Peer Review Rubric:** Numeric grade (`X/10`), itemized technical strengths, identified gaps, and actionable summary verdict.
3. **Audit Trail:** Raw search result payloads and stripped DOM text context for full inspection.

---

## 📜 Architectural Decisions

For a detailed breakdown of architectural decisions, failure handling strategies, and future reflection loop plans, refer to [`DECISIONS.md`](DECISIONS.md).
