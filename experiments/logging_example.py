'''Logging Test'''
# pylint: disable=I0011,C0103

# ====== Imports ======
# Standard imports
import bleach
from datetime import datetime
import json
import os
import pprint
# Flask and related imports
from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, redirect, request, flash, send_from_directory, session
import sys
import logging
LOG_FILENAME = 'chatty.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

logging.debug("\n\n\t\tSTART HERE: This message should go to the log file")

# shandler = logging.StreamHandler()
# shandler.setLevel(logging.DEBUG)
# app.logger.addHandler(shandler)
# logging.config.fileConfig('logging.conf')



# ====== Server Start-up ======
# Create a Flask app
app = Flask(__name__)

# Set up the secret key needed for session and debug-toolbar
app.secret_key = 'BalloonicornSmash'

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

# Set up logging
# Create logger
# logger = logging.getLogger("simple_example")
# logger.setLevel(logging.DEBUG)
# # Create console handler and set level to debug
# console_logger = logging.StreamHandler()
# console_logger.setLevel(logging.DEBUG)
# # Create formatter
# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# # Add formatter to console_logger
# console_logger.setFormatter(formatter)
# # Add console_logger to logger
# logger.addHandler(console_logger)
# app.logger.addHandler(logger)


# ====== END Server Start-up ======



# ====== Routes Definitions ======

######  Flask Routes  ######
# Show homepage
@app.route('/')
def index():
    '''Home page'''

    logging.debug("in def {}: {}".format("index","test"))
    return "Hello world"


@app.route('/favicon.ico')
def serve_favicon():
    '''Serve our favicon'''
    return send_from_directory(os.path.join(app.root_path, '../static/img'), 'favicon.ico')


# ====== Main Application ======
if __name__ == "__main__":

    # Figure out which db to connect to
    db_uri = os.environ.get("DATABASE_URL","postgres:///travis_ci_test")
    # Test
    #connect_to_db(app, db_uri="postgresql:///travis_ci_test")
    # Prod
    #connect_to_db(app, db_uri="postgresql:///chatty")
    print "\n      {}\n\n".format(db_uri)
    logging.debug(db_uri)
    # connect_to_db(app, db_uri)


    # Right now, we only have one room and one user in that room

    print "\n    HEREEEEE!\n\n"

    # DebugToolbarExtension requires debug=True before it will run correctly
    # Leave this as is because of the 'No handlers could be found for logger
    # "sqlalchemy.pool.QueuePool"' http 500 error that results when it is taken
    # out
    DEBUG = "NO_DEBUG" not in os.environ
    # app.debug = True
    app.debug = DEBUG
    print "debug: {}".format(DEBUG)
    logging.debug("debug: {}".format(DEBUG))

    # Set the port
    port = int(os.environ.get("PORT", 5005))
    logging.debug("port: {}".format(port))

    # Allow more processes so there's enough wiggle room to handle multiple requests
    # Use the DebugToolbar
    # DebugToolbarExtension(app)
    app.run(host="0.0.0.0", port=port, processes=3)





SELECT room_user.room_user_id AS room_user_room_user_id, room_user.room_id AS room_user_room_id, room_user.user_id AS room_user_user_id, room_user.time_stamp AS room_user_time_stamp
FROM room_user
WHERE room_user.room_id = 1 AND room_user.user_id = 3;



