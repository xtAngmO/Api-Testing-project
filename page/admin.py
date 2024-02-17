import streamlit as st
import requests
from config import server_url
from streamlit_option_menu import option_menu
from page.manageOrder import show_manageOrder
from page.manageProduct import show_manageProduct


# page/main.py
def show_admin():
    st.set_page_config(
        page_title="Hello world",
        page_icon="🛍️",
        layout="centered",
    )
    
    handle_navigation()

    # Display the selected page content based on session state
    if st.session_state['current_page'] == "manageorder":
        show_manageOrder()
    elif st.session_state['current_page'] == "manageproduct":
        show_manageProduct()

        
def handle_navigation():
    selected = option_menu(
        menu_title=None,
        options=["Products","Orders", "Logout"],  
        icons=["shop","clock-history","box-arrow-right"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )
    
    page_map = {
        "Products" : "manageproduct",
        "Orders" : "manageorder",
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
