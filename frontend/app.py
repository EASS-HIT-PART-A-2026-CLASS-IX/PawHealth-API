import streamlit as st
import httpx
import pandas as pd
import time
from datetime import datetime, timedelta

# Page config
st.set_page_config(page_title="PawHealth Pro", page_icon="🐾", layout="wide")

# Constants
URL_API = "http://api:8000"
URL_PHOTO_DISPLAY = URL_API

# Initialize Session States
if "token" not in st.session_state: st.session_state.token = None
if "username" not in st.session_state: st.session_state.username = None
if "selected_patient" not in st.session_state: st.session_state.selected_patient = None
if "registration_done" not in st.session_state: st.session_state.registration_done = False

def make_request(method, endpoint, **kwargs):
    headers = {"Authorization": f"Bearer {st.session_state.token}"} if st.session_state.token else {}
    try:
        return httpx.request(method, f"{URL_API}{endpoint}", headers=headers, follow_redirects=True, timeout=10.0, **kwargs)
    except Exception as e:
        st.error(f"Backend connection failed: {e}")
        return None

# --- AUTHENTICATION ---
if st.session_state.token is None:
    st.title("🏥 PawHealth Pro Portal")
    tab_login, tab_reg = st.tabs(["🔐 Sign In", "📝 Staff Registration"])
    
    with tab_login:
        with st.form("login_form"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("Access Dashboard", use_container_width=True):
                r = httpx.post(f"{URL_API}/auth/login", json={"username": u, "password": p})
                if r.status_code == 200:
                    st.session_state.token = r.json()["access_token"]
                    st.session_state.username = r.json()["username"]
                    st.rerun()
                else: st.error("Authentication failed. Check credentials.")

    with tab_reg:
        if st.session_state.registration_done:
            st.success("✅ Account created! You can now log in.")
            if st.button("Return to Login"): 
                st.session_state.registration_done = False
                st.rerun()
        else:
            with st.form("reg_form", clear_on_submit=True):
                nu = st.text_input("Choose Username")
                np = st.text_input("Create Password", type="password")
                if st.form_submit_button("Register New Staff", use_container_width=True):
                    res = httpx.post(f"{URL_API}/auth/register", json={"username": nu, "password": np})
                    if res.status_code in [200, 201]:
                        st.session_state.registration_done = True
                        st.rerun()
                    else: st.error("Registration failed. Username might be taken.")
    st.stop()

# --- DASHBOARD LOAD ---
res_dogs = make_request("GET", "/dogs/")
dog_list = res_dogs.json() if res_dogs and res_dogs.status_code == 200 else []
if dog_list and not st.session_state.selected_patient:
    st.session_state.selected_patient = dog_list[0]["id"]

with st.sidebar:
    st.title("🐾 PawHealth Pro")
    st.info(f"👤 Logged in: **{st.session_state.username}**")
    if st.button("🚪 Logout", use_container_width=True):
        for key in st.session_state.keys(): st.session_state[key] = None
        st.rerun()

st.title("🏥 Clinical Management Dashboard")
tabs = st.tabs(["📊 Registry", "➕ Add Patient", "📈 Weight", "📊 Analysis", "🩺 Visits", "💉 Vaccines"])

# --- TAB 1: REGISTRY ---
with tabs[0]:
    if dog_list:
        dog = next((d for d in dog_list if d["id"] == st.session_state.selected_patient), dog_list[0])
        st.session_state.selected_patient = dog["id"]
        
        # Selector
        names = {d["id"]: d["name"] for d in dog_list}
        picked = st.selectbox("Current Patient File", options=list(names.keys()), format_func=lambda x: names[x], index=list(names.keys()).index(dog["id"]))
        if picked != st.session_state.selected_patient:
            st.session_state.selected_patient = picked
            st.rerun()

        st.divider()
        c1, c2 = st.columns([1, 2])
        with c1:
            if dog.get("photo_filename"):
                photo_resp = make_request("GET", f"/uploads/{dog['photo_filename']}")
                if photo_resp and photo_resp.status_code == 200:
                    st.image(photo_resp.content, use_container_width=True)
                else:
                    st.warning("Unable to load profile photo.")
            else:
                st.info("No profile photo.")
        with c2:
            st.subheader(f"{dog['name']} {'⭐' if dog['is_favorite'] else ''}")
            st.write(f"**Breed:** {dog['breed']} | **Age:** {dog['age']} years")
            st.write(f"**Current Weight:** {dog['current_weight_kg']} kg")
            st.write(f"**Ideal Weight:** {dog['ideal_weight_kg']} kg")
            st.write(f"**Clinical History:** {dog.get('medical_history') or 'None'}")
            if st.button("🗑️ Delete Profile"):
                resp = make_request("DELETE", f"/dogs/{dog['id']}")
                if resp and resp.status_code == 200:
                    st.success("Patient deleted")
                    st.session_state.selected_patient = None
                    st.rerun()
                else:
                    st.error(f"Failed to delete patient ({resp.status_code if resp else 'no response'})")

            with st.expander("✏️ Edit patient"):
                with st.form("edit_patient_form", clear_on_submit=False):
                    ename = st.text_input("Name", value=dog.get("name"))
                    ebreed = st.text_input("Breed", value=dog.get("breed"))
                    eage = st.number_input("Age", value=dog.get("age") or 0)
                    ecurr = st.number_input("Current Weight (kg)", value=dog.get("current_weight_kg") or 0.1)
                    eideal = st.number_input("Ideal Weight (kg)", value=dog.get("ideal_weight_kg") or 0.1)
                    efav = st.checkbox("Favorite", value=dog.get("is_favorite", False))
                    emed = st.text_area("Medical History", value=dog.get("medical_history") or "")
                    new_photo = st.file_uploader("Replace Photo (optional)", type=["jpg","jpeg","png"])
                    if st.form_submit_button("Save changes"):
                        payload = {
                            "name": ename,
                            "breed": ebreed,
                            "age": eage,
                            "current_weight_kg": ecurr,
                            "ideal_weight_kg": eideal,
                            "is_favorite": efav,
                            "medical_history": emed,
                        }
                        r = make_request("PATCH", f"/dogs/{dog['id']}", json=payload)
                        if r and r.status_code == 200:
                            st.success("Patient updated")
                            if new_photo is not None:
                                try:
                                    files = {"file": (new_photo.name, new_photo.read(), new_photo.type)}
                                    up = make_request("POST", f"/dogs/{dog['id']}/photo", files=files)
                                    if up and up.status_code == 200:
                                        st.success("Photo updated")
                                    else:
                                        st.warning(f"Photo upload failed ({up.status_code if up else 'no response'})")
                                except Exception as e:
                                    st.warning(f"Photo upload exception: {e}")
                            st.rerun()
                        else:
                            st.error(f"Update failed ({r.status_code if r else 'no response'}) - {r.text if r else ''}")
        st.divider()
        if st.button("⬇️ Export Registry as CSV"):
            import io
            df = pd.DataFrame(dog_list)
            cols = [c for c in ["id","name","breed","age","current_weight_kg","ideal_weight_kg","is_favorite","medical_history"] if c in df.columns]
            csv_bytes = df[cols].to_csv(index=False).encode()
            st.download_button("Download CSV", data=csv_bytes, file_name="pawhealth_registry.csv", mime="text/csv")
    else: st.info("Patient registry is empty.")

# --- TAB 2: ADD PATIENT ---
with tabs[1]:
    st.subheader("Register New Patient Record")
    with st.form("new_dog_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        n = c1.text_input("Name")
        b = c1.text_input("Breed")
        age_input = c1.text_input("Age", value="", placeholder="e.g. 5")
        aw = c2.text_input("Current Weight", value="", placeholder="e.g. 10.5")
        iw = c2.text_input("Ideal Weight", value="", placeholder="e.g. 9.0")
        fav = c1.checkbox("Mark as Favorite")
        hist = st.text_area("Medical History / Background")
        photo_new = st.file_uploader("Photo (optional)", type=["jpg","jpeg","png"])
        if st.form_submit_button("Finalize Registration"):
            try:
                if not n or not b or not aw or not iw:
                    raise ValueError("Please enter name, breed, current weight and ideal weight.")
                age = int(age_input) if age_input.strip() else 0
                aw_val = float(aw)
                iw_val = float(iw)
            except ValueError as e:
                st.error(f"Invalid patient form values: {e}")
            else:
                r = make_request("POST", "/dogs/", json={"name":n, "breed":b, "age":age, "is_favorite":fav, "ideal_weight_kg":iw_val, "current_weight_kg":aw_val, "medical_history":hist})
                if r and r.status_code in [200,201]:
                    created = r.json()
                    # Upload photo if provided
                    if photo_new is not None:
                        try:
                            files = {"file": (photo_new.name, photo_new.read(), photo_new.type)}
                            up = make_request("POST", f"/dogs/{created['id']}/photo", files=files)
                            if up and up.status_code == 200:
                                st.success("Patient and photo saved")
                            else:
                                st.warning(f"Patient created but photo upload failed ({up.status_code if up else 'no response'})")
                        except Exception as e:
                            st.warning(f"Photo upload exception: {e}")
                    else:
                        st.success("✅ Success: Patient record created.")
                    time.sleep(0.6)
                    st.rerun()
                else:
                    st.error(f"Failed creating patient ({r.status_code if r else 'no response'}) - {r.text if r else ''}")

# --- TAB 3: WEIGHT TELEMETRY ---
with tabs[2]:
    if st.session_state.selected_patient:
        pid = st.session_state.selected_patient
        dog = next((d for d in dog_list if d["id"] == pid), None)
        if dog:
            st.write(f"**Patient:** {dog['name']}")
        w_res = make_request("GET", f"/health/weight/{pid}")
        weights = w_res.json() if w_res and w_res.status_code == 200 else []
        if w_res and w_res.status_code == 200:
            if weights:
                df_w = pd.DataFrame(weights)
                df_w["date"] = pd.to_datetime(df_w["date"]).dt.strftime("%Y-%m-%d")
                df_w = df_w.sort_values("date")
                df_w["Target"] = dog["ideal_weight_kg"] if dog else None
                st.line_chart(df_w.set_index("date")[["weight_kg", "Target"]], use_container_width=True)
                st.caption("Target weight is shown as a reference line alongside actual weight history.")
                st.dataframe(df_w[["date", "weight_kg", "Target"]], use_container_width=True, hide_index=True)

                for entry in weights:
                    c1, c2, c3, c4 = st.columns([2, 2, 2, 1])
                    c1.write(entry["date"][:10])
                    c2.write(f"{entry['weight_kg']} kg")
                    c3.write(f"Target {dog['ideal_weight_kg']} kg")
                    if c4.button("✏️", key=f"edit_w_{entry['id']}"):
                        st.session_state.edit_weight_id = entry["id"]
                        st.session_state.edit_weight_data = entry
                        st.rerun()
                    if c4.button("🗑️", key=f"del_w_{entry['id']}"):
                        make_request("DELETE", f"/health/weight/{entry['id']}")
                        st.rerun()

            else:
                st.info("No weight entries yet.")
        else:
            st.warning("Unable to load weight history.")

        if st.session_state.get("edit_weight_id"):
            edit_id = st.session_state.edit_weight_id
            edit_entry = next((item for item in weights if item["id"] == edit_id), None)
            if edit_entry:
                st.divider()
                st.subheader("Edit Weight Entry")
                with st.form("edit_weight_form", clear_on_submit=False):
                    updated_weight = st.number_input(
                        "Weight (kg)",
                        min_value=0.01,
                        step=0.1,
                        value=float(edit_entry.get("weight_kg", 0.0)),
                        format="%.1f"
                    )
                    updated_date = st.date_input(
                        "Date",
                        value=datetime.fromisoformat(edit_entry.get("date")[:10]) if edit_entry.get("date") else datetime.now()
                    )
                    cols = st.columns([1, 1])
                    if cols[0].form_submit_button("Save Changes"):
                        resp = make_request("PATCH", f"/health/weight/{edit_id}", json={
                            "weight_kg": updated_weight,
                            "date": str(updated_date)
                        })
                        if resp and resp.status_code == 200:
                            st.success("Weight entry updated")
                            st.session_state.edit_weight_id = None
                            st.rerun()
                        else:
                            st.error(f"Failed to update weight ({resp.status_code if resp else 'no response'}) - {resp.text if resp else ''}")
                    if cols[1].form_submit_button("Cancel"):
                        st.session_state.edit_weight_id = None
                        st.rerun()

        st.divider()
        with st.form("add_w_form"):
            new_w_str = st.text_input("Weight (kg)", value="", placeholder="e.g. 10.2")
            new_date = st.date_input("Date", value=datetime.now())
            if st.form_submit_button("Save Weight"):
                try:
                    if not new_w_str.strip():
                        raise ValueError("Weight is required")
                    new_w = float(new_w_str)
                    if new_w <= 0:
                        raise ValueError("Weight must be greater than zero")
                except ValueError as e:
                    st.error(f"Invalid weight value: {e}")
                else:
                    res = make_request("POST", "/health/weight", json={
                        "dog_id": pid,
                        "weight_kg": new_w,
                        "date": str(new_date)
                    })
                    if res and res.status_code in [200, 201]:
                        st.success("Weight logged")
                        st.rerun()
                    else:
                        st.error(f"Failed to log weight ({res.status_code if res else 'no response'}) - {res.text if res else ''}")
    else:
        st.info("Select a patient in the Registry tab first.")

# --- TAB 4: HEALTH ANALYSIS ---
with tabs[3]:
    if st.session_state.selected_patient:
        pid = st.session_state.selected_patient
        res_a = make_request("GET", f"/health/analysis/{pid}")
        if res_a and res_a.status_code == 200:
            analysis = res_a.json()
            variance = analysis["current_weight_kg"] - analysis["ideal_weight_kg"]
            variance_pct = (variance / analysis["ideal_weight_kg"] * 100) if analysis["ideal_weight_kg"] else 0
            col1, col2, col3 = st.columns(3)
            col1.metric("Current Weight", f"{analysis['current_weight_kg']:.1f} kg")
            col2.metric("Ideal Weight", f"{analysis['ideal_weight_kg']:.1f} kg")
            col3.metric("Variance", f"{variance:+.1f} kg ({variance_pct:+.1f}%)")
            if analysis["status"] == "healthy":
                st.success("Good weight status — keep it up.")
            elif analysis["status"] == "overweight":
                st.warning("Overweight — review feeding and exercise.")
            else:
                st.info("Underweight — monitor nutrition closely.")
            st.write(f"**Recommendation:** {analysis['recommendation']}")
        else:
            st.info("Add weight history first to generate analysis.")
    else:
        st.info("Select a patient in the Registry tab first.")

# --- TAB 5: CLINIC VISITS ---
with tabs[4]:
    if st.session_state.selected_patient:
        pid = st.session_state.selected_patient
        with st.form("visit_form", clear_on_submit=True):
            r = st.text_input("Visit Reason")
            n = st.text_area("Clinical Notes")
            nv = st.date_input("Next Routine Checkup", value=datetime.now() + timedelta(days=180))
            if st.form_submit_button("Record Visit"):
                resp = make_request("POST", "/clinic/visits", json={"dog_id": pid, "reason": r, "notes": n, "next_checkup_date": str(nv)})
                if resp and resp.status_code in [200,201]:
                    st.success("Visit saved")
                    st.rerun()
                else:
                    st.error(f"Failed to save visit ({resp.status_code if resp else 'no response'}) - {resp.text if resp else ''}")
        
        visit_resp = make_request("GET", f"/clinic/visits/{pid}")
        visits = visit_resp.json() if visit_resp and visit_resp.status_code == 200 else []
        for v in visits:
            c1, c2, c3, c4 = st.columns([2, 5, 1, 1])
            c1.write(v["visit_date"][:10])
            c2.write(f"**{v['reason']}**\n{v.get('notes') or ''}\nNext: {v.get('next_checkup_date', '')[:10]}")
            if c3.button("✏️", key=f"edit_v_{v['id']}"):
                st.session_state.edit_visit_id = v['id']
                st.session_state.edit_visit_data = v
                st.rerun()
            if c4.button("🗑️", key=f"del_v_{v['id']}"):
                make_request("DELETE", f"/clinic/visits/{v['id']}")
                st.rerun()

        if st.session_state.get('edit_visit_id'):
            edit_id = st.session_state.edit_visit_id
            edit_visit = next((item for item in visits if item['id'] == edit_id), None)
            if edit_visit:
                st.divider()
                st.subheader("Edit Visit")
                with st.form("edit_visit_form", clear_on_submit=False):
                    er = st.text_input("Visit Reason", value=edit_visit.get('reason', ''))
                    en = st.text_area("Clinical Notes", value=edit_visit.get('notes', ''))
                    env = st.date_input(
                        "Next Routine Checkup",
                        value=datetime.fromisoformat(edit_visit.get('next_checkup_date')[:10]) if edit_visit.get('next_checkup_date') else datetime.now()
                    )
                    if st.form_submit_button("Save Visit Changes"):
                        resp = make_request("PATCH", f"/clinic/visits/{edit_id}", json={
                            "reason": er,
                            "notes": en,
                            "next_checkup_date": str(env)
                        })
                        if resp and resp.status_code == 200:
                            st.success("Visit updated")
                            st.session_state.edit_visit_id = None
                            st.rerun()
                        else:
                            st.error(f"Failed to update visit ({resp.status_code if resp else 'no response'}) - {resp.text if resp else ''}")
            else:
                st.session_state.edit_visit_id = None

# --- TAB 6: VACCINATIONS ---
with tabs[5]:
    if st.session_state.selected_patient:
        pid = st.session_state.selected_patient
        with st.form("vac_form", clear_on_submit=True):
            vn = st.text_input("Vaccine Type")
            ad = st.date_input("Date Administered", value=datetime.now())
            nd = st.date_input("Next Due Date", value=datetime.now() + timedelta(days=365))
            if st.form_submit_button("Log Vaccination"):
                resp = make_request("POST", "/clinic/vaccinations", json={"dog_id": pid, "vaccine_name": vn, "date_administered": str(ad), "next_due_date": str(nd)})
                if resp and resp.status_code in [200,201]:
                    st.success("Vaccine logged")
                    st.rerun()
                else:
                    st.error(f"Failed to log vaccine ({resp.status_code if resp else 'no response'}) - {resp.text if resp else ''}")
        
        vac_resp = make_request("GET", f"/clinic/vaccinations/{pid}")
        vacs = vac_resp.json() if vac_resp and vac_resp.status_code == 200 else []
        for v in vacs:
            c1, c2, c3 = st.columns([7, 1, 1])
            c1.write(f"💉 {v['vaccine_name']}\nAdministered: {v['date_administered'][:10]}\nNext: {v['next_due_date'][:10]}")
            if c2.button("✏️", key=f"edit_vac_{v['id']}"):
                st.session_state.edit_vac_id = v['id']
                st.session_state.edit_vac_data = v
                st.rerun()
            if c3.button("🗑️", key=f"del_vac_{v['id']}"):
                make_request("DELETE", f"/clinic/vaccinations/{v['id']}")
                st.rerun()

        if st.session_state.get('edit_vac_id'):
            edit_id = st.session_state.edit_vac_id
            edit_vac = next((item for item in vacs if item['id'] == edit_id), None)
            if edit_vac:
                st.divider()
                st.subheader("Edit Vaccination")
                with st.form("edit_vac_form", clear_on_submit=False):
                    evn = st.text_input("Vaccine Name", value=edit_vac.get('vaccine_name', ''))
                    ead = st.date_input(
                        "Administered Date",
                        value=datetime.fromisoformat(edit_vac.get('date_administered')[:10]) if edit_vac.get('date_administered') else datetime.now()
                    )
                    end = st.date_input(
                        "Next Due Date",
                        value=datetime.fromisoformat(edit_vac.get('next_due_date')[:10]) if edit_vac.get('next_due_date') else datetime.now()
                    )
                    if st.form_submit_button("Save Vaccine Changes"):
                        resp = make_request("PATCH", f"/clinic/vaccinations/{edit_id}", json={
                            "vaccine_name": evn,
                            "date_administered": str(ead),
                            "next_due_date": str(end)
                        })
                        if resp and resp.status_code == 200:
                            st.success("Vaccination updated")
                            st.session_state.edit_vac_id = None
                            st.rerun()
                        else:
                            st.error(f"Failed to update vaccine ({resp.status_code if resp else 'no response'}) - {resp.text if resp else ''}")
            else:
                st.session_state.edit_vac_id = None

