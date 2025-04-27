# TravelGenie: Your Personalized AI Travel Companion 🌍✈️

An AI-powered RAG (Retrieval-Augmented Generation) travel planning app that combines YouTube content, real-time web search, and LLMs to create smart, customized travel itineraries.

---

## 🚀 Project Overview

TravelGenie is designed to simplify travel planning by integrating semantic search, real-time updates, and AI-driven personalization into one platform.
It fetches data from YouTube videos, live web search APIs, and combines it using GPT-4o to deliver complete, day-by-day travel plans.

---

## 📚 Features

- User Authentication: Sign Up, Login, Logout system.
- Interactive Chatbot: Plan your trips using a conversational interface (built with Streamlit).
- Semantic Retrieval: Pulls personalized data using Pinecone Vector DB.
- Real-Time Updates: Fetches fresh travel information from the internet using Tavily API.
- YouTube Integration: Shows relevant travel videos alongside plans.
- Travel Itinerary PDF: Download your full itinerary as a structured PDF.
- User-Friendly Navigation: Welcome page, sidebar for easy movement between sections.

---

## 🛠️ Technologies Used

- **Frontend:** Streamlit
- **Backend:** FastAPI
- **Large Language Model:** OpenAI GPT-4o
- **Vector Database:** Pinecone
- **APIs:**
  - YouTube Data API (for video content)
  - Tavily Web Search API (for live updates)
- **Authentication Storage:** Snowflake (optional)

---

## 🧩 System Architecture

- **Data Layer:** Collects YouTube data and real-time web content; stores embeddings in Pinecone DB.
- **Application Layer:** Handles query processing, semantic retrieval (RAG Helper), real-time updates (Web Search Helper), and response generation (GPT-4o).
- **Presentation Layer:** Streamlit UI for interactive travel planning and itinerary download.

---

## 🗺️ Flow Diagrams

- **System Interaction Flow:** User authenticates → submits query → pulls from YouTube, Tavily, Pinecone → generates itinerary → displays in chatbot → allows PDF download.
- **Pinecone Query Flow:** User query → semantic search → retrieve matching travel data → context building → GPT-based response generation → display to user.

---

## 📸 Project Walkthrough

1. **Welcome Page:**
   Sidebar with options — Welcome, Signup, Login, Chat, Logout.

2. **Signup Page:**
   Create a new account with a username and password.

3. **Login Page:**
   Enter credentials to access the TravelGenie platform.

4. **Chat Page:**
   Input your destination query and get a detailed itinerary.

5. **View Relevant Videos:**
   Get embedded YouTube videos for better exploration.

6. **Download PDF:**
   Export your full travel plan into a neatly organized PDF.

7. **Logout:**
   Securely exit back to the Welcome page.

---

## 🏃‍♂️ How to Run TravelGenie Locally

Follow these steps to set up and run the TravelGenie project on your local machine:

1. **Download the ZIP file**

   ```
   Open the zipfile in VSCode

   ```

2. **Install Required Libraries in fast_api and streamlit folders**

   ```
   pip install -r requirements.txt

   ```

3. **Create a `.env` File for API Keys in the FastAPI folder**
   In the root directory, create a `.env` file and add:

   ```
   OPENAI_API_KEY=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
   SNOWFLAKE_USER=YASHASWINITADISHETTY
   SNOWFLAKE_PASSWORD=Kattachinnu@2001
   SNOWFLAKE_ACCOUNT=ZCRAKFL-MXB17886
   SNOWFLAKE_DATABASE=TRAVEL_PLANNER_DB
   SNOWFLAKE_SCHEMA=PUBLIC
   SNOWFLAKE_WAREHOUSE=COMPUTE_WH
   PINECONE_API_KEY=pcsk_2MmSGd_KDCXnuKptRnCE8uRk25pdf25BeV3jo7jjBDNzbXPs1zf5GMjyahpiwkD6uJzxGr
   PINECONE_ENVIRONMENT=us-east-1
   ```

   **Create another `.env` File in the StreamLit folder for the below API Keys**
   FASTAPI_URL=http://127.0.0.1:8000
   PINECONE_API_KEY=pcsk_2MmSGd_KDCXnuKptRnCE8uRk25pdf25BeV3jo7jjBDNzbXPs1zf5GMjyahpiwkD6uJzxGr
   PINECONE_ENVIRONMENT=us-east-1
   OPENAI_API_KEY=sk-proj-Y325g7LExFKWFqoIPxsPRQhZcbv6HQvfcRCfgf8yXLdyQCd9hPg_o1LGlywdt_xbhXvKEL-\_PrT3BlbkFJc03mpiMMMNYGsNZPxulUkr1NFAFaMeG0mGGi6Lp0l-m2VM10LS5lRXCnKljvbcha8bHEYsxTYA

4. **Start the Backend (FastAPI) Server in the FastAPI folder**

   ```
   uvicorn main:app --reload --port 8000 --env-file .env
   ```

   - Make sure FastAPI runs on default `http://127.0.0.1:8000`.

5. **Start the Frontend (Streamlit) App**
   In a new terminal (or new tab):

   ```
   streamlit run app.py
   ```

   - Streamlit will open automatically in your browser (usually at `http://localhost:8501`).

6. **Interact with TravelGenie!**
   - Sign Up / Login
   - Enter your travel query
   - View generated travel plan + YouTube videos
   - Download the PDF
   - Logout when done

---

### ⚡ Quick Notes:

- Make sure ports `8000` (FastAPI) and `8501` (Streamlit) are free.
- Internet connection is needed for real-time search (Tavily) and YouTube video retrieval.
- Snowflake is optional if you just want basic login functionality.
- Use correct API keys else backend fetching might fail.

---

## 📈 Evaluation Metrics

- **Accuracy:** How well the results match user queries.
- **Response Time:** How fast the itinerary is generated.
- **User Experience:** Ease of using the chatbot interface.
- **Quality of Plans:** Relevance and completeness of the travel itinerary.
- **PDF Download:** Smooth functionality for exporting plans offline.

---

## 📜 License

This project is licensed under the [MIT License](#).

---

## 🤝 Contributors

- **Saipavan Katta** – 002209016
- **Yashaswini Tadishetty** – 002209058

---

> ✨ TravelGenie makes travel planning smarter, faster, and way more exciting!
