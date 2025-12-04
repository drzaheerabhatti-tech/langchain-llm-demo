# import load_dotenv function from python-dotenv package. 
# When you install python-dotenv package (pip install python-dotenv), a python module named dotenv is also installed.
# A module is a .py file or a directory containing Python files. load_dotenv is a function inside the module.
# load_dotenv() loads key-values pairs from .env into environment

from dotenv import load_dotenv

# import ChatOpenAI class from langchain_openai package module. Note - import name does not match package name (langchain-openai) as Python cannot use hyphens (-) in import names.
# ChatOpenAI is a class that warps OpenAI chat models inside LangChain.
from langchain_openai import ChatOpenAI

load_dotenv() 

# This line creates an instance of the ChatOpenAI class, which is LangChain’s high-level interface for interacting with OpenAI chat models.
llm = ChatOpenAI(
   model="gpt-4o-mini",
   temperature=0.7,
   max_completion_tokens=500,
   verbose=True,
)
# ChatOpenAI is a class (wraps OpenAI API behind a LangChain interface)
# llm becomes an instance (object) - a specific model configuration we can call to generate text.
# model --> specifies underlying OpenAI model the llm instance should use
# ***temperature*** --> controls how creative vs predictable the model is.
# Low temperature (0-0.3) -> very focused, precise, predictable. Good for facts, math, code, troubleshooting.
# Medium temperature (0.5-0.7) -> some creativity, still logical.
# High temparature (0.8 - 1) -> more creative, random or imaginative. Good for brainstorming, storytelling.
# *** max_completion_tokens*** -> max output tokens the model can generate in one response.
# verbose --> enables class' built-in debugging output, showing request/response details.

# This line sends the text "Hi, how are you?" to the model and gets back the model’s reply.
#.invoke() sends a prompt to the model and returns its response in a structured object.
response = llm.invoke("Hi, how are you?")
print(response.content)

# This dictionary stores how much the model costs per token - A token is a chunk of text (~0.75 words per token - 100 tokens ~75 words)
# E.g. For every 1,000,000 tokens, the cost is 0.15 or 0.60 dollars. 
PRICES = {
    "gpt-4o-mini": {"input": 0.15 / 1_000_000, "output": 0.60 / 1_000_000},
}

# This is a python function that takes two parameters - model name and usage dictionary 
# PRICES is my own lookup table containing the cost per token for each model.
# These prices do NOT come from OpenAI's response — they are defined manually.
# "input"  = cost per input token
# "output" = cost per output token
def estimate_cost(model, usage):
    # usage is the dictionary returned by response.usage_metadata
    # It contains:
    #   usage["input_tokens"]  → number of tokens in my prompt
    #   usage["output_tokens"] → number of tokens in the model's answer
    t_in = usage["input_tokens"]
    t_out = usage["output_tokens"]
    # p contains the pricing information from the PRICES table above
    # p["input"]  = price per input token
    # p["output"] = price per output token
    p = PRICES[model]
    # Total cost = (input tokens × input token price)
    #            + (output tokens × output token price)
    cost = t_in * p["input"] + t_out * p["output"] 
    return t_in, t_out, cost

t_in, t_out, cost = estimate_cost("gpt-4o-mini", response.usage_metadata)
print(response.usage_metadata)
print(f"input tokens: {t_in}")
print(f"output tokens: {t_in}")
print(f"Estimated cost for this call: ${cost:.8f}")
