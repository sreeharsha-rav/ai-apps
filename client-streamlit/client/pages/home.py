import streamlit as st

st.title("Home Page")
st.markdown("**Welcome back, {}!**".format(st.session_state.user_name))

col1, col2 = st.columns(2)
with col1:
    st.metric("Shared Counter", st.session_state.counter)
with col2:
    st.metric("Theme", st.session_state.theme)

if st.button("➕ Increment Shared Counter", use_container_width=True):
    st.session_state.counter += 1
    st.rerun()

st.info("👈 Change name/theme in sidebar - see it update here instantly!")
