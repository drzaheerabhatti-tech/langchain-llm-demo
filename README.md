# 🧠 LangChain Python Projects

This workspace contains hands-on demos and experiments using **LangChain**, **LangGraph**, and **LangSmith** — focused on building interpretable, multi-step agents with strong evaluation workflows.

Each subfolder is a self-contained agent or demo, with its own code, README, and environment.

---

## 📦 Projects

### [`agent_demo/`](agent_demo/)

A complete learning assistant called **ChunkBuddy**, built with LangGraph and evaluated using LangSmith.

- ✅ Multi-step DAG: explanation → chunking → questions → summary  
- ✅ LangSmith evaluation: rule-based + LLM-as-judge  
- ✅ Streamlit UI for interactive exploration  
- ✅ Cognitive-science-aligned design (chunking, retrieval practice, clarity)

Explore the full walkthrough, code, and evaluation results in [`agent_demo/README.md`](agent_demo/README.md).

---

## 🧪 Goals of This Workspace

- Showcase real-world LangGraph agents  
- Demonstrate LangSmith evaluation workflows  
- Build reusable components for agent development  

---

## 📁 Structure
```
LANGCHAIN-PYTHON/
│
├── agent_demo/              # ChunkBuddy agent (LangGraph + LangSmith + Streamlit)
│   ├── chunkbuddy_graph.py
│   ├── evaluate_chunkbuddy.py
│   ├── chunkbuddy_ui.py
│   ├── load_env.py
│   ├── README.md
│   ├── requirements.txt
│   └── images/              # Screenshots and diagrams for agent_demo README
│
├── .env                     # Optional root-level config
├── .gitignore
├── README.md                # Workspace overview (this file)
└── requirements.txt         # Optional shared dependencies

```
---

## 🛠 Setup

Each project folder contains its own setup instructions. To run `agent_demo`, follow the steps in [`agent_demo/README.md`](agent_demo/README.md).

---

## 📬 Contact

Created by [Zaheer Bhatti](https://github.com/drzaheerabhatti-tech)  
Feel free to fork, adapt, or reach out with questions or feedback.

---

