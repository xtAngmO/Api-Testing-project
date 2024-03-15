import os
import requests
from dotenv import load_dotenv

load_dotenv()
serverURL = os.environ.get('server_url')

# ============================================== Add product API Testing =========================================================
addproductAPI = serverURL + '/addproduct'

# Test Case 1 : Not Input Anything
noneInput = {
    "username": None,
    "id_product": None,
    "product_name": None,
    "price": None,
    "amount": None,
    "image_path": None
}
# Test Case 2 : Username is not admin

notAdmin = {
    "username": "user",
    "id_product": "0006",
    "product_name": "Oppo A31",
    "price": 3000,
    "amount": 3,
    "image_path": "./image/0006.jpg"
}

# Test Case 3 : Not complete input

someIsNone = {
    "username": "admin",
    "id_product": "0006",
    "product_name": "Oppo A31",
    "price": None,
    "amount": 3,
    "image_path": "./image/0006.jpg"
}

# Test Case 4 : That id already exists

idAlreadyexists = {
    "username": "admin",
    "id_product": "0005",
    "product_name": "Geforce RTX 3080",
    "price": 1000,
    "amount": 187,
    "image_path": "./image/0005.jpg"
}

# Test Case 5 : Price and Amount is less or eqaul 0

less_equalZero = {
    "username": "admin",
    "id_product": "0006",
    "product_name": "Oppo A31",
    "price": -1,
    "amount": 0,
    "image_path": "./image/0006.jpg",
}

# Test Case 6 : Complete add Product form

completeFrom = {
    "username": "admin",
    "id_product": "0006",
    "product_name": "Oppo A31",
    "price": 6000,
    "amount": 3,
    "image_path": "./image/0006.jpg"
}

addproduct1 = requests.post(addproductAPI, json = noneInput)
addproduct2 = requests.post(addproductAPI, json = notAdmin)
addproduct3 = requests.post(addproductAPI, json = someIsNone)
addproduct4 = requests.post(addproductAPI, json = idAlreadyexists)
addproduct5 = requests.post(addproductAPI, json = less_equalZero)
addproduct6 = requests.post(addproductAPI, json = completeFrom)

def test_addProduct():
    # Test Case 1 : Not Input Anything
    assert addproduct1.json()['error'] == "Incomplete information not provided"
    # Test Case 2 : Username is not admin
    assert addproduct2.json()['message'] == "Admin only"
    # Test Case 3 : Not complete input
    assert addproduct3.json()['error'] == "Incomplete information not provided"
    # Test Case 4 : That id already exists
    assert addproduct4.json()['message'] == "Id_product already exists. Please choose another."
    # Test Case 5 : Price and Amount is less or eqaul 0
    assert addproduct5.json()['message'] == "Price or amount is can't less or equal 0"
    # Test Case 6 : Complete add Product form
    assert addproduct6.json()['message'] == "add product successfully"

# ============================================== Delete product API Testing =========================================================

deleteProductAPI = serverURL + '/deleteproduct'

# Test Case 1 : Not Input Anything
deleteEmpthyInput = {
    "username": None,
    "id_product": None,
}

# Test Case 2 : Not admin

otherDelete = {
    "username" : "user",
    "id_product": "0006",
}

# Test Case 3 : Product not found

ProductNotFound = {
    "username" : "admin",
    "id_product": "0007", 
}

# Test Case 4 : Complete delete 

DeleteComplete = {
    "username" : "admin",
    "id_product": "0006",
}

deleteproduct1 = requests.post(deleteProductAPI, json = deleteEmpthyInput)
deleteproduct2 = requests.post(deleteProductAPI, json = otherDelete)
deleteproduct3 = requests.post(deleteProductAPI, json = ProductNotFound)
deleteproduct4 = requests.post(deleteProductAPI, json = DeleteComplete)

def test_delete_product():
    # Test Case 1 : Not Input Anything
    assert deleteproduct1.json()['error'] == "Please fill all input to delete"
    # Test Case 3 : Product not found
    assert deleteproduct2.json()['message'] == "Admin only"
    # Test Case 3 : Product not found
    assert deleteproduct3.json()['error'] == "id product not found"
    # Test Case 4 : Complete delete 
    assert deleteproduct4.json()['message'] == "delete product successfully"


# ============================================== Add amount product API Testing =========================================================
    
AddamountAPI = serverURL + '/addamountproduct'

# Test Case 1 : No Input Anything
AddamountnoInput = {
    "username" : None,
    "id_product" : None,
    "amount" : None,
}

# Test Case 2 : Not admin add amount

NotadminAddamount = {
    "username" : "user",
    "id_product" : "0005",
    "amount" : 10,
}

# Test Case 3 : Not have a Product

NothaveProduct = {
    "username" : "admin",
    "id_product" : "0007",
    "amount" : 10,
}

# Test Case 4 : Amount less than 0

AmountLessthanZero = {
    "username" : "admin",
    "id_product" : "0005",
    "amount" : -1,
}

# Test Case 5 : Update Successfully

addAmountSuccess = {
    "username" : "admin",
    "id_product" : "0005",
    "amount" : 10,
}

addamount1 = requests.put(AddamountAPI, json = AddamountnoInput)
addamount2 = requests.put(AddamountAPI, json = NotadminAddamount)
addamount3 = requests.put(AddamountAPI, json = NothaveProduct)
addamount4 = requests.put(AddamountAPI, json = AmountLessthanZero)
addamount5 = requests.put(AddamountAPI, json = addAmountSuccess)

def test_add_amount():
    # Test Case 1 : No Input Anything
    assert addamount1.json()['error'] == "Incomplete information not provided"
    # Test Case 2 : Not admin add amount
    assert addamount2.json()['message'] == "Admin only"
    # Test Case 3 : Not have a Product
    assert addamount3.json()['error'] == "id product not found"
    # Test Case 4 : Amount less than 0
    assert addamount4.json()['error'] == "Amount can't less than or equal 0"
    # Test Case 5 : Update Successfully
    assert addamount5.json()['message'] == "edit amount product successfully"

# ============================================== Update order status API Testing =========================================================

UpdateOrderAPI = serverURL + '/updateorderstatus'

# Test Case 1 : No input Anything

noinputUpdate = {
    "username" : None,
    "id_order" : None,
    "status": None,
} 

# Test Case 2 : Id order is not exist

IdnotexistUpdate = {
    "username" : "user001",
    "id_order" : 832468,
    "status": "wait",
}

# Test Case 3 : Username doesn't exist

UsernamenotExist = {
    "username" : "user002",
    "id_order" : 832469,
    "status" : "wait",
}

# Test Case 4 : Update Complete

UpdateOrderComplete = {
    "username" : "user001",
    "id_order" : 832469,
    "status": "wait",
}

updateorder1 = requests.post(UpdateOrderAPI, json = noinputUpdate)
updateorder2 = requests.post(UpdateOrderAPI, json = IdnotexistUpdate)
updateorder3 = requests.post(UpdateOrderAPI, json = UsernamenotExist)
updateorder4 = requests.post(UpdateOrderAPI, json = UpdateOrderComplete)

def test_Update_order():
    assert updateorder1.json()['error'] == "Incomplete information not provided"
    assert updateorder2.json()['error'] == "id order not found in user"
    assert updateorder3.json()['error'] ==  "user not found"
    assert updateorder4.json()['message'] == "Order status updated successfully"

# ============================================== Show User Orders API Testing =========================================================
ShowAllOrdersAPI = serverURL + '/showallorders'

# Test Case 1 : No input Anything
noUsernameShowAllOrders = {
    "username" : None
} 

# Test Case 2 : Not admin
notAdminShowAllOrders = {
    "username" : "user001"
}

# Test Case 3 : Admin request
adminShowAllOrders = {
    "username" : "admin"
} 

showAllOrders1 = requests.get(ShowAllOrdersAPI, json=noUsernameShowAllOrders)
showAllOrders2 = requests.get(ShowAllOrdersAPI, json=notAdminShowAllOrders)
showAllOrders3 = requests.get(ShowAllOrdersAPI, json=adminShowAllOrders)

def test_showAllOrders():
    assert showAllOrders1.json()['error'] == "Username is not provided"
    assert showAllOrders2.json()['error'] == "Admin only"
    assert showAllOrders3.status_code == 200
