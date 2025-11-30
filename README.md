# LangChain LLM Demo

A simple, minimal Python project demonstrating how to:

- Load environment variables with `python-dotenv`
- Call OpenAI’s models using **LangChain**
- Print model responses and token usage
- Estimate API cost for each call
- Use a clean project structure with a virtual environment and `.env`

This is an ideal starting point for experimentation or learning how LangChain and OpenAI's API work together.

---

# 🚀 Getting Started

Follow these steps to run the project from scratch on any machine.

---

## 1. Install Python 3.10+ (if needed)

Download from:  
https://www.python.org/downloads/

Make sure to check:

✔ “Add Python to PATH”

---

## 2. Clone the repository

```bash
git clone https://github.com/drzaheerabhatti-tech/langchain-llm-demo.git
cd langchain-llm-demo
```

---

## 3. Create and activate a virtual environment

### Windows (PowerShell):

```bash
python -m venv venv
.\venv\Scripts\activate
```

### macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

When active, your terminal will show:

```
(venv)
```

---

## 4. Install project dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Get an OpenAI API Key

### 5.1 Sign in to OpenAI  
https://platform.openai.com/

### 5.2 Create a secret API key  
Go to:  
**Dashboard → API Keys → Create new secret key**

Copy the key:

```
sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

> Keep it private — **never commit it to GitHub**.

### 5.3 Create a `.env` file

In the project root, create:

```
.env
```

Inside it, add:

```env
OPENAI_API_KEY=sk-your-real-key-here
```

This file is **ignored by Git** because `.gitignore` includes `.env`.

---

## 6. Run the script

Run:

```bash
python llm.py
```

You should see output similar to:

```
REPLY: Solace PubSub+ is a high-performance event streaming and messaging platform.
USAGE: {'input_tokens': 12, 'output_tokens': 16, 'total_tokens': 28}
Estimated cost for this call: $0.00001234
```

---

# 📂 Project Structure

```
langchain-llm-demo/
│
├── llm.py                # Main script
├── requirements.txt      # Python dependencies
├── .gitignore            # Excludes venv + env files
├── PYTHON_CONCEPTS.md    # Python concepts used in the project
├── LANGCHAIN_CONCEPTS.md # LangChain concepts explained simply
└── venv/                 # Virtual environment (ignored by Git)
```

---

# 📘 Helpful Learning Resources

- **Python Concepts Overview**  
  → See `PYTHON_CONCEPTS.md`

- **LangChain Concepts Overview**  
  → See `LANGCHAIN_CONCEPTS.md`

- **OpenAI API Documentation**  
  https://platform.openai.com/docs

- **LangChain Documentation**  
  https://python.langchain.com/

---

# 🙌 Summary

This project is designed to help developers:

- Learn Python best practices  
- Understand how to work with `.env` files  
- Call OpenAI models using LangChain  
- Estimate token costs  
- Safely structure a Python project with Git

If you want to expand the project (add CLI arguments, add streaming, use agents, add RAG, etc.), feel free to build on top of this template.

---

# 📚 Retrieval-Augmented Generation (RAG) Demo

This project also includes a simple **RAG (Retrieval-Augmented Generation)** example that lets the LLM answer questions using your own local documents.  
The demo uses:

- **OpenAI embeddings**
- **FAISS** (local vector database)
- **LangChain** retrievers

This is a great starting point to learn how to build intelligent assistants that use your personal knowledge base.

---

## 🧠 What the RAG demo does

- Converts your documents into embeddings (numeric vectors)
- Stores them in a local vector database (FAISS)
- When you ask a question:
  1. It finds the most relevant document chunks
  2. Sends them to the model as context
  3. The model answers *based only on your documents*

This prevents hallucinations and makes the model respond based on **your actual notes**.

---

## ▶️ Running the RAG demo

Activate your venv:

```bash
.\venv\Scripts\activate
```

Run the script:

```bash
python rag_demo.py
```

You will see:

```
RAG demo over your markdown notes.
Ask questions about Python or LangChain concepts.
Type 'exit' to quit.

Question (or 'exit'):
```

Try questions like:

```
What is LangChain?
Explain the estimate_cost function.
What does load_dotenv() do?
```

---

## 🗂️ Documents used in retrieval

By default, the RAG demo loads:

- `PYTHON_CONCEPTS.md`
- `LANGCHAIN_CONCEPTS.md`

You can add more documents (Markdown or text) by editing:

```python
markdown_files = ["PYTHON_CONCEPTS.md", "LANGCHAIN_CONCEPTS.md"]
```

in `rag_demo.py`.

---

## 🏗 How it works (high-level flow)

1. **Load documents**  
   Reads your `.md` files from disk.

2. **Embed documents**  
   Uses OpenAI’s `text-embedding-3-small` model via:

   ```python
   OpenAIEmbeddings()
   ```

3. **Store in vector database (FAISS)**  
   Efficient local similarity search.

4. **Semantic Search**  
   For each question, retrieves the most relevant snippets.

5. **LLM Answer**  
   The retrieved context is injected into the prompt:

   ```
   You are a helpful assistant. Use ONLY the context below...
   ```

   ensuring grounded, accurate responses.

---

## 🔧 Requirements

Ensure these packages are installed:

```bash
pip install langchain-openai langchain-community faiss-cpu
```

---

## 🧩 Where to go next

Once the RAG demo works, you can:

- Connect it to the **chatbot** for long-term memory  
- Load all your Solace docs or observability notes  
- Build a full personal assistant with your own knowledge base  
- Move from FAISS to a hosted vector DB (Pinecone, Milvus, Weaviate, Chroma Cloud)

Let me know if you want to build:
- a **chatbot with RAG**,  
- a **document ingestion pipeline**,  
- or a **full FastAPI/Streamlit UI** for querying your knowledge.

