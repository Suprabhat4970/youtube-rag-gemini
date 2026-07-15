import streamlit as st

from rag_pipeline import YouTubeRAG

from agent.summary_agent import SummaryAgent
from agent.quiz_agent import QuizAgent
from agent.notes_agent import NotesAgent
from agent.content_agent import ContentAgent
from agent.qa_agent import QAAgent
st.set_page_config(
    page_title="VideoMind AI",
    page_icon="🎥",
    layout="wide"
)

st.title("🎥 VideoMind AI")
st.subheader(
    "Agentic Video Intelligence Platform"
)

video_id = st.text_input(
    "Enter YouTube Video ID"
)

if "rag" not in st.session_state:
    st.session_state.rag = None

if st.button("Load Video"):

    with st.spinner("Loading transcript..."):

        rag = YouTubeRAG()

        transcript = rag.load_transcript(
            video_id
        )

        rag.build_index(transcript)

        st.session_state.rag = rag
        st.session_state.transcript = transcript

        st.success(
            "Video Loaded Successfully"
        )

if st.session_state.rag:

    rag = st.session_state.rag
    transcript = st.session_state.transcript

    summary_agent = SummaryAgent(
        rag.client
    )

    quiz_agent = QuizAgent(
        rag.client
    )

    notes_agent = NotesAgent(
        rag.client
    )

    content_agent = ContentAgent(
        rag.client
    )

    qa_agent = QAAgent(
        rag.vectorstore,
        rag.client
    )

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "Summary",
            "Q&A",
            "Quiz",
            "Notes",
            "Content"
        ]
    )

    with tab1:

        if st.button(
            "Generate Summary"
        ):

            result = summary_agent.run(
                transcript
            )

            st.markdown(result)

    with tab2:

        question = st.text_input(
            "Ask Question"
        )

        if st.button("Ask"):

            answer = qa_agent.run(
                question
            )

            st.markdown(answer)

    with tab3:

        if st.button(
            "Generate Quiz"
        ):

            quiz = quiz_agent.run(
                transcript
            )

            st.markdown(quiz)

    with tab4:

        if st.button(
            "Generate Notes"
        ):

            notes = notes_agent.run(
                transcript
            )

            st.markdown(notes)

    with tab5:

        if st.button(
            "Generate Content"
        ):

            content = content_agent.run(
                transcript
            )

            st.markdown(content)