import sys
from typing import Optional

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# Load environment variables from .env
load_dotenv()

# Pricing table for cost estimation
PRICES = {
    "gpt-4o-mini": {
        "input": 0.15 / 1_000_000,
        "output": 0.60 / 1_000_000,
    },
}


def estimate_cost(model: str, usage: dict) -> float:
    """Estimate $ cost based on token usage."""
    t_in = usage["input_tokens"]
    t_out = usage["output_tokens"]
    p = PRICES[model]
    return t_in * p["input"] + t_out * p["output"]


def chat_loop(initial_prompt: Optional[str] = None) -> None:
    """
    Run an interactive chat loop with in-session memory.

    - Keeps conversation history in memory while the script runs
    - Type 'exit' or 'quit' to end the chat
    """

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        max_completion_tokens = 500,
        verbose=False,
    )

    # Conversation history (memory)
    history = [
        SystemMessage(
            content=(
                "You are a friendly, concise personal assistant. "
                "You are chatting with Zaheer. Keep answers short and clear."
            )
        )
    ]

    print("💬 Mini Chatbot with Memory (gpt-4o-mini)")
    print("Type your message and press Enter.")
    print("Type 'exit' or 'quit' to end the chat.\n")

    # If the user passed a first prompt via CLI, handle it before the loop
    if initial_prompt:
        _handle_turn(initial_prompt, llm, history)

    # Main interactive loop
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Goodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit"}:
            print("👋 Goodbye!")
            break

        _handle_turn(user_input, llm, history)


def _handle_turn(user_input: str, llm: ChatOpenAI, history: list) -> None:
    """Handle a single user → model turn with memory + cost printing."""
    # Add the user's message to history
    history.append(HumanMessage(content=user_input))

    # Send full history to the model
    response = llm.invoke(history)

    # Print reply
    print(f"Assistant: {response.content}\n")

    # Add assistant reply to history
    history.append(AIMessage(content=response.content))

    # Optional: usage + cost per turn
    if getattr(response, "usage_metadata", None):
        usage = response.usage_metadata
        cost = estimate_cost("gpt-4o-mini", usage)
        print(f"   🔎 usage: {usage}")
        print(f"   💰 cost for this reply: ${cost:.8f}\n")


if __name__ == "__main__":
    # Optional initial prompt via CLI:
    # python llm_prompt.py "Explain Solace PubSub+ in one sentence"
    first_prompt: Optional[str] = None
    if len(sys.argv) > 1:
        first_prompt = " ".join(sys.argv[1:]).strip() or None

    chat_loop(initial_prompt=first_prompt)
