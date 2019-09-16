from flask import Flask

from .core import wx_oauth
from .views import bp


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('demo.default_settings')
    app.config.from_pyfile('application.cfg')

    wx_oauth.init_app(app)
    # views
    app.register_blueprint(bp)

    return app
