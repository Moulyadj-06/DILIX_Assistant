import streamlit as st
from backend.llm_engine import get_llm_response
from backend.memory_manager import save_conversation
from backend.document_ingestor import extract_text_from_pdf, extract_text_from_docx, save_uploaded_file
from backend.vector_store import add_to_vector_store, query_vector_store
from datetime import datetime


st.set_page_config(page_title="🧠 DILIX", layout="wide")
st.title("🤖 DILIX — Diligent Intelligent Assistant")

# -----------------------------
# Initialize chat history
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Sidebar file upload
# -----------------------------
st.sidebar.header(" Upload Documents")
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
[data-testid="stSidebar"] { 
    background-color: #1e1e2f; 
    color: white; 
    padding: 10px; 
}

.chat-container {
    display: flex;
    flex-direction: column;
    padding: 10px;
    gap: 10px;          
    margin-bottom: 70px;  
}

.chat-bubble {
    padding: 10px 15px;
    border-radius: 12px;
    max-width: 60%;
    font-family: 'Segoe UI', sans-serif;
    word-wrap: break-word;
    margin: 5px 0;
}

.user {
    background-color: #0a84ff;
    color: white;
    align-self: flex-end;       
    text-align: right;
    border-top-left-radius: 12px;
    border-top-right-radius: 0;
    border-bottom-left-radius: 12px;
    border-bottom-right-radius: 12px;
    margin-left: auto;          
}

.bot {
    background-color: #2a2a3c;
    color: white;
    align-self: flex-start;     
    text-align: left;
    border-top-right-radius: 12px;
    border-top-left-radius: 0;
    border-bottom-left-radius: 12px;
    border-bottom-right-radius: 12px;
    margin-right: auto;         
}

.fixed-input {
    position: fixed;
    bottom: 10px;
    left: 20rem;  /* offset for sidebar */
    width: calc(100% - 20rem);
    padding: 10px 20px;
    background-color: #1e1e2f;
    display: flex;
    gap: 15px;
    z-index: 100;
}

.fixed-input input {
    flex: 1;
    padding: 10px;
    border-radius: 10px;
    border: none;
    font-size: 16px;
}

.fixed-input button {
    padding: 10px 20px;
    border-radius: 8px;
    border: none;
    background-color: #0a84ff;
    color: white;
    font-weight: bold;
    cursor: pointer;
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






