import requests
import streamlit as st
from config import server_url
import os

def show_admin():
    st.title("Add Product")

    # Product details input
    cols = st.columns([1,1])
    with cols[0] :
        id_product = st.text_input("Product ID")
        price = st.number_input("Price", min_value=0.01, step=0.01)
        
    with cols[1] :
        product_name = st.text_input("Product Name")
        amount = st.number_input("Amount", min_value=1, step=1)

    image = st.file_uploader("Choose a file", type=['png', 'jpg', 'jpeg'])
    
    if image is not None:
            # Display the uploaded image
            st.image(image, caption='Uploaded image product.', width=100)

    if st.button("Add Product"):
        if image is not None and id_product:
            image_path = f"./image/{id_product}.jpg"
            username = st.session_state['username']
            data = {
                "username": username,
                "id_product": id_product,
                "product_name": product_name,
                "price": price,
                "amount": amount,
                "image_path": image_path
            }
            
            # Send data to Flask API
            response = requests.post(server_url+"/addproduct", json=data)
            if response.status_code == 200:
                with open(image_path, "wb") as f:
                    f.write(image.getbuffer())
                st.success("Product added successfully.")
            else:
                st.error(f"Failed to add product {response.json()['message']}.")
        else:
            st.error("Please fill in all fields and upload an image.")
            
    st.title("Manage Product")
    response_product = requests.get(server_url + "/product")
    if response_product.status_code == 200:
        products = response_product.json()
        
        # Iterate over products to display them
        for product in products:
            with st.expander(f"{product['product_name']} (${product['price']})"):
                st.image(product.get('image_path', "./image/notfound.png"), width=100)
                st.write(f"Amount: {product['amount']}")
                add_amount = st.number_input("Add Amount", min_value=1, max_value=1000, value=1, key=f"add_{product['id_product']}")
                if st.button("Add Amount", key=f"addamount_{product['id_product']}"):
                    update_product_amount(product['id_product'], add_amount)
                if st.button("Remove Product", key=f"remove_{product['id_product']}"):
                    remove_product(product['id_product'])
    else:
        st.error("Failed to fetch products")
         
    confirm_logout()

def update_product_amount(id_product, add_amount):
    username = st.session_state.get('username')
    if username == 'admin':
        data = {
            "username": username,
            "id_product": id_product,
            "amount": add_amount
        }
        response = requests.put(f"{server_url}/addamountproduct", json=data)
        if response.status_code == 200:
            st.success("Product amount updated successfully.")
            st.rerun()
        else:
            st.error(f"Failed to update product amount: {response.json().get('message')}")
    else:
        st.error("Admin privileges required.")

def remove_product(id_product):
    username = st.session_state.get('username')
    if username == 'admin':
        data = {
            "username": username,
            "id_product": id_product
        }
        response = requests.post(f"{server_url}/deleteproduct", json=data)
        if response.status_code == 200:
            st.success("Product removed successfully.")
            st.rerun()
        else:
            st.error(f"Failed to remove product: {response.json().get('message')}")
    else:
        st.error("Admin privileges required.")
        
def confirm_logout():
    # Directly ask for confirmation within the same button click handling
    if st.button("Logout"):
        # Instead of immediately logging out, set a flag in the session state
        st.session_state['confirm_logout'] = True
    
    if 'confirm_logout' in st.session_state and st.session_state['confirm_logout']:
        # Display the confirmation prompt
        st.warning("Are you sure you want to logout?")
        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
        if col2.button("Yes, Logout"):
            # Perform the logout actions
            st.session_state['login_status'] = False
            st.session_state['username'] = ''
            st.session_state['current_page'] = 'login'
            # Reset the logout confirmation flag
            del st.session_state['confirm_logout']
            # Optionally, use st.experimental_rerun() to refresh the app
            st.rerun()
        if col4.button("Cancel"):
            # Reset the logout confirmation flag without logging out
            del st.session_state['confirm_logout']