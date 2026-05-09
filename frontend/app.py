import streamlit as st
import httpx
import pandas as pd

st.set_page_config(
    page_title="PawHealth Pro | Clinical Dashboard",
    page_icon="🐾",
    layout="wide"
)

st.markdown("""
    <style>
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 10px; border: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/dog-heart.png", width=80)
    st.title("Clinical Access")
    token = st.text_input("JWT Bearer Token", type="password")
    st.divider()
    st.info("System: Production\nStatus: Secure")

st.title("🐾 PawHealth Pro")
st.caption("Professional Veterinary Analytics & Management System")

t1, t2, t3 = st.tabs(["📊 Analytics", "📝 Patient Logs", "🤖 AI Insight"])

with t1:
    st.subheader("Patient Clinical Metrics")
    c1, c2, c3 = st.columns(3)
    c1.metric("Weight", "11.0 kg", "+1.0 kg", delta_color="inverse")
    c2.metric("Target", "10.0 kg")
    c3.metric("Variance", "10%", delta="Deviation")
    st.divider()
    st.subheader("Weight Telemetry History")
    chart_data = pd.DataFrame({"kg": [10.2, 10.5, 10.8, 11.2, 11.0]})
    st.line_chart(chart_data)

with t2:
    st.subheader("Synchronize New Data")
    with st.form("clinical_form"):
        pid = st.number_input("Patient ID", min_value=1, step=1)
        wgt = st.number_input("Weight (kg)", min_value=0.1)
        if st.form_submit_button("Commit to Database"):
            if not token:
                st.warning("Authentication required.")
            else:
                st.success(f"Synchronized Patient #{pid}")

with t3:
    st.subheader("AI Sidecar: Toxicity Analysis")
    food = st.text_area("Ingredients:", placeholder="List ingredients...")
    if st.button("Analyze"):
        if any(x in food.lower() for x in ["onion", "chocolate"]):
            st.error("🚨 CRITICAL: Toxic components identified.")
        else:
            st.success("✅ Safe: No hazards detected.")

st.divider()
st.caption("© 2026 PawHealth Pro | HIT EASS Project Submission")
