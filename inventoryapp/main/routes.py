from flask import Blueprint, render_template

main = Blueprint('main', __name__) # pass in the name of our blueprint too: "main"

@main.route('/') #define a route and code to run. this route would be at our base url. like base google.com
@main.route('/index')
def index():
    return render_template('index.html')