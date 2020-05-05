from flask import Flask #import flask library that we installed.
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
#from flask_redis import FlaskRedis


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
#redis_store = FlaskRedis()


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class) # from config.py

    db.init_app(app)
    migrate.init_app(app, db)
    #redis_store.init_app(app)

    from inventoryapp.main.routes import main
    from inventoryapp.inventory.routes import inven as inventory

    app.register_blueprint(main)
    app.register_blueprint(inventory)


    return app