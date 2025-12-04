# chunkbuddy_graph.py
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END

llm = ChatOpenAI(
    model="gpt-4o-mini",  # or "gpt-4o" if available to you
    temperature=0.5,
)

# 1. Define the state that flows through the graph
class LearningState(TypedDict, total=False):
    topic: str                   # e.g. "Kafka partitions"
    level: str                   # e.g. "beginner" or "intermediate"
    raw_explanation: str         # one coherent explanation
    chunks: List[str]            # list of chunked explanations
    check_questions: List[str]   # list of questions
    summary: str                 # one-sentence TL;DR
    meta: dict

# 2. Define the nodes (for now with dummy logic so you see the flow clearly)


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
- Aim to reduce cognitive load: focus on the core ideas first, details later.
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    explanation = response.content

    return {
        "raw_explanation": explanation
    }


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
- Do NOT add any extra commentary before or after the chunks.

Explanation to chunk:
\"\"\"{raw}\"\"\"
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    text = response.content

    # Very simple parsing: split on blank lines and keep non-empty parts
    raw_chunks = [c.strip() for c in text.split("\n\n") if c.strip()]

    return {
        "chunks": raw_chunks
    }


def generate_check_questions(state: LearningState) -> dict:
    print("\n>>> generate_check_questions received state:", state)
    chunks = state.get("chunks", [])

    if not chunks:
        return {"check_questions": []}

    # Join chunks into a single text block for the prompt
    chunks_text = "\n\n".join(chunks)

    prompt = f"""
You are a learning coach helping someone understand a technical topic.

You will be given several learning chunks that explain the topic step by step.

Your job is to create 3–5 SHORT questions that help the learner check their understanding.

Rules:
- Prefer open-ended questions (e.g. "In your own words..." or "Explain why...").
- Ask about the key ideas across different chunks, not tiny details.
- Use simple language.
- Return the questions as a numbered list, like:
  1. Question one...
  2. Question two...
  3. Question three...

Here are the chunks:

\"\"\"{chunks_text}\"\"\"
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    text = response.content

    # Simple parsing: split by lines starting with a number and a dot
    questions: List[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        # Handle formats like "1. Question" or "1) Question"
        if line[0].isdigit() and (line[1:3] in [". ", ") "] or line[1] in [".", ")"]):
            # Remove leading "1. " or "1)" etc.
            q = line[2:].strip() if line[1] in [".", ")"] else line[3:].strip()
            if q:
                questions.append(q)
        else:
            # Fallback: if the model didn't follow numbering strictly, just treat non-empty lines as questions
            if line and len(line.split()) > 3:  # avoid super-short noise
                questions.append(line)

    return {
        "check_questions": questions
    }


def summarize_and_meta(state: LearningState) -> dict:
    print("\n>>> summarize_and_meta received state:", state)
    topic = state.get("topic", "this topic")
    level = state.get("level", "beginner")
    raw = state.get("raw_explanation", "")
    chunks = state.get("chunks", [])
    questions = state.get("check_questions", [])

    prompt = f"""
You are a learning scientist and technical explainer.

The learner has just seen:
- A topic: "{topic}"
- Level: {level}
- An explanation
- A set of chunks
- A few check-for-understanding questions

Your tasks:

1) Write a ONE-SENTENCE TL;DR summary of the topic for this learner level.
   - It should be clear, simple, and focused on the core idea.

2) Then, write 2–3 short bullet points explaining how this explanation structure
   supports learning, using ideas like:
   - chunking (breaking concepts into pieces)
   - analogies
   - retrieval practice (questions)
   - reducing cognitive load

Format your answer exactly like this:

Summary: <one sentence here>
Bullets:
- <bullet 1>
- <bullet 2>
- <bullet 3> (optional)

Here is the explanation, chunks, and questions:

EXPLANATION:
\"\"\"{raw}\"\"\"

CHUNKS:
\"\"\"{chunks}\"\"\"

QUESTIONS:
\"\"\"{questions}\"\"\"
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    text = response.content

    summary_line = ""
    bullets: List[str] = []

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("Summary:"):
            summary_line = line[len("Summary:"):].strip()
        elif line.startswith("- "):
            bullets.append(line[2:].strip())

    result: dict = {
        "summary": summary_line or f"A short overview of {topic}."
    }

    # Only include meta if you added it to LearningState
    result["meta"] = {
        "learning_design_notes": bullets,
        "num_chunks": len(chunks),
        "num_questions": len(questions),
    }

    return result


# 3. Build and wire the graph


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

    # Compile graph into an executable app
    app = graph.compile()
    return app


# 4. Simple test harness


if __name__ == "__main__":
    app = build_app()

    initial_state: LearningState = {
        "topic": "Kafka partitions",
        "level": "beginner",
    }

    final_state = app.invoke(initial_state)

    print("\n=== FINAL STATE ===")
    for k, v in final_state.items():
        print(f"{k}: {v}")
