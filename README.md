# LangChain LLM Demo

Simple Python script that calls OpenAI's `gpt-4o-mini` via LangChain and prints
the reply.

Environment variables are loaded from `.env` (not committed to Git).


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
