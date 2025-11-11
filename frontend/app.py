import streamlit as st
from backend.llm_engine import get_llm_response
from backend.memory_manager import save_conversation
from backend.document_ingestor import extract_text_from_pdf, extract_text_from_docx, save_uploaded_file
from backend.vector_store import add_to_vector_store, query_vector_store
from datetime import datetime
import os
import base64

st.set_page_config(page_title="🧠 DILIX", layout="wide")
# st.title("🤖 DILIX — Diligent Intelligent Assistant")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(120deg, #0b0b0b, #1a1a1a, #2b2b2b);
        color: white;
        background-attachment: fixed;
    }

    /* Centered text fade-in animation */
    h1, p {
        animation: fadeIn 1.5s ease-in-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Optional: Adjust spacing for better visual balance */
    .block-container {
        padding-top: 3rem;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Centered Header Section
# -----------------------------
logo_path = "assets/diligent_logo.png"  # Change path if needed

center_col = st.columns([1, 3, 1])[1]  # Middle column for centering
with center_col:
    if os.path.exists(logo_path):
        # Convert image to base64
        with open(logo_path, "rb") as img_file:
            logo_base64 = base64.b64encode(img_file.read()).decode()

        # Display logo + title + tagline (proper alignment)
        st.markdown(f"""
            <div style="text-align:center; margin-bottom:10px;">
                <div style="display:inline-flex; align-items:center; justify-content:center; gap:15px;">
                    <img src="data:image/png;base64,{logo_base64}" width="65" style="border-radius:10px;"/>
                    <h1 style="font-size:45px; color:#ef233c; margin:0; font-weight:900; letter-spacing:3px;">
                        DILIX — Diligent Intelligent Assistant
                    </h1>
                </div>
                <p style="font-size:20px; color:#f5f5f5; opacity:0.95; margin-top:10px; line-height:1.6;">
                    Empowering organizations with intelligent insights to clarify risk, strengthen governance, and drive smarter decisions.
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="text-align:center;">
                <h1 style="font-size:45px; color:#ef233c; margin-top:-10px; font-weight:900; letter-spacing:3px;">
                    DILIX — Diligent Intelligent Assistant
                </h1>
                <p style="font-size:20px; color:#f5f5f5; opacity:0.95; margin-top:10px; line-height:1.6;">
                    Empowering organizations with intelligent insights to clarify risk, strengthen governance, and drive smarter decisions.
                </p>
            </div>
        """, unsafe_allow_html=True)

# footer placeholder (we will style it fixed via CSS below)
st.markdown("""<div id="app-footer">© 2025 Diligent Technologies | Empowering Intelligent Governance</div>""", unsafe_allow_html=True)
# -----------------------------
# Initialize chat history
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Sidebar file upload
# -----------------------------
st.sidebar.header("📂 Upload Documents")
uploaded_file = st.sidebar.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])
if uploaded_file:
    file_path = save_uploaded_file(uploaded_file)
    text = extract_text_from_pdf(file_path) if uploaded_file.name.endswith(".pdf") else extract_text_from_docx(file_path)
    add_to_vector_store(file_path)
    st.sidebar.success(f" '{uploaded_file.name}' added to DILIX memory!")

# -----------------------------
# CSS Styling
# -----------------------------

st.markdown("""
<style>
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stApp {
    background: linear-gradient(-45deg, #8B0000, #1C1C1C, #B22222, #2E2E2E);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
    font-family: 'Segoe UI', sans-serif;
    color: #f8f9fa;
}

[data-testid="stSidebar"] {
    background: rgba(20, 20, 20, 0.9);
    color: white;
    padding: 20px;
    border-right: 1px solid rgba(255,255,255,0.1);
}

/* Chat container */
.chat-container {
    display: flex;
    flex-direction: column;
    padding: 10px 20px 120px; /* Add bottom padding for input */
    overflow-y: auto;
    max-height: 70vh;
}

/* Chat bubbles */
.chat-bubble {
    padding: 12px 18px;
    border-radius: 15px;
    max-width: 65%;
    word-wrap: break-word;
    font-size: 16px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    transition: all 0.3s ease;
    margin-top: 12px;
    margin-bottom: 12px;
}
.user {
    background-color: #ef233c;
    color: #fff;
    align-self: flex-end;
    border-top-right-radius: 0;
    margin-left: auto;       /* ✅ push to far right */
    border-bottom-right-radius: 5px;
}
.bot {
    background: rgba(255, 255, 255, 0.15);
    color: #fff;
    align-self: flex-start;
    border-top-left-radius: 0;
    margin-right: auto;      /* ✅ push to far left */
    border-bottom-left-radius: 5px;
    backdrop-filter: blur(8px);
}

/* Input form styling */
.stTextInput>div>div>input {
    height: 45px !important;
    background-color: #1E1E2F !important;
    color: #fff !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 10px 15px !important;
}
.stTextInput>div>div>input::placeholder {
    color: #aaa !important;
}
.stButton>button {
    height: 45px !important;
    background-color: #ef233c !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    transition: 0.3s ease;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
}
.stButton>button:hover {
    background-color: #d90429 !important;
    transform: translateY(-2px);
}

/* Footer */
#app-footer {
    position: fixed;
    bottom: 6px;
    left: 0;
    width: 100%;
    text-align: center;
    font-size: 14px;
    opacity: 0.85;
    color: #e6e6e6;
    z-index: 90;
}
</style>
""", unsafe_allow_html=True)



# -----------------------------
# Chat container
# -----------------------------
chat_placeholder = st.empty()

def render_chat():
    with chat_placeholder.container():
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        for msg in st.session_state.messages:
            bubble_class = "user" if msg['sender'] == "user" else "bot"
            icon = "👤" if msg['sender'] == "user" else "🤖"
            st.markdown(
                f"""
                <div class='chat-bubble {bubble_class}'>
                    <strong>{icon} {msg['sender'].capitalize()}</strong><br>
                    {msg['text']}<br>
                    <span style='font-size:10px; color:#ccc;'>{msg.get('time', '')}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown("</div>", unsafe_allow_html=True)

# Initial render
render_chat()

# -----------------------------
# Fixed input at bottom using form
# -----------------------------
with st.container():
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([8, 1])
        with col1:
            user_input = st.text_input("", placeholder="Type your message here...", key="chat_input")
        with col2:
            send_button = st.form_submit_button("Send")

# -----------------------------
# Process user input
# -----------------------------
if send_button and user_input.strip():
    # -----------------------------
    # Check if user is asking about the assistant itself
    # -----------------------------
    if any(word in user_input.lower() for word in ["who are you", "about yourself", "yourself"]):
        response = "I am DILIX, Diligent intelligent AI assistant. I can help you with documents, answer questions, " \
                   "and provide insights. I exist entirely in the digital space and am here to assist you."
    else:
        # -----------------------------
        # Normal vector store + LLM response
        # -----------------------------
        system_prompt = "You are DILIX, an AI assistant. Be helpful and polite."
        context_chunks = query_vector_store(user_input, top_k=5)
        context = "\n".join([chunk['answer'] for chunk in context_chunks if chunk.get('answer')]) \
            if context_chunks else "No relevant context found."
        prompt = f"{system_prompt}\n\nUse the below context to answer the user's question.\nContext:\n{context}\n\nQuestion: {user_input}\nAnswer:"
        response = get_llm_response(prompt).strip()

    # -----------------------------
    # Save conversation
    # -----------------------------
    save_conversation(user_input, response)

    # -----------------------------
    # Append messages and re-render chat
    # -----------------------------
    st.session_state.messages.append({
        "sender": "user",
        "text": user_input,
        "time": datetime.now().strftime("%H:%M")
    })
    st.session_state.messages.append({
        "sender": "bot",
        "text": response,
        "time": datetime.now().strftime("%H:%M")
    })
    render_chat()






