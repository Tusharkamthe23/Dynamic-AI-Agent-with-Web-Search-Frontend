import streamlit as st
import requests
import os 
# 🔹 Your Render backend URL 
BACKEND_URL = os.environ.get("BACKEND_URL")

st.set_page_config(page_title="Dynamic AI Agent with Web Search", page_icon="🤖", layout="wide")
st.title("🤖 Dynamic AI Agent with Web")
st.write(" Create and Interact with the AI Agents!")

# Sidebar settings
st.sidebar.header("⚙️ Settings")

model_provider = st.sidebar.selectbox("Model Provider", ["Groq", "OpenAI"])
model_name = st.sidebar.selectbox(
    "Model Name",
    ["llama3-70b-8192", "mixtral-8x7b-32768", "llama-3.3-70b-versatile", "gpt-4o-mini"]
)
allow_search = st.sidebar.checkbox("Enable Web Search", value=False)
system_prompt = st.sidebar.text_area("System Prompt", "Act as an AI chatbot who is smart and friendly")

# Chat session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display past messages
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if user_input := st.chat_input("Type your message..."):
    # Add user message to chat
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare request payload
    payload = {
        "model_name": model_name,
        "model_provider": model_provider,
        "system_prompt": system_prompt,
        "messages": st.session_state["messages"],
        "allow_search": allow_search
    }

    # Send request to FastAPI backend
    try:
        response = requests.post(BACKEND_URL, json=payload)
        response_data = response.json()
        ai_response = response_data.get("response", "⚠️ No response from AI agent")

    except Exception as e:
        ai_response = f"⚠️ Error connecting to backend: {e}"

    # Add AI response to chat
    st.session_state["messages"].append({"role": "assistant", "content": ai_response})
    with st.chat_message("assistant"):
        st.markdown(ai_response)
