import streamlit as st
from dotenv import load_dotenv
import os

# Set the page configuration ONCE at the top of the app
st.set_page_config(page_title="TravelGenie", page_icon="🧳", layout="wide")



FASTAPI_URL ="https://travelgenie-ob24.onrender.com" 

# Your welcome page function
def welcome_page():
    # Render the welcome page content with a more modern and visually appealing design
    st.markdown(
        """
        <style>
            .container {
                text-align: center;
                background-color: #f7f7f7;
                padding: 50px;
                border-radius: 10px;
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
                margin-top: 50px;
            }
            h1 {
                font-family: 'Arial', sans-serif;
                font-size: 36px;
                color: #5E5C5C;
            }
            p {
                font-size: 18px;
                line-height: 1.6;
                color: #333;
                font-family: 'Arial', sans-serif;
            }
            .highlight {
                color: #4CAF50;
                font-weight: bold;
            }
            .feature-list {
                text-align: left;
                margin-top: 20px;
                list-style-type: none;
                padding: 0;
            }
            .feature-list li {
                font-size: 16px;
                margin-bottom: 10px;
                padding-left: 20px;
                position: relative;
            }
            .feature-list li::before {
                content: "✔️";
                position: absolute;
                left: 0;
                top: 0;
                font-size: 18px;
            }
            .footer {
                font-size: 14px;
                margin-top: 30px;
                color: #888;
            }
        </style>
        <div class="container">
            <h1>🤖 Welcome to TravelGenie: Your Friendly AI Travel Planner</h1>
            <p>Plan smarter, chat better, and stay productive with <span class="highlight">TravelGenie</span>!</p>
            <p>We help you with:</p>
            <ul class="feature-list">
                <li>🗺️ Finding relevant searches for your travel plans</li>
                <li>📋 Creating personalized itineraries tailored just for you</li>
                <li>🎥 Suggesting YouTube videos to explore new destinations</li>
                <li>🌐 Providing website links for easy access to bookings</li>
                <li>🖨️ Allowing you to take a printout of your itinerary for a hassle-free trip</li>
            </ul>
            <p><span class="highlight">Your one-stop solution to smarter, easier, and more personalized travel planning!</span></p>
        </div>
        <div class="footer">
            <p>&copy; 2025 TravelGenie. All rights reserved.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Call welcome_page() if this script is the main one being executed
if __name__ == "__main__":
    welcome_page()
