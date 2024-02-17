import streamlit as st
import requests
import pandas as pd
from config import server_url

def show_payment():
    st.header("Payment")
    username = st.session_state.get('username', 'default_user')
    
    # Fetch the shopping cart for the user
    cart_response = requests.get(server_url + f"/showcart?username={username}")
        
    cart_items = cart_response.json()
    
    if not cart_items :
        st.write("No product in your cart")
    else :
        # Convert the cart_items into a pandas DataFrame
        df_cart_items = pd.DataFrame(cart_items)
        
        # Rename and reorder columns for better readability
        df_cart_items.rename(columns={
            'id_product': 'Product ID',
            'product_name': 'Product Name',
            'quantity': 'Quantity',
            'price': 'Price'
        }, inplace=True)
        df_cart_items = df_cart_items[['Product ID', 'Product Name', 'Quantity', 'Price']]
        
        # Display the DataFrame using Streamlit
        st.table(df_cart_items)
        
        # Fetch total price, discount, and total payment for the user
        allPrice_response = requests.get(server_url + f"/calculatecart?username={username}")
        allPrice = allPrice_response.json()
        
        st.header("Summary")
        st.markdown(f"""
            <style>
                .summary-row {{
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 5px; /* Adjust this value to reduce/increase space */
                }}
            </style>
            <div class="summary-row"><span>Total Price:</span> <span>{allPrice['total_price']}</span></div>
            <div class="summary-row"><span>Discount:</span> <span> -{allPrice['discount']}</span></div>
            <div class="summary-row"><span>Total Payment:</span> <span>{allPrice['total_payment']}</span></div>
            """, unsafe_allow_html=True)
        
        # Make Payment section
        st.header("Make Payment")
        st.write("Please upload the payment slip below:")
        uploaded_file = st.file_uploader("Choose a file", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file is not None:
            # Display the uploaded image
            st.image(uploaded_file, caption='Uploaded Payment Slip.', width=100)
            st.success("Payment slip uploaded successfully!")
            if st.button("make payment") :
                response_mayment = requests.post(server_url + "/payment", json={"username": username})
                if response_mayment.status_code == 200 :
                    st.success("payment success")
                    st.rerun()
                else :
                    st.error("you can't payment")
                
