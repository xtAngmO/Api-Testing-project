import streamlit as st
import requests
from config import server_url

def show_login_page():
    st.title("Login Page")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")

        if login_button:
            response = requests.post(server_url + "/authenticate", json={"username": username, "password": password})
            if response.status_code == 200:
                data = response.json()
                if data["success"]:
                    st.session_state['login_status'] = True
                    st.session_state['username'] = username
                    st.experimental_rerun()
                else:
                    st.error(data["message"])
            else:
                st.error("Failed to communicate with the authentication server.")
                
    if st.button("Register"):
        st.session_state['current_page'] = 'register'
        st.experimental_rerun()
