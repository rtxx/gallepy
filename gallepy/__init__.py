# gallepy - simple gallery made with python
# major source is from https://flask.palletsprojects.com/en/3.0.x/tutorial/
from flask import Flask, render_template
from .config import LOG


def create_app():
    LOG.info("gallepy starting!")
    app = Flask(__name__)
    app.config.from_pyfile('config.py', silent=True)

    from . import db, gallery
    db.init_app(app)
    gallery.init_app(app)

    from . import main
    app.register_blueprint(main.bp)

    register_errorhandlers(app)

    return app


# from https://github.com/jamescurtin/demo-cookiecutter-flask/blob/master/my_flask_app/app.py
def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template(f"/errors/{error_code}.html"), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
