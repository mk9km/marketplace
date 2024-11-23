from flask import Flask
# from flask_session import Session

from marketplace.api import blueprint
from marketplace.models import db, migration


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    db.init_app(app)
    migration.init_app(app, db)

    # Session(app)

    app.register_blueprint(blueprint, url_prefix='/api')

    return app
