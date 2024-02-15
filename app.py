import streamlit as st
from page.authentication import show_login_page
from page.register import show_registration_page
from page.profiles import show_user_profile

# Initialize session state
if 'login_status' not in st.session_state:
    st.session_state['login_status'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ''
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'login'

def main():
    if st.session_state['current_page'] == 'login':
        if st.session_state['login_status']:
            show_user_profile()
        else:
            show_login_page()
    elif st.session_state['current_page'] == 'register':
        show_registration_page()

if __name__ == "__main__":
    main()
