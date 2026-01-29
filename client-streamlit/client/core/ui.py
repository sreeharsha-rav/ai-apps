import streamlit as st
from typing import Callable, Optional

from .models import Thread, Message


class Sidebar:
    """Thread management sidebar."""

    @staticmethod
    def render(
        threads: list[Thread],
        current_id: Optional[str],
        on_new: Callable,
        on_load: Callable[[str], None],
        on_delete: Callable[[str], None]
    ):
        st.header("💬 Threads")

        if st.button("➕ New Chat", use_container_width=True):
            on_new()

        st.divider()

        if threads:
            for thread in threads:
                col1, col2 = st.columns([4, 1])
                with col1:
                    btn_type = "primary" if thread.thread_id == current_id else "secondary"
                    if st.button(
                        thread.name,
                        key=f"load_{thread.thread_id}",
                        use_container_width=True,
                        type=btn_type
                    ):
                        on_load(thread.thread_id)
                with col2:
                    if st.button("🗑️", key=f"del_{thread.thread_id}"):
                        on_delete(thread.thread_id)
        else:
            st.info("No threads yet")


class ChatView:
    """Chat message display."""

    @staticmethod
    def render(messages: list[Message], height: int = 600):
        container = st.container(height=height)
        with container:
            for msg in messages:
                with st.chat_message(msg.role.value):
                    st.markdown(msg.content)

        return container
