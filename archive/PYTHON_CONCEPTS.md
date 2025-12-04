# Python Concepts in This Project

This project is intentionally small, so it’s a great place to review some core Python ideas.  
Below are the main concepts used in `llm.py` and how they fit together.

---

## 1. Modules and Imports

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
```

- **Modules** are Python files or packages that contain reusable code.
- `from X import Y` loads specific functions or classes from a module.
- Here:
  - `dotenv` loads environment variables from `.env`
  - `langchain_openai` provides the `ChatOpenAI` class (wrapper for OpenAI models)

---

## 2. Environment Variables and `.env` Files

```python
from dotenv import load_dotenv
load_dotenv()
```

- Environment variables store secrets (API keys) **outside** your Python code.
- Prevents exposing secrets in GitHub.
- `load_dotenv()` reads `.env` and injects those values into the environment.

Example `.env`:

```env
OPENAI_API_KEY=sk-...
```

---

## 3. Classes and Objects

```python
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.7,
    max_tokens=500,
    verbose=True,
)
```

- `ChatOpenAI` is a **class**
- `llm` is an **instance**
- Keyword arguments configure:
  - model name
  - randomness
  - max response length
  - debug logging

---

## 4. Methods on Objects

```python
response = llm.invoke("Say one short sentence about Solace PubSub+.")
```

- `.invoke()` is a **method** (function bound to an object)
- Returns a structured `AIMessage` object with:
  - `response.content`  
  - `response.usage_metadata`  

---

## 5. Printing Output

```python
print("REPLY:", response.content)
print("USAGE:", response.usage_metadata)
```

- `print()` sends text to the terminal.
- Useful for debugging and experimentation.

---

## 6. Dictionaries

```python
PRICES = {
    "gpt-4o-mini": {"input": 0.15 / 1_000_000, "output": 0.60 / 1_000_000},
}
```

- A dictionary maps keys → values.
- Here:
  - outer key = model name  
  - inner dict = per-token input/output pricing  

Access:

```python
p = PRICES["gpt-4o-mini"]
p["input"]
p["output"]
```

---

## 7. Functions

```python
def estimate_cost(model, usage):
    t_in = usage["input_tokens"]
    t_out = usage["output_tokens"]
    p = PRICES[model]
    return t_in * p["input"] + t_out * p["output"]
```

Concepts used:

- `def` defines a function
- Parameters: `model`, `usage`
- Token usage extracted from dict
- Price lookup from dict
- Final number returned to caller

Usage:

```python
cost = estimate_cost("gpt-4o-mini", response.usage_metadata)
```

---

## 8. Numeric Formatting (`f-strings`)

```python
print(f"Estimated cost: ${cost:.8f}")
```

- Formats floats
- `:.8f` → 8 digits after decimal

---

## 9. Virtual Environments and `requirements.txt`

- `venv/` contains a project-specific Python environment  
- Never committed to Git  
- `requirements.txt` captures package versions:

```sh
pip freeze > requirements.txt
```

Others can recreate your environment:

```sh
pip install -r requirements.txt
```

---

## 10. Full Flow Summary

1. Load environment variables  
2. Create LLM object  
3. Send a prompt  
4. Print reply  
5. Estimate and print cost  

A simple, clean example showing the core building blocks of Python scripting.
