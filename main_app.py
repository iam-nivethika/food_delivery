'''
In this project, various API's were created for food delivery
application using FastAPI
'''
from typing import Dict
from fastapi import FastAPI, HTTPException,Body,Form
import pymysql
from database import get_connection

#Creating object for FastApi class
app = FastAPI()


@app.post("/user_register")
def register(username: str=Form(...), password: str=Form(...)):
    '''
    This is a post api for user registration.
    The details provided would be saved in the MySQL database.
    '''
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            s='[@_!#$%^&*()<>?/\|}{~:]'
            c=0
            for i in username:
                if i in s:
                    c+=1
            if c:
                return {"message" : "Invalid username"}
            else:
                query="SELECT * from users where username=%s"
                user=cursor.execute(query,(username,))
                if user:
                    return {"message" : "Username is already taken"}
                sql_insert = "INSERT INTO users (username, password) VALUES (%s, %s)"
                cursor.execute(sql_insert, (username, password))
                connection.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error ") from e
    finally:
        connection.close()
    return {"message": "User registered successfully"}


@app.post("/user_login")
def login(username: str=Form(...), password: str=Form(...)):
    '''
    This is a post api for user login.
    The details provided would be saved in the MySQL database.
    '''
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(sql, (username, password))
            user=cursor.fetchone()
            if not user:
                raise HTTPException(status_code=401, detail="Unauthorized access")
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Database error ") from e
    finally:
        connection.close()
    return {"message": "Login successful"}


@app.get("/restaurants")
def list_restaurants():
    '''
    This is a get api for retrieving the availabale list of restaurants.
    The details are fetched from the MySQL database
    '''
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM restaurants"
            cursor.execute(sql)
            restaurants = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error ") from e
    finally:
        connection.close()
    return {"restaurants": restaurants}


@app.get("/restaurants/{id}")
def get_restaurant(restaurant_id: int):
    '''
    This is a get api for retrieving particular restaurant details.
    The details are retrieved from the MySQL database.
    '''
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM restaurants WHERE id = %s"
            cursor.execute(sql, (restaurant_id,))
            restaurant = cursor.fetchone()
            if not restaurant:
                raise HTTPException(status_code=404, detail="Restaurant not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error ") from e
    finally:
        connection.close()
    return {"restaurant": restaurant}


@app.post("/restaurants/{id}/menu")
def add_or_update_menu_items(restaurant_id: int, menu_items: list = Body(...)):
    '''
    This is a post api for adding or updating a menu item for a specific restaurant.
    The details provided would be saved in the MySQL database.

    Request body example format
        [
        {
        "name": "Red sauce pasta",
        "price" : 400
        },
        {
        "name" : "White sauce pasta",
        "price" : 400
        }
        ]
    '''
    try:
        connection = get_connection()
        if not menu_items:
            raise HTTPException(status_code=400, detail="Menu items list cannot be empty")
        cursor = connection.cursor()
        for menu_item in menu_items:
            name = menu_item.get("name")
            price = menu_item.get("price")
            if not name or not price:
                raise HTTPException(status_code=400, 
                   detail="Each menu item must have a name and price") 
            query = """
                INSERT INTO menu_items (restuarant_id, name, price)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                price = VALUES(price)
            """
            cursor.execute(query, (restaurant_id, name, price))
        connection.commit()
        cursor.close()
        return {"message": "Menu items added/updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e
    finally:
        connection.close()

@app.post("/orders")
def place_order(body: Dict):
    '''
    This is a post api for making orders.
    The details provided would be saved in the MySQL database.

    Request body example format
    {
        "customer_id":2,
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
    '''
    try:
        connection = get_connection()
        cursor = connection.cursor()
        customer_id = body["customer_id"]
        restaurant_id = body["restaurant_id"]
        items = body["items"]
        number_of_items=len(items)
        total_price = 0
        item_not_found = []
        cursor.execute("""
                INSERT INTO orders (customer_id, restaurant_id, total_price, status) 
                VALUES (%s, %s, %s, %s)
            """,(customer_id, restaurant_id, total_price, 'pending'))
        order_id = cursor.lastrowid
        for item in items:
            cursor.execute("SELECT price FROM menu_items WHERE id = %s and restuarant_id=%s",
             (item["item_id"],restaurant_id)) 
            result = cursor.fetchone()
            if not result:
                item_not_found.append(item["item_id"])
                continue
            price = result["price"]
            item_total_price = price * item["quantity"]
            total_price += item_total_price
            cursor.execute("""
                INSERT INTO order_items (order_id, item_id, quantity, price) 
                VALUES (%s, %s, %s, %s)
                """, (order_id, item["item_id"], item["quantity"], price))
            cursor.execute("UPDATE orders SET total_price=%s WHERE id = %s",(total_price,order_id))
        if len(item_not_found)==number_of_items:
            cursor.execute("DELETE FROM orders where id=%s",(order_id,))
        connection.commit()
        cursor.close()
        if len(item_not_found)==0:
            return {"message": "Order placed successfully"}
        if number_of_items==len(item_not_found):
            return {"message" : "No items found in this restaurant"}
        if number_of_items>len(item_not_found):
            return {"message": "Order placed successfully but some items not found"} 
        #return {"message": "Unexpected condition encountered"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail="Error placing order: " + str(e)) from e
    finally:
        connection.close()

@app.get("/orders/history")
def get_order_history(customer_id : int):
    '''
    This is a get api for retrieving order history of particular customer.
    '''
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, restaurant_id, total_price, status 
            FROM orders 
            WHERE customer_id = %s""", (customer_id,))
        orders = cursor.fetchall()
        if not orders:
            raise HTTPException(status_code=404, detail="No orders found for this customer")
        cursor.close()
        return {"orders": orders}
    except Exception as e:
        raise HTTPException(status_code=500,detail="Error fetching order history: "+str(e)) from e
    finally:
        connection.close()

@app.post("/owner_register")
def register_owner(username: str=Form(...), password: str=Form(...)):
    '''
    This is a post api for owner registration.
    The details provided would be saved in the MySQL database.
    '''
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            s='[@_!#$%^&*()<>?/\|}{~:]'
            c=0
            for i in username:
                if i in s:
                    c+=1
            if c:
                return {"message" : "Invalid username"}
            else:
                sql_insert = "INSERT INTO restuarant_owners (username, password) VALUES (%s, %s)"
                cursor.execute(sql_insert, (username, password))
                connection.commit()
    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail="Database error ") from e
    finally:
        connection.close()
    return {"message": "Restaurant owner registered successfully"}


@app.post("/owner_login")
def login_owner(username: str=Form(...), password: str=Form(...)):
    '''
    This is a post api for user login.
    '''
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM restuarant_owners WHERE username = %s AND password = %s"
            cursor.execute(sql, (username, password))
            owner = cursor.fetchone()
            if not owner:
                raise HTTPException(status_code=401, detail="Invalid credentials")
    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail="Database error ") from e
    finally:
        connection.close()
    return {"message": "Login successful"}


@app.put("/orders/{order_id}/status")
def update_order_status(body : Dict):
    '''
    This is a put api for updating status of the order.
    The details provided would be saved in the MySQL database.
    
    Request body sample
    {
    "order_id" : 23,
    "status" : "completed"
    }
    '''
    try:
        connection = get_connection()
        cursor = connection.cursor()
        order_id = body["order_id"]
        status = body["status"]
        cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
        order = cursor.fetchone()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        cursor.execute("UPDATE orders SET status = %s WHERE id = %s", (status, order_id))
        connection.commit()
        cursor.close()
        return {"message": "Order status updated successfully"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail="Error updating order status: " + str(e)) from e
    finally:
        connection.close()
