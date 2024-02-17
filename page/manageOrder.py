import requests
import streamlit as st
import pandas as pd
from config import server_url

def update_order_status(username, id_order, new_status):
    """Send a request to update the order status."""
    response = requests.post(f"{server_url}/updateorderstatus", json={
        "username": username,
        "id_order": id_order,
        "status": new_status
    })
    return response.status_code == 200

def show_manageOrder():
    st.header("Manage Orders")

    response = requests.get(f"{server_url}/showallorders")
    if response.status_code == 200:
        all_orders = response.json()
        
        # Transforming the data into a format suitable for display in a DataFrame
        table_data = []
        for order in all_orders:
            for o in order['orders']:
                # Check the format of the 'time' field
                if isinstance(o['time'], dict) and '$date' in o['time']:
                    time_str = o['time']['$date']
                else:
                    time_str = o['time']  # Assuming 'time' is a string if not a dictionary
                
                table_data.append({
                    "Username": order['username'],
                    "Order ID": o['id_order'],
                    "Time": time_str,
                    "Total Payment": o['total_payment'],
                    "Status": o['status']
                })
                
        if table_data:
            df = pd.DataFrame(table_data)
            st.dataframe(df, use_container_width=True)
            
            usernames = [order['username'] for order in all_orders]
            selected_username = st.selectbox("Select User", options=usernames)
            
            if selected_username:
                user_orders = next((order for order in all_orders if order['username'] == selected_username), None)
                if user_orders:
                    order_ids = [str(order['id_order']) for order in user_orders['orders']]
                    selected_order_id = st.selectbox("Select Order ID", options=order_ids)
                    
                    if selected_order_id:
                        new_status = st.selectbox("New Status", options=["success", "wait"])
                        if st.button("Update Status"):
                            update_response = requests.post(f"{server_url}/updateorderstatus", json={
                                "username": selected_username,
                                "id_order": int(selected_order_id),
                                "status": new_status
                            })
                            if update_response.status_code == 200:
                                st.success("Order status updated successfully.")
                                st.rerun()
                            else:
                                st.error("Failed to update order status.")
        else:
            st.write("No orders found.")
    else:
        st.error("Failed to fetch orders.")