import streamlit as st
import requests
from config import server_url

def show_user_profile():
    st.title("Profile Page")
    username = st.session_state.get('username')  # Use get to avoid KeyError if 'username' not set
    
    if username:
        response = requests.get(server_url + f"/profile", params={'username': username})
        if response.status_code == 200:
            user_profile = response.json()
            
            # Display user profile in a structured layout
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("User Information")
                st.text(f"Username: {user_profile.get('username', '')}")
                st.text(f"First Name: {user_profile.get('first_name', '')}")
                st.text(f"Last Name: {user_profile.get('last_name', '')}")
                st.text(f"Email: {user_profile.get('email', '')}")
                st.text(f"Phone Number: {user_profile.get('phone_number', '')}")
            
            with col2:
                st.subheader("Additional Details")
                st.text(f"Age: {user_profile.get('age', '')}")

        else:
            st.error("Failed to retrieve profile.")
    else:
        st.error("Username not set in session state.")
