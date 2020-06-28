from config import app
from functions import Views

view = Views()

app.add_url_rule("/", "home", view.home, methods=["GET"])

app.add_url_rule("/add_user", "register", view.register, methods=["GET", "POST"])

app.add_url_rule("/create_post", "create_post", view.create_post, methods=["GET", "POST"])

app.add_url_rule("/get_profile", "login", view.login, methods=["GET", "POST"])

app.add_url_rule("/posts", "rooms", view.rooms, methods=["GET"])

app.add_url_rule("/filter", "filter", view.filter, methods=["GET"])

if __name__ == "__main__":
    app.run(debug=True)