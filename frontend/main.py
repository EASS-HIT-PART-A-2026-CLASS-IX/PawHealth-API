import streamlit as st
import httpx
import os
import uuid

st.set_page_config(page_title="PawHealth Pro", layout="wide")
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

with st.sidebar:
    st.title("PawHealth Pro")
    try:
        httpx.get(f"{BACKEND_URL}/healthz", timeout=1.0)
        st.success("System Connectivity: Online")
    except:
        st.error("System Connectivity: Offline")
    st.caption(f"Trace ID: {uuid.uuid4()}")

st.title("Pet Management & Nutrition Diagnostics")
t1, t2, t3 = st.tabs(["📋 Registry", "🧪 AI Analysis", "➕ Add Pet"])

with t1:
    if st.button("Sync Data"):
        try:
            dogs = httpx.get(f"{BACKEND_URL}/dogs/").json()
            for d in dogs:
                st.write(f"**{d['name']}** ({d['breed']}) - Age: {d['age']}")
        except: st.error("Sync Failed")

with t2:
    st.subheader("AI Toxicity Check")
    food = st.text_input("Analyte")
    if st.button("Analyze"):
        st.info("Inference engine processing...")
