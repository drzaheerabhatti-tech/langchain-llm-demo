# chunkbuddy_graph.py
# ---------------------------------------------------------------------------
# This file defines the core LangGraph workflow for ChunkBuddy.
# It wires together multiple nodes (explanation → chunking → questions → summary)
# into a Directed Acyclic Graph (DAG). Both the CLI harness, Streamlit UI,
# and evaluation script reuse this graph.
# ---------------------------------------------------------------------------

# --- Imports & environment bootstrap ---------------------------------------
# Environment loading is kept in a helper (load_env.py) so all scripts
# share the same configuration (API keys, tracing, project name).
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from load_env import load_env

# Load API keys and other config from .env into process environment.
# This happens once, at import time, so everything below can assume
# OPENAI_API_KEY / LANGCHAIN_API_KEY are available.
load_env()

# --- LLM configuration ------------------------------------------------------
# Single shared LLM instance used by all graph nodes.
# Using gpt-4o-mini keeps the demo fast and inexpensive while still
# being strong enough for explanation, chunking, and question generation.
llm = ChatOpenAI(
    model="gpt-4o-mini",
    # temperature controls creativity vs determinism:
    # 0.0 = very predictable, 1.0 = very creative.
    # 0.5 is a balanced setting: clear, consistent explanations
    # with a bit of variation so it doesn't feel robotic.
    temperature=0.5,
)

# --- Shared State Definition ------------------------------------------------
# This TypedDict defines the fields that flow through the graph.
# Each node reads/writes only the fields it owns; LangGraph merges them.
class LearningState(TypedDict, total=False):
    topic: str                   # e.g. "Kafka partitions"
    level: str                   # e.g. "beginner" or "intermediate"
    raw_explanation: str         # one coherent explanation
    chunks: List[str]            # list of chunked explanations
    check_questions: List[str]   # list of questions
    summary: str                 # one-sentence TL;DR
    meta: dict                   # optional metadata (learning design notes, counts)

# --- Node 1: draft_explanation ----------------------------------------------
# Generates a level-appropriate explanation of the topic.
# Input: topic, level
# Output: raw_explanation
def draft_explanation(state: LearningState) -> dict:
    print("\n>>> draft_explanation received state:", state)
    topic = state.get("topic", "a technical topic")
    level = state.get("level", "beginner")

    prompt = f"""
You are a friendly technical learning assistant.

Explain the topic below to a {level} learner.

Topic: {topic}

Requirements:
- Use simple, clear language.
- Keep it to one coherent explanation (around 2–4 short paragraphs).
- Avoid unnecessary jargon, or explain it when you must use it.
- Include at least one analogy or metaphor that makes the concept relatable.
- Define technical terms the first time you use them.
- Aim to reduce cognitive load: focus on the core ideas first, details later.
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"raw_explanation": response.content}

# --- Node 2: chunk_explanation ----------------------------------------------
# Splits the explanation into 3–6 digestible chunks.
# Input: raw_explanation
# Output: chunks (list of strings)
def chunk_explanation(state: LearningState) -> dict:
    print("\n>>> chunk_explanation received state:", state)
    raw = state.get("raw_explanation", "")
    if not raw:
        return {"chunks": []}

    prompt = f"""
You are a learning coach.

You will be given an explanation of a technical topic.

Your job is to break it into 3–6 SHORT learning chunks that are easy for a beginner to digest.

Rules:
- Each chunk should focus on ONE idea.
- Each chunk should be 2–4 sentences.
- Start each chunk with a title like: "Chunk 1: What a partition is"
- Return ONLY the chunks, each as its own paragraph.
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    # Simple parsing: split on blank lines
    raw_chunks = [c.strip() for c in response.content.split("\n\n") if c.strip()]
    return {"chunks": raw_chunks}

# --- Node 3: generate_check_questions ---------------------------------------
# Creates 3–5 retrieval-practice questions based on the chunks.
# Input: chunks
# Output: check_questions (list of strings)
def generate_check_questions(state: LearningState) -> dict:
    print("\n>>> generate_check_questions received state:", state)
    chunks = state.get("chunks", [])
    if not chunks:
        return {"check_questions": []}

    chunks_text = "\n\n".join(chunks)
    prompt = f"""
You are a learning coach helping someone understand a technical topic.

You will be given several learning chunks that explain the topic step by step.

Your job is to create 3–5 SHORT questions that help the learner check their understanding.
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    # Parse numbered list into questions
    questions: List[str] = []
    for line in response.content.splitlines():
        line = line.strip()
        if line and line[0].isdigit():
            q = line[2:].strip() if line[1] in [".", ")"] else line[3:].strip()
            if q:
                questions.append(q)
    return {"check_questions": questions}

# --- Node 4: summarize_and_meta ---------------------------------------------
# Produces a one-sentence TL;DR and meta-learning notes.
# Input: topic, level, raw_explanation, chunks, check_questions
# Output: summary, meta (notes + counts)
def summarize_and_meta(state: LearningState) -> dict:
    print("\n>>> summarize_and_meta received state:", state)
    topic = state.get("topic", "this topic")
    raw = state.get("raw_explanation", "")
    chunks = state.get("chunks", [])
    questions = state.get("check_questions", [])

    prompt = f"""
You are a learning scientist and technical explainer.

Tasks:
1) Write a ONE-SENTENCE TL;DR summary of the topic.
2) Write 2–3 bullets explaining how the structure supports learning.
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    summary_line, bullets = "", []
    for line in response.content.splitlines():
        if line.startswith("Summary:"):
            summary_line = line[len("Summary:"):].strip()
        elif line.startswith("- "):
            bullets.append(line[2:].strip())

    return {
        "summary": summary_line or f"A short overview of {topic}.",
        "meta": {
            "learning_design_notes": bullets,
            "num_chunks": len(chunks),
            "num_questions": len(questions),
        },
    }

# --- Graph Construction -----------------------------------------------------
def build_app():
    graph = StateGraph(LearningState)
    # Register nodes
    graph.add_node("draft_explanation", draft_explanation)
    graph.add_node("chunk_explanation", chunk_explanation)
    graph.add_node("generate_check_questions", generate_check_questions)
    graph.add_node("summarize_and_meta", summarize_and_meta)
    # Wire them: START → draft → chunk → questions → summary → END
    graph.add_edge(START, "draft_explanation")
    graph.add_edge("draft_explanation", "chunk_explanation")
    graph.add_edge("chunk_explanation", "generate_check_questions")
    graph.add_edge("generate_check_questions", "summarize_and_meta")
    graph.add_edge("summarize_and_meta", END)
    return graph.compile()

# --- CLI Test Harness -------------------------------------------------------
# Allows quick local testing without LangSmith dataset.
# For evaluation, evaluate_chunkbuddy.py loads chunkbuddy-topics instead.
if __name__ == "__main__":
    app = build_app()
    initial_state: LearningState = {
        "topic": "TLS Handshake",
        "level": "beginner",
    }
    final_state = app.invoke(initial_state)
    print("\n=== FINAL STATE ===")
    for k, v in final_state.items():
        print(f"{k}: {v}")
