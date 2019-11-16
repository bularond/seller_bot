# -*- coding: utf-8 -*-
import sqlite3

from random import getrandbits

class database:
    """
    #Database
    ## products ##
    | id  | name | description | cost |
    |:--- |:---- |:----------- |:---- |
    | int | text | text        | int  |
    ## purchases ##
    | id  | user_id | product | code |
    |:--- |:------- |:------- |:---- |
    | int | int     | int     | int  |
    ## keys ##
    | id  | product | value   |
    |:--- |:------- |:------- |
    | int | int     | text    |
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
                                            WHERE id == {id} AND count > 0"""):
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
            code = getrandbits(32)
            while(self.get_purchase_by_code(code)):
                code = getrandbits(32)
            conn.execute(f"""INSERT INTO purchases (user_id, product, code)
                             VALUES ({user_id}, {product}, {code})""")
            conn.commit()


    def get_key_by_product_id(self, product_id):
        with sqlite3.connect('database.db') as conn:
            for key in conn.execute(f"""SELECT * FROM keys 
                                        WHERE product == {product_id}"""):
                return key
            return None

    def remove_purcases_by_code(self, code):
        with sqlite3.connect('database.db') as conn:
            conn.execute(f"""DELETE FROM purchases
                             WERE code == {code}""")

if __name__ == "__main__":
    db = database()
    print(db.add_purchase(12, 21))

