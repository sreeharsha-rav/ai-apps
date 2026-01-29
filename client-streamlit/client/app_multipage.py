import streamlit as st

# Initialize shared session state
if "user_name" not in st.session_state:
    st.session_state.user_name = "Guest"
if "counter" not in st.session_state:
    st.session_state.counter = 0
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

st.set_page_config(
    page_title="Multi-Page Demo",
    page_icon="🚀",
    layout="wide"
)

home_page = st.Page("pages/home.py", title="Home", icon="🏠")
dashboard_page = st.Page("pages/dashboard.py", title="Dashboard", icon="📈")
settings_page = st.Page("pages/settings.py", title="Settings", icon="⚙️")

# Shared sidebar widget (syncs across all pages)
st.sidebar.markdown("### **Shared Controls**")
st.session_state.user_name = st.sidebar.text_input(
    "User Name",
    value=st.session_state.user_name,
    key="shared_user_name"
)


# top navigation (position="sidebar" is default)
pg = st.navigation(
    [home_page, dashboard_page, settings_page],
    position="top",   # or "top"
    expanded=True,        # keep sidebar menu open
)

pg.run()
