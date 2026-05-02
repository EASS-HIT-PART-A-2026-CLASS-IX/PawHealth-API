import streamlit as st
import pandas as pd
from client import get_dogs, add_dog

st.set_page_config(page_title="PawHealth Dashboard", page_icon="🐾")
st.title("🐾 PawHealth Management")

dogs_list = get_dogs()
st.sidebar.metric("Total Dogs", len(dogs_list))

st.subheader("Dog Registry")
if dogs_list:
    df = pd.DataFrame(dogs_list)
    st.dataframe(df, use_container_width=True)
else:
    st.info("The registry is currently empty.")

st.divider()
st.subheader("Register a New Dog")
with st.form("new_dog"):
    name = st.text_input("Name")
    breed = st.text_input("Breed")
    age = st.number_input("Age", 0, 30, 1)
    if st.form_submit_button("Add Dog"):
        if name and breed:
            try:
                add_dog(name, breed, age)
                st.success(f"{name} added!")
                st.rerun()
            except Exception as e:
                st.error("Connection error: Make sure Backend is running on port 8000")
