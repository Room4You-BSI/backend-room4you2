from flask import Flask
class Router(object):
    @staticmethod
    def build(views, app):
        
        app.add_url_rule("/posts",
                         "rooms",
                         views.rooms, methods=["GET"])

        return app