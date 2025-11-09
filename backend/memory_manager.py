conversation_history = []

def save_conversation(user_input, assistant_response):
    conversation_history.append({"user": user_input, "assistant": assistant_response})

def get_conversation_history():
    history_text = ""
    for entry in conversation_history:
        history_text += f"User: {entry['user']}\nDILIX: {entry['assistant']}\n\n"
    return history_text.strip()
