from datetime import datetime
from inventoryapp import db#, login_manager, bcrypt


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