import streamlit as st
import requests
from dotenv import load_dotenv
import os


# Use a default value if FASTAPI_URL is not set
FASTAPI_URL ="https://travelgenie-ob24.onrender.com" 

# Set the page configuration to have a wide layout
# st.set_page_config(page_title="TravelGenie", page_icon="🧳", layout="wide")

# Custom CSS to style the login page
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(135deg, #6a11cb, #2575fc);  /* Gradient background */
            color: white;
            font-family: 'Arial', sans-serif;
            height: 100vh;
            margin: 0;
        }

        .login-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
            padding: 20px;
        }

        .login-box {
            background-color: rgba(0, 0, 0, 0.7);
            padding: 30px;
            border-radius: 10px;
            width: 100%;
            max-width: 400px;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        }

        .login-header {
            font-size: 32px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 30px;
        }

        .input-field {
            margin-bottom: 20px;
        }

        .input-field input {
            width: 100%;
            padding: 15px;
            border-radius: 5px;
            border: none;
            margin-top: 5px;
            font-size: 16px;
            color: #333;
        }

        .input-field input:focus {
            outline: none;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
        }

        .login-btn {
            background-color: #2575fc;
            color: white;
            border: none;
            padding: 15px;
            border-radius: 5px;
            width: 100%;
            font-size: 18px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        .login-btn:hover {
            background-color: #6a11cb;
        }

        .error-message {
            color: #ff4d4d;
            font-size: 14px;
            margin-top: 10px;
        }
    </style>
    """, unsafe_allow_html=True
)

def login():
    st.title("🔑 Login")
    
    # Center the form with flexbox
    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<h1 class="login-header">Login to TravelGenie</h1>', unsafe_allow_html=True)

        # Username input field
        username = st.text_input("👤 Username", placeholder="Enter your username", key="username", label_visibility="collapsed")
        password = st.text_input("🔒 Password", placeholder="Enter your password", type="password", key="password", label_visibility="collapsed")

        if st.button("Login", key="login", use_container_width=True):
            if username and password:
                try:
                    response = requests.post(f"{FASTAPI_URL}/login", params={"username": username, "password": password})

                    if response.status_code == 200:
                        st.success("✅ Login successful! Redirecting to Chat...")
                        st.session_state.logged_in = True  # Mark the user as logged in
                        st.session_state.page = "Chat"  # Redirect to the Chat page
                        st.rerun()  # Refresh the page to apply the new session state
                    elif response.status_code == 401:
                        st.error("🚫 Invalid username or password. Please try again.")
                    else:
                        st.error(f"⚠️ Error: {response.json().get('detail', 'Something went wrong.')}")
                except requests.exceptions.RequestException as e:
                    st.error(f"⚠️ Unable to connect to the server. Error: {e}")
            else:
                st.error("⚠️ Please enter both username and password.", key="empty-error")

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Run the login function
if __name__ == "__main__":
    login()
