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