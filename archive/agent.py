from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

# Load your API key (OPENAI_API_KEY) from a .env file so ChatOpenAI can authenticate.
load_dotenv()


@tool
def calculator(a: float, b: float) -> float:
    """
    A simple tool the agent can use.
    The docstring tells the model what the tool does.
    """
    return a + b


# This tells the agent how it should behave.
SYSTEM_PROMPT = "You are a helpful math assistant."


# Create the LLM the agent will use to think and make decisions.
# This is the "brain" of the agent.
model = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.0,  # 0 = deterministic answers
)


# Create the agent:
# - connects the model and the tools
# - lets the model decide when to call a tool
# - handles the think → act → observe → answer loop automatically
agent = create_agent(
    model,
    tools=[calculator],          # list of tools the agent can use
    system_prompt=SYSTEM_PROMPT, # instructions guiding its behavior
)


# Run a single query through the agent.
# The agent will:
# 1. read the user's message
# 2. decide to call the calculator tool
# 3. receive the tool output (5)
# 4. return a final answer to the user
result = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "What is 2 + 3?"}
        ],
    }
)


# The agent returns a list of all messages (user, tool calls, tool outputs, final answer).
# The last message (-1) is the assistant's final answer.
print(result["messages"][-1].content)
