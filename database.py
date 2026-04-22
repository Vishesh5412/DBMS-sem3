import os
from pymongo import MongoClient
import streamlit as st
from dotenv import load_dotenv

# Priority: Streamlit secrets (cloud) → env var (.env file)
def _get_uri():
    try:
        return st.secrets["MONGO_URI"]
    except Exception:
        pass
    
    load_dotenv()
    uri = os.getenv("MONGO_URI")
    if not uri:
        raise ValueError("MONGO_URI is not set. Please add it to your .env file or Streamlit secrets.")
    return uri

MONGO_URI = _get_uri()

@st.cache_resource
def get_mongo_client():
    return MongoClient(MONGO_URI)

def get_users_collection():
    return get_mongo_client()["clinical_db"]["users"]
