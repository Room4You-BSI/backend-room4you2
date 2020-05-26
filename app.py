# redirect é uma biblioteca pra dar redirect e url_for pra montar urls
# o request pega informações da requisição que foi feita. request.method retorna o tipo de requisição que foi feita
# dumps é extensão de json
# abort para retornar status "abort(403)"
# render_template retorna nas rotas o documento HTML
from flask import Flask, redirect, url_for, request, abort, render_template
from json import dumps

# eu posso colocar no segundo parâmetro algo como "app = Flask(__name__, static_folder='public')"
# isso significa que a se eu tiver uma pasta chamada public com um documento html, ela vai ter as rotas locais 
# eu não preciso criar nada aqui, tipo, seu eu digitar "blabla.com/public/index.html" ele pega direto das pastas
# quando eu faço isso eu posso acessar o html tranquilamente sem ter que definir as rotas aqui. 
# application é para o aws
application = app = Flask(__name__, static_folder='public')

@app.route('/')
def helloworld():
    return 'Hello World!'

if __name__ == "__main__":
    app.run(debug=True)