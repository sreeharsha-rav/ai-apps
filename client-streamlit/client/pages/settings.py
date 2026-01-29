import streamlit as st


st.markdown("**Configure your shared preferences**")


# Theme options (define at top)
theme_options = ["Light", "Dark"]

# Initialize session state
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

# Use selectbox - returns list, so index with [0]
selected_index = st.selectbox(
    "Select Theme:",
    options=range(len(theme_options)),  # Use indices 0,1 instead of strings
    index=theme_options.index(st.session_state.theme),
    format_func=lambda i: theme_options[i]
)

# Fix: Use selected_index directly (int) or selected_index[0] if using strings
st.session_state.theme = theme_options[selected_index]  # ✅ selected_index is now int

st.rerun()  # Apply theme change immediately

