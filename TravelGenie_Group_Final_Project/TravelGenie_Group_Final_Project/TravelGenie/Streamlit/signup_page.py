import streamlit as st
import requests
from dotenv import load_dotenv
import os
load_dotenv()

# Use a default value if FASTAPI_URL is not set
FASTAPI_URL ="https://travelgenie-ob24.onrender.com" 



# Custom CSS to style the sign-up page
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

        .sign-up-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
            padding: 20px;
        }

        .sign-up-box {
            background-color: rgba(0, 0, 0, 0.7);
            padding: 30px;
            border-radius: 10px;
            width: 100%;
            max-width: 400px;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        }

        .sign-up-header {
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

        .sign-up-btn {
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

        .sign-up-btn:hover {
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

def sign_up():
    st.title("📝 Sign Up")

    # Center the form with flexbox
    with st.container():
        st.markdown('<div class="sign-up-container">', unsafe_allow_html=True)
        st.markdown('<div class="sign-up-box">', unsafe_allow_html=True)
        st.markdown('<h1 class="sign-up-header">Sign Up for TravelGenie</h1>', unsafe_allow_html=True)

        # Username input field
        username = st.text_input("👤 Username", placeholder="Enter username", key="username", label_visibility="collapsed")
        password = st.text_input("🔒 Password", placeholder="Choose password", type="password", key="password", label_visibility="collapsed")

        if st.button("Sign Up", key="sign-up", use_container_width=True):
            if username and password:
                try:
                    # Make a request to the FastAPI signup endpoint
                    response = requests.post(f"{FASTAPI_URL}/signup", params={"username": username, "password": password})

                    if response.status_code == 200:
                        st.success("🎉 Sign-up successful! You can now log in.")
                    elif response.status_code == 400:
                        st.error("🚨 Username already exists. Try another one.")
                    else:
                        st.error(f"⚠️ Error: {response.json().get('detail', 'Something went wrong.')}")
                except requests.exceptions.RequestException as e:
                    st.error(f"⚠️ Unable to connect to the server. Error: {e}")
            else:
                st.error("⚠️ Please fill in both fields.", key="empty-error")

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Run the sign-up function
if __name__ == "__main__":
    sign_up()
