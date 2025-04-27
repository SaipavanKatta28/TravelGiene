from dotenv import load_dotenv
import os
import json
import logging
from typing import Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
import pandas as pd

from websearch_normal import search_web, generate_response
from youtube_search import search_youtube
from openai_response import is_travel_related_gpt, generate_response_with_relevant_data
from openai import OpenAI

# ------------------------
# Load environment variables (.env)
# ------------------------
load_dotenv()  # Load the environment variables from the .env file
#print(f"✅ OPENAI_API_KEY loaded: {os.getenv('OPENAI_API_KEY') is not None}")
#print(f"✅ Snowflake User loaded: {os.getenv('SNOWFLAKE_USER') is not None}")

# ------------------------
# Environment Variables
# ------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")

# Validate keys
if not OPENAI_API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY missing! Check your .env file!")

# ------------------------
# Initialize FastAPI + OpenAI
# ------------------------
app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
client = OpenAI(api_key=OPENAI_API_KEY)

# ------------------------
# Helper Functions
# ------------------------
def get_snowflake_connection():
    import snowflake.connector
    return snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
        warehouse=SNOWFLAKE_WAREHOUSE
    )

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# ------------------------
# Models
# ------------------------
class SignupModel(BaseModel):
    username: str
    password: str

class LoginModel(BaseModel):
    username: str
    password: str


class SearchRequest(BaseModel):
    query: str
    max_results: int = 1

class GenerateRequest(BaseModel):
    query: str

class YouTubeSearchRequest(BaseModel):
    query: str
    max_results: int = 1

class GenerateResponseRequest(BaseModel):
    query: str
    top_k: int = 5
    threshold: float = 0.75

# ------------------------
# Routes
# ------------------------

@app.post("/signup")
async def signup(username: str, password: str):
    conn = get_snowflake_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Username already taken")
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        return {"message": "User signed up successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.post("/login")
async def login(username: str, password: str):
    conn = get_snowflake_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        if not result or not verify_password(password, result[0]):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        return {"message": "Login successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.post("/search")
async def search(request: SearchRequest):
    try:
        results = search_web(query=request.query, max_results=request.max_results)
        if "error" in results:
            raise HTTPException(status_code=400, detail=results["error"])
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-response")
async def generate(request: GenerateRequest):
    try:
        response = generate_response(query=request.query)
        if response.startswith("Error"):
            raise HTTPException(status_code=400, detail=response)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/youtube-search")
async def youtube_search(request: YouTubeSearchRequest):
    try:
        results = search_youtube(query=request.query, max_results=request.max_results)
        if "error" in results:
            raise HTTPException(status_code=400, detail=results["error"])
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/validate-query")
async def validate_query(query: str):
    try:
        is_travel_related = is_travel_related_gpt(query)
        return {"is_travel_related": is_travel_related}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating query: {e}")

@app.post("/generate-openai-response")
async def generate_openai_response(request: GenerateResponseRequest):
    try:
        is_travel_related = is_travel_related_gpt(request.query)
        if not is_travel_related:
            raise HTTPException(status_code=400, detail="This query doesn't seem travel-related.")
        relevant_matches = [
            {"metadata": {"text": "Visit the Eiffel Tower and the Louvre Museum.", "title": "Paris Highlights"}},
            {"metadata": {"text": "Enjoy a Seine River Cruise and explore Montmartre.", "title": "Romantic Paris"}},
        ]
        response = generate_response_with_relevant_data(request.query, relevant_matches)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

