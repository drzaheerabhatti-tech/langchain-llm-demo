from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.7,
    max_tokens=500,
    verbose=True,
)



response = llm.invoke("Hi, how are you?")
print(response.content)


PRICES = {
    "gpt-4o-mini": {"input": 0.15 / 1_000_000, "output": 0.60 / 1_000_000},
}

def estimate_cost(model, usage):
    t_in = usage["input_tokens"]
    t_out = usage["output_tokens"]
    p = PRICES[model]
    return t_in * p["input"] + t_out * p["output"]

cost = estimate_cost("gpt-4o-mini", response.usage_metadata)
print(f"Estimated cost for this call: ${cost:.8f}")
