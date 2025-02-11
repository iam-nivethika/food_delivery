import requests
import pytest
ENDPOINT = "http://127.0.0.1:8000"

def user_register():
    '''This function is used for user registration'''
    data = {
        "username": "bhavan",
        "password": "12345"
    }
    user_register_response = requests.post(ENDPOINT + "/user_register",
                                           data=data, timeout=10)
    return user_register_response.json()

def test_user_register_mocked(mocker):
    '''This is a mock function to test the user registrtion'''
    mock_post=mocker.patch('requests.post')
    mock_post.return_value.json.return_value= {"message": "User registered successfully"}
    result=user_register()
    assert result == mock_post.return_value.json.return_value
    assert type(result) is dict
    data = {"username": "bhavan", "password": "12345"}
    mock_post.assert_called_once_with(ENDPOINT+"/user_register",data=data,timeout=10)

def user_login():
    '''
    This function is used for user login
    '''
    data={
        "username": "nithya",
        "password" : "nith"
    }
    user_login_response = requests.post(ENDPOINT+"/user_login",
    data=data , timeout=10)
    return user_login_response.json()


def test_user_login_mocked(mocker):
    '''This is a mock function to test the user login'''
    mock_post = mocker.patch('requests.post')
    mock_post.return_value.json.return_value = {"message": "Login successful"}
    result = user_login()
    assert result == mock_post.return_value.json.return_value
    assert type(result) is dict
    data = {"username": "nithya", "password": "nith"}
    mock_post.assert_called_once_with(ENDPOINT + "/user_login", data=data, timeout=10)

def owner_register():
    '''
    This function is used for owner registration
    '''
    data={
        "username": "jake",
        "password" : "12345"
    }
    owner_register_response = requests.post(ENDPOINT+"/owner_register",
    data=data , timeout=10)
    return owner_register_response.json()

def test_owner_register_mocked(mocker):
    '''This is a mock function for owner regstration'''
    mock_post=mocker.patch('requests.post')
    mock_post.return_value.json.return_value= {"message": "Restaurant owner registered successfully"}
    result=owner_register()
    assert result == mock_post.return_value.json.return_value
    assert type(result) is dict
    data = {"username": "jake", "password": "12345"}
    mock_post.assert_called_once_with(ENDPOINT+"/owner_register",data=data,timeout=10)

def owner_login():
    '''
    This function is used for owner login
    '''
    data={
        "username": "steve",
        "password" : "st123"
    }
    owner_login_response=requests.post(ENDPOINT+"/owner_login",
    data=data , timeout=10)
    return owner_login_response.json()

def test_owner_login_mocked(mocker):
    '''This is a mock tets function for owner login'''
    mock_post = mocker.patch('requests.post')
    mock_post.return_value.json.return_value = {"message": "Login successful"}
    result = owner_login()
    assert result == mock_post.return_value.json.return_value
    assert type(result) is dict
    data = {"username": "steve", "password": "st123"}
    mock_post.assert_called_once_with(ENDPOINT + "/owner_login", data=data, timeout=10)

def list_restaurants():
    '''
    This function lists the details of all restaurants
    '''
    list_restaurant_response = requests.get(ENDPOINT+"/restaurants", timeout=10)
    return list_restaurant_response.json()

def test_list_restaurants_mocked(mocker):
    '''THis is a mock function to get restaurant details'''
    mock_get = mocker.patch('requests.get')
    response_dict = {
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
    mock_get.return_value.json.return_value = response_dict
    result = list_restaurants()
    assert result == response_dict
    assert type(result) is dict
    mock_get.assert_called_once_with(ENDPOINT+"/restaurants", timeout=10)

def get_restaurant_details():
    '''
    This function tests is uded to get particular restaurant details
    '''
    restaurant_id=2
    get_restaurant_details_response=requests.get(
        f"{ENDPOINT}/restaurants/{restaurant_id}?restaurant_id={restaurant_id}", timeout=10)
    return get_restaurant_details_response.json()

def test_get_restaurant_details_mocked(mocker):
    '''THis is a mock function to get the particular restaurant details'''
    mock_get= mocker.patch('requests.get')
    restaurant_id = 2
    response_dict = {
        "restaurant": {
            "id": 2,
            "name": "pizza hut",
            "address": "38,Whitefield,Bangalore"
        }
    }
    mock_get.return_value.json.return_value = response_dict
    result = get_restaurant_details()
    assert result == response_dict
    assert type(result) is dict
    mock_get.assert_called_once_with(f"{ENDPOINT}/restaurants/{restaurant_id}?restaurant_id={restaurant_id}", timeout=10)

def modify_menu_item():
    '''
    This function is used for adding or updating menu items
    '''
    res_id=2
    menu_items = [
        {"name": "Margherita Pizza", "price": 500},
        {"name": "Veggie Burger", "price": 350},
        {"name": "Pasta Alfredo", "price": 400}
    ]
    modify_menu_item_response=requests.post(f"{ENDPOINT}/restaurants/{res_id}/menu?restaurant_id={res_id}",
    json=menu_items, timeout=10)
    return modify_menu_item_response.json()

def test_modify_menu_item_mocked(mocker):
    '''THis is a mock function to modify the menu items'''
    mock_post=mocker.patch("requests.post")
    mock_post.return_value.json.return_value={
            "message": "Menu items added/updated successfully"
        }
    modify_menu = modify_menu_item()
    assert modify_menu == mock_post.return_value.json.return_value
    assert type(modify_menu) is dict
    res_id = 2
    menu_items = [
        {"name": "Margherita Pizza", "price": 500},
        {"name": "Veggie Burger", "price": 350},
        {"name": "Pasta Alfredo", "price": 400}
    ]
    mock_post.assert_called_once_with(f"{ENDPOINT}/restaurants/{res_id}/menu?restaurant_id={res_id}",json=menu_items,timeout=10)

def place_order():
    '''
    This function is uded to place the order
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
    return place_order_response.json()

def test_place_order(mocker):
    '''This is a mock function to test placing order'''
    mock_post=mocker.patch('requests.post')
    mock_post.return_value.json.return_value = {"message": "Order placed successfully"}
    order = place_order()
    assert order == mock_post.return_value.json.return_value
    assert type(order) is dict
    order_details = {
        "customer_id": 9,
        "restaurant_id": 3,
        "items": [
            {
                "item_id": 8,
                "quantity": 2
            },
            {
                "item_id": 9,
                "quantity": 3
            }
        ]
    }
    mock_post.assert_called_once_with(f"{ENDPOINT}/orders",json=order_details,timeout=10)

def order_history():
    '''
    This function tests is used to retriev the order history
    '''
    customer_id=15
    order_history_response = requests.get(
        f"{ENDPOINT}/orders/history?customer_id={customer_id}" , timeout=10)
    return order_history_response.json()

def test_order_history_mocked(mocker):
    '''This is a mock function to test the order hsitory'''
    mock_get = mocker.patch('requests.get')
    response_dict={
      "orders": [
        {
          "id": 40,
          "restaurant_id": 2,
          "total_price": 1650,
          "status": "pending"
        }
      ]
    }
    mock_get.return_value.json.return_value = response_dict
    history = order_history()
    assert history == response_dict
    customer_id=15
    mock_get.assert_called_once_with(f"{ENDPOINT}/orders/history?customer_id={customer_id}" , timeout=10)

def update_order_status():
    '''
    This function is used to update the order status
    '''
    order_details={
        "order_id":27,
        "status":"completed"
    }
    status_response=requests.put(
        f"{ENDPOINT}/orders/{order_details['order_id']}/status",
        json=order_details , timeout=10)
    return status_response.json()

def test_update_order_status_mocked(mocker):
    '''This is a mock function to test the updation of  order status'''
    mock_put = mocker.patch('requests.put')
    mock_put.return_value.json.return_value = {"message": "Order status updated successfully"}
    status=update_order_status()
    assert status == mock_put.return_value.json.return_value
    order_details = {
        "order_id": 27,
        "status": "completed"
    }
    mock_put.assert_called_once_with(
        f"{ENDPOINT}/orders/{order_details['order_id']}/status",
        json=order_details, timeout=10)

