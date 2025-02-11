'''
This file is about testsing the api calls that have created in main.py file
Testing using pytest framework and requests library
'''

import pytest
import requests
from database import get_connection

def test_db_connection():
    '''
    This function tests the db connectivity
    '''
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT DATABASE()")
            print("Connected to database:", cursor.fetchone())
    finally:
        connection.close()

ENDPOINT = "http://127.0.0.1:8000"


def test_user_register():
    '''
    This function tests whether user registration is working properly
    '''
    data={
        "username": "bhavana",
        "password" : "12345"
    }
    user_register_response = requests.post(ENDPOINT+"/user_register",
    data=data , timeout=10)
    assert user_register_response.status_code == 200



def test_user_login():
    '''
    This function tests whether user login is working properly
    '''
    data={
        "username": "nithya",
        "password" : "nith"
    }
    user_login_response = requests.post(ENDPOINT+"/user_login",
    data=data , timeout=10)
    assert user_login_response.status_code == 200


def test_owner_register():
    '''
    This function tests whether owner registration is working properly
    '''
    data={
        "username": "jack",
        "password" : "12345"
    }
    owner_register_response = requests.post(ENDPOINT+"/owner_register",
    data=data , timeout=10)
    assert owner_register_response.status_code==200

#sample comment
def test_owner_login():
    '''
    This function tests whether owner login is working properly
    '''
    data={
        "username": "steve",
        "password" : "st123"
    }
    owner_login_response=requests.post(ENDPOINT+"/owner_login",
    data=data , timeout=10)
    assert owner_login_response.status_code==200


def test_list_restaurants():
    '''
    This function tests whether the 
    list of restaurants is retrieved and displayed properly
    '''
    list_restaurant_response = requests.get(ENDPOINT+"/restaurants", timeout=10)
    assert list_restaurant_response.status_code==200
    response_data=list_restaurant_response.json()
    assert "restaurants" in response_data, "'restaurant' field is missing in the response"
    restaurants_data = response_data["restaurants"]
    assert isinstance(restaurants_data, list), "'restaurants' should be a list"
    assert len(restaurants_data) > 0, "'restaurants' list should not be empty"
    assert isinstance(restaurants_data, list), "Restaurants entry should be a list"
    for restaurant in restaurants_data:
        assert isinstance(restaurant, dict), "Each restaurant should be dict"
        assert len(restaurant) == 3, "Each restaurant entry should have 3 elements"
        assert isinstance(restaurant['id'], int), "'id' should be an integer"
        assert isinstance(restaurant['name'], str), "'name' should be a string"
        assert isinstance(restaurant['address'], str), "'address' should be a string"
    print("All restaurants details:", restaurants_data)
    print("Restaurant list received successfully:", response_data)


def test_get_restaurant_details():
    '''
    This function tests whether the details of particular restaurant
    is retrieved and displayed properly
    '''
    restaurant_id=2
    get_restaurant_details_response=requests.get(
        f"{ENDPOINT}/restaurants/{restaurant_id}?restaurant_id={restaurant_id}", timeout=10)
    assert get_restaurant_details_response.status_code==200
    print(get_restaurant_details_response.text)
    response_detail=get_restaurant_details_response.json()
    assert "restaurant" in response_detail, "restaurant is not found"
    restaurant_data=response_detail["restaurant"]
    assert isinstance(restaurant_data, dict), "restaurant should be dict"
    assert len(restaurant_data) == 3, "restaurant should have 3 elements"
    assert isinstance(restaurant_data['id'], int), "'id' should be an integer"
    assert isinstance(restaurant_data['name'], str), "'name' should be a string"
    assert isinstance(restaurant_data['address'], str), "'address' should be a string"
    print("restaurant details:",restaurant_data)



def test_modify_menu_item():
    '''
    This function tests for adding or updating menu items
    '''
    res_id=2
    menu_items = [
        {"name": "Margherita Pizza", "price": 500},
        {"name": "Veggie Burger", "price": 350},
        {"name": "Pasta Alfredo", "price": 400}
    ]
    modify_menu_item_response=requests.post(f"{ENDPOINT}/restaurants/{res_id}/menu?restaurant_id={res_id}",
    json=menu_items, timeout=10)
    assert modify_menu_item_response.status_code==200



def test_place_order():
    '''
    This function tests whether the order is placed successfully
    '''
    order_details={
        "customer_id":9,
        "restaurant_id":3,
        "items":[
            {
            "item_id":8,
            "quantity":2
            },
            {
            "item_id":9,
            "quantity":3
            }
        ]
    }
    place_order_response=requests.post(f"{ENDPOINT}/orders",
    json=order_details, timeout=10)
    assert place_order_response.status_code==200



def test_order_history():
    '''
    This function tests whether the order history is retrieved successfully
    '''
    customer_id=9
    test_order_history_response = requests.get(
        f"{ENDPOINT}/orders/history?customer_id={customer_id}" , timeout=10)
    assert test_order_history_response.status_code==200
    history_data = test_order_history_response.json()
    assert "orders" in history_data,"Orders not found"
    order_history=history_data["orders"]
    assert isinstance(order_history,list),"Order history should be in a list"
    for item in order_history:
        assert isinstance(item,dict),"Each order should be represented as a dict"
        assert len(item)==4,"Each order should contain 4 fields"
        assert isinstance(item["id"],int),"id should be a integer"
        assert isinstance(item["restaurant_id"],int),"restaurant_id should be a integer"
        assert isinstance(item["total_price"],float),"total_price should be float"
        assert isinstance(item["status"],str),"status should be a string"



def test_update_order_status():
    '''
    This function tests whether the status of the order is updated properly
    '''
    order_details={
        "order_id":23,
        "status":"completed"
    }
    status_response=requests.put(
        f"{ENDPOINT}/orders/{order_details['order_id']}/status",
        json=order_details , timeout=10)
    assert status_response.status_code==200
