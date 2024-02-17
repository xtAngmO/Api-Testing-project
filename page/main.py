import streamlit as st
import requests
from config import server_url
from streamlit_option_menu import option_menu
from page.profiles import show_user_profile
from page.home import show_home
from page.store import show_store
from page.payment import show_payment
from page.history import show_history

# page/main.py
def show_main_page():
    st.set_page_config(
        page_title="Hello world",
        page_icon="🛍️",
        layout="centered",
    )
    
    handle_navigation()

    # Display the selected page content based on session state
    if st.session_state['current_page'] == "home":
        show_home()
    elif st.session_state['current_page'] == "store":
        show_store()
    elif st.session_state['current_page'] == "profile":
        show_user_profile()
    elif st.session_state['current_page'] == "payment":
        show_payment()
    elif st.session_state['current_page'] == "history" :
        show_history()
        
def handle_navigation():
    selected = option_menu(
        menu_title=None,
        options=["Home", "Store", "Pay" , "History","Profile", "Logout"],  
        icons=["house", "shop", "credit-card", "clock-history","person-fill","box-arrow-right"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )
    
    page_map = {
        "Home": "home",
        "Store": "store",
        "Profile": "profile",
        "History" : "history",
        "Pay": "payment", 
        "Logout": "logout"
    }
    
    if selected == "Logout":
        confirm_logout()
    else:
        st.session_state['current_page'] = page_map[selected]

def confirm_logout():
    st.warning("Are you sure you want to logout?")
    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
    if col2.button("Yes, Logout"):
        st.session_state['login_status'] = False
        st.session_state['username'] = ''
        st.session_state['current_page'] = 'login'
        st.rerun()
    if col4.button("Cancel"):
        pass
