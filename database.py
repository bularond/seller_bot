# -*- coding: utf-8 -*-

class database:

    ls = [
        {
            'id': 0,
            'name': 'A',
            'cost': 100,
            'description': 'aaaaa'
        },
        {
            'id': 1,
            'name': 'B',
            'cost': 110,
            'description': 'bbbbb'
        },
        {
            'id': 2,
            'name': 'C',
            'cost': 120,
            'description': 'ccccc'
        },
        {
            'id': 3,
            'name': 'D',
            'cost': 130,
            'description': 'ddddd'
        },
        {
            'id': 4,
            'name': 'E',
            'cost': 140,
            'description': 'eeeee'
        },
        {
            'id': 5,
            'name': 'F',
            'cost': 150,
            'description': 'fffff'
        }
    ]
    
    def __init__(self):
        pass

    def get_catalog(self, count=10, offset=0):
        return self.ls[offset:offset+count] 

    def get_item_by_id(self, id):
        return self.ls[id]
