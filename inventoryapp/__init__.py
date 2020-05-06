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
login_manager.login_view = 'users.login' # the 'login' here is the function of our login route, in our users blueprint. send visitors there when they hit a login_required and are not logged in
login_manager.login_message_category = 'info' #  Bootstrap for the "Login required" message
#redis_store = FlaskRedis()


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class) # from config.py

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    #redis_store.init_app(app)

    from inventoryapp.main.routes import main
    from inventoryapp.inventory.routes import inven as inventory
    from inventoryapp.users.routes import users

    app.register_blueprint(main)
    app.register_blueprint(inventory)
    app.register_blueprint(users)


    return app