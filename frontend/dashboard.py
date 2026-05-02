import streamlit as st
import pandas as pd
from client import get_dogs, add_dog

st.set_page_config(page_title="PawHealth Dashboard", page_icon="🐾")
st.title("🐾 PawHealth Management")

# EX2 Requirement: Provide one small extra (summary metric)
dogs = get_dogs()
st.sidebar.metric("Total Dogs Registered", len(dogs))

# EX2 Requirement: Allow users to list existing entries
st.subheader("Dog Registry")
if dogs:
    # Updated to width='stretch' to match latest Streamlit API
    st.dataframe(pd.DataFrame(dogs), width='stretch')
else:
    st.info("The registry is currently empty.")

st.divider()

# EX2 Requirement: Allow users to add a new entry
st.subheader("Register a New Dog")
with st.form("add_dog_form"):
    name = st.text_input("Name")
    breed = st.text_input("Breed")
    age = st.number_input("Age", 0, 30, 1)
    if st.form_submit_button("Add Dog"):
        if name and breed:
            try:
                add_dog(name, breed, age)
                st.success(f"Added {name} successfully!")
                st.rerun()
            except Exception:
                st.error("Connection error: Is the Backend running?")
