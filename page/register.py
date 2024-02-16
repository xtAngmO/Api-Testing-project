import streamlit as st
import requests
from config import server_url

def show_registration_page():
    st.title("Register")
    with st.form("registration_form"):
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm password", type = "password")
        new_email = st.text_input("Email")
        name = st.text_input("Name")
        age = st.text_input("Age")
        register_button = st.form_submit_button("Register")

        if register_button:
            response = requests.post(server_url + "/register", json={"username": new_username, "password": new_password, "confirm_password" : confirm_password,'email' : new_email, 'name': name, 'age': age})
            if response.status_code == 200:
                st.success("Registration successful! Please go back to login.")
            else:
                st.error("Registration failed. Please try again.")

    # Moved outside the form
    if st.button("Back to Login"):
        st.session_state['current_page'] = 'login'
        st.rerun()