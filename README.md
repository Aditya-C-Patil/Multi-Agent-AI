## 🔬 ResearchMind · Autonomous Multi-Agent AI Research System

ResearchMind is an automated multi-stage research engine built with **LangChain**, **Mistral AI (`mistral-small-2506`)**, **Tavily AI Search**, and **BeautifulSoup4**. The system features both an interactive, dark-themed **Streamlit** dashboard and a standalone terminal execution pipeline (`Pipeline.py`).

Given any research topic, the pipeline autonomously executes live web search queries, scrapes and cleans body text from the most relevant source, drafts a structured technical briefing, and evaluates the final report with an objective critique and score.

---

## 🏗️ Architecture & Sequential Workflow

The research lifecycle processes data across two specialized agent loops and two structured LCEL chains:

```text
                           ┌────────────────────────┐
                           │  User Research Topic   │
                           └───────────┬────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. Search Agent (`build_search_agent`)                                      │
│    • Model: ChatMistralAI (`mistral-small-2506`)                            │
│    • Tool: `web_search` via Tavily API                                      │
│    • Retrieves top 5 verified web sources with titles, URLs, and snippets   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. Reader Agent (`build_reader_agent`)                                      │
│    • Model: ChatMistralAI (`mistral-small-2506`)                            │
│    • Tool: `scrape_url` via BeautifulSoup4                                  │
│    • Analyzes search results, selects the top URL, purges clutter           │
│      (<script>, <style>, <nav>, <footer>), and extracts 3,000 clean chars   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 3. Writer Chain (`writer_chain`)                                            │
│    • Chain: `ChatPromptTemplate` | `ChatMistralAI` | `StrOutputParser`      │
│    • Synthesizes search snippets + deep scraped body text into a formal     │
│      briefing: Introduction, Key Findings (≥3 points), Conclusion, Sources  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 4. Critic Chain (`critic_chain`)                                            │
│    • Chain: `ChatPromptTemplate` | `ChatMistralAI` | `StrOutputParser`      │
│    • Reviews the report: Score (/10), Strengths, Areas to Improve, Verdict  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                     ┌─────────────────┴─────────────────┐
                     ▼                                   ▼
        ┌─────────────────────────┐         ┌─────────────────────────┐
        │  Streamlit UI Dashboard │         │  Terminal / CLI Output  │
        │  (Interactive / Export) │         │      (Pipeline.py)      │
        └─────────────────────────┘         └─────────────────────────┘
```
## **📁Repository Structure**
├── tools.py            # Custom tool definitions (Tavily search & BeautifulSoup scraper)
├── Agents.py           # Agent constructors (Search & Reader) and LCEL chains (Writer & Critic)
├── Pipeline.py         # Terminal CLI research orchestration pipeline
├── app.py              # Streamlit web application with custom CSS & state handling
├── requirements.txt    # Python package dependencies
├── .gitignore          # Git ignore rules for virtual environments and credentials
└── README.md           # Project documentation
