# -*- coding: utf-8 -*-
import sqlite3

class database:

    def get_catalog(self, offset=0, count=10):
        with sqlite3.connect('database.db') as cur:
            out = []
            for item in cur.execute(f"""SELECT * FROM products
                                             ORDER BY id
                                             LIMIT {count} OFFSET {offset}"""):
                out.append(item)
            return out

    def get_product_by_id(self, id):
        with sqlite3.connect('database.db') as cur:
            for item in cur.execute(f"""SELECT * FROM products WHERE id == {id}"""):
                return item
