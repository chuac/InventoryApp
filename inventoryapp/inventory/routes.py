from datetime import datetime
from decimal import *
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from inventoryapp import db
from inventoryapp.models import Inventory
from inventoryapp.inventory.forms import InventoryForm

inven = Blueprint('inventory', __name__) # pass in the name of our blueprint too: "inventory". set it to "inven" here so no collisions


i = [
    {
        'id': '1',
        'name': 'Milk',
        'count': '2',
        'size': '2L'
    },
    {
        'id': '2',
        'name': 'Chocolate',
        'count': '12',
        'size': '70g'
    }
]

@inven.route('/inventory')
def inventory():

    all_inventory = Inventory.query.order_by(Inventory.last_updated).all()

    return render_template('inventory.html', inventory = all_inventory, i=i)


@inven.route('/inventory/new', methods=['GET', 'POST'])
def new_inventory():
    form = InventoryForm()
    if form.validate_on_submit():
        inventory = Inventory(name = form.name.data, size = form.size.data, count = form.count.data, description = form.description.data)

        db.session.add(inventory)
        db.session.commit()
        flash("New item added", 'success')
        return redirect(url_for('inventory.inventory')) # inventory route in inventory package?
    return render_template('new_inventory.html', form = form)