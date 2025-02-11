'''This file is about database connection'''
import pymysql.cursors

def get_connection():
    '''This function is about connecting with mysql database'''
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="#Nive@2003",
        database="food_delivery",
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection
#sample
