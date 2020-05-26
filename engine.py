# redirect é uma biblioteca pra dar redirect e url_for pra montar urls
# o request pega informações da requisição que foi feita. request.method retorna o tipo de requisição que foi feita
# dumps é extensão de json
# abort para retornar status "abort(403)"
# render_template retorna nas rotas o documento HTML
from flask import Flask, redirect, url_for, request, abort, render_template
from json import dumps

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


class Engine(object):
    
    # retornar posts
    def post_page(self):
        """Return welcome message and the latest git commit hash."""
        return 'ok'