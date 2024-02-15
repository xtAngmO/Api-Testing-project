from flask import Flask, request, jsonify
from pymongo import MongoClient
from database import Database
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
    name = data.get('name')
    age = data.get('age')

    # Username validation regex
    username_regex = "^[A-Za-z0-9]{6,12}$"
    # Password validation regex (at least one letter, 8-24 characters)
    password_regex = "^(?=.*[A-Za-z])[A-Za-z\d@$!%*#?&]{8,24}$"

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
    
    
if __name__ == '__main__':
    app.run(debug=True, port=8080)
