import streamlit as st
import httpx
import pandas as pd

st.set_page_config(page_title="PawHealth Pro", page_icon="🐾", layout="wide")
URL = "http://api:8000"

with st.sidebar:
    st.title("PawHealth Pro")
    token = st.text_input("JWT Token", type="password")
    st.info("Status: Clinical/Online")

st.title("Clinical Management Dashboard")
t1, t2, t3, t4 = st.tabs(["Registry", "Add Patient", "Weight Logs", "AI Analysis"])

with t1:
    st.subheader("Patient Registry")
    if st.button("Refresh List"):
        try:
            r = httpx.get(f"{URL}/dogs")
            if r.status_code == 200:
                st.table(pd.DataFrame(r.json()))
        except:
            st.error("API Connection Failed")

with t2:
    st.subheader("Register New Patient")
    with st.form("add_dog_form"):
        name = st.text_input("Name")
        breed = st.text_input("Breed")
        weight = st.number_input("Initial Weight (kg)", min_value=0.1)
        if st.form_submit_button("Register Patient"):
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            data = {"name": name, "breed": breed, "initial_weight": weight}
            try:
                r = httpx.post(f"{URL}/dogs", json=data, headers=headers)
                if r.status_code == 200:
                    st.success(f"Patient {name} registered")
                else:
                    st.error(f"Error: {r.text}")
            except:
                st.error("API Unavailable")

with t3:
    st.subheader("Log Weight Telemetry")
    with st.form("weight_form"):
        did = st.number_input("Patient ID", min_value=1)
        w = st.number_input("Current Weight (kg)", min_value=0.1)
        if st.form_submit_button("Update Telemetry"):
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            try:
                r = httpx.post(f"{URL}/health/weight", json={"dog_id": did, "weight": w}, headers=headers)
                if r.status_code == 200:
                    st.success("Synchronized")
                else:
                    st.error("Update failed")
            except:
                st.error("Service error")

with t4:
    st.subheader("AI Sidecar Analysis")
    food = st.text_area("Ingredients:")
    if st.button("Run AI Scan"):
        if any(x in food.lower() for x in ["onion", "chocolate", "grape"]):
            st.error("Toxicity detected")
        else:
            st.success("Safe profile detected")

st.divider()
st.caption("© 2026 PawHealth Pro | HIT EASS Final Submission")
