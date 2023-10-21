import streamlit as st
from app import page2
from Snowpark_Streamlit_Revenue_Prediction import page3

st.set_page_config(page_title="Multi-Page Streamlit App")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Page 1", "Page 2"])

if page == "Page 1":
    page2()
elif page == "Page 2":
    page3()
