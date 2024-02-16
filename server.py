from flask import Flask, request, jsonify
from pymongo import MongoClient
from database import Database
from bson.json_util import dumps
from bson.objectid import ObjectId
import os
import re

# load mongo database
db = Database('ApiTesting').db

app = Flask(__name__)

@app.route('/authenticate', methods=['POST'])
def authenticate():
    # Extract username and password from the request
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    collection = db['user_account']
    responseUser = collection.find_one({'username' : username, 'password' : password})
    if responseUser == None :
        return jsonify({"success": False, "message": "Authentication failed."})
    else :
        return jsonify({"success": True, "message": "Authentication successful."})
    

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    name = data.get('name')
    age = data.get('age')

    # Username validation regex
    username_regex = "^[A-Za-z0-9]{6,12}$"
    # Password validation regex (at least one letter, 8-24 characters)
    password_regex = "^(?=.*[A-Za-z])[A-Za-z\d@$!%*#?&]{8,24}$"
    
    
    if not password == confirm_password:
        return jsonify({"success : " : False, "message" : "Passwords do not match. Please try again."}), 400

    # Validate username
    if not re.match(username_regex, username):
        return jsonify({"success": False, "message": "Username must be 6-12 characters long and contain only English letters and numbers."}), 400

    # Validate password
    if not re.match(password_regex, password):
        return jsonify({"success": False, "message": "Password must be 8-24 characters long and include at least one English letter."}), 400

    
    collection = db['user_account']
    count = collection.count_documents({})
    collection.insert_one({'user_id' : count + 1, 'username' : username, 'password' : password, 'name' : name, 'age': age})
    return jsonify({"success": True, "message": "Registration successful."})


@app.route('/profile', methods=['POST'])
def profile():
    data = request.json
    username = data.get('username')
    
    collection = db['user_account']
    responseUser = collection.find_one({'username' : username})
    if responseUser != None :
        return jsonify({"name": responseUser.get('name'), "age" : responseUser.get('age')}), 200
    else :
        return jsonify({"success": False, "message": "error get data user"}), 400
    
@app.route('/product', methods=['GET'])
def product():
    collection = db['product']
    products = list(collection.find({}))
    response = dumps(products)
    return response, 200
    
@app.route('/cart', methods=['POST'])
def cart():
    data = request.json
    username = data.get("username")
    product = data.get("product")
    product_id = product.get("id_product")
    product_quantity = product.get("quantity", 0)  # Get quantity from input, default to 0 if not provided
    
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
    if not id_product:
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

if __name__ == '__main__':
    app.run(debug=True, port=8080)
