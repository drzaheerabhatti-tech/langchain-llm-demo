# 📘 ChunkBuddy: A LangGraph-Powered Learning Workflow

ChunkBuddy is an AI-powered learning assistant built using **LangGraph**, **LangChain**, and **LangSmith**.

It takes any technical topic and produces a structured, pedagogy-informed learning output:

1. A level-appropriate explanation  
2. Chunked learning sections  
3. Retrieval-practice questions  
4. A 1-sentence quick summary  
5. Meta-learning insights (chunking, cognitive load, analogies, etc.)

ChunkBuddy is designed to feel like a “learning buddy” that understands cognitive science and breaks down complex topics into digestible mental units.

---

## 🚀 Goals

ChunkBuddy was built to:

1. Demonstrate LangGraph through a realistic, multi-step agent workflow  
2. Apply cognitive science principles (chunking, retrieval practice, cognitive load)  
3. Show how LangSmith can be used to evaluate and trace each node  
4. Provide a clean Streamlit UI for interactive exploration and demos  

This creates a complete, transparent, and highly interpretable educational pipeline.

---

## 🧠 How ChunkBuddy Works

ChunkBuddy is implemented as a **Directed Acyclic Graph (DAG)** using LangGraph:

```
START
  ↓
draft_explanation
  ↓
chunk_explanation
  ↓
generate_check_questions
  ↓
summarize_and_meta
  ↓
END
```

Each node:

- Receives a structured portion of the shared state  
- Adds only the fields it is responsible for  
- Returns partial updates  
- LangGraph merges these updates into the global state  

This results in a modular, debuggable workflow.

---

## 🗂 Shared State Definition

All data shared between nodes lives in a `TypedDict`, ensuring clarity and structure:

```python
class LearningState(TypedDict, total=False):
    topic: str
    level: str
    raw_explanation: str
    chunks: List[str]
    check_questions: List[str]
    summary: str
    meta: dict
```

---

# 🔧 Node-by-Node Breakdown

### 🟦 1. `draft_explanation`
**Purpose:** Generate a level-appropriate explanation of the topic  
**Input:** `topic`, `level`  
**Output:** `raw_explanation`  

---

### 🟩 2. `chunk_explanation`
**Purpose:** Break the explanation into cognitively manageable pieces  
**Input:** `raw_explanation`  
**Output:** `chunks: List[str]`  

**Cognitive Principle:** Chunking reduces cognitive load.

---

### 🟧 3. `generate_check_questions`
**Purpose:** Generate open-ended retrieval questions  
**Input:** `chunks`  
**Output:** `check_questions: List[str]`  

**Cognitive Principle:** Retrieval practice improves long-term retention.

---

### 🟥 4. `summarize_and_meta`
**Purpose:** Generate a TL;DR summary and meta-learning insights  
**Input:** topic, chunks, questions  
**Output:** `summary`, `meta`  

Makes the agent aware of *how* it helps you learn.

---

# 🔄 Graph Construction

```python
graph = StateGraph(LearningState)

graph.add_node("draft_explanation", draft_explanation)
graph.add_node("chunk_explanation", chunk_explanation)
graph.add_node("generate_check_questions", generate_check_questions)
graph.add_node("summarize_and_meta", summarize_and_meta)

graph.add_edge(START, "draft_explanation")
graph.add_edge("draft_explanation", "chunk_explanation")
graph.add_edge("chunk_explanation", "generate_check_questions")
graph.add_edge("generate_check_questions", "summarize_and_meta")
graph.add_edge("summarize_and_meta", END)

app = graph.compile()
```

---

# 🧪 LangSmith Integration (Experiment Tracking)

LangSmith is enabled through environment variables:

```bash
pip install langsmith
```

Set:

```powershell
$env:LANGCHAIN_TRACING_V2="true"
$env:LANGCHAIN_API_KEY="<your-key>"
$env:LANGCHAIN_PROJECT="chunkbuddy"
```

Every graph run automatically appears as a full trace in LangSmith, including:

- Node-by-node execution
- Input/output state
- Prompts and LLM responses
- Timing and token usage

This dramatically improves observability and debugging.

---

# 🖥️ Streamlit UI (Interactive Learning App)

ChunkBuddy includes a simple **Streamlit-based web interface** that makes the learning experience visual, interactive, and demo-friendly.

### ⭐ What the UI provides

- Enter any topic  
- Choose your learning level  
- View:
  - Explanation  
  - Chunked sections (expandable)  
  - Retrieval questions  
  - Summary  
  - Meta-learning insights  
- Optional developer mode showing the raw LangGraph state  
- Instant interaction powered by the same DAG pipeline

---

## ▶️ Running the Streamlit App

Install:

```bash
pip install streamlit
```

Run the UI:

```bash
streamlit run chunkbuddy_ui.py
```

This opens the app at:

```
http://localhost:8501
```

You can try topics like:

- “Kafka partitions”  
- “TLS handshake”  
- “Kubernetes pods vs nodes”  
- “Event-driven backpressure”  

The UI showcases the entire end-to-end pipeline elegantly.

---

# 📈 Evaluation Strategy

Tested with topics such as:

- Kafka partitions  
- TLS handshake  
- Kubernetes fundamentals  
- Backpressure in distributed systems  

Evaluated for:

- Explanation clarity  
- Chunk structure and granularity  
- Question quality  
- Summary fidelity  
- Meta-learning depth  

LangSmith made iterative refinement straightforward.

### 📸 Streamlit UI Preview
![ChunkBuddy UI](./screenshot_ui_1.png)

---

# 🧭 What I Learned

- LangGraph’s partial state updates make multi-step agents clean and modular  
- TypedDict shared state is powerful for workflow clarity  
- Streamlit is excellent for lightweight AI UI demos  
- LangSmith traces are invaluable for debugging multi-step workflows  
- DAG-based reasoning pipelines reduce prompt complexity and improve interpretability  

---

# ⚠️ Friction / Improvements

- Some examples mix `MessagesState` and custom state, which can confuse beginners  
- Node naming conventions could be highlighted more clearly  
- More examples of multi-step educational agents would help new users  

---

# 📦 How to Run (Script Mode)

```bash
pip install langgraph langchain-openai langsmith
python chunkbuddy_graph.py
```

Traces will appear in LangSmith under the project name **chunkbuddy**.

---

# 🎯 Summary

ChunkBuddy demonstrates:

- A multi-step LangGraph workflow  
- LLM-powered explanation, chunking, questioning, and summarization  
- A polished Streamlit interface  
- Full LangSmith observability  
- A learning design grounded in cognitive science  

This is a strong foundation for more advanced educational or tutoring agents.

# 🧪 Evaluating with LangSmith (SDK)

Run:

```bash
python evaluate_chunkbuddy.py
This triggers:

Dataset loading from LangSmith

The ChunkBuddy graph execution for each example

Three evaluators:

Chunk count sanity check

Question count sanity check

LLM-as-judge clarity evaluation
All results appear in LangSmith under an automatically generated experiment name.


### Why I chose this agent design  
I wanted a workflow that demonstrates the strengths of LangGraph:  
a clear multi-step pipeline, state passing, deterministic edges, and modular nodes.  
A learning assistant is naturally multi-stage (explain → chunk → question → summarize),  
so it showcases LangGraph’s structure while being easy to reason about.  
It also produces rich outputs, which makes LangSmith evaluation meaningful.

