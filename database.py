# -*- coding: utf-8 -*-
import sqlite3

from random import randint
from time import time

class database:
    """
    #Database
    ## products ##
    | id  | name | description | cost |
    |:--- |:---- |:----------- |:---- |
    | int | text | text        | int  |
    ## purchases ##
    | id  | user_id | product | code | datetime |
    |:--- |:------- |:------- |:---- |:-------- |
    | int | int     | int     | int  | int      |
    ## keys ##
    | id  | product | key  |
    |:--- |:------- |:---- |
    | int | int     | text |
    ## users_keys ##
    | id  | key  | user_id | datetime |
    |:--- |:---- |:------- |:-------- |
    | int | text | int     | int      |
    """


    def get_catalog(self, offset=0, count=10):
        with sqlite3.connect('database.db') as conn:
            out = []
            for item in conn.execute(f"""SELECT * FROM products
                                        ORDER BY id
                                        LIMIT {count} OFFSET {offset}"""):
                out.append(item)
            return out


    def get_product_by_id(self, id):
        with sqlite3.connect('database.db') as conn:
            for product in conn.execute(f"""SELECT * FROM products 
                                            WHERE id == {id}"""):
                return product 
            return None


    def get_purchase_by_code(self, code):
        with sqlite3.connect('database.db') as conn:
            for purchase in conn.execute(f"""SELECT * FROM purchases 
                                             WHERE code == {code}"""):
                return purchase  
            return None


    def add_purchase(self, user_id, product):
        with sqlite3.connect('database.db') as conn:
            code = randint(10000, 99999)
            while(self.get_purchase_by_code(code)):
                code = randint(10000, 99999)
            conn.execute(f"""INSERT INTO purchases (user_id, product, code, datetime)
                             VALUES ({user_id}, {product}, {code}, {time()})""")
            conn.commit()
            return code


    def get_key_by_product_id(self, product_id):
        with sqlite3.connect('database.db') as conn:
            for key in conn.execute(f"""SELECT * FROM keys 
                                        WHERE product == {product_id}"""):
                return key
            return None


    def remove_purcases_by_code(self, code):
        with sqlite3.connect('database.db') as conn:
            conn.execute(f"""DELETE FROM purchases
                             WHERE code == {code}""")
            conn.commit()


    def remove_key(self, key):
        with sqlite3.connect('database.db') as conn:
            conn.execute(f"""DELETE FROM keys
                             WHERE key == {key}""")
            conn.commit()


    def add_key_to_user(self, key, user_id):
        with sqlite3.connect('database.db') as conn:
            conn.execute(f"""INSERT INTO users_keys (key, user_id, datetime)\
                             VALUES ({key}, {user_id}, {time()})""")
            conn.commit()


    def get_users_keys(self, user_id):
        with sqlite3.connect('database.db') as conn:
            users_keys = []
            for user_key in conn.execute(f"""SELECT * FROM users_keys
                                            WHERE user_id == {user_id}"""):
                users_keys.append(user_key)
            return users_keys


if __name__ == "__main__":
    db = database()
    db.remove_key("123123")

