import time
from Agents import build_reader_agent, build_search_agent, critic_chain, writer_chain


def run_research_pipeline(topic: str) -> dict:
    if not topic or not topic.strip():
        raise ValueError("Topic cannot be empty.")

    t0 = time.time()
    state = {"topic": topic.strip(), "steps": {}}

    # Step 1: Search Agent
    print(f"\n{'='*50}\nStep 1: Search Agent Investigating...\n{'='*50}")
    search_agent = build_search_agent()
    search_res = search_agent.invoke({
        "messages": [("user", f"Find recent, authoritative technical information and key sources about: {topic}")]
    })
    state["search_results"] = search_res["messages"][-1].content
    state["steps"]["search"] = "completed"

    # Step 2: Reader Agent
    print(f"\n{'='*50}\nStep 2: Reader Agent Scraping Primary Source...\n{'='*50}")
    reader_agent = build_reader_agent()
    reader_res = reader_agent.invoke({
        "messages": [(
            "user",
            f"From these search results on '{topic}', identify the most authoritative URL and scrape it for full technical depth:\n\n"
            f"{state['search_results'][:1200]}",
        )]
    })
    state["scraped_content"] = reader_res["messages"][-1].content
    state["steps"]["reader"] = "completed"

    # Step 3: Writer Chain
    print(f"\n{'='*50}\nStep 3: Writer Drafting Research Synthesis...\n{'='*50}")
    research_combined = (
        f"SEARCH SNIPPETS & SOURCES:\n{state['search_results']}\n\n"
        f"DEEP SCRAPED CONTENT:\n{state['scraped_content']}"
    )
    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined,
    })
    state["steps"]["writer"] = "completed"

    # Step 4: Critic Chain
    print(f"\n{'='*50}\nStep 4: Critic Reviewing Report Quality...\n{'='*50}")
    state["feedback"] = critic_chain.invoke({"report": state["report"]})
    state["steps"]["critic"] = "completed"

    state["elapsed_time"] = round(time.time() - t0, 2)
    return state


if __name__ == "__main__":
    user_topic = input("\nEnter research topic: ").strip()
    if user_topic:
        res = run_research_pipeline(user_topic)
        print("\n--- FINAL REPORT ---\n", res["report"])
        print("\n--- CRITIC REVIEW ---\n", res["feedback"])
