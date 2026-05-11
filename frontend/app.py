import streamlit as st
import httpx
import pandas as pd
import time
from datetime import datetime, timedelta

st.set_page_config(page_title="PawHealth Pro", page_icon="🐾", layout="wide")
URL = "http://api:8000"

if "token" not in st.session_state: st.session_state.token = None
if "username" not in st.session_state: st.session_state.username = None

def make_request(method, endpoint, **kwargs):
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    return httpx.request(method, f"{URL}{endpoint}", headers=headers, follow_redirects=True, **kwargs)

# --- LOGIN SCREEN ---
if st.session_state.token is None:
    st.title("🐾 PawHealth Pro Login")
    tab_l, tab_r = st.tabs(["Login", "Register"])
    with tab_l:
        with st.form("login_f"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("Sign In"):
                r = httpx.post(f"{URL}/auth/login", json={"username": u, "password": p})
                if r.status_code == 200:
                    st.session_state.token = r.json()["access_token"]
                    st.session_state.username = r.json()["username"]
                    st.rerun()
    # (Register logic follows same pattern as your original)
    st.stop()

# --- MAIN DASHBOARD ---
with st.sidebar:
    st.title("🐾 PawHealth Pro")
    st.info(f"👤 User: **{st.session_state.username}**")
    if st.button("Logout"):
        st.session_state.token = None
        st.rerun()

st.title("🏥 Clinical Management Dashboard")
tabs = st.tabs(["📊 Registry", "➕ Add Patient", "📈 Weight Telemetry", "🩺 Visits", "💉 Vaccines", "🚨 AI Analysis"])

# Pre-fetch dogs
res_dogs = make_request("GET", "/dogs/")
dog_list = res_dogs.json() if res_dogs and res_dogs.status_code == 200 else []
dog_map = {d["name"]: d["id"] for d in dog_list}

# Tab 1: Registry
with tabs[0]:
    if dog_list:
        df = pd.DataFrame(dog_list)
        df['Favorite'] = df['is_favorite'].apply(lambda x: "⭐" if x else "")
        st.dataframe(df[['Favorite', 'name', 'breed', 'current_weight_kg', 'ideal_weight_kg', 'medical_history']], use_container_width=True)

# Tab 2: Add Patient
with tabs[1]:
    with st.form("new_dog"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Dog Name", placeholder="e.g. Joey")
            breed = st.text_input("Breed")
            curr_w = st.number_input("Current Weight (kg)", min_value=0.0, value=None)
        with c2:
            ideal_w = st.number_input("Ideal Weight (kg)", min_value=0.0, value=None)
            age = st.number_input("Age", min_value=0, value=None)
            is_fav = st.checkbox("Mark as Favorite")
        history = st.text_area("Medical History / Background")
        if st.form_submit_button("Register Patient"):
            payload = {"name": name, "breed": breed, "age": age or 0, "is_favorite": is_fav,
                       "ideal_weight_kg": ideal_w, "current_weight_kg": curr_w, "medical_history": history}
            make_request("POST", "/dogs/", json=payload)
            st.rerun()

# Tab 3: Weight (With Target Line & Chronological Graph)
with tabs[2]:
    if dog_list:
        sel_dog = st.selectbox("Select Dog", options=list(dog_map.keys()), key="w_sel")
        dog_data = next(d for d in dog_list if d["id"] == dog_map[sel_dog])
        h_res = make_request("GET", f"/health/weight/{dog_map[sel_dog]}")
        if h_res and h_res.status_code == 200:
            df_h = pd.DataFrame(h_res.json())
            if not df_h.empty:
                df_h['date'] = pd.to_datetime(df_h['date'])
                df_h['Target Weight'] = dog_data['ideal_weight_kg']
                st.line_chart(data=df_h, x='date', y=['weight_kg', 'Target Weight'])
        
        with st.form("add_w"):
            new_w = st.number_input("Log New Weight", min_value=0.1)
            new_date = st.date_input("Entry Date")
            if st.form_submit_button("Save"):
                make_request("POST", "/health/weight", json={"dog_id": dog_map[sel_dog], "weight_kg": new_w, "date": str(new_date)})
                st.rerun()

# Tab 4: Clinic Visits
with tabs[3]:
    if dog_list:
        sel_v = st.selectbox("Select Patient", options=list(dog_map.keys()), key="v_sel")
        c1, c2 = st.columns(2)
        with c1:
            with st.form("visit_f"):
                reason = st.text_input("Reason")
                notes = st.text_area("Notes")
                next_v = st.date_input("Next Routine Checkup", value=datetime.now() + timedelta(days=180))
                if st.form_submit_button("Record Visit"):
                    make_request("POST", "/clinic/visits", json={"dog_id": dog_map[sel_v], "reason": reason, "notes": notes, "next_checkup_date": str(next_v)})
                    st.rerun()
        with c2:
            v_data = make_request("GET", f"/clinic/visits/{dog_map[sel_v]}").json()
            if v_data: st.table(pd.DataFrame(v_data))

# Tab 5: Vaccines
with tabs[4]:
    if dog_list:
        sel_vac = st.selectbox("Select Patient", options=list(dog_map.keys()), key="vac_sel")
        c1, c2 = st.columns(2)
        with c1:
            with st.form("vac_f"):
                v_name = st.text_input("Vaccine Name")
                v_next = st.date_input("Next Due Date", value=datetime.now() + timedelta(days=365))
                if st.form_submit_button("Log Vaccine"):
                    make_request("POST", "/clinic/vaccinations", json={"dog_id": dog_map[sel_vac], "vaccine_name": v_name, "next_due_date": str(v_next)})
                    st.rerun()
        with c2:
            vac_data = make_request("GET", f"/clinic/vaccinations/{dog_map[sel_vac]}").json()
            if vac_data: st.table(pd.DataFrame(vac_data))

# Tab 6: AI Diagnostic (Scary Alert)
with tabs[5]:
    food = st.text_area("Ingredients:")
    if st.button("Scan"):
        if any(x in food.lower() for x in ["onion", "chocolate", "garlic", "grape", "raisin", 
    "xylitol", "avocado", "caffeine", "alcohol", "macadamia"]):
            st.error("🚨 DANGER: TOXIC FOOD DETECTED! ☠️")
        else: st.success("✅ Profile Safe")