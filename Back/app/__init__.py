from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)

    from .routes import api
    app.register_blueprint(api)

    with app.app_context():
        from .models import Order
        db.create_all()

    return app
