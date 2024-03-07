# codeTesting
import os
import requests
from dotenv import load_dotenv

load_dotenv()
serverURL = os.environ.get('server_url')

# ============================================== LOGIN API TESTING ==============================================
loginAPI = serverURL + '/authenticate'

# Test Case 1 : Correct Username and Password
response1 = requests.post(loginAPI, json={"username": "user001", "password": "12345678Ggg"})
# Test Case 2 : Correct Username but Wrong Password
response2 = requests.post(loginAPI, json={"username": "user001", "password": "456789Ggg"})
# Test Case 3 : Wrong Username but Correct Password
response3 = requests.post(loginAPI, json={"username": "wrongUsername", "password": "12345678Ggg"})
# Test Case 4 : Wrong Username and Password
response4 = requests.post(loginAPI, json={"username": "wrongUsername", "password": "456789Ggg"})

def test_authenticate():
    assert response1.json()['success'] == True
    assert response2.json()['success'] == False
    assert response3.json()['success'] == False
    assert response4.json()['success'] == False

# ============================================== Register API Testing ==============================================
# registerAPI = serverURL + '/register'

# # Test Case 1 : Not Input Anything
# noneInput = {"username": None,
#              "password": None, 
#              "confirm_password" : None,
#              'email' : None, 
#              'first_name': None, 
#              "last_name": None, 
#              "phone_number" : None,
#              'age': None
# }

# registerRes1 = requests.post(registerAPI, json=noneInput)

# # Test Case 2 : Username Length Testing using BVA-2
#     # Test Case 2.1 : Username Length = 5
# unLength5 = {"username": "five5",
#              "password": "correct1", 
#              "confirm_password" : "correct1",
#              'email' : "correct@email.com", 
#              'first_name': "fname", 
#              "last_name": "lname", 
#              "phone_number" : "0626148977",
#              'age': 20
# }
#     # Test Case 2.2 : Username Length = 6 
# unLength6 = {"username": "sixSix",
#              "password": "correct1", 
#              "confirm_password" : "correct1",
#              'email' : "correct@email.com", 
#              'first_name': "fname", 
#              "last_name": "lname", 
#              "phone_number" : "0626148977",
#              'age': 20
# }
#     # Test Case 2.3 : Username Length = 12
# unLength12 = {"username": "twelve121212",
#              "password": "correct1", 
#              "confirm_password" : "correct1",
#              'email' : "correct@email.com", 
#              'first_name': "fname", 
#              "last_name": "lname", 
#              "phone_number" : "0626148977",
#              'age': 20
# }
#     # Test Case 2.4 : Username Length = 13
# unLength13 = {"username": "thirteen13131",
#              "password": "correct1", 
#              "confirm_password" : "correct1",
#              'email' : "correct@email.com", 
#              'first_name': "fname", 
#              "last_name": "lname", 
#              "phone_number" : "0626148977",
#              'age': 20
# }

# registerRes2_1 = requests.post(registerAPI, json=unLength5)
# registerRes2_2 = requests.post(registerAPI, json=unLength6)
# registerRes2_3 = requests.post(registerAPI, json=unLength12)
# registerRes2_4 = requests.post(registerAPI, json=unLength13)

# # Test Case 3 : Password Length Testing using BVA-2
#     # Test Case 3.1 : Pasword Length = 7
# pwLength7 = {"username": "correctP7",
#              "password": "seven77", 
#              "confirm_password" : "seven77",
#              'email' : "correct@email.com", 
#              'first_name': "fname", 
#              "last_name": "lname", 
#              "phone_number" : "0626148977",
#              'age': 20
# }
#     # Test Case 3.2 : Password Length = 8 with Correct Password Form
# pwLength8 = {"username": "correctP8",
#              "password": "eight888", 
#              "confirm_password" : "eight888",
#              'email' : "correct@email.com", 
#              'first_name': "fname", 
#              "last_name": "lname", 
#              "phone_number" : "0626148977",
#              'age': 20
# }
#     # Test Case 3.3 : Password Length = 24 with Incorrect Password Form
# pwLength24 = {"username": "correctP24",
#              "password": "242424242424242424242424", 
#              "confirm_password" : "242424242424242424242424",
#              'email' : "correct@email.com", 
#              'first_name': "fname", 
#              "last_name": "lname", 
#              "phone_number" : "0626148977",
#              'age': 20
# }
#     # Test Case 3.4 : Password Length = 25
# pwLength25 = {"username": "correctP25",
#              "password": "twentyFive252525252525252", 
#              "confirm_password" : "twentyFive252525252525252",
#              'email' : "correct@email.com", 
#              'first_name': "fname", 
#              "last_name": "lname", 
#              "phone_number" : "0626148977",
#              'age': 20
# }

# registerRes3_1 = requests.post(registerAPI, json=pwLength7)
# registerRes3_2 = requests.post(registerAPI, json=pwLength8)
# registerRes3_3 = requests.post(registerAPI, json=pwLength24)
# registerRes3_4 = requests.post(registerAPI, json=pwLength25)

# # Test Case 4 : Confirm Password Match and Unmatch
#     # Test Case 4.1 : Confirm Password Match
# matchPass = {"username": "correctCP",
#              "password": "matchPass1", 
#              "confirm_password" : "matchPass1",
#              'email' : "correct@email.com", 
#              'first_name': "fname", 
#              "last_name": "lname", 
#              "phone_number" : "0626148977",
#              'age': 20
# }
#     # Test Case 4.2 : Confirm Password Unmatch
# unMatchPass = {"username": "correctCP",
#                "password": "matchPass1", 
#                "confirm_password" : "unMatchPass1",
#                'email' : "correct@email.com", 
#                'first_name': "fname", 
#                "last_name": "lname", 
#                "phone_number" : "0626148977",
#                'age': 20
# }

# registerRes4_1 = requests.post(registerAPI, json=matchPass)
# registerRes4_2 = requests.post(registerAPI, json=unMatchPass)

# # Test Case 5 : Email Form
#     # Test Case 5.1 : Correct Email Form
# correctEmail = {"username": "correctE",
#                 "password": "password001", 
#                 "confirm_password" : "password001",
#                 'email' : "correct@email.com", 
#                 'first_name': "fname", 
#                 "last_name": "lname", 
#                 "phone_number" : "0626148977",
#                 'age': 20
# }
#     # Test Case 5.2 : Incorrect Email Form
# incorrectEmail = {"username": "correctE",
#                   "password": "password001", 
#                   "confirm_password" : "password001",
#                   'email' : "incorrect.com", 
#                   'first_name': "fname", 
#                   "last_name": "lname", 
#                   "phone_number" : "0626148977",
#                   'age': 20
# }

# registerRes5_1 = requests.post(registerAPI, json=correctEmail)
# registerRes5_2 = requests.post(registerAPI, json=incorrectEmail)

# # Test Case 6 : Phone Digit Length
#     # Test Case 6.1 : Phone Digit Length = 9
# pdLength9  = {"username": "correctPD",
#               "password": "password001", 
#               "confirm_password" : "password001",
#               'email' : "correct@email.com", 
#               'first_name': "fname", 
#               "last_name": "lname", 
#               "phone_number" : "999999999",
#               'age': 20
# }
#     # Test Case 6.2 : Phone Digit Length = 10
# pdLength10 = {"username": "correctPD",
#               "password": "password001", 
#               "confirm_password" : "password001",
#               'email' : "correct@email.com", 
#               'first_name': "fname", 
#               "last_name": "lname", 
#               "phone_number" : "1010101010",
#               'age': 20
# }
#     # Test Case 6.3 : Phone Digit Length = 11
# pdLength11 = {"username": "correctPD",
#               "password": "password001", 
#               "confirm_password" : "password001",
#               'email' : "correct@email.com", 
#               'first_name': "fname", 
#               "last_name": "lname", 
#               "phone_number" : "11111111111",
#               'age': 20
# }

# registerRes6_1 = requests.post(registerAPI, json=pdLength9)
# registerRes6_2 = requests.post(registerAPI, json=pdLength10)
# registerRes6_3 = requests.post(registerAPI, json=pdLength11)

# # Test Case 7 : Correct Age
#     # Test Case 7.1 : Age < 1
# ageMinus1 = {"username": "correctA",
#              "password": "password001", 
#              "confirm_password" : "password001",
#              'email' : "correct@email.com", 
#              'first_name': "fname", 
#              "last_name": "lname", 
#              "phone_number" : "0626148977",
#              'age': -1
# }
#     # Test Case 7.2 : Age = 1
# age1 = {"username": "correctA",
#              "password": "password001", 
#              "confirm_password" : "password001",
#              'email' : "correct@email.com", 
#              'first_name': "fname", 
#              "last_name": "lname", 
#              "phone_number" : "0626148977",
#              'age': 1
# }
#     # Test Case 7.3 : Age = 120
# age120 = {"username": "correctA120",
#           "password": "password001", 
#           "confirm_password" : "password001",
#           'email' : "correct@email.com", 
#           'first_name': "fname", 
#           "last_name": "lname", 
#           "phone_number" : "0626148977",
#           'age': 120
# }
#     # Test Case 7.4 : Age > 120
# age121 = {"username": "correctA",
#           "password": "password001", 
#           "confirm_password" : "password001",
#           'email' : "correct@email.com", 
#           'first_name': "fname", 
#           "last_name": "lname", 
#           "phone_number" : "0626148977",
#           'age': 121
# }

# registerRes7_1 = requests.post(registerAPI, json=ageMinus1)
# registerRes7_2 = requests.post(registerAPI, json=age1)
# registerRes7_3 = requests.post(registerAPI, json=age120)
# registerRes7_4 = requests.post(registerAPI, json=age121)

# def test_register():
#     # Test Case 1 : Not Input Anything
#     assert registerRes1.json()['message'] == "Incomplete information not provided"
#     # Test Case 2 : Username Length Testing using BVA-2
#     assert registerRes2_1.json()['message'] == "Username must be 6-12 characters long and contain only English letters and numbers."
#     assert registerRes2_2.json()['message'] == "Registration successful."
#     assert registerRes2_3.json()['message'] == "Registration successful."
#     assert registerRes2_4.json()['message'] == "Username must be 6-12 characters long and contain only English letters and numbers."
#     # Test Case 3 : Password Length Testing using BVA-2
#     assert registerRes3_1.json()['message'] == "Password must be 8-24 characters long and include at least one English letter."
#     assert registerRes3_2.json()['message'] == "Registration successful."
#     assert registerRes3_3.json()['message'] == "Password must be 8-24 characters long and include at least one English letter."
#     assert registerRes3_4.json()['message'] == "Password must be 8-24 characters long and include at least one English letter."
#     # Test Case 4 : Confirm Password Match and Unmatch
#     assert registerRes4_1.json()['message'] == "Registration successful."
#     assert registerRes4_2.json()['message'] == "Passwords do not match. Please try again."
#     # Test Case 5 : Email Form
#     assert registerRes5_1.json()['message'] == "Registration successful."
#     assert registerRes5_2.json()['message'] == "Email must be a valid email address."
#     # Test Case 6 : Phone Digit Length
#     assert registerRes6_1.json()['message'] == "Phone number must be exactly 10 digits long and contain only numbers."
#     assert registerRes6_2.json()['message'] == "Registration successful."
#     assert registerRes6_3.json()['message'] == "Phone number must be exactly 10 digits long and contain only numbers."
#     # Test Case 7 : Correct Age
#     assert registerRes7_1.json()['message'] == "Age must be a number between 0 and 120."
#     assert registerRes7_2.json()['message'] == "Registration successful."
#     assert registerRes7_3.json()['message'] == "Registration successful."
#     assert registerRes7_4.json()['message'] == "Age must be a number between 0 and 120."

# ============================================== Product API Testing ==============================================
# from database import Database

# # load mongo database
# db = Database('ApiTesting').db
# collection = db['product']
# productsFromDB = list(collection.find({}, {"_id" : 0}))


# # GET Product for showing
# productAPI = serverURL + '/product'

# productsFromAPI = requests.get(productAPI)

# def test_product():
#     assert productsFromAPI.json() == productsFromDB

# # ============================================== Cart API Testing ==============================================
# from database import Database

# # load mongo database
# db = Database('ApiTesting').db
# # load cart collection
# collection = db['cart']

# # Get Cart for showing
# showCartAPI = serverURL + '/showcart'
    
# # Test Case 1 : No "username" Argument
# noArgs_response = requests.get(showCartAPI)

# # Test Case 2 : "username" Argument Exists in DB and Cart already created
# existArgsCartCreated_response = requests.get(showCartAPI + '?username=user001')

# # Test Case 3 : "username" Argument Doesn't Exist in DB
# noExistArgs_response = requests.get(showCartAPI + '?username=noExist')

# productsInCreatedCartFromDB = collection.find_one({"username":"user001"})
# productsInNotCreatedCartFromDB = collection.find_one({"username":"admin"})

# def test_showcart():
#     assert noArgs_response.json()['error'] == "Username not provided"
#     assert noExistArgs_response.json()['error'] == "User not found"
#     assert existArgsCartCreated_response.json() == productsInCreatedCartFromDB.get('products')

# # Add Product to Cart 
# addToCartAPI = serverURL + '/cart'

# # Test Case 1 : None or Missing Input
# addProduct1 = {
#     "username": None,
#     "product": {
#         "id_product": "0002",
#         'product_name': 'Thinkpad T14', 
#         "quantity": 10,
#         'price': 1000
#     }
# }

# noneInputProduct_response = requests.post(addToCartAPI, json=addProduct1)

# # Test Case 2 : No User Exist
# addProduct2 = {
#     "username": "noExists",
#     "product": {
#         "id_product": "0002",
#         'product_name': 'Thinkpad T14', 
#         "quantity": 10,
#         'price': 1000
#     }   
# }

# noExistUserAddProduct_response = requests.post(addToCartAPI, json=addProduct2)

# # Test Case 3 : Create Cart
# addProduct3 = {
#     "username": "admin",
#     "product": {
#         "id_product": "0002",
#         'product_name': 'Thinkpad T14', 
#         "quantity": 10,
#         'price': 1000
#     }   
# }

# createCart_response = requests.post(addToCartAPI, json=addProduct3)

# # Test Case 4 : Add Product to Cart
# addProduct4 = {
#     "username": "user001",
#     "product": {
#         'id_product': '0004', 
#         'product_name': 'Iphone 15 pro', 
#         'quantity': 1, 
#         'price': 500.0
#     }
# }

# addProductToCart_response = requests.post(addToCartAPI, json=addProduct4)

# # Test Case 5 : Update Product to Cart
# addProduct5 = {
#     "username": "user001",
#     "product": {
#         "id_product": "0002",
#         'product_name': 'Thinkpad T14', 
#         "quantity": 10,
#         'price': 1000
#     }
# }

# updateProductToCart_response = requests.post(addToCartAPI, json=addProduct5)

# # Test Case 6 : Add Product that not exist in DB
# addProduct6 = {
#     "username": "user001",
#     "product": {
#         "id_product": "0006",
#         'product_name': 'Thinkpad T10', 
#         "quantity": 15,
#         'price': 1000
#     }
# }

# addNotExistProductToCart_response = requests.post(addToCartAPI, json=addProduct6)

# def test_addtocart():
#     assert noneInputProduct_response.json()['error'] == "Incomplete information not provided"
#     assert noExistUserAddProduct_response.json()['message'] == "No User Found"
#     assert createCart_response.json()['message'] == "Create Cart Success"
#     assert addProductToCart_response.json()['message'] == "Added Product to the Cart"
#     assert updateProductToCart_response.json()['message'] == "Update Cart Success"
#     assert addNotExistProductToCart_response.json()['message'] == "No Product Found"

# # Delete Product from Cart
# removeFromCartAPI = serverURL + '/deletecart'

# # Test Case 1 : None Input
# removeProduct1 = {
#     "username": "user001",
#     "id_product": None
# }

# noneInputRemove = requests.put(removeFromCartAPI, json=removeProduct1)

# # Test Case 2 : Product that want to remove Not Found
# removeProduct2 = {
#     "username": "user001",
#     "id_product": "0001"
# }

# productNotFoundRemove = requests.put(removeFromCartAPI, json=removeProduct2)

# # Test Case 3 : Remove Success
# removeProduct3 = {
#     "username": "user001",
#     "id_product": "0004"
# }

# productSuccessRemove = requests.put(removeFromCartAPI, json=removeProduct3)

# def test_deletecart():
#     assert noneInputRemove.json()['error'] == "Product ID not provided"
#     assert productNotFoundRemove.json()['error'] == "Product not found in the cart or username is incorrect"
#     assert productSuccessRemove.json()['message'] == "Product removed from cart successfully"

# ============================================== Payment API Testing ==============================================
# Calculate Cart for Discounts
calCartAPI = serverURL + '/calculatecart'

# Test Case 1 : No 'username' Argument
calCart1_response = requests.get(calCartAPI)

# Test Case 2 : User Doesn't Have Cart Yet
calCart2_response = requests.get(calCartAPI + '?username=admin')

# Test Case 3 : User Have Cart, User Get "Every 1000 Baht, User will get discount 50 baht" with BVA-2
    # Test Case 3.1 ; Price In Cart = 999 Baht
calCart3_1Response = requests.get(calCartAPI + '?username=user999')
cart3_1 = {"total_price" : 999, "total_payment": 999, "discount" : 0}

    # Test Case 3.2 ; Price In Cart = 1000 Baht
calCart3_2Response = requests.get(calCartAPI + '?username=user1000')
cart3_2 = {"total_price" : 1000, "total_payment": 950, "discount" : 50}

    # Test Case 3.3 ; Price In Cart = 1999 Baht
calCart3_3Response = requests.get(calCartAPI + '?username=user1999')
cart3_3 = {"total_price" : 1999, "total_payment": 1949, "discount" : 50}

    # Test Case 3.4 ; Price In Cart = 2000 Baht
calCart3_4Response = requests.get(calCartAPI + '?username=user2000')
cart3_4 = {"total_price" : 2000, "total_payment": 1900, "discount" : 100}

# Test Case 4 : User Have Cart, User will get "Discount 5% and Every 1000 Baht will get discount 50 baht" with BVA-2
    # Test Case 4.1 ; Price In Cart = 4999 Baht
calCart4_1Response = requests.get(calCartAPI + '?username=user5000')
cart4_1 = {"total_price" : 5000, "total_payment": 4750, "discount" : 250}

    # Test Case 4.2 ; Price In Cart = 5000 Baht
calCart4_2Response = requests.get(calCartAPI + '?username=user5001')
cart4_2 = {"total_price" : 5001, "total_payment": 4500.95, "discount" : 500.05}

    # Test Case 4.3 ; Price In Cart = 10000 Baht
calCart4_3Response = requests.get(calCartAPI + '?username=user10000')
cart4_3 = {"total_price" : 10000, "total_payment": 9000, "discount" : 1000}

def test_calculatecart():
    # Test Case 1 : No 'username' Argumentt
    assert calCart1_response.json()['error'] == "Username not provided"
    # Test Case 2 : User Doesn't Have Cart Yet
    assert calCart2_response.json()['error'] == "Cart not found for the user"
    # Test Case 3 : User Have Cart, User Get "Every 1000 Baht, User will get discount 50 baht" with BVA-2
    assert calCart3_1Response.json() == cart3_1
    assert calCart3_2Response.json() == cart3_2
    assert calCart3_3Response.json() == cart3_3
    assert calCart3_4Response.json() == cart3_4
    # Test Case 4 : User Have Cart, User will get "Discount 5% and Every 1000 Baht will get discount 50 baht" with BVA-2
    assert calCart4_1Response.json() == cart4_1
    assert calCart4_2Response.json() == cart4_2
    assert calCart4_3Response.json() == cart4_3

# Make a Payment
paymentAPI = serverURL + '/payment'

# Test Case 1 : No 'username' Argument
noArgPayment = requests.post(paymentAPI, headers={'Content-Type': 'application/json'}, json={})

# Test Case 2 : User's Cart is Empty
noCartPayment = requests.post(paymentAPI, json={"username": "userNoCart", "total_payment" : 1000})

# Test Case 3 : Payment Successfull and Order Created
addProductForPayment = {
    "username": "demoPayment",
    "product": {
        "id_product": "0002",
        'product_name': 'Thinkpad T14', 
        "quantity": 1,
        'price': 1000
    }   
}

addToCartAPI = serverURL + '/cart'
createNewOneforPayment = requests.post(addToCartAPI, json=addProductForPayment)

successPayment = requests.post(paymentAPI + '?username=demoPayment', json={"username": "demoPayment", "total_payment" : 1000})

def test_payment():
    assert noArgPayment.json()['error'] == "Username not provided"
    assert noCartPayment.json()['error'] == "Cart is empty or does not exist"
    assert successPayment.json()['message'] == "Payment successful, products updated"

# ============================================== Order History API Testing ==============================================
from database import Database
from datetime import datetime

# load mongo database
db = Database('ApiTesting').db
ordersCollection = db['orders']
ordersFromDB = ordersCollection.find_one({'username': "user001"}, {"_id": 0})

orderHistoryAPI = serverURL + '/showorder'

# Test Case 1 : No 'usernaame' Argument
noArgOrder = requests.get(orderHistoryAPI)

# Test Case 2 : No Orders Found
noOrder = requests.get(orderHistoryAPI + '?username=userNoOrder')

# Test Case 3 : Found Orders!
foundOrder = requests.get(orderHistoryAPI + '?username=user001')

def test_showorder():
    assert noArgOrder.json()['error'] == "Username not provided"
    assert noOrder.json()['message'] == 'No Orders Found'

    # Extract relevant fields for comparison
    found_order_data = foundOrder.json()['orders'][0]
    orders_db_data = ordersFromDB['orders'][0]

    # Compare fields individually
    assert found_order_data['id_order'] == orders_db_data['id_order']
    assert found_order_data['list'] == orders_db_data['list']
    assert found_order_data['total_payment'] == orders_db_data['total_payment']
    assert found_order_data['status'] == orders_db_data['status']

    # Convert the time field in foundOrder.json() to a datetime object
    found_order_time = datetime.strptime(found_order_data['time'], '%a, %d %b %Y %H:%M:%S GMT')
    found_order_data['time'] = found_order_time.strftime('%Y-%m-%d %H:%M:%S')

    # Convert orders_db_data['time'] to a string
    orders_db_data_time_str = orders_db_data['time'].strftime('%Y-%m-%d %H:%M:%S')

    # Compare the time field
    assert found_order_data['time'] == orders_db_data_time_str

# ============================================== Profile API Testing ==============================================
profileAPI = serverURL + '/profile'

# Test Case 1 : No 'username' Argument
profileNoArgRes = requests.get(profileAPI)

# Test Case 2 : No User Found
profileNoUserRes = requests.get(profileAPI + '?username=noUser')

# Test Case 3 : User Found
profileUserFoundRes = requests.get(profileAPI + '?username=user001')

def test_profile():
    assert profileNoArgRes.json()['error'] == 'Username not provided'
    assert profileNoUserRes.json()['message'] == 'error getting data user'
    assert profileUserFoundRes.status_code == 200

# =================================================================================================================