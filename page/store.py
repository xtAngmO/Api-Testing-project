import streamlit as st
import requests
from config import server_url

def show_store():
    st.title("Store")

    # Fetch products from the backend
    response_product = requests.get(server_url + "/product")
    products = []
    product_image_map = {}
    if response_product.status_code == 200:
        products = response_product.json()
        for product in products:
            product.pop('_id', None)  # Remove the '_id' key if it exists
            product_image_map[product['id_product']] = product.get('image_path', "./image/notfound.png")

        for i in range(0, len(products), 3):
            cols = st.columns(3)  # Create a row of 3 columns
            for j in range(3):
                if i + j < len(products):
                    product = products[i + j]
                    with cols[j]:  # Use each column to display a product
                        st.image(product.get('image_path', "./image/notfound.png"), width=100, use_column_width=True)
                        product_info = f"""
                        <div style="margin-bottom: 10px;">
                            <h5 style="margin:0;">{product['product_name']}</h5>
                            <p style="margin:0;color: orange;">${product['price']}</p>
                            <p style="margin:0;">Amount: {product['amount']}</p>
                        </div>
                        """
                        st.markdown(product_info, unsafe_allow_html=True)
                        if product['amount'] > 0:
                            quantity = st.number_input("Quantity", min_value=1, max_value=product.get('amount', 10), value=1, key=f"qty_{product['id_product']}{i+j}")
                            if st.button("Add to Cart", key=f"add_{product['id_product']}"):
                                add_to_cart(product, quantity)
                        else:
                            st.write("Out of Stock")
    else:
        st.error("Failed to fetch products")

    # Assuming the username is stored in session state
    username = st.session_state.get('username', 'default_user')

    # Fetch the shopping cart for the user
    cart_response = requests.get(server_url + f"/showcart?username={username}")
    if cart_response.status_code == 200:
        cart_items = cart_response.json()
        if cart_items:
            st.title("Shopping Cart")
            cols = st.columns([3, 1, 1, 1,1])
            with cols[0] :
                st.write("*image*")
            with cols[1] : 
                st.write("*name*")
            with cols[2] :
                st.write("*quantity*")
            with cols[3] : 
                st.write("*price*")
            for item in cart_items:
                # Using columns to layout the item details and the remove button
                cols = st.columns([3, 1, 1, 1, 1])
                with cols[0]:
                    # Retrieve the image path using the product ID from the mapping
                    image_path = product_image_map.get(item['id_product'], "./image/notfound.png")
                    st.image(image_path, width=100)  # Display product image
                with cols[1]:
                    st.markdown(f"**{item['product_name']}**")
                with cols[2]:
                    st.markdown(f"**{item['quantity']}**")
                with cols[3]:
                    st.markdown(f"**${item['price']}**")
                # Remove button in the last column
                if cols[4].button("Remove", key=f"remove_{item['id_product']}"):
                    remove_from_cart(item)
        else:
            st.write("Your shopping cart is empty.")
    else:
        st.error("Failed to fetch shopping cart")
        
        
def add_to_cart(product, quantity):
    username = st.session_state.get('username', 'default_user')
    
    # Fetch the current cart for the user
    cart_response = requests.get(server_url + f"/showcart?username={username}")
    if cart_response.status_code == 200:
        cart_items = cart_response.json()
        existing_quantity = 0
        # Check if the product is already in the cart and sum up the quantity
        for item in cart_items:
            if item['id_product'] == product['id_product']:
                existing_quantity += item['quantity']
        
        # Calculate total quantity after addition
        total_quantity = existing_quantity + quantity

        # Check if total quantity exceeds product's available amount
        if total_quantity > product['amount']:
            st.warning("Cannot add more than the available stock.")
            return
        
        # Proceed to add to cart if the total quantity is within the available stock
        product_with_qty = {"id_product": product['id_product'], "product_name" : product["product_name"], "quantity": quantity, "price": product['price']}
        add_cart_response = requests.post(server_url + "/cart", json={"username": username, "product": product_with_qty})
        
        if add_cart_response.status_code == 200:
            st.success("Product added to cart successfully.")
            st.experimental_rerun()
        else:
            st.error("Failed to add product to cart.")
    else:
        st.error("Failed to fetch current cart.")

        
def remove_from_cart(item) :
    username = st.session_state['username']
    id_product = item.get("id_product")
    response = requests.put(server_url + '/deletecart', json = {"username" : username, "id_product" : id_product})
    st.rerun()