import streamlit as st
from welcome_page import welcome_page
from signup_page import sign_up
from login_page import login
from chat_page import chat
from dotenv import load_dotenv
import os

load_dotenv()

FASTAPI_URL = os.getenv("FASTAPI_URL")

# Set the page configuration ONCE at the top of app.py (ensure it's only once)
# st.set_page_config(page_title="AI Planner", page_icon="🤖", layout="wide")  # Remove this line

# Initialize session state variables
if "page" not in st.session_state:
    st.session_state.page = "Welcome"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "users" not in st.session_state:
    st.session_state.users = {}

# Sidebar navigation
selected_page = st.sidebar.radio(
    "Go to:",
    ["🏠 Welcome", "🔑 Login", "📝 Sign Up", "💬 Chat"],
    index=["Welcome", "Login", "Sign Up", "Chat"].index(st.session_state.page)
)

# Update the current page based on sidebar selection
if selected_page.startswith("🏠"):
    st.session_state.page = "Welcome"
elif selected_page.startswith("🔑"):
    st.session_state.page = "Login"
elif selected_page.startswith("📝"):
    st.session_state.page = "Sign Up"
elif selected_page.startswith("💬"):
    if not st.session_state.logged_in:
        st.sidebar.warning("🔒 Please log in to access Chat.")
        st.session_state.page = "Login"
    else:
        st.session_state.page = "Chat"

# Add Logout button if the user is logged in
if st.session_state.logged_in:
    st.sidebar.markdown("---")  # Add a separator
    if st.sidebar.button("🔓 Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "Welcome"
        st.sidebar.success("You have been logged out successfully.")

# Page routing logic
if st.session_state.page == "Welcome":
    welcome_page()
elif st.session_state.page == "Sign Up":
    sign_up()
elif st.session_state.page == "Login":
    login()
elif st.session_state.page == "Chat":
    chat()
