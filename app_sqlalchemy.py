from sqlalchemy import create_engine, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import DeclarativeBase, mapped_column , Mapped , sessionmaker
from typing import Dict
from fastapi import FastAPI, HTTPException,Body,Form
user='root'
password="#Nive%402003"
host='127.0.0.1'
port=3306
database="food_delivery"
engine=create_engine(url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
    user,password,host,port,database))
Session = sessionmaker(bind=engine)
session = Session()

class Base(DeclarativeBase):
    pass

app=FastAPI()

class users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer , primary_key=True , autoincrement=True )
    username: Mapped[str] =mapped_column(String(50) , unique=True)
    password: Mapped[str] = mapped_column(String(50) )

class Restaurants(Base):
    __tablename__ = "restaurants"
    id: Mapped[int] = mapped_column(Integer , primary_key=True , autoincrement=True )
    name: Mapped[str] = mapped_column(String(100) )
    address: Mapped[str] = mapped_column(String(255) )

class MenuItems(Base):
    __tablename__ = "menu_items"
    id:Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    restuarant_id: Mapped[int] = mapped_column(Integer,
                                               ForeignKey("restaurants.id" , ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(100), unique=True)
    price:Mapped[float] = mapped_column(DECIMAL(10,2))

class Orders(Base):
    __tablename__="orders"
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_id : Mapped[int] = mapped_column(Integer)
    restaurant_id : Mapped[int] = mapped_column(Integer,
                                                ForeignKey("restaurants.id" , ondelete="CASCADE"))
    total_price : Mapped[float] = mapped_column(DECIMAL(10,2))
    status : Mapped[str] = mapped_column(String(50))

class OrderItems(Base):
    __tablename__="order_items"
    id:Mapped[int] = mapped_column(Integer , primary_key=True , autoincrement= True)
    order_id : Mapped[int] =mapped_column(Integer , ForeignKey("orders.id",ondelete="CASCADE"))
    item_id : Mapped[int] =mapped_column(Integer , ForeignKey("menu_items.id",ondelete="CASCADE"))
    quantity : Mapped[int] = mapped_column(Integer)
    price : Mapped[float] = mapped_column(DECIMAL(10,2))

class Owners(Base):
    __tablename__ = "restuarant_owners"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(255))


@app.post("/user_register")
def register(username: str=Form(...), password: str=Form(...)):
    '''
    This is a post api for user registration.
    The details provided would be saved in the MySQL database.
    '''

    try:
        s='[@_!#$%^&*()<>?/\|}{~:]'  #pylint:disable=anomalous-backslash-in-string
        c=0
        for i in username:
            if i in s:
                c+=1
        if c:
            return {"message" : "Invalid username"}
        else:
            user = session.query(Owners).filter(users.username == username).first()
            if user:
                return {"message": "Username is already taken"}
            new_user = users(username= username, password= password)
            session.add(new_user)
            session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error ") from e
    return {"message": "User registered successfully"}

@app.post("/user_login")
def login(name: str=Form(...), pwd: str=Form(...)):
    '''
    This is a post api for user login.
    The details provided would be saved in the MySQL database.
    '''
    try:
        sql = session.query(users).filter(users.username==name,users.password==pwd).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error ") from e
    return {"message": "Login successful"}

@app.get("/restaurants")
def list_restaurants():
    '''
    This is a get api for retrieving the availabale list of restaurants.
    The details are fetched from the MySQL database
    '''
    try:
        sql = session.query(Restaurants)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error ") from e
    return {"restaurants": sql.all()}


@app.get("/restaurants/{id}")
def get_restaurant(restaurant_id: int):
    '''
    This is a get api for retrieving particular restaurant details.
    The details are retrieved from the MySQL database.
    '''
    try:
        sql=session.query(Restaurants).filter(Restaurants.id == restaurant_id).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error ") from e
    return {"restaurant": sql}

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
        if not menu_items:
            raise HTTPException(status_code=400, detail="Menu items list cannot be empty")
        for menu_item in menu_items:
            name = menu_item.get("name")
            price = menu_item.get("price")
            if not name or not price:
                raise HTTPException(status_code=400,
                   detail="Each menu item must have a name and price")
            new_item=MenuItems(restuarant_id=restaurant_id , name=name , price=price)
            session.add(new_item)
            session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e
    return {"message": "Menu items added/updated successfully"}

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
        customer_id = body["customer_id"]
        restaurant_id = body["restaurant_id"]
        items = body["items"]
        number_of_items=len(items)
        total_price = 0
        item_not_found = []
        new_order=Orders(customer_id = customer_id,
                         restaurant_id = restaurant_id , total_price = total_price, status = "pending")
        session.add(new_order)
        session.flush() #keeps the primary key of inserted row
        order_id=new_order.id
        session.commit()
        for item in items:
            result=session.query(MenuItems).filter(MenuItems.id == item["item_id"],
                                                   MenuItems.restuarant_id == restaurant_id).first()
            if not result:
                item_not_found.append(item["item_id"])
                continue
            price = result.price
            item_total_price = price * item["quantity"]
            total_price += item_total_price
            new=OrderItems(order_id = order_id, item_id= item["item_id"],
                           quantity=item["quantity"], price=price)
            session.add(new)
            session.commit()
            session.query(Orders).filter(Orders.id==order_id).update(
                {Orders.total_price : total_price})
            session.commit()
        if len(item_not_found)==number_of_items:
            del_order=session.query(Orders).filter(Orders.id == order_id)
            session.delete(del_order)
            session.commit()
        if len(item_not_found)==0:
            return {"message": "Order placed successfully"}
        if number_of_items==len(item_not_found):
            return {"message" : "No items found in this restaurant"}
        if number_of_items>len(item_not_found):
            return {"message": "Order placed successfully but some items not found"}
        #return {"message": "Unexpected condition encountered"}
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail="Error placing order: " + str(e)) from e


@app.get("/orders/history")
def get_order_history(customer_id : int):
    '''
    This is a get api for retrieving order history of particular customer.
    '''
    try:
        order_history=session.query(Orders).filter(Orders.customer_id == customer_id).all()
        if not order_history:
            raise HTTPException(status_code=404, detail="No orders found for this customer")
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail="Error fetching order history: "+str(e)) from e
    return {"orders": order_history}

@app.post("/owner_register")
def register_owner(username: str=Form(...), password: str=Form(...)):
    '''
    This is a post api for owner registration.
    The details provided would be saved in the MySQL database.
    '''
    try:
        s='[@_!#$%^&*()<>?/\|}{~:]'
        c=0
        for i in username:
            if i in s:
                c+=1
        if c:
            return {"message" : "Invalid username"}
        else:
            user=session.query(Owners).filter(Owners.username== username).first()
            if user:
                return {"message" : "Username is already taken"}
            owner=Owners(username = username , password = password)
            session.add(owner)
            session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error ") from e
    return {"message": "Restaurant owner registered successfully"}

@app.post("/owner_login")
def login_owner(username: str=Form(...), password: str=Form(...)):
    '''
    This is a post api for user login.
    '''
    try:
        owner=session.query(Owners).filter(Owners.username==username , Owners.password == password).first()
        if not owner:
            return {"message" : "User not found"}
    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail="Database error ") from e
    return {"message": "Login successful"}


@app.put("/orders/{order_id}/status")
def update_order_status(body: Dict):
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
        order_id = body["order_id"]
        status = body["status"]
        order=session.query(Orders).filter(Orders.id == order_id).first()
        if not order:
            return {"message" : "Order id is not found"}
        session.query(Orders).filter(Orders.id==order_id).update({ Orders.status : status})
        session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error updating order status: " + str(e)) from e
    return {"message": "Order status updated successfully"}









