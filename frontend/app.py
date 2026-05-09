import streamlit as st
import httpx
import pandas as pd

# Page configuration for PawHealth Pro
st.set_page_config(page_title="PawHealth Pro", page_icon="🐾", layout="wide")
URL = "http://api:8000"

# Sidebar for authentication and system status
with st.sidebar:
    st.title("PawHealth Pro")
    token = st.text_input("JWT Token", type="password")
    st.info("System Status: Clinical/Online")

# Main Clinical Dashboard Header
st.title("Clinical Management Dashboard")
t1, t2, t3, t4 = st.tabs(["Registry", "Add Patient", "Weight Logs", "AI Analysis"])

# Tab 1: View existing patients
with t1:
    st.subheader("Patient Registry")
    if st.button("Refresh Registry"):
        try:
            r = httpx.get(f"{URL}/dogs")
            if r.status_code == 200:
                st.table(pd.DataFrame(r.json()))
        except:
            st.error("Connection to API failed")

# Tab 2: Register a new pet (e.g., Joey the King)
with t2:
    st.subheader("Register New Patient")
    with st.form("add_dog"):
        name = st.text_input("Name")
        breed = st.text_input("Breed")
        weight = st.number_input("Initial Weight (kg)", min_value=0.1)
        if st.form_submit_button("Register"):
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            data = {"name": name, "breed": breed, "initial_weight": weight}
            try:
                r = httpx.post(f"{URL}/dogs", json=data, headers=headers)
                if r.status_code == 200:
                    st.success(f"Patient {name} registered successfully")
                else:
                    st.error(f"Error: {r.text}")
            except:
                st.error("API Unavailable")

# Tab 3: Log weight updates for health monitoring
with t3:
    st.subheader("Log Weight Telemetry")
    with st.form("log_weight"):
        did = st.number_input("Patient ID", min_value=1)
        w = st.number_input("Current Weight (kg)", min_value=0.1)
        if st.form_submit_button("Update Weight"):
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            try:
                r = httpx.post(f"{URL}/health/weight", json={"dog_id": did, "weight": w}, headers=headers)
                if r.status_code == 200:
                    st.success("Weight telemetry synchronized")
                else:
                    st.error("Update failed")
            except:
                st.error("Service error")

# Tab 4: AI Sidecar toxicity diagnostics
with t4:
    st.subheader("AI Sidecar Analysis")
    food = st.text_area("Ingredients:")
    if st.button("Analyze"):
        # Check for common toxins like chocolate, onions, or grapes
        if any(x in food.lower() for x in ["onion", "chocolate", "grape", "garlic"]):
            st.error("Toxicity detected: Harmful ingredients found")
        else:
            st.success("Safe profile: No common hazards detected")

# Footer for HIT academic submission
st.divider()
st.caption("© 2026 PawHealth Pro | HIT EASS Final Project Submission")
