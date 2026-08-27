import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from tools import scrape_url, web_search

load_dotenv()


def get_llm():
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY is not set in environment or .env file.")
    return ChatMistralAI(
        model="mistral-small-latest",
        temperature=0.1,
        max_retries=6,
        timeout=90,
    )


# Agent 1: Web Search Investigator
def build_search_agent():
    return create_agent(
        model=get_llm(),
        tools=[web_search],
    )


# Agent 2: Deep Document / Web Reader
def build_reader_agent():
    return create_agent(
        model=get_llm(),
        tools=[scrape_url],
    )


# Agent 3: Research Report Synthesis Chain
writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert technical research writer. Your task is to produce deep, "
        "well-structured, and factual reports based strictly on the provided research context.",
    ),
    (
        "human",
        """Write an exhaustive technical research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Format Requirements:
# Executive Overview
- Provide a high-level summary of the domain and recent developments.

# Key Technical Findings
- Minimum 4 detailed, distinct analytical findings with clear subheaders.

# Critical Implications & Challenges
- Highlight bottlenecks, industry hurdles, and future trends.

# Verified Sources & References
- List all unique URLs extracted during research.

Ensure tone is analytical, rigorous, and citation-backed.""",
    ),
])

writer_chain = writer_prompt | get_llm() | StrOutputParser()


# Agent 4: Evaluator / Critic Chain
critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a rigorous peer-review critic evaluating research reports. "
        "Judge technical depth, factual coherence, source attribution, and actionable value.",
    ),
    (
        "human",
        """Review the research report below:

Report:
{report}

Respond strictly in this markdown format:

### Peer Evaluation Score: X/10

**Strengths:**
- [Specific strength 1]
- [Specific strength 2]

**Gaps & Missing Context:**
- [Critical gap 1]
- [Critical gap 2]

**Verdict:**
[One concise summary paragraph of overall report quality and reliability]""",
    ),
])

critic_chain = critic_prompt | get_llm() | StrOutputParser()
