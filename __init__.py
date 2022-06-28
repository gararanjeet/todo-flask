from flask import Flask
from .extensions import db, ma
from .routes.main import main
import os

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")

    db.init_app(app)

    ma.init_app(app)

    app.register_blueprint(main)

    return app