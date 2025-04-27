import streamlit as st
import requests
from fpdf import FPDF
import os

# ✅ Backend URL
FASTAPI_URL = "https://travelgenie-ob24.onrender.com"

# Function to make POST request to FastAPI
def call_fastapi_endpoint(endpoint, payload):
    url = f"{FASTAPI_URL}{endpoint}"
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Failed to call {endpoint}: {e}")
        return None

# ✅ Create PDF without custom fonts (safe for Streamlit Cloud)
def create_pdf(content):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Use built-in font (no need for external font file)
        pdf.set_font("Arial", size=16)
        pdf.cell(0, 10, "Your Travel Itinerary", ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", size=12)
        paragraphs = content.split("\n\n")
        for paragraph in paragraphs:
            pdf.multi_cell(0, 10, paragraph)
            pdf.ln(5)

        pdf_file = "travel_itinerary.pdf"
        pdf.output(pdf_file)
        return pdf_file
    except Exception as e:
        raise RuntimeError(f"Failed to create PDF: {e}")

# Main Streamlit App
def chat():
    st.title("🌍 Travel Itinerary & Vlogs")

    # Query input
    query = st.text_area("✍️ Enter your travel-related query:", placeholder="e.g., 'Plan a 5-day itinerary for Paris'")

    if st.button("Generate Full Travel Suggestions"):
        if query.strip():
            st.write(f"🤔 **Your Query:** {query}")
            
            st.info("💡 **Generating your personalized travel itinerary...**")
            response_payload = {"query": query, "top_k": 5, "threshold": 0.75}
            itinerary_response = call_fastapi_endpoint("/generate-openai-response", response_payload)

            if itinerary_response and "response" in itinerary_response:
                st.session_state.itinerary_response = itinerary_response["response"]
                st.markdown(itinerary_response["response"])
            else:
                st.warning("⚠️ Could not generate a proper itinerary. Please try refining your query.")

            st.info("🔍 **Fetching additional web suggestions...**")
            search_payload = {"query": f"Create a detailed travel itinerary: {query}", "max_results": 1}
            search_results = call_fastapi_endpoint("/search", search_payload)

            if search_results and "results" in search_results:
                st.markdown("### 🗺️ More information for your exploration:")
                for idx, item in enumerate(search_results["results"], start=1):
                    st.write(f"**{item.get('title', 'No Title')}**")
                    st.write(f"📍 {item.get('content', 'No description available.')}")
                    st.write(f"🌐 [Learn More]({item.get('url', '#')})")
                    st.markdown("---")
            else:
                st.warning("⚠️ No web suggestions found.")

            st.info("🎥 **Fetching related YouTube videos...**")
            youtube_payload = {"query": f"Best travel vlogs for {query}", "max_results": 1}
            youtube_results = call_fastapi_endpoint("/youtube-search", youtube_payload)

            if youtube_results and "results" in youtube_results and len(youtube_results["results"]) > 0:
                st.markdown("### 🎥 Watch related YouTube videos:")
                for idx, video in enumerate(youtube_results["results"], start=1):
                    st.write(f"**{video.get('title', 'No Title')}**")
                    st.video(video.get("url", "#"))
                    st.markdown("---")
            else:
                st.warning("🎬 No related YouTube videos found.")

            if itinerary_response and "response" in itinerary_response:
                st.info("💾 **Download Your Itinerary as a PDF**")

                try:
                    pdf_file = create_pdf(itinerary_response["response"])

                    with open(pdf_file, "rb") as file:
                        st.download_button(
                            label="📥 Download PDF",
                            data=file,
                            file_name="travel_itinerary.pdf",
                            mime="application/pdf"
                        )
                except Exception as e:
                    st.error(f"⚠️ Failed to generate the PDF. Error: {e}")

    if st.button("Go Back to Chat"):
        st.session_state.page = "Chat"
        st.rerun()

if __name__ == "__main__":
    chat()
