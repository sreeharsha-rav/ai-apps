import os
import streamlit as st
from dotenv import load_dotenv

from core.storage import JSONStorage
from services.chat import ChatService
from services.thread import ThreadManager
from core.ui import Sidebar, ChatView
from core.models import Role

load_dotenv()

st.set_page_config(page_title="LLM Chat", page_icon="💬", layout="wide")


# Initialize services
@st.cache_resource
def init_services():
    storage = JSONStorage("../data/threads.json")
    thread_manager = ThreadManager(storage)
    chat_service = ChatService(
        thread_manager=thread_manager,
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o-mini"
    )
    return thread_manager, chat_service


thread_mgr, chat_svc = init_services()

if "current_thread_id" not in st.session_state:
    st.session_state.current_thread_id = None


# Event handlers
def new_thread():
    thread = thread_mgr.create()
    st.session_state.current_thread_id = thread.thread_id
    st.rerun()


def load_thread(thread_id: str):
    st.session_state.current_thread_id = thread_id
    st.rerun()


def delete_thread(thread_id: str):
    thread_mgr.delete(thread_id)
    if st.session_state.current_thread_id == thread_id:
        st.session_state.current_thread_id = None
    st.rerun()


# Render UI
with st.sidebar:
    Sidebar.render(
        threads=thread_mgr.list_all(),
        current_id=st.session_state.current_thread_id,
        on_new=new_thread,
        on_load=load_thread,
        on_delete=delete_thread
    )

st.title("💬 LLM Chat")

current_thread = None
if st.session_state.current_thread_id:
    current_thread = thread_mgr.get(st.session_state.current_thread_id)
    if current_thread:
        st.caption(f"📝 {current_thread.name}")

messages = current_thread.messages if current_thread else []
chat_container = ChatView.render(messages)

if prompt := st.chat_input("Type your message..."):
    # Auto-create thread
    if not st.session_state.current_thread_id:
        thread = thread_mgr.create()
        st.session_state.current_thread_id = thread.thread_id
        current_thread = thread

    # Show user message
    with chat_container:
        with st.chat_message(Role.USER.value):
            st.markdown(prompt)

        # Stream response
        with st.chat_message(Role.ASSISTANT.value):
            response = st.write_stream(
                chat_svc.send_message(
                    thread_id=st.session_state.current_thread_id,
                    content=prompt
                )
            )

    chat_svc.save_response(
        thread_id=st.session_state.current_thread_id,
        content=response
    )
    st.rerun()


