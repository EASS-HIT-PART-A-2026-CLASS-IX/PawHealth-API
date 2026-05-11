import streamlit as st
import httpx
import pandas as pd

# Page configuration for PawHealth Pro
st.set_page_config(page_title="PawHealth Pro", page_icon="🐾", layout="wide")
URL = "http://api:8000"

# Initialize session state for token management
if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None
if "show_register" not in st.session_state:
    st.session_state.show_register = False

# Sidebar for authentication and system status
with st.sidebar:
    st.title("PawHealth Pro")
    
    if st.session_state.token is None:
        # Show login/register forms
        st.subheader("🔐 Authentication")
        
        # Toggle between login and register
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login", use_container_width=True):
                st.session_state.show_register = False
                st.rerun()
        with col2:
            if st.button("Register", use_container_width=True):
                st.session_state.show_register = True
                st.rerun()
        
        st.divider()
        
        if st.session_state.show_register:
            # Registration form
            st.write("**Create Account**")
            with st.form("register_form"):
                username = st.text_input("Username", key="reg_username")
                password = st.text_input("Password", type="password", key="reg_password")
                password_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
                
                if st.form_submit_button("Register"):
                    if not username.strip():
                        st.error("Username is required")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters")
                    elif password != password_confirm:
                        st.error("Passwords don't match")
                    else:
                        try:
                            response = httpx.post(
                                f"{URL}/auth/register",
                                json={"username": username, "password": password}
                            )
                            if response.status_code == 200:
                                data = response.json()
                                st.session_state.token = data["access_token"]
                                st.session_state.username = data["username"]
                                st.success(f"Account created! Welcome, {data['username']}! ✅")
                                st.rerun()
                            else:
                                error_detail = response.json().get("detail", "Registration failed")
                                st.error(f"Registration failed: {error_detail}")
                        except Exception as e:
                            st.error(f"Connection error: {str(e)}")
        else:
            # Login form
            st.write("**Sign In**")
            with st.form("login_form"):
                username = st.text_input("Username", key="login_username")
                password = st.text_input("Password", type="password", key="login_password")
                
                if st.form_submit_button("Login"):
                    if not username.strip():
                        st.error("Username is required")
                    elif not password:
                        st.error("Password is required")
                    else:
                        try:
                            response = httpx.post(
                                f"{URL}/auth/login",
                                json={"username": username, "password": password}
                            )
                            if response.status_code == 200:
                                data = response.json()
                                st.session_state.token = data["access_token"]
                                st.session_state.username = data["username"]
                                st.success(f"Welcome back, {data['username']}! ✅")
                                st.rerun()
                            else:
                                st.error("Invalid username or password")
                        except Exception as e:
                            st.error(f"Connection error: {str(e)}")
    else:
        # Show logged-in state
        st.info(f"👤 **{st.session_state.username}**")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.token = None
            st.session_state.username = None
            st.rerun()
    
    st.divider()
    st.caption("System Status: Clinical/Online")

# Redirect to login if not authenticated
if st.session_state.token is None:
    st.warning("⚠️ Please log in to access the dashboard")
    st.stop()

# Main Clinical Dashboard Header
st.title("Clinical Management Dashboard")
t1, t2, t3, t4 = st.tabs(["Registry", "Add Patient", "Weight Logs", "AI Analysis"])

# Helper function to make authenticated requests
def make_request(method, endpoint, **kwargs):
    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"Bearer {st.session_state.token}"
    
    try:
        if method == "GET":
            return httpx.get(f"{URL}{endpoint}", headers=headers, follow_redirects=True, **kwargs)
        elif method == "POST":
            return httpx.post(f"{URL}{endpoint}", headers=headers, follow_redirects=True, **kwargs)
        elif method == "PUT":
            return httpx.put(f"{URL}{endpoint}", headers=headers, follow_redirects=True, **kwargs)
        elif method == "DELETE":
            return httpx.delete(f"{URL}{endpoint}", headers=headers, follow_redirects=True, **kwargs)
    except Exception as e:
        st.error(f"Connection failed: {str(e)}")
        return None

# Tab 1: View existing patients
with t1:
    st.subheader("Patient Registry")
    if st.button("Refresh Registry"):
        try:
            r = make_request("GET", "/dogs")
            if r and r.status_code == 200:
                data = r.json()
                if data:
                    st.table(pd.DataFrame(data))
                else:
                    st.info("No patients registered yet")
            else:
                st.error("Failed to fetch registry")
        except:
            st.error("Connection to API failed")

# Tab 2: Register a new pet (e.g., Joey the King)
with t2:
    st.subheader("Register New Patient")
    with st.form("add_dog"):
        name = st.text_input("Name")
        breed = st.text_input("Breed")
        ideal_weight = st.number_input("Ideal Weight (kg)", min_value=0.1)
        age = st.number_input("Age (years)", min_value=0, value=3)
        
        if st.form_submit_button("Register"):
            if name.strip() and breed.strip():
                data = {
                    "name": name,
                    "breed": breed,
                    "ideal_weight_kg": ideal_weight,
                    "age": age
                }
                r = make_request("POST", "/dogs", json=data)
                if r and r.status_code in (200, 201):
                    st.success(f"Patient {name} registered successfully ✅")
                else:
                    st.error(f"Registration failed: {r.text if r else 'Unknown error'}")
            else:
                st.warning("Please fill in all required fields")

# Tab 3: Log weight updates for health monitoring
with t3:
    st.subheader("Log Weight Telemetry")
    with st.form("log_weight"):
        dog_id = st.number_input("Patient ID", min_value=1)
        weight_kg = st.number_input("Current Weight (kg)", min_value=0.1)
        
        if st.form_submit_button("Update Weight"):
            data = {"dog_id": dog_id, "weight_kg": weight_kg}
            r = make_request("POST", "/health/weight", json=data)
            if r and r.status_code == 200:
                st.success("Weight telemetry synchronized ✅")
            else:
                st.error(f"Update failed: {r.text if r else 'Unknown error'}")

# Tab 4: AI Sidecar toxicity diagnostics
with t4:
    st.subheader("AI Sidecar Analysis")
    food = st.text_area("Ingredients:")
    if st.button("Analyze"):
        # Check for common toxins like chocolate, onions, or grapes
        if any(x in food.lower() for x in ["onion", "chocolate", "grape", "garlic"]):
            st.error("🚨 Toxicity detected: Harmful ingredients found")
        else:
            st.success("✅ Safe profile: No common hazards detected")

# Footer for HIT academic submission
st.divider()
st.caption("© 2026 PawHealth Pro | HIT EASS Final Project Submission")

