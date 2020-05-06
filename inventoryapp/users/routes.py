from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from inventoryapp import db, bcrypt
from inventoryapp.models import User
from inventoryapp.users.forms import RegistrationForm, LoginForm


users = Blueprint('users', __name__) # blueprint

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: # user is already logged in, no need to show them register page
        return redirect(url_for('inventory.inventory'))
    form = RegistrationForm()
    if form.validate_on_submit() and request.method == 'POST': # validate POST data
        #hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        user = User(form.username.data, form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}! You are now able to log in", 'success') # flash message, using python f-strings. 2nd arg is a "category". 'success' is Bootstrap style
        return redirect(url_for('users.login')) # is a valid form so now we redirect to posts page
    return render_template('register.html', form = form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: # user is already logged in, no need to show them login page
        return redirect(url_for('inventory.inventory'))
    form = LoginForm()
    if form.validate_on_submit(): # validate POST data
        user = User.query.filter_by(email = form.email.data).first() # retrieve a user in db that has same email as entered into the form
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next') # capture what page the user was trying to visit before we asked them to login
            return redirect(next_page) if next_page else redirect(url_for('inventory.inventory'))
        else:
            flash(f"Login unsuccessful. Please check email and password", 'danger')
        #flash(f"Login successful for {form.username.data}!", 'success') # flash message, using python f-strings. 2nd arg is a "category". 'success' is Bootstrap style
        #return redirect(url_for('posts')) # is a valid form so now we redirect to posts page
    return render_template('login.html', form = form) # login unsuccessful so just return them to login page


@users.route('/logout')
def logout():
    logout_user() # imported this above, from flask_login
    return redirect(url_for('main.index'))

