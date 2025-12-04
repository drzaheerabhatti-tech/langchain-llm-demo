# chunkbuddy_ui.py

import streamlit as st
from typing import TypedDict, List

from chunkbuddy_graph import build_app, LearningState  # reuse your existing graph


# Build the LangGraph app once at startup
app = build_app()

st.set_page_config(page_title="ChunkBuddy", page_icon="🧠", layout="wide")

st.title("🧠 ChunkBuddy – LangGraph Learning Assistant")
st.write(
    "Turn any technical topic into a structured learning experience with "
    "explanations, chunks, questions, and a summary."
)

# --- Sidebar controls ---
st.sidebar.header("Settings")
default_topic = "Kafka partitions"
topic = st.sidebar.text_input("Topic you want to learn", value=default_topic)

level = st.sidebar.selectbox(
    "Your level",
    options=["beginner", "intermediate", "advanced"],
    index=0,
)

run_button = st.sidebar.button("Teach me 🚀")

st.markdown("---")

if run_button:
    if not topic.strip():
        st.error("Please enter a topic.")
    else:
        with st.spinner("ChunkBuddy is thinking..."):
            # Prepare initial state for the graph
            initial_state: LearningState = {
                "topic": topic.strip(),
                "level": level,
            }
            result = app.invoke(initial_state)

        # --- Layout: 2 columns ---
        col1, col2 = st.columns([2, 1])

        # 1. Full explanation
        with col1:
            st.subheader("1. Explanation")
            st.write(result.get("raw_explanation", "_No explanation generated._"))

        # 2. TL;DR
        with col2:
            st.subheader("4. TL;DR")
            st.write(result.get("summary", "_No summary generated._"))

        st.markdown("---")

        # 3. Chunks (expandable)
        st.subheader("2. Learning chunks")
        chunks = result.get("chunks", [])
        if not chunks:
            st.write("_No chunks generated._")
        else:
            for i, chunk in enumerate(chunks, start=1):
                with st.expander(f"Chunk {i}"):
                    st.write(chunk)

        st.markdown("---")

        # 4. Check-your-understanding questions
        st.subheader("3. Check your understanding")
        questions = result.get("check_questions", [])
        if not questions:
            st.write("_No questions generated._")
        else:
            for q in questions:
                st.markdown(f"- {q}")

        st.markdown("---")

        # 5. Meta learning notes (optional)
        meta = result.get("meta", {})
        notes = meta.get("learning_design_notes", [])
        if notes:
            st.subheader("🧩 How this structure helps you learn")
            for note in notes:
                st.markdown(f"- {note}")

        # 6. (Optional) Debug / raw state
        with st.expander("Developer view: raw state"):
            st.json(result)

else:
    st.info("Enter a topic and click **Teach me 🚀** in the sidebar to get started.")
