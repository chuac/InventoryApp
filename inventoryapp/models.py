from datetime import datetime
from inventoryapp import db, login_manager, bcrypt
from flask import current_app
from flask_login import UserMixin # login manager needs this


@login_manager.user_loader #login manager needs this
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable = False) # max length 20, must be unique
    email = db.Column(db.String(120), unique=True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default='default_user.jpg') # length 20 because it'll hold the hash of their image
    password = db.Column(db.String(60), nullable = False)

    def __init__(self, username, email, plaintext_password): ## new way of initialising new user in db, simplified operations in register route (https://www.patricksoftwareblog.com/testing-a-flask-application-using-pytest/)
        self.username = username
        self.email = email
        self.image_file = 'default.jpg'
        self.password = bcrypt.generate_password_hash(plaintext_password).decode('utf-8') # we now hash the passwords in here, instead of at routes.py

    def is_correct_password(self, plaintext_password): # user trying to log in, compare password stored in this User db object vs. function argument password (from the form)
        return bcrypt.check_password_hash(self.password, plaintext_password)

    def __repr__(self): #how your object is formatted when it is printed out
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    size = db.Column(db.String(100), nullable = True)
    count = db.Column(db.Float(asdecimal = True), nullable = False)
    description = db.Column(db.Text, nullable = True)
    image_file = db.Column(db.String(20), nullable = False, default='default_item.png') #length 20 because it'll hold the hash of their image
    last_updated = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f"Inventory item('{self.name}' - '{self.author.size}', count: '{self.count}')"