from datetime import datetime
from decimal import Decimal
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from inventoryapp import db
from inventoryapp.models import Inventory
from inventoryapp.inventory.forms import InventoryForm, UpdateInventoryItemForm
from inventoryapp.inventory.utils import calc_time_delta, remove_exponent

inven = Blueprint('inventory', __name__) # pass in the name of our blueprint too: "inventory". set it to "inven" here so no collisions


@inven.route('/inventory')
@login_required
def inventory():
    all_inventory = Inventory.query.order_by(Inventory.last_updated.desc()).all() # the desc() puts the most recently updated items first
    
    return render_template('inventory.html', inventory = all_inventory, calc_time_delta = calc_time_delta, remove_exponent = remove_exponent)


@inven.route('/inventory/<int:id>') # view a singular item
@login_required
def item(id):
    item = Inventory.query.get_or_404(id)
    return render_template('item.html', title = item.name, item = item)

@inven.route('/inventory/new', methods=['GET', 'POST'])
@login_required
def new_item():
    form = InventoryForm()
    if form.validate_on_submit():
        item = Inventory(name = form.name.data, size = form.size.data, count = form.count.data, description = form.description.data)

        db.session.add(item)
        db.session.commit()
        flash("New item added", 'success')
        return redirect(url_for('inventory.inventory')) # inventory route in inventory package?
    return render_template('new_item.html', form = form)


@inven.route('/inventory/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_item(id):
    form = UpdateInventoryItemForm()
    item = Inventory.query.get_or_404(id)
    if form.validate_on_submit(): # user submitted valid updated post
        item.count = form.count.data
        item.last_updated = datetime.utcnow() # update the last updated time for this item to "now"
        db.session.commit()
        flash('Your item has been updated!', 'success')
        return redirect(url_for('inventory.inventory', id = item.id)) # should redirect to url_for('inventory.item') but not implemented yet, so just go back to inventory
    elif request.method == 'GET': # user just visited the edit page of their item so we populate the field with the current item's data
        form.name.data = item.name
        form.size.data = item.size
        form.count.data = item.count # can't remove exponent here because the Form is set to a DecimalField anyways
        form.description.data = item.description
    return render_template('update.html', title = 'Update item count', form = form, remove_exponent = remove_exponent, id = id)


@inven.route('/inventory/<int:id>/delete', methods=['POST'])
@login_required
def delete_item(id):
    item = Inventory.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('inventory.inventory'))