from flask import Flask
from router import Router
from views import Views

application = app = Flask(__name__)

def run():
    my_views = Views()
    routed_app = Router.build(my_views, app)
    routed_app.run(debug=True)
    
if __name__ == '__main__':  
    run()