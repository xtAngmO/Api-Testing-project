import streamlit as st
import requests
from config import server_url

def show_user_profile():
    st.title("Profile Page")
    username = st.session_state['username']
    
    response = requests.post(server_url + "/profile", json={"username": username})
    if response.status_code == 200:
        data = response.json()
        st.write(f"Name: {data['name']}")
        st.write(f"Age: {data['age']}")
    else:
        st.error("User profile not found.")

    if st.button('Logout'):
        st.session_state['login_status'] = False
        st.session_state['username'] = ''
        st.experimental_rerun()
