import os
from pymongo import MongoClient
import streamlit as st

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

@st.cache_resource
def get_mongo_client():
    return MongoClient(MONGO_URI)

def get_users_collection():
    return get_mongo_client()["clinical_db"]["users"]
