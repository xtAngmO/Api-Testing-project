from flask import Flask, request, jsonify
from database import Database
from datetime import datetime
import random
import secrets
import bcrypt

# load mongo database
db = Database('ApiTesting').db

app = Flask(__name__)

def generate_unique_id_order():
    while True:
        # Generate a potential id_order
        potential_id_order = random.randint(100000, 999999)
        # Check if it already exists in the orders collection
        existing_order = db['orders'].find_one({"orders.id_order": str(potential_id_order)})
        if not existing_order:
            return potential_id_order  # Return it if it's unique

@app.route('/authenticate', methods=['POST'])
def authenticate():
    # Extract username and password from the request
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    collection = db['user_account']
    responseUser = collection.find_one({'username': username})
    
    if responseUser is None:
        return jsonify({"success": False, "message": "Authentication failed."})
    
    # Verify the password
    if bcrypt.checkpw(password.encode('utf-8'), responseUser['password']):
        return jsonify({"success": True, "message": "Authentication successful."})
    else:
        return jsonify({"success": False, "message": "Authentication failed."})
    

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    email = data.get('email')
    firstname = data.get('first_name')
    lastname = data.get('last_name')
    phone_number = data.get('phone_number')
    age = data.get('age')
    
    if not username or not password or not confirm_password or not firstname or not lastname or not email or not phone_number or not age:
        return jsonify({"error": "Incomplete information not provided"}), 400

    # Email validation regex
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    
    # Username validation regex
    username_regex = "^[A-Za-z0-9]{6,12}$"
    
    # Password validation regex (at least one letter, 8-24 characters)
    password_regex = "^(?=.*[A-Za-z])[A-Za-z\d@$!%*#?&]{8,24}$"
    
    # Phone number validation regex (exactly 10 digits)
    phone_number_regex = "^\d{10}$"
    
    if not password == confirm_password:
        return jsonify({"success": False, "message": "Passwords do not match. Please try again."}), 400

    # Validate username
    if not re.match(username_regex, username):
        return jsonify({"success": False, "message": "Username must be 6-12 characters long and contain only English letters and numbers."}), 400

    # Validate password
    if not re.match(password_regex, password):
        return jsonify({"success": False, "message": "Password must be 8-24 characters long and include at least one English letter."}), 400

    # Validate email
    if not re.match(email_regex, email):
        return jsonify({"success": False, "message": "Email must be a valid email address."}), 400

    # Validate phone number
    if not re.match(phone_number_regex, phone_number):
        return jsonify({"success": False, "message": "Phone number must be exactly 10 digits long and contain only numbers."}), 400
    
    # Validate age
    try:
        age = int(age)
        if age < 0 or age > 120:  # Assuming a reasonable age range
            raise ValueError
    except ValueError:
        return jsonify({"success": False, "message": "Age must be a number between 0 and 120."}), 400

    collection = db['user_account']
    # Ensure unique usernames
    if collection.find_one({'username': username}):
        return jsonify({"success": False, "message": "Username already exists. Please choose another."}), 400

    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insert the new user into the database with the hashed password
    collection.insert_one({'username': username, 'password': hashed_password, 'email': email, 'first_name': firstname, "last_name": lastname, "phone_number": phone_number, 'age': age})
    return jsonify({"success": True, "message": "Registration successful."})


@app.route('/profile', methods=['GET'])
def profile():
    username = request.args.get('username')
    
    if not username:
        return jsonify({"error": "Username not provided"}), 400
    
    collection = db['user_account']
    responseUser = collection.find_one({'username': username}, {'_id': 0, 'password' : 0})  # Excluding MongoDB's _id from the response
    
    if responseUser:
        return jsonify(responseUser), 200
    else:
        return jsonify({"success": False, "message": "error getting data user"}), 400
    
@app.route('/product', methods=['GET'])
def product():
    collection = db['product']
    products = list(collection.find({}, {"_id" : 0}))
    return jsonify(products), 200
    
@app.route('/cart', methods=['POST'])
def cart():
    data = request.json
    username = data.get("username")
    product = data.get("product")
    product_id = product.get("id_product")
    product_quantity = product.get("quantity", 0)
    
    if not username or not product or not product_id :
        return jsonify({"error": "Incomplete information not provided"}), 400
    
    collection = db['cart']
    user_cart = collection.find_one({"username": username})
    
    if user_cart is None:
        # If the user does not have a cart, create one with the product
        collection.insert_one({"username": username, "products": [product]})
    else:
        # Check if the product exists in the user's cart
        product_index = next((index for (index, p) in enumerate(user_cart["products"]) if p["id_product"] == product_id), None)
        
        if product_index is not None:
            # If the product exists, update its quantity
            current_quantity = user_cart["products"][product_index].get("quantity", 0)
            new_quantity = current_quantity + product_quantity
            # Update the quantity of the existing product in the cart
            collection.update_one({"username": username, "products.id_product": product_id}, {"$set": {"products.$.quantity": new_quantity}})
        else:
            # If the product does not exist, add it to the cart
            collection.update_one({"username": username}, {"$push": {"products": product}})
    
    return jsonify({"success": True, "message": "Cart updated successfully"}), 200

@app.route('/showcart', methods=['GET'])
def showCart():
    # Assuming the username is passed as a query parameter
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Username not provided"}), 400

    collection = db['cart']
    # Find the document in the collection
    response = collection.find_one({"username": username})
    
    if response is None:
        # If the user does not have a cart, create one with the product
        collection.insert_one({"username": username, "products": []})

    # Check if the document is found
    if response:
        # Extract the products field
        products = response.get("products", [])
        return jsonify(products)
    else:
        return jsonify({"error": "User not found"}), 404
    
@app.route('/deletecart', methods=['PUT'])
def deleteCart():
    data = request.json
    username = data.get("username")
    id_product = data.get("id_product")
    if not id_product or not username:
        return jsonify({"error": "Product ID not provided"}), 400
    
    collection = db['cart']
    
    # Use the $pull operator to remove the item from the array
    response = collection.update_one(
        {"username": username},
        {"$pull": {"products": {"id_product": id_product}}}
    )
    
    if response.modified_count == 0:
        # If no document was modified, it means the product was not found in the user's cart
        return jsonify({"error": "Product not found in the cart or username is incorrect"}), 404
    
    return jsonify({"message": "Product removed from cart successfully"})


@app.route('/calculatecart', methods=['GET'])
def calculateCart():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Username not provided"}), 400

    collection = db['cart']
    # Find the document in the collection
    response = collection.find_one({"username": username})

    if not response:
        return jsonify({"error": "Cart not found for the user"}), 404

    total_price = 0
    for product in response['products']:
        product_total = product['price'] * product['quantity']
        total_price += product_total
        
    total_payment = total_price
    discount1 = int(total_price / 1000) * 50
    countdiscount = 0
    if total_price > 5000 :
        countdiscount = total_price*0.05
        total_payment = total_price - countdiscount
        
    total_payment = total_price - discount1
    return jsonify({"total_price" : total_price, "total_payment": total_payment, "discount" : countdiscount + discount1}), 200

@app.route('/payment', methods=['POST'])
def makePayment():
    data = request.json
    username = data.get("username")
    total_payment = data.get("total_payment")

    if not username:
        return jsonify({"error": "Username not provided"}), 400
    
    cart_collection = db['cart']
    product_collection = db['product']

    # Fetch the user's cart
    cart = cart_collection.find_one({"username": username})

    if cart is None or not cart.get("products"):
        return jsonify({"error": "Cart is empty or does not exist"}), 400

    # Iterate through the products in the user's cart
    for cart_item in cart["products"]:
        # Fetch the corresponding product from the `product` collection
        product = product_collection.find_one({"id_product": cart_item["id_product"]})
        
        if product:
            # Calculate the new amount
            new_amount = product["amount"] - cart_item["quantity"]
            
            # Update the product in the `product` collection
            product_collection.update_one(
                {"id_product": cart_item["id_product"]},
                {"$set": {"amount": new_amount}}
            )
    
    cart_collection.update_one({"username": username}, {"$set": {"products": []}})
    
    order_collection = db['orders']
    if not order_collection.find_one({"username": username}):
        order_collection.insert_one({"username": username, "orders": []})
        
    # Generate a 6-character id_order
    id_order = generate_unique_id_order()
    
    timenow = datetime.now()
    
    order_collection.update_one({"username": username}, 
                                {"$push": 
                                    {"orders": {
                                        "time": timenow,
                                        "id_order": id_order,
                                        "list" : cart['products'],
                                        "total_payment": total_payment,
                                        "status": 'wait',
                                    }}
                                })
    
    return jsonify({"message": f"Payment successful, products updated, order ID: {id_order}"}), 200

@app.route('/showorder', methods=['GET'])
def showOrders():
    username = request.args.get("username")
    
    collection = db['orders']
    
    if not collection.find_one({"username" : username}) :
        collection.insert_one({"username": username, "orders": []})
        
    response = collection.find_one({"username" : username}, {"_id" : 0})
    
    return jsonify(response), 200



@app.route('/addproduct', methods=['POST'])
def addProduct():
    data = request.json
    username = data.get("username")
    id_product = data.get("id_product")
    product_name = data.get("product_name")
    price = data.get("price")
    amount = data.get("amount")
    image_path = data.get("image_path")
    
    if username != 'admin' :
        return jsonify({"success" : False, "message" : "Admin only"}), 400
    
    if not id_product or not price or not amount or not image_path or not product_name :
        return jsonify({"error": "Incomplete information not provided"}), 400
    
    collection = db["product"]
    if collection.find_one({"id_product": id_product}) :
        return jsonify({"success": False, "message": "Id_product already exists. Please choose another."}), 400
    
    response = collection.insert_one({"id_product" : id_product, 
                           "product_name" : product_name, 
                           "price" : price, 
                           "amount" : amount,
                           "image_path" : image_path})
    
    return jsonify({"success": True, "message": "add product successfully"}), 200

@app.route('/deleteproduct', methods=['POST'])
def deleteProduct() :
    data = request.json
    username = data.get("username")
    id_product = data.get("id_product")
    if username != 'admin' :
        return jsonify({"success" : False, "message" : "Admin only"}), 400
    
    if not id_product :
        return jsonify({"error" : "id product not provided"}), 400
    
    collection = db["product"]
    if not collection.find_one({"id_product" : id_product}) :
        return jsonify({"error" : "id product not found"}), 400
    
    response = collection.delete_one({"id_product" : id_product})
    return jsonify({"success": True, "message": "delete product successfully"}), 200

@app.route('/addamountproduct', methods=['PUT'])
def addAmountOfProduct():
    data = request.json
    username = data.get("username")
    id_product = data.get("id_product")
    amount = data.get("amount")
    if username != 'admin' :
        return jsonify({"success" : False, "message" : "Admin only"}), 400
    
    if not id_product or not amount :
        return jsonify({"error": "Incomplete information not provided"}), 400
    
    collection = db["product"]
    if not collection.find_one({"id_product" : id_product}) :
        return jsonify({"error" : "id product not found"}), 400
    
    data_old = collection.find_one({"id_product" : id_product})
    old_amount = data_old.get("amount")
    
    amount = amount + old_amount
    response = collection.update_one({"id_product" : id_product}, {"$set" : {"amount" : amount}})
    return jsonify({"success": True, "message": "edit amount product successfully"}), 200

@app.route('/showallorders', methods=['GET'])
def showAllOrders() :
    collection = db['orders']
    orders = list(collection.find({}, {"_id" : 0}))
    return jsonify(orders), 200
    

@app.route('/updateorderstatus', methods=['POST'])
def updateOrderStatus():
    data = request.json
    username = data.get("username")
    id_order = data.get("id_order")
    new_status = data.get("status")
    
    # Update the order status
    result = db['orders'].update_one(
        {"username": username, "orders.id_order": id_order},
        {"$set": {"orders.$.status": new_status}}
    )
    
    if result.modified_count:
        return jsonify({"message": "Order status updated successfully"}), 200
    else:
        return jsonify({"error": "Order not found or update failed"}), 404
    

if __name__ == '__main__':
    app.run(debug=True, port=8080)
