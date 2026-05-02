import streamlit as st
import pandas as pd
from client import get_dogs, add_dog

st.set_page_config(page_title="PawHealth Dashboard", page_icon="🐾")
st.title("🐾 PawHealth Management")

# Fetch data from the backend
dogs_data = get_dogs()
st.sidebar.metric("Total Dogs Registered", len(dogs_data))

# Convert to DataFrame
df = pd.DataFrame(dogs_data)

st.subheader("Dog Registry")

if not df.empty:
    # 1. Search Bar
    search_term = st.text_input("🔍 Search by dog name", "")
    if search_term:
        df = df[df['name'].str.contains(search_term, case=False)]
    
    # 2. Results Table
    st.dataframe(df, width='stretch')

    # 3. Visualization
    st.divider()
    st.subheader("📊 Age Distribution")
    age_counts = df['age'].value_counts().sort_index()
    st.bar_chart(age_counts)
else:
    st.info("The registry is currently empty. Add your first dog below!")

st.divider()

# 4. Improved Form Layout
st.subheader("Register a New Dog")
with st.form("new_dog_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name")
    with col2:
        breed = st.text_input("Breed")
    
    age = st.number_input("Age", 0, 30, 1)
    
    if st.form_submit_button("Add Dog"):
        if name and breed:
            try:
                add_dog(name, breed, age)
                st.success(f"Successfully added {name}!")
                st.rerun()
            except Exception:
                st.error("Error: Could not connect to API.")
