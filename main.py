from config import app
from functions import Views

view = Views()

app.add_url_rule("/", "home", view.home, methods=["GET"])

app.add_url_rule("/add_user", "register", view.register, methods=["GET", "POST"])

app.add_url_rule("/create_post", "create_post", view.create_post, methods=["GET", "POST"])

app.add_url_rule("/get_profile", "login", view.login, methods=["GET", "POST"])

app.add_url_rule("/posts", "rooms_list", view.rooms_list, methods=["GET"])

app.add_url_rule("/posts/<int:id>", "rooms_detail", view.rooms_detail, methods=["GET"])

app.add_url_rule("/post_author/<int:id>", "post_author", view.post_author, methods=["GET"])

app.add_url_rule("/search", "search", view.search, methods=["GET"])

app.add_url_rule("/add_as_favorite/<int:post_id>", "add_as_favorite", view.add_as_favorite, methods=["GET", "POST"])

app.add_url_rule("/remove_favorite/<int:id_post>", "remove_favorite", view.remove_favorite, methods=["GET", "POST"])

app.add_url_rule("/upload-photo", "upload_photo", view.upload_photo, methods=["GET", "POST"])

app.add_url_rule("/upload-photo-list", "upload_photo_list", view.upload_photo_list, methods=["GET", "POST"])

app.add_url_rule("/favorite_list", "favorite_list", view.favorite_list, methods=["GET"])

app.add_url_rule("/my_posts_list", "my_posts_list", view.my_posts_list, methods=["GET"])

if __name__ == "__main__":
    app.run(debug=True)