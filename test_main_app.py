import pytest
import main_app

from fastapi import HTTPException

def test_valid_user_register():
    username="xavier"
    password="12345"
    assert isinstance(username,str),"Username should be a string"
    assert isinstance(password,str),"Password should be a string"
    assert main_app.register(username,password) == {"message": "User registered successfully"}

def test_user_register_httpex():
    username="pawan"
    password="pa123"
    assert isinstance(username,str),"Username should be a string"
    assert isinstance(password,str),"Password should be a string"
    with pytest.raises(HTTPException) as exc_info:
        main_app.register(username,password)
    assert isinstance(exc_info.value, HTTPException)
    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Database error "

def test_invalid_username():
    username="paw/an"
    password="pa123"
    assert isinstance(username,str),"Username should be a string"
    assert isinstance(password,str),"Password should be a string"
    assert main_app.register(username,password) == {"message": "Invalid username"}

def test_valid_user_login():
    username="saravana"
    password="sh123"
    assert isinstance(username,str),"Username should be a string"
    assert isinstance(password,str),"Password should be a string"
    assert main_app.login(username,password) == {"message": "Login successful"}

def test_invalid_user_login():
    username="adfhrr"
    password="dgshr"
    assert isinstance(username,str),"Username should be a string"
    assert isinstance(password,str),"Password should be a string"
    with pytest.raises(HTTPException) as exc_info:
        main_app.login(username,password)
    assert isinstance(exc_info.value, HTTPException)
    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Database error "

def test_restaurant_list():
    response_dict={
        "restaurants": [
            {
            "id": 1,
            "name": "dominos",
            "address": "123,HSR Layout,Bangalore"
            },
            {
            "id": 2,
            "name": "pizza hut",
            "address": "38,Whitefield,Bangalore"
            },
            {
            "id": 3,
            "name": "A2B",
            "address": "T.Nagar,Chennai"
            }
        ]
        }
    assert main_app.list_restaurants() == response_dict

def test_restaurant_details():
    res_id=2
    assert isinstance(res_id,int),"Restaurant id should be a integer"
    response_dict={
        "restaurant": {
            "id": 2,
            "name": "pizza hut",
            "address": "38,Whitefield,Bangalore"
        }
        }
    assert main_app.get_restaurant(2) == response_dict

def test_invalid_restaurant_details():
    res_id=5
    assert isinstance(res_id,int),"Restaurant id should be a integer"
    with pytest.raises(HTTPException) as exc_info:
        main_app.get_restaurant(5)
        assert isinstance(exc_info.value, HTTPException)
        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Database error "

def test_update_menu():
    res_id=2
    menu_items= [
            {"name": "Margherita Pizza", "price": 400},
            {"name": "Veggie Burger", "price": 200},
            {"name": "Pasta Alfredo", "price": 400}
        ]
    assert isinstance(res_id,int),"Restaurant id should be a integer"
    assert isinstance(menu_items,list),"Menu items should be a list"
    for i in menu_items:
        assert isinstance(i,dict),"item details should be a dict"
    assert main_app.add_or_update_menu_items(res_id, menu_items) == {"message": "Menu items added/updated successfully"}

def test_update_empty_menu():
    res_id=2
    menu_items=[]
    assert isinstance(res_id,int),"Restaurant id should be a integer"
    assert isinstance(menu_items,list),"Menu items should be a list"
    for i in menu_items:
        assert isinstance(i,dict),"item details should be a dict"
    with pytest.raises(HTTPException) as exc_info:
        main_app.add_or_update_menu_items(res_id, menu_items)
        assert isinstance(exc_info.value, HTTPException)
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail=="Menu items list cannot be empty"

def test_update_invalid_menu():
    res_id=2
    menu_items=[
        {"name":"" , "price":100},
        {"name": "Margherita Pizza", "price":""}
    ]
    assert isinstance(res_id,int),"Restaurant id should be a integer"
    assert isinstance(menu_items,list),"Menu items should be a list"
    for i in menu_items:
        assert isinstance(i,dict),"item details should be a dict"
    with pytest.raises(HTTPException) as exc_info:
        main_app.add_or_update_menu_items(res_id, menu_items)
        assert isinstance(exc_info.value, HTTPException)
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail=="Each menu item must have a name and price"

    
def test_order_details():
    order_details={
        "customer_id":29,
        "restaurant_id":2,
        "items":[
            {
            "item_id":10,
            "quantity":2
            },
            {
            "item_id":11,
            "quantity":3
            }
        ]
    }
    assert "customer_id" in order_details, "Order details must contain customer id"
    assert "restaurant_id" in order_details, "Order details must contain restaurant id"
    assert "items" in order_details, "Order details must contain items"
    assert isinstance(order_details["customer_id"],int),"Customer id should be a integer"
    assert isinstance(order_details["restaurant_id"],int),"Restaurant id should be a integer"
    assert isinstance(order_details["items"],list),"Items should be a list"
    for i in order_details["items"]:
        assert isinstance(i,dict),"item details should be a dict"
        assert "item_id" in i, "Each item must have an item id"
        assert "quantity" in i, "Each item must have a quantity"
        assert isinstance(i["item_id"],int),"Item id should be a integer"
        assert isinstance(i["quantity"],int),"Quantity should be a integer"
    assert main_app.place_order(order_details) == {"message": "Order placed successfully"}

def test_order_invalid_items():
    order_details={
        "customer_id":29,
        "restaurant_id":2,
        "items":[
            {
            "item_id":4,
            "quantity":2
            },
            {
            "item_id":5,
            "quantity":3
            }
        ]
    }
    assert "customer_id" in order_details, "Order details must contain customer id"
    assert "restaurant_id" in order_details, "Order details must contain restaurant id"
    assert "items" in order_details, "Order details must contain items"
    assert isinstance(order_details["customer_id"],int),"Customer id should be a integer"
    assert isinstance(order_details["restaurant_id"],int),"Restaurant id should be a integer"
    assert isinstance(order_details["items"],list),"Items should be a list"
    for i in order_details["items"]:
        assert isinstance(i,dict),"item details should be a dict"
        assert "item_id" in i, "Each item must have an item id"
        assert "quantity" in i, "Each item must have a quantity"
        assert isinstance(i["item_id"],int),"Item id should be a integer"
        assert isinstance(i["quantity"],int),"Quantity should be a integer"
    assert main_app.place_order(order_details)=={"message" : "No items found in this restaurant"}

def test_order_with_missing_items():
    order_details={
        "customer_id":29,
        "restaurant_id":2,
        "items":[
            {
            "item_id":11,
            "quantity":2
            },
            {
            "item_id":5,
            "quantity":3
            }
        ]
    }
    assert "customer_id" in order_details, "Order details must contain customer id"
    assert "restaurant_id" in order_details, "Order details must contain restaurant id"
    assert "items" in order_details, "Order details must contain items"
    assert isinstance(order_details["customer_id"],int),"Customer id should be a integer"
    assert isinstance(order_details["restaurant_id"],int),"Restaurant id should be a integer"
    assert isinstance(order_details["items"],list),"Items should be a list"
    for i in order_details["items"]:
        assert isinstance(i,dict),"item details should be a dict"
        assert "item_id" in i, "Each item must have an item id"
        assert "quantity" in i, "Each item must have a quantity"
        assert isinstance(i["item_id"],int),"Item id should be a integer"
        assert isinstance(i["quantity"],int),"Quantity should be a integer"
    assert main_app.place_order(order_details)=={"message": "Order placed successfully but some items not found"}

def test_order_history():
    customer_id=15
    assert isinstance(customer_id,int),"Customer id should be a integer"
    customer_orders={
    "orders": [
        {
        "id": 40,
        "restaurant_id": 2,
        "total_price": 1650,
        "status": "pending"
        }
    ]
    }
    assert main_app.get_order_history(customer_id) == customer_orders

def test_no_order_history():
    customer_id=22
    assert isinstance(customer_id,int),"Customer id should be a integer"
    with pytest.raises(HTTPException) as exc_info:
        main_app.get_order_history(customer_id)
        assert isinstance(exc_info.value, HTTPException)
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "No orders found for this customer"
        
def test_valid_owner_register():
    username="neha"
    password="123"
    assert isinstance(username,str),"Username should be a string"
    assert isinstance(password,str),"Password should be a string"
    assert main_app.register_owner(username,password) == {"message": "Restaurant owner registered successfully"}

def test_owner_register_httpex():
    username="cibi"
    password="12345"
    assert isinstance(username,str),"Username should be a string"
    assert isinstance(password,str),"Password should be a string"
    with pytest.raises(HTTPException) as exc_info:
        main_app.register_owner(username,password)
    assert isinstance(exc_info.value, HTTPException)
    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Database error "

def test_invalid_owner_username():
    username="paw/an"
    password="pa123"
    assert isinstance(username,str),"Username should be a string"
    assert isinstance(password,str),"Password should be a string"
    assert main_app.register_owner(username,password) == {"message": "Invalid username"}

def test_valid_owner_login():
    username="sanjay"
    password="sa123"
    assert isinstance(username,str),"Username should be a string"
    assert isinstance(password,str),"Password should be a string"
    assert main_app.login_owner(username,password) == {"message": "Login successful"}

def test_invalid_owner_login():
    username="adfhrr"
    password="dgshr"
    assert isinstance(username,str),"Username should be a string"
    assert isinstance(password,str),"Password should be a string"
    with pytest.raises(HTTPException) as exc_info:
        main_app.login_owner(username,password)
    assert isinstance(exc_info.value, HTTPException)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid credentials"


def test_update_status():
    details={
    "order_id" : 18,
    "status" : "completed"
    }
    assert isinstance(details,dict),"Details should be a dictionary"
    assert isinstance(details["order_id"],int),"order id should be a int"
    assert isinstance(details["status"],str),"status should be a string"

    assert main_app.update_order_status(details) == {"message": "Order status updated successfully"}
    

def test_invalid_update_status():
    details={
    "order_id" : 4,
    "status" : "completed"
    }
    assert isinstance(details,dict),"Details should be a dictionary"
    assert isinstance(details["order_id"],int),"order id should be a int"
    assert isinstance(details["status"],str),"status should be a string"
    with pytest.raises(HTTPException) as exc_info:
        main_app.update_order_status(details)
        assert isinstance(exc_info.value, HTTPException)
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Order not found"
    
    