import streamlit as st
import httpx
import pandas as pd
import time
from datetime import datetime

# Page configuration
st.set_page_config(page_title="PawHealth Pro", page_icon="🐾", layout="wide")
URL = "http://api:8000"

# Initialize session state
if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None

# Helper for authenticated API requests
def make_request(method, endpoint, **kwargs):
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    try:
        return httpx.request(method, f"{URL}{endpoint}", headers=headers, follow_redirects=True, **kwargs)
    except Exception as e:
        st.error(f"Network Error: {e}")
        return None

# --- AUTHENTICATION SCREEN ---
if st.session_state.token is None:
    st.title("🐾 Welcome to PawHealth Pro")
    st.subheader("Clinical Staff Portal")
    
    auth_tab1, auth_tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with auth_tab1:
        with st.form("main_login"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            submit = st.form_submit_button("Sign In", use_container_width=True)
            
            if submit:
                try:
                    r = httpx.post(f"{URL}/auth/login", json={"username": u, "password": p})
                    if r.status_code == 200:
                        # Update state FIRST
                        st.session_state.token = r.json()["access_token"]
                        st.session_state.username = r.json()["username"]
                        st.success("Access Granted! Refreshing...")
                        time.sleep(0.5)
                        st.rerun() # Now it will pass the 'None' check at the top
                    else:
                        st.error("Invalid username or password")
                except httpx.RequestError:
                    st.error("Auth Service Offline - Check if API is running")
                    
    with auth_tab2:
        with st.form("main_reg"):
            nu = st.text_input("New Username")
            np = st.text_input("New Password", type="password")
            if st.form_submit_button("Create Account", use_container_width=True):
                try:
                    r = httpx.post(f"{URL}/auth/register", json={"username": nu, "password": np})
                    if r.status_code == 200:
                        st.success("Account created! You can now log in.")
                    else:
                        st.error(f"Failed: {r.text}")
                except httpx.RequestError:
                    st.error("API unreachable")
    st.stop()

# --- DASHBOARD LOGIC (Shown only after successful login) ---
with st.sidebar:
    st.title("🐾 PawHealth Pro")
    st.info(f"👤 User: **{st.session_state.username}**")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.token = None
        st.session_state.username = None
        st.rerun()
    st.divider()
    st.caption("System Status: Online")

st.title("🏥 Clinical Management Dashboard")
t1, t2, t3, t4 = st.tabs(["📊 Registry", "➕ Add Patient", "📈 Weight Telemetry", "🧠 AI Analysis"])

# Tab 1: Registry
with t1:
    st.subheader("Patient Database")
    res = make_request("GET", "/dogs/")
    if res and res.status_code == 200:
        data = res.json()
        if data:
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
        else:
            st.info("No patients found.")

# Tab 2: Add Patient
with t2:
    st.subheader("Register New Dog")
    with st.form("new_dog"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Dog Name")
            breed = st.text_input("Breed")
        with c2:
            ideal_w = st.number_input("Ideal Weight (kg)", min_value=0.1, value=11.0)
            age = st.number_input("Age", min_value=0, value=3)
        
        is_fav = st.checkbox("⭐ Mark as Favorite")
        
        if st.form_submit_button("Register Patient"):
            payload = {
                "name": name, "breed": breed, 
                "ideal_weight_kg": ideal_w, "age": age,
                "is_favorite": is_fav
            }
            res = make_request("POST", "/dogs/", json=payload)
            if res and res.status_code in [200, 201]:
                st.success(f"{name} added successfully!")
                time.sleep(1)
                st.rerun()

# Tab 3: Weight Telemetry (Reactive Graph)
with t3:
    st.subheader("Weight Tracking & History")
    
    res_dogs = make_request("GET", "/dogs/")
    if res_dogs and res_dogs.status_code == 200 and res_dogs.json():
        dog_list = res_dogs.json()
        dog_map = {d["name"]: d["id"] for d in dog_list}
        
        selected_name = st.selectbox("Select Patient to view/edit", options=list(dog_map.keys()))
        current_dog_id = dog_map[selected_name]

        col_input, col_graph = st.columns([1, 2])
        
        with col_input:
            st.write(f"### Update {selected_name}")
            with st.form("weight_form"):
                weight_val = st.number_input("Current Weight (kg)", min_value=0.1, value=11.0)
                entry_date = st.date_input("Measurement Date", value=datetime.now())
                
                if st.form_submit_button("Save Telemetry"):
                    w_payload = {"dog_id": current_dog_id, "weight_kg": weight_val, "date": str(entry_date)}
                    res_w = make_request("POST", "/health/weight", json=w_payload)
                    if res_w and res_w.status_code == 200:
                        st.success("Weight Logged.")
                        st.rerun()
        
        with col_graph:
            st.write(f"### History for {selected_name}")
            h_res = make_request("GET", f"/health/weight/{current_dog_id}")
            if h_res and h_res.status_code == 200:
                h_data = h_res.json()
                if h_data:
                    df_h = pd.DataFrame(h_data)
                    df_h['date'] = pd.to_datetime(df_h['date'])
                    df_h = df_h.sort_values('date')
                    # Fixed date axis display
                    st.line_chart(data=df_h, x='date', y='weight_kg')
                else:
                    st.info("No data entries found for this dog.")
    else:
        st.warning("Register a dog record first.")

# Tab 4: AI Analysis (UPDATED SCARY MESSAGE)
with t4:
    st.subheader("AI Toxicity Diagnostic")
    food = st.text_area("Paste ingredients:")
    if st.button("Analyze"):
        if any(x in food.lower() for x in ["onion", "chocolate", "grape", "garlic", "raisin", "xylitol"]):
            st.error("🚨 DANGER: TOXIC FOOD DETECTED! ☠️")
        else:
            st.success("✅ Profile Safe: No known toxins found.")

st.divider()
st.caption("© 2026 PawHealth Pro | Bar Aizenberg | HIT EASS Final Project")