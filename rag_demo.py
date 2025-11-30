from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

# 1. Load markdown files as documents
def load_markdown_files(files):
    docs = []
    for fp in files:
        path = Path(fp)
        if path.exists():
            text = path.read_text(encoding="utf-8")
            docs.append(text)
        else:
            print(f"Warning: {fp} not found, skipping.")
    return docs


markdown_files = ["PYTHON_CONCEPTS.md", "LANGCHAIN_CONCEPTS.md"]
raw_docs = load_markdown_files(markdown_files)

if not raw_docs:
    raise RuntimeError("No documents loaded. Make sure the .md files exist.")

# 2. Create embeddings + vector store
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = FAISS.from_texts(raw_docs, embedding=embeddings)

# 3. LLM client
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)


def answer_question(question: str) -> str:
    # Retrieve top relevant docs
    retrieved = vectorstore.similarity_search(question, k=3)
    context = "\n\n---\n\n".join([d.page_content for d in retrieved])

    prompt = f"""
You are a helpful assistant. Use ONLY the context below to answer the question.

Context:
{context}

Question: {question}

If the answer is not in the context, say you don't know.
"""

    response = llm.invoke(prompt)
    return response.content


if __name__ == "__main__":
    print("RAG demo over your markdown notes.")
    print("Ask questions about Python or LangChain concepts.")
    print("Type 'exit' to quit.\n")

    while True:
        q = input("Question (or 'exit'): ").strip()
        if q.lower() in {"exit", "quit"}:
            break

        if not q:
            continue

        answer = answer_question(q)
        print("Answer:", answer)
        print()
