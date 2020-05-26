class Router(object):
    @staticmethod
    def build(engine, app):
        """Assign all engines to Flask App routes."""

        app.add_url_rule("/post",
                         "post_page",
                         engine.index, methods=["GET"])

        return app