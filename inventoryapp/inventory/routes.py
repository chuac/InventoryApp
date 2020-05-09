from datetime import datetime
from decimal import Decimal
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import current_user, login_required
from sqlalchemy import func
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
    flash("Item deleted successfully", 'success')
    return redirect(url_for('inventory.inventory'))


"""
Incomplete functionality
"""
@inven.route('/inventory/stocktake', methods=['GET', 'POST'])
@login_required
def stocktake():
    all_inventory = Inventory.query.order_by(Inventory.last_updated.desc()).all()
    form = UpdateInventoryItemForm()
    return render_template('stocktake.html', inventory = all_inventory, calc_time_delta = calc_time_delta, remove_exponent = remove_exponent)


@inven.route('/inventory/purchasing', methods=['GET', 'POST'])
@login_required
def purchasing():
    # get will give them a checklist for which items, post returns a shopping list
    all_inventory = Inventory.query.order_by(Inventory.last_updated.desc()).all()
    count = len(all_inventory)
    

    if request.method == 'POST':
        list_checked = []
        i = 1
        while i < count + 1:
            x = request.form.get(str(i), "off")
            if x == 'on':
                list_checked.append(i)
            i = i + 1
        if len(list_checked) != 0: # not an empty list. the user did select at least one checkbox
            return render_template('purchasing_list.html', inventory = all_inventory, list_checked = list_checked, remove_exponent = remove_exponent)
        
        return redirect(url_for('inventory.inventory'))

    return render_template('purchasing.html', inventory = all_inventory, count = count)

