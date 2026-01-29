import streamlit as st

st.markdown("**Live data synced from other pages**")

# Charts using shared state
col1, col2 = st.columns(2)

with col1:
    st.subheader("Counter History")
    st.bar_chart([st.session_state.counter] * 5)

with col2:
    st.subheader("User Stats")
    st.metric("Active User", st.session_state.user_name)
    st.metric("Page Visits", st.session_state.counter)

st.success("✅ Counter and user name sync from Home/Settings!")
