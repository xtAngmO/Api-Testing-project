import requests
import streamlit as st
from config import server_url
import pandas as pd
import os

def show_history():
    st.header("Order History")

    username = st.session_state['username']
    url = f"{server_url}/showorder?username={username}"
    
    response = requests.get(url)
    if response.status_code == 200:
        orders = response.json().get('orders', [])
        
        if not orders:
            st.write("No orders found.")
            return
        
        for order in orders:
            # Check the format of the time field and parse it accordingly
            order_time_str = order['time']['$date'] if isinstance(order['time'], dict) else order['time']
            order_time = pd.to_datetime(order_time_str)
            
            with st.expander(f"Order ID: {order['id_order']} - Status: {order['status']}"):
                order_details = pd.DataFrame(order['list'])
                order_details['Total'] = order_details['quantity'] * order_details['price']
                st.table(order_details[['id_product', 'product_name', 'quantity', 'price', 'Total']])
                
                st.metric(label="Total Payment", value=f"${order['total_payment']}")
                st.write(f"Order Time: {order_time.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        st.error("Failed to fetch order history.")
