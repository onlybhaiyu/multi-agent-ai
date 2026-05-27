from dotenv import load_dotenv

from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools import web_search, scrape_url

# Load environment variables
load_dotenv()

# =========================
# LLM Setup
# =========================

llm = ChatGroq(
    model="llama3-8b-8192",
    temperature=0,
    max_retries=2
)

# =========================
# Search Agent
# =========================

def build_search_agent():
    return create_react_agent(
        model=llm,
        tools=[web_search],
        name="search_agent"
    )

# =========================
# Reader Agent
# =========================

def build_reader_agent():
    return create_react_agent(
        model=llm,
        tools=[scrape_url],
        name="reader_agent"
    )

# =========================
# Writer Chain
# =========================

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert research writer. Write clear, structured, and insightful reports."
    ),

    (
        "human",
        """
Write a detailed research report on the topic below.

Topic:
{topic}

Research Gathered:
{research}

Structure the report as:

1. Introduction
2. Key Findings (minimum 3 detailed points)
3. Conclusion
4. Sources

Be detailed, factual, and professional.
"""
    ),
])

writer_chain = writer_prompt | llm | StrOutputParser()

# =========================
# Critic Chain
# =========================

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a sharp and constructive research critic. Be honest and specific."
    ),

    (
        "human",
        """
Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
...
"""
    ),
])

critic_chain = critic_prompt | llm | StrOutputParser()

# =========================
# Test
# =========================

if __name__ == "__main__":

    topic = "Future of Agentic AI"

    report = writer_chain.invoke({
        "topic": topic,
        "research": "Agentic AI systems can autonomously plan, reason, and use tools."
    })

    print("\n===== REPORT =====\n")
    print(report)

    critique = critic_chain.invoke({
        "report": report
    })

    print("\n===== CRITIQUE =====\n")
    print(critique)