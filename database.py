# -*- coding: utf-8 -*-

class database:

    ls = [
        {
            'name': 'A',
            'cost': 100,
            'description': 'aaaaa'
        },
        {
            'name': 'B',
            'cost': 110,
            'description': 'bbbbb'
        },
        {
            'name': 'C',
            'cost': 120,
            'description': 'ccccc'
        },
        {
            'name': 'D',
            'cost': 130,
            'description': 'ddddd'
        },
        {
            'name': 'E',
            'cost': 140,
            'description': 'eeeee'
        },
        {
            'name': 'F',
            'cost': 150,
            'description': 'fffff'
        }
    ]
    
    def __init__(self):
        pass

    def get_catalog(self, count=10, offset=0):
        return self.ls[offset:offset+count] 
