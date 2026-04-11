import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="PawHealth Pro", page_icon="🐾", layout="wide")

API_URL = "http://127.0.0.1:8000"

st.title("🐾 PawHealth Pro Dashboard")
st.markdown("---")

try:
    # Sidebar - Dog Selection
    response = requests.get(f"{API_URL}/dogs/")
    dogs = response.json()

    if not dogs:
        st.info("No dogs found. Add one via Swagger!")
    else:
        dog_names = {d["id"]: d["name"] for d in dogs}
        selected_id = st.sidebar.selectbox("Choose a Dog", options=list(dog_names.keys()), format_func=lambda x: dog_names[x])
        dog = next(d for d in dogs if d["id"] == selected_id)

        # Profile Card
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader(f"Profile: {dog['name']}")
            st.write(f"**Breed:** {dog['breed']}")
            st.write(f"**Created At:** {dog['created_at'][:10]}")
        
        with col2:
            st.subheader("Status")
            if dog["is_favorite"]:
                st.success("🌟 Favorite Pet")
            else:
                st.info("Standard Profile")
            
            if st.button("Toggle Favorite"):
                requests.patch(f"{API_URL}/dogs/{dog['id']}", json={"is_favorite": not dog["is_favorite"]})
                st.rerun()

        st.markdown("---")

        # Weight Graph Section
        st.subheader("📊 Weight Tracking History")
        weight_res = requests.get(f"{API_URL}/dogs/{dog['id']}/weight")
        weights = weight_res.json()
        
        if weights:
            df = pd.DataFrame(weights)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            # Line Chart
            st.line_chart(df.set_index('date')['weight_kg'])
            
            with st.expander("Show Data Table"):
                st.dataframe(df[['date', 'weight_kg']].rename(columns={'weight_kg': 'Weight (kg)'}))
        else:
            st.warning("No weight logs found for this dog.")

except Exception as e:
    st.error(f"Connect to API failed: {e}")
