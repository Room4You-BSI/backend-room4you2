from json import dumps
from flask import Response

# informações sobre os posts
posts = [
    { 
        'title': 'Quarto São Carlos',
        'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        'image': '',
        'price': 10,
        'rate': 50,
        'distance': '4,0 km do centro',
        'favorite': False,
        'attributesColumn1': 'OfferCardColumnItemModel[]',
        'attributesColumn2': 'OfferCardColumnItemModel[]'
    },
    {
        'title': 'Quarto Rodoviária',
        'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        'image': '',
        'price': 10,
        'rate': 50,
        'distance': '4,0 km do centro',
        'favorite': False,
        'attributesColumn1': 'OfferCardColumnItemModel[]',
        'attributesColumn2': 'OfferCardColumnItemModel[]'
    },
    {
        'title': 'Quarto Embaré',
        'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        'image': '',
        'price': 10,
        'rate': 50,
        'distance': '4,0 km do centro',
        'favorite': False,
        'attributesColumn1': 'OfferCardColumnItemModel[]',
        'attributesColumn2': 'OfferCardColumnItemModel[]'
    }
]


class Views(object):
    
    # retornar posts
    def rooms(self):
        return Response(dumps(posts), status=200, mimetype="application/json")

