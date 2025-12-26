import streamlit as st

from app.models import ChatHistory, Message
from app.llm import get_streaming_response

st.title("LLM Chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    
# React to user input
if prompt := st.chat_input("What is up?"):
    
    with st.chat_message("user"):
        st.markdown(prompt)
        
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        # Convert dictionary messages to Message objects for the ChatHistory
        message_objects = [Message(role=msg["role"], content=msg["content"]) for msg in st.session_state.messages]
        response = st.write_stream(get_streaming_response(
            system_instruction="You are a helpful assistant.",
            history=ChatHistory(messages=message_objects)
        ))
    st.session_state.messages.append({"role": "assistant", "content": response})