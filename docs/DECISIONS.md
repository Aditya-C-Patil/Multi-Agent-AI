# Architectural Decisions & Technical Trade-Offs

## 1. Orchestration Topology: Deterministic Staged Pipeline vs. Unconstrained Agent Swarm
- **Decision:** Implemented a structured, sequential multi-agent execution pipeline (`Search Agent` → `Reader/DOM Extractor Agent` → `Synthesis Writer` → `Evaluator Critic`) rather than an open-ended cyclic agent swarm (e.g., unbounded AutoGen/CrewAI loops)[cite: 3, 4].
- **Rationale & Trade-Offs:**
  - Fully autonomous, unconstrained agent swarms frequently suffer from non-deterministic tool looping, unpredictable recursion depths, and token cost runaway.
  - A staged pipeline establishes strict input/output contracts between specialized nodes while granting autonomy to agents within their individual boundaries[cite: 3, 4].
  - Enforces reproducible, sub-15s response latency suitable for production UI interaction.

---

## 2. Scraping Resiliency & Noise Filtering Architecture
- **Decision:** Implemented a two-tier content extraction strategy combining custom DOM element decomposition (`script`, `style`, `nav`, `footer`, `header`, `noscript`, `aside`) with fallback extraction via the Tavily Extract API.
- **Rationale & Trade-Offs:**
  - Raw HTML contains excessive boilerplate (navigation trees, tracking scripts, and cookie banners) that pollutes the LLM context window and increases token consumption.
  - Standard HTTP GET requests often fail on JavaScript-heavy Single Page Applications (SPAs) or trigger 403 Forbidden responses.
  - Pre-filtering the DOM and maintaining an API-backed extraction fallback guarantees clean, high-density context for the downstream Writer agent without silent extraction failures.

---

## 3. Decoupling Synthesis from Evaluation (Critic Independence)
- **Decision:** Separated the Evaluator Critic into an independent prompt chain with an explicit, structured rubric (Score, Strengths, Gaps, Verdict) rather than combining writing and self-critique in a single prompt[cite: 2].
- **Rationale & Trade-Offs:**
  - Large Language Models exhibit notable self-concurrence bias when tasked with evaluating their own drafts within the same conversational thread.
  - Decoupling the Critic persona into a separate inference call ensures impartial scoring, strict rubric enforcement, and actionable feedback generation[cite: 2, 3].

---

## 4. API Resilience & Rate Limit Recovery
- **Decision:** Configured `ChatMistralAI` with `max_retries=6`, timeout constraints, and temperature isolation (`0.1` for factual synthesis and evaluation)[cite: 2].
- **Rationale & Trade-Offs:**
  - Intensive multi-agent workflows issue multiple rapid API calls across tool invocations and generation chains[cite: 3, 4].
  - Built-in exponential backoff handles transient upstream server overloads (HTTP 503) and rate limits (HTTP 429) without crashing the user session[cite: 2].

---

## 5. Architectural Roadmap: Conditional Reflection State Machine
- **Current Implementation:** A single-pass feed-forward execution designed to optimize response time (< 15s) and prevent token exhaustion on free/starter tiers.
- **Future Scope:** Transitioning the pipeline into a LangGraph state graph with conditional feedback loops:
  - **Threshold-Driven Self-Correction:** If the Critic's parsed score falls below `8.0/10`, the system routes the identified "Gaps & Missing Context" back as revision vectors.
  - **Dynamic Re-Querying:** When information absence is flagged, the pipeline routes missing sub-queries back to Node 01 (Search) to retrieve secondary documentation before rewriting.
  - **Loop Termination Guardrail:** Enforcing a hard cap (`max_revisions = 2`) to ensure deterministic termination and avoid infinite execution loops.
