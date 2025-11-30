import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()


# Pricing table
PRICES = {
    "gpt-4o-mini": {
        "input": 0.15 / 1_000_000,
        "output": 0.60 / 1_000_000,
    },
}


def estimate_cost(model, usage):
    """Estimate $ cost based on token usage."""
    t_in = usage["input_tokens"]
    t_out = usage["output_tokens"]
    p = PRICES[model]
    return t_in * p["input"] + t_out * p["output"]


def run_llm(prompt: str):
    """Send prompt to the LLM and print everything nicely."""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        n=1,
        verbose=False,
    )

    print("\n📨 Sending prompt...\n")
    response = llm.invoke(prompt)

    print("🧠 MODEL REPLY:")
    print(response.content)
    print("\n📊 USAGE:", response.usage_metadata)

    cost = estimate_cost("gpt-4o-mini", response.usage_metadata)
    print(f"💰 ESTIMATED COST: ${cost:.8f}\n")


if __name__ == "__main__":
    # Case 1: User passes text as a command-line argument
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        # Case 2: Interactive input mode
        prompt = input("Enter your prompt: ").strip()

    if not prompt:
        print("Error: Prompt cannot be empty.")
        sys.exit(1)

    run_llm(prompt)
