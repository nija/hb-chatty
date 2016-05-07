'''Chat Engine'''
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
#from model import Logs, Messages, Rooms, Users, connect_to_db, db


# Create a Flask app
app = Flask(__name__)

# Set up the secret key needed for session and debug-toolbar
app.secret_key = 'BalloonicornSmash'

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    '''Home page'''

    return render_template("home.html")







if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    #connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
