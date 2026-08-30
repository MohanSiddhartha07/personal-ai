import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from memory import (
    initialize_memory,
    save_memory,
    get_recent_memories
)

from memory_extractor import extract_memory
from retrieval import search


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SIRA — Sid's Intelligent Resource Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# GEMINI SETUP
# ============================================================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("OPENAI_API_KEY not found in .env file")
    st.stop()

client = OpenAI(
    api_key=api_key
)
initialize_memory()


# ============================================================
# HTML HELPER
# ============================================================

def render_html(content):
    st.html(content)


# ============================================================
# CUSTOM CSS
# ============================================================

render_html("""
<style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 80% 10%,
                rgba(124, 58, 237, 0.13),
                transparent 28%
            ),
            radial-gradient(
                circle at 20% 90%,
                rgba(59, 130, 246, 0.08),
                transparent 30%
            ),
            #05070d;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #080b14 0%,
                #05070d 100%
            );

        border-right: 1px solid rgba(148, 163, 184, 0.10);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    .sidebar-brand {
        padding: 0.4rem 0.5rem 1rem 0.5rem;
    }

    .sidebar-logo {
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -1px;
        color: #f8fafc;
    }

    .sidebar-tagline {
        margin-top: 4px;
        color: #a78bfa;
        font-size: 0.78rem;
        font-style: italic;
    }

    .sidebar-status {
        margin-top: 1rem;
        padding: 1rem;

        border-radius: 18px;

        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.95),
                rgba(8, 12, 24, 0.75)
            );

        border: 1px solid rgba(139, 92, 246, 0.18);

        box-shadow:
            0 15px 40px rgba(0, 0, 0, 0.22);
    }

    .status-row {
        display: flex;
        align-items: center;
        gap: 10px;

        color: #e2e8f0;
        font-size: 0.88rem;
        font-weight: 600;
    }

    .green-dot {
        display: inline-block;

        width: 9px;
        height: 9px;

        border-radius: 50%;

        background: #22c55e;

        box-shadow:
            0 0 14px rgba(34, 197, 94, 0.65);
    }

    .status-subtitle {
        margin-top: 8px;

        color: #64748b;
        font-size: 0.74rem;
        line-height: 1.4;
    }

    .sidebar-section-title {
        margin-top: 1.7rem;
        margin-bottom: 0.6rem;

        color: #a78bfa;

        font-size: 0.68rem;
        font-weight: 800;

        letter-spacing: 1.6px;
        text-transform: uppercase;
    }

    .knowledge-item {
        display: flex;
        align-items: center;
        gap: 10px;

        padding: 0.42rem 0;

        color: #cbd5e1;
        font-size: 0.85rem;
    }

    .knowledge-check {
        display: flex;
        align-items: center;
        justify-content: center;

        width: 18px;
        height: 18px;

        border-radius: 50%;

        background: rgba(34, 197, 94, 0.12);
        color: #22c55e;

        font-size: 0.65rem;
    }

    .sidebar-footer {
        margin-top: 2rem;
        padding: 1rem;

        border-radius: 18px;

        background:
            rgba(15, 23, 42, 0.55);

        border: 1px solid rgba(148, 163, 184, 0.08);

        color: #64748b;
        font-size: 0.72rem;
        line-height: 1.6;
    }

    .sidebar-footer strong {
        color: #c4b5fd;
    }


    /* ========================================================
       MAIN BRAND
       ======================================================== */

    .main-brand {
        margin-top: 0.5rem;
    }

    .main-brand-title {
        display: flex;
        align-items: center;
        gap: 18px;

        font-size: 5rem;
        line-height: 1;

        font-weight: 850;
        letter-spacing: -4px;

        background:
            linear-gradient(
                135deg,
                #ffffff 10%,
                #ddd6fe 50%,
                #a78bfa 100%
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .brain {
        font-size: 4.3rem;
        -webkit-text-fill-color: initial;
    }

    .main-tagline {
        margin-top: 0.7rem;

        font-size: 1.8rem;
        font-weight: 500;

        font-style: italic;

        color: #a78bfa;

        letter-spacing: -0.5px;

        text-shadow:
            0 0 30px rgba(139, 92, 246, 0.22);
    }

    .main-description {
        margin-top: 0.55rem;

        color: #94a3b8;
        font-size: 0.98rem;
    }

    .online-pill {
        display: inline-flex;
        align-items: center;
        gap: 9px;

        margin-top: 1rem;
        padding: 0.42rem 0.85rem;

        border-radius: 999px;

        background:
            rgba(15, 23, 42, 0.55);

        border: 1px solid rgba(148, 163, 184, 0.13);

        color: #cbd5e1;
        font-size: 0.78rem;
    }


    /* ========================================================
       HERO
       ======================================================== */

    .hero-card {
        position: relative;

        margin-top: 2rem;

        min-height: 190px;

        padding: 2rem 2.2rem;

        border-radius: 28px;

        background:
            radial-gradient(
                circle at 80% 0%,
                rgba(124, 58, 237, 0.18),
                transparent 35%
            ),
            radial-gradient(
                circle at 20% 100%,
                rgba(59, 130, 246, 0.07),
                transparent 30%
            ),
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.92),
                rgba(7, 11, 21, 0.82)
            );

        border: 1px solid rgba(139, 92, 246, 0.20);

        box-shadow:
            0 25px 70px rgba(0, 0, 0, 0.30),
            inset 0 1px 0 rgba(255, 255, 255, 0.035);
    }

    .greeting {
        font-size: 2rem;
        font-weight: 700;

        color: #f8fafc;
    }

    .greeting span {
        background:
            linear-gradient(
                90deg,
                #c084fc,
                #818cf8
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-question {
        margin-top: 0.5rem;

        color: #94a3b8;
        font-size: 1rem;
    }

    .quote {
        position: absolute;

        top: 2rem;
        right: 2.2rem;

        max-width: 260px;

        color: #64748b;

        font-size: 0.82rem;
        font-style: italic;

        line-height: 1.6;

        text-align: right;
    }

    .quote-highlight {
        color: #a78bfa;
    }


    /* ========================================================
       CARDS
       ======================================================== */

    .cards-title {
        margin-top: 1.7rem;
        margin-bottom: 0.9rem;

        color: #cbd5e1;

        font-size: 0.9rem;
        font-weight: 650;
    }

    .action-card {
        min-height: 185px;

        padding: 1.3rem;

        border-radius: 22px;

        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.90),
                rgba(7, 11, 21, 0.78)
            );

        border: 1px solid rgba(148, 163, 184, 0.11);

        box-shadow:
            0 12px 35px rgba(0, 0, 0, 0.18);

        transition:
            transform 0.2s ease,
            border-color 0.2s ease,
            box-shadow 0.2s ease;
    }

    .action-card:hover {
        transform: translateY(-4px);

        border-color:
            rgba(139, 92, 246, 0.35);

        box-shadow:
            0 18px 50px rgba(76, 29, 149, 0.16);
    }

    .card-icon {
        display: flex;
        align-items: center;
        justify-content: center;

        width: 45px;
        height: 45px;

        margin-bottom: 1rem;

        border-radius: 14px;

        background:
            linear-gradient(
                135deg,
                rgba(124, 58, 237, 0.22),
                rgba(59, 130, 246, 0.13)
            );

        border: 1px solid rgba(139, 92, 246, 0.20);

        font-size: 1.25rem;
    }

    .card-title {
        color: #f8fafc;

        font-size: 0.98rem;
        font-weight: 650;
    }

    .card-description {
        margin-top: 0.45rem;

        color: #94a3b8;

        font-size: 0.76rem;
        line-height: 1.5;
    }

    .card-arrow {
        margin-top: 0.8rem;

        color: #a78bfa;

        font-size: 1rem;
    }


    /* ========================================================
       STREAMLIT BUTTONS
       ======================================================== */

    .stButton > button {
        width: 100%;

        margin-top: 0.65rem;

        border-radius: 12px;

        background:
            rgba(124, 58, 237, 0.08);

        border:
            1px solid rgba(139, 92, 246, 0.16);

        color: #a78bfa;

        font-size: 0.75rem;

        transition:
            background 0.2s ease,
            border-color 0.2s ease;
    }

    .stButton > button:hover {
        background:
            rgba(124, 58, 237, 0.16);

        border-color:
            rgba(139, 92, 246, 0.35);

        color: #c4b5fd;
    }


    /* ========================================================
       CHAT
       ======================================================== */

    div[data-testid="stChatMessage"] {
        background: transparent;
    }

    div[data-testid="stChatMessageContent"] {
        color: #e2e8f0;
    }

    .stChatInput {
        margin-top: 1.2rem;
    }

    .stChatInput > div {
        border-radius: 20px !important;

        border:
            1px solid rgba(139, 92, 246, 0.30) !important;

        background:
            rgba(7, 11, 21, 0.92) !important;

        box-shadow:
            0 10px 40px rgba(0, 0, 0, 0.28),
            0 0 35px rgba(124, 58, 237, 0.06);
    }

    .stChatInput textarea {
        color: #f8fafc !important;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .privacy-note {
        margin-top: 1.3rem;

        text-align: center;

        color: #475569;

        font-size: 0.7rem;
    }

    .privacy-note strong {
        color: #64748b;
    }


    /* ========================================================
       HIDE STREAMLIT DEFAULT UI
       ======================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

</style>
""")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    render_html("""
    <div class="sidebar-brand">

        <div class="sidebar-logo">
            🧠 SIRA
        </div>

        <div class="sidebar-tagline">
            Sid's Intelligent Resource Assistant
        </div>

    </div>
    """)

    render_html("""
    <div class="sidebar-status">

        <div class="status-row">
            <span class="green-dot"></span>
            Personal AI is online
        </div>

        <div class="status-subtitle">
            Always here to help you grow.
        </div>

    </div>
    """)

    render_html("""
    <div class="sidebar-section-title">
        Modes
    </div>
    """)

    mode = st.radio(
        "Mode",
        [
            "💬 General",
            "🎤 Interview",
            "💼 Career",
            "📚 Learning",
            "💻 Projects"
        ],
        label_visibility="collapsed"
    )

    render_html("""
    <div class="sidebar-section-title">
        Knowledge Base
    </div>
    """)

    knowledge_items = [
        "Profile",
        "Resume",
        "Projects",
        "Interviews",
        "Learning"
    ]

    for item in knowledge_items:

        render_html(f"""
        <div class="knowledge-item">

            <span class="knowledge-check">
                ✓
            </span>

            <span>
                {item}
            </span>

        </div>
        """)

    render_html("""
    <div class="sidebar-footer">

        ⚡ Powered by<br>

        <strong>GPT-5.6-luna</strong><br>

        + ChromaDB

    </div>
    """)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ============================================================
# WELCOME SCREEN
# ============================================================

if len(st.session_state.messages) == 0:

    render_html("""
    <div class="hero-card">

        <div class="greeting">
            👋 Good to see you, <span>Sid!</span>
        </div>

        <div class="hero-question">
            What do you want to work on today?
        </div>

        <div class="quote">

            "Focus on progress,<br>
            not perfection."

            <br><br>

            <span class="quote-highlight">
                — Keep building
            </span>

        </div>

    </div>
    """)

    render_html("""
    <div class="cards-title">
        What can I help you with?
    </div>
    """)

    columns = st.columns(5)

    cards = [

        (
            "🎤",
            "Interview Prep",
            "Practice questions and get personalized interview guidance.",
            "Prepare me for an interview."
        ),

        (
            "📚",
            "What should I learn?",
            "Get a personalized learning direction based on your goals.",
            "What should I learn next?"
        ),

        (
            "💼",
            "Career Guidance",
            "Get advice based on your experience and career direction.",
            "Give me career guidance."
        ),

        (
            "💻",
            "My Projects",
            "Explore your projects, technologies and technical experience.",
            "Tell me about my projects."
        ),

        (
            "📊",
            "Resume Review",
            "Review your experience and identify areas to improve.",
            "Review my resume."
        )
    ]

    for column, card in zip(columns, cards):

        icon, title, description, prompt = card

        with column:

            render_html(f"""
            <div class="action-card">

                <div class="card-icon">
                    {icon}
                </div>

                <div class="card-title">
                    {title}
                </div>

                <div class="card-description">
                    {description}
                </div>

                <div class="card-arrow">
                    →
                </div>

            </div>
            """)

            if st.button(
                "Open",
                key=f"card_{title}"
            ):

                st.session_state.pending_prompt = prompt

                st.rerun()


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

pending_prompt = st.session_state.pop(
    "pending_prompt",
    None
)

user_input = st.chat_input(
    "Ask SIRA anything about you..."
)

if pending_prompt:

    user_input = pending_prompt


# ============================================================
# PROCESS QUESTION
# ============================================================

if user_input:

    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

    with st.chat_message("user"):

        st.markdown(user_input)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    # --------------------------------------------------------
    # RETRIEVAL
    # --------------------------------------------------------

    results = search(
        user_input,
        top_k=3
    )

    memories = get_recent_memories(
        limit=10
    )

    memory_context = "\n\n".join(
        [
            f"""
    Memory type: {memory['memory_type']}

    {memory['content']}
    """
            for memory in memories
        ]
    )


    retrieved_context = "\n\n".join(
        [
            f"""
Source: {result['source']}

{result['content']}
"""
            for result in results
        ]
    )


    # --------------------------------------------------------
    # MODE INSTRUCTIONS
    # --------------------------------------------------------

    mode_instructions = {

        "💬 General":
            """
            Answer naturally and helpfully using
            the user's personal context.
            """,

        "🎤 Interview":
            """
            Focus on interview preparation,
            technical questions, behavioral questions,
            and interview improvement.
            """,

        "💼 Career":
            """
            Focus on career development,
            role selection, skill gaps,
            resume positioning, and career decisions.
            """,

        "📚 Learning":
            """
            Focus on learning plans,
            technical concepts, study priorities,
            and identifying what the user should
            learn next.
            """,

        "💻 Projects":
            """
            Focus on the user's projects,
            technologies, architecture,
            contributions, achievements,
            and interview explanations.
            """
    }


    selected_instruction = mode_instructions.get(
        mode,
        mode_instructions["💬 General"]
    )


    # --------------------------------------------------------
    # PROMPT
    # --------------------------------------------------------

    prompt = f"""
    You are SIRA — Sid's Intelligent Resource Assistant.

    You are a personal AI assistant designed specifically
    to help Sid with his career, interviews, learning,
    projects, resume, and professional development.

    CURRENT MODE:

    {mode}

    MODE INSTRUCTION:

    {selected_instruction}

    IMPORTANT RULES:

    - Use the retrieved personal context when relevant.
    - Use personal memories when they are relevant.
    - Do not invent personal information.
    - Do not claim Sid has experience with something
    unless the available context supports it.
    - If the available context does not contain enough
    information, clearly say so.
    - Prefer Sid's actual experience over generic assumptions.
    - Give practical and personalized answers.
    - Do not mention RAG, ChromaDB, embeddings, or
    internal implementation details unless Sid asks.
    - Speak naturally like a personal assistant.

    RETRIEVED PERSONAL KNOWLEDGE:

    {retrieved_context}

    PERSONAL MEMORY:

    {memory_context}

    USER QUESTION:

    {user_input}
    """


    # --------------------------------------------------------
    # GEMINI RESPONSE
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("SIRA is thinking..."):

            response = client.responses.create(
                model="gpt-5.6-luna",
                input=prompt
            )

            response_text = response.output_text
            st.markdown(response_text)

            memory_result = extract_memory(user_input)

            if memory_result != "NONE":

                lines = memory_result.splitlines()

                memory_type = "general"
                memory_content = ""

                for line in lines:

                    if line.startswith("TYPE:"):
                        memory_type = (
                            line.replace(
                                "TYPE:",
                                ""
                            )
                            .strip()
                        )

                    elif line.startswith("MEMORY:"):
                        memory_content = (
                            line.replace(
                                "MEMORY:",
                                ""
                            )
                            .strip()
                        )

                if memory_content:

                    save_memory(
                        memory_type,
                        memory_content
                    )

                    st.markdown(response_text)


    # --------------------------------------------------------
    # SAVE RESPONSE
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response_text
        }
    )


# ============================================================
# FOOTER
# ============================================================

render_html("""
<div class="privacy-note">

    🔒
    <strong>
        SIRA uses your personal knowledge base
    </strong>

    to provide relevant and personalized answers.

</div>
""")