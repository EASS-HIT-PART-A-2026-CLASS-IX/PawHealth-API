import streamlit as st
import httpx
import pandas as pd
import time
from datetime import datetime, timedelta

st.set_page_config(page_title="PawHealth Pro", page_icon="🐾", layout="wide")
URL = "http://api:8000"

if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None
if "selected_patient" not in st.session_state:
    st.session_state.selected_patient = None


def make_request(method, endpoint, **kwargs):
    headers = {}
    if st.session_state.get("token"):
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    return httpx.request(method, f"{URL}{endpoint}", headers=headers or None, follow_redirects=True, **kwargs)


def fetch_dogs():
    response = make_request("GET", "/dogs/")
    if response and response.status_code == 200:
        return response.json()
    return []


def get_current_patient(dogs):
    if not dogs:
        return None
    if st.session_state.selected_patient not in [dog["id"] for dog in dogs]:
        st.session_state.selected_patient = dogs[0]["id"]
    return next((dog for dog in dogs if dog["id"] == st.session_state.selected_patient), dogs[0])


# --- LOGIN & REGISTRATION ---
if st.session_state.token is None:
    st.title("🐾 PawHealth Pro")
    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        with st.form("login_form"):
            st.subheader("Sign In")
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("🔓 Sign In", use_container_width=True)
            if submit:
                if not username or not password:
                    st.error("Please enter both username and password")
                else:
                    response = httpx.post(f"{URL}/auth/login", json={"username": username, "password": password})
                    if response.status_code == 200:
                        st.session_state.token = response.json()["access_token"]
                        st.session_state.username = response.json()["username"]
                        st.success("✅ Login successful")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials")

    with tab_register:
        with st.form("register_form"):
            st.subheader("Create Account")
            reg_username = st.text_input("Username", placeholder="Choose a username")
            reg_password = st.text_input("Password", type="password")
            reg_password_confirm = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("📝 Register", use_container_width=True)
            if submit:
                if not reg_username or not reg_password or not reg_password_confirm:
                    st.error("Please complete the form")
                elif reg_password != reg_password_confirm:
                    st.error("Passwords do not match")
                elif len(reg_password) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    response = httpx.post(f"{URL}/auth/register", json={"username": reg_username, "password": reg_password})
                    if response.status_code in [200, 201]:
                        st.success("✅ Account created — please log in.")
                    elif response.status_code == 409:
                        st.error("❌ Username already exists")
                    else:
                        st.error(f"❌ Registration failed ({response.status_code})")

    st.stop()

# --- DASHBOARD ---
with st.sidebar:
    st.title("🐾 PawHealth Pro")
    st.info(f"👤 {st.session_state.username}")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.token = None
        st.session_state.username = None
        st.session_state.selected_patient = None
        st.rerun()

st.title("🏥 Clinical Management Dashboard")

dog_list = fetch_dogs()
selected_patient = get_current_patient(dog_list)
if selected_patient:
    st.session_state.selected_patient = selected_patient["id"]

dog_map = {dog["id"]: dog for dog in dog_list}

if selected_patient is None:
    st.warning("No patients found. Add one in the Add Patient tab.")

tabs = st.tabs([
    "📊 Registry",
    "➕ Add Patient",
    "📈 Weight Telemetry",
    "📊 Health Analysis",
    "🏥 Clinic Visits",
    "💉 Vaccinations",
    "🚨 AI Analysis",
])

# --- Registry ---
with tabs[0]:
    st.subheader("Patient Registry")
    if dog_list:
        options = [dog["name"] for dog in dog_list]
        selected_name = st.selectbox("Tap a patient to view details", options=options, index=options.index(selected_patient["name"]))
        selected_id = next(dog["id"] for dog in dog_list if dog["name"] == selected_name)
        st.session_state.selected_patient = selected_id
        selected_patient = dog_map[selected_id]

        left, right = st.columns([2, 1])
        with left:
            st.markdown(f"### {selected_patient['name']} {'⭐' if selected_patient['is_favorite'] else ''}")
            st.write(f"**Breed:** {selected_patient['breed']}")
            st.write(f"**Age:** {selected_patient['age']} years")
            st.write(f"**Current Weight:** {selected_patient['current_weight_kg']} kg")
            st.write(f"**Ideal Weight:** {selected_patient['ideal_weight_kg']} kg")
            st.write(f"**Medical History:** {selected_patient.get('medical_history') or 'None'}")
            st.write(f"**Photo file:** {selected_patient.get('photo_filename') or 'No photo uploaded'}")
            if selected_patient.get("photo_filename"):
                try:
                    img_url = f"{URL}/uploads/{selected_patient['photo_filename']}"
                    st.image(img_url, caption=selected_patient['name'], width=250)
                except Exception:
                    st.write("Unable to load photo")

        with right:
            st.write("**Quick overview**")
            overview = pd.DataFrame([{
                "Name": selected_patient["name"],
                "Breed": selected_patient["breed"],
                "Age": selected_patient["age"],
                "Current Weight": selected_patient["current_weight_kg"],
                "Ideal Weight": selected_patient["ideal_weight_kg"],
                "Favorite": "Yes" if selected_patient["is_favorite"] else "No"
            }])
            st.table(overview)
            if st.button("🗑️ Delete Patient", use_container_width=True):
                res = make_request("DELETE", f"/dogs/{selected_patient['id']}")
                if res and res.status_code == 200:
                    st.success("Patient deleted")
                    st.session_state.selected_patient = None
                    st.rerun()
                else:
                    st.error("Delete failed")

        with st.expander("Edit patient details"):
            with st.form("edit_patient_form"):
                edit_name = st.text_input("Name", value=selected_patient["name"])
                edit_breed = st.text_input("Breed", value=selected_patient["breed"])
                edit_age = st.number_input("Age", min_value=0, value=selected_patient["age"])
                edit_current = st.number_input("Current Weight (kg)", min_value=0.1, value=selected_patient["current_weight_kg"])
                edit_ideal = st.number_input("Ideal Weight (kg)", min_value=0.1, value=selected_patient["ideal_weight_kg"])
                edit_fav = st.checkbox("Favorite", value=selected_patient["is_favorite"])
                edit_medical = st.text_area("Medical History", value=selected_patient.get("medical_history") or "")
                if st.form_submit_button("Save changes", use_container_width=True):
                    payload = {
                        "name": edit_name,
                        "breed": edit_breed,
                        "age": edit_age,
                        "current_weight_kg": edit_current,
                        "ideal_weight_kg": edit_ideal,
                        "is_favorite": edit_fav,
                        "medical_history": edit_medical,
                    }
                    res = make_request("PATCH", f"/dogs/{selected_patient['id']}", json=payload)
                    if res and res.status_code == 200:
                        st.success("Patient updated")
                        st.rerun()
                    else:
                        st.error("Update failed")

        st.divider()
        st.write("### All Patients")
        df = pd.DataFrame(dog_list)
        df["Favorite"] = df["is_favorite"].apply(lambda x: "⭐" if x else "")
        st.dataframe(df[["Favorite", "name", "breed", "age", "current_weight_kg", "ideal_weight_kg"]], use_container_width=True)
    else:
        st.info("No patients registered yet.")

# --- Add Patient ---
with tabs[1]:
    st.subheader("Register New Patient")
    col_form, col_photo = st.columns([2, 1])
    with col_form:
        with st.form("new_dog_form"):
            name = st.text_input("Patient Name", placeholder="e.g. Joey")
            breed = st.text_input("Breed", placeholder="e.g. Golden Retriever")
            age = st.number_input("Age", min_value=0, value=0)
            curr_w = st.number_input("Current Weight (kg)", min_value=0.1, value=0.1)
            ideal_w = st.number_input("Ideal Weight (kg)", min_value=0.1, value=0.1)
            is_fav = st.checkbox("Mark as Favorite")
            history = st.text_area("Medical History", placeholder="Allergies, conditions, notes...")
            uploaded_file_new = st.file_uploader("Patient Photo (optional)", type=["jpg", "jpeg", "png"])
            submit = st.form_submit_button("Register Patient")
            if submit:
                payload = {
                    "name": name,
                    "breed": breed,
                    "age": age,
                    "current_weight_kg": curr_w,
                    "ideal_weight_kg": ideal_w,
                    "is_favorite": is_fav,
                    "medical_history": history,
                }
                res = make_request("POST", "/dogs/", json=payload)
                if res and res.status_code in [200, 201]:
                    created = res.json()
                    st.success("Patient added")
                    # If a photo was provided, upload it to the new dog record
                    if uploaded_file_new is not None:
                        try:
                            files = {"file": (uploaded_file_new.name, uploaded_file_new.read(), uploaded_file_new.type)}
                            up = make_request("POST", f"/dogs/{created['id']}/photo", files=files)
                            if up and up.status_code == 200:
                                st.success("Photo uploaded for new patient")
                            else:
                                st.warning(f"Patient created but photo upload failed ({up.status_code if up else 'no response'})")
                        except Exception as e:
                            st.warning(f"Patient created but photo upload failed: {e}")
                    st.rerun()
                else:
                    # Show backend error text for debugging
                    msg = res.text if res is not None else "no response"
                    st.error(f"Add patient failed ({res.status_code if res else 'no status'}) - {msg}")
    with col_photo:
        st.write("Upload Photo for Existing Patient")
        if dog_list:
            photo_target = st.selectbox("Select patient", options=[(dog["id"], dog["name"]) for dog in dog_list], format_func=lambda x: x[1])
            uploaded_file = st.file_uploader("Upload photo", type=["jpg", "jpeg", "png"])
            if st.button("Upload Photo"):
                if uploaded_file:
                    files = {"file": (uploaded_file.name, uploaded_file.read(), uploaded_file.type)}
                    res = make_request("POST", f"/dogs/{photo_target[0]}/photo", files=files)
                    if res and res.status_code == 200:
                        st.success("Photo uploaded")
                        st.rerun()
                    else:
                        st.error("Photo upload failed")
                else:
                    st.error("Please choose a file")
        else:
            st.info("Add a patient first.")

# --- Weight Telemetry ---
with tabs[2]:
    st.subheader("Weight Telemetry")
    if selected_patient:
        st.write(f"**Patient:** {selected_patient['name']}")
        w_res = make_request("GET", f"/health/weight/{selected_patient['id']}")
        if w_res and w_res.status_code == 200:
            weights = w_res.json()
            if weights:
                df_w = pd.DataFrame(weights)
                df_w["date"] = pd.to_datetime(df_w["date"]).dt.strftime("%Y-%m-%d")
                df_w["Target"] = selected_patient["ideal_weight_kg"]
                st.line_chart(df_w.set_index("date")[["weight_kg", "Target"]], use_container_width=True)
                st.dataframe(df_w[["date", "weight_kg", "Target"]], use_container_width=True, hide_index=True)
            else:
                st.info("No weight entries yet.")
        else:
            st.warning("Unable to load weight history.")
        with st.form("add_weight_form"):
            new_w = st.number_input("Weight (kg)", min_value=0.1, value=selected_patient["current_weight_kg"])
            new_date = st.date_input("Date", value=datetime.now())
            if st.form_submit_button("Save Weight"):
                res = make_request("POST", "/health/weight", json={
                    "dog_id": selected_patient["id"],
                    "weight_kg": new_w,
                    "date": str(new_date),
                })
                if res and res.status_code in [200, 201]:
                    st.success("Weight logged")
                    st.rerun()
                else:
                    st.error("Failed to log weight")
    else:
        st.info("Select a patient in the Registry tab first.")

# --- Health Analysis ---
with tabs[3]:
    st.subheader("Health Analysis")
    if selected_patient:
        a_res = make_request("GET", f"/health/analysis/{selected_patient['id']}")
        if a_res and a_res.status_code == 200:
            analysis = a_res.json()
            variance = analysis["current_weight_kg"] - analysis["ideal_weight_kg"]
            variance_pct = (variance / analysis["ideal_weight_kg"] * 100) if analysis["ideal_weight_kg"] else 0
            col1, col2, col3 = st.columns(3)
            col1.metric("Current Weight", f"{analysis['current_weight_kg']:.1f} kg")
            col2.metric("Ideal Weight", f"{analysis['ideal_weight_kg']:.1f} kg")
            col3.metric("Variance", f"{variance:+.1f} kg ({variance_pct:+.1f}%)")
            if analysis["status"] == "healthy":
                st.success("Healthy weight range")
            elif analysis["status"] == "overweight":
                st.warning("Overweight — consider diet and exercise")
            else:
                st.info("Underweight — monitor feeding plan")
            st.write(f"**Recommendation:** {analysis['recommendation']}")
        else:
            st.info("Add weight history first to generate analysis.")
    else:
        st.info("Select a patient in the Registry tab first.")

# --- Clinic Visits ---
with tabs[4]:
    st.subheader("Clinic Visits")
    if selected_patient:
        c1, c2 = st.columns([1, 1])
        with c1:
            with st.form("visit_form"):
                reason = st.text_input("Reason")
                notes = st.text_area("Notes")
                next_visit = st.date_input("Next Routine Checkup", value=datetime.now() + timedelta(days=180))
                if st.form_submit_button("Record Visit"):
                    res = make_request("POST", "/clinic/visits", json={
                        "dog_id": selected_patient["id"],
                        "reason": reason,
                        "notes": notes,
                        "next_checkup_date": str(next_visit),
                    })
                    if res and res.status_code in [200, 201]:
                        st.success("Visit saved")
                        st.rerun()
                    else:
                        st.error("Failed to save visit")
        with c2:
            v_res = make_request("GET", f"/clinic/visits/{selected_patient['id']}")
            if v_res and v_res.status_code == 200:
                visits = v_res.json()
                if visits:
                    df_v = pd.DataFrame(visits)
                    df_v["visit_date"] = pd.to_datetime(df_v["visit_date"]).dt.strftime("%Y-%m-%d")
                    df_v["next_checkup_date"] = pd.to_datetime(df_v["next_checkup_date"]).dt.strftime("%Y-%m-%d")
                    st.dataframe(df_v[["visit_date", "reason", "notes", "next_checkup_date"]], use_container_width=True, hide_index=True)
                else:
                    st.info("No visits found.")
            else:
                st.warning("Unable to load visit history")
    else:
        st.info("Select a patient in the Registry tab first.")

# --- Vaccinations ---
with tabs[5]:
    st.subheader("Vaccinations")
    if selected_patient:
        c1, c2 = st.columns([1, 1])
        with c1:
            with st.form("vac_form"):
                v_name = st.text_input("Vaccine Name")
                v_date = st.date_input("Date Administered", value=datetime.now())
                next_due = st.date_input("Next Due Date", value=datetime.now() + timedelta(days=365))
                if st.form_submit_button("Record Vaccine"):
                    res = make_request("POST", "/clinic/vaccinations", json={
                        "dog_id": selected_patient["id"],
                        "vaccine_name": v_name,
                        "date_administered": str(v_date),
                        "next_due_date": str(next_due),
                    })
                    if res and res.status_code in [200, 201]:
                        st.success("Vaccine saved")
                        st.rerun()
                    else:
                        st.error("Failed to save vaccine")
        with c2:
            vac_res = make_request("GET", f"/clinic/vaccinations/{selected_patient['id']}")
            if vac_res and vac_res.status_code == 200:
                vaccines = vac_res.json()
                if vaccines:
                    df_vac = pd.DataFrame(vaccines)
                    df_vac["date_administered"] = pd.to_datetime(df_vac["date_administered"]).dt.strftime("%Y-%m-%d")
                    df_vac["next_due_date"] = pd.to_datetime(df_vac["next_due_date"]).dt.strftime("%Y-%m-%d")
                    df_vac["Overdue"] = pd.to_datetime(df_vac["next_due_date"]) < datetime.now()
                    st.dataframe(df_vac[["vaccine_name", "date_administered", "next_due_date", "Overdue"]], use_container_width=True, hide_index=True)
                    overdue = df_vac["Overdue"].sum()
                    if overdue > 0:
                        st.warning(f"⚠️ {overdue} overdue vaccine(s)")
                else:
                    st.info("No vaccines found.")
            else:
                st.warning("Unable to load vaccinations")
    else:
        st.info("Select a patient in the Registry tab first.")

# --- AI Analysis ---
with tabs[6]:
    st.subheader("Toxic Food Scanner")
    food = st.text_area("Enter ingredients or food item")
    if st.button("Scan"):
        if not food.strip():
            st.warning("Please enter something to scan")
        else:
            toxic = ["onion", "chocolate", "garlic", "grape", "raisin", "xylitol", "avocado", "caffeine", "alcohol", "macadamia", "theobromine", "hops"]
            found = [item for item in toxic if item in food.lower()]
            if found:
                st.error(f"🚨 Toxic ingredients detected: {', '.join(found)}")
            else:
                st.success("✅ No dangerous ingredients detected")
