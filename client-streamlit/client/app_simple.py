import streamlit as st

from core.llm import get_streaming_response

st.set_page_config(page_title="LLM Chat", page_icon="💬", layout="wide")
st.title("💬 LLM Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

chat_container = st.container(height=600)
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Input your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with chat_container:
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = st.write_stream(get_streaming_response(
                system_instruction="You are a helpful assistant.",
                history=st.session_state.messages
            ))

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
