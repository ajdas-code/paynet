import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret'
print(SECRET_KEY)
app.config['SECRET_KEY'] = SECRET_KEY

# Set up the SQLAlchemy Database to be a local file 'desserts.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///desserts.db'
db = SQLAlchemy(app)


if __name__ == "__main__":

    # We need to make sure Flask knows about its views before we run
    # the app, so we import them. We could do it earlier, but there's
    # a risk that we may run into circular dependencies, so we do it at the
    # last minute here.

    from views import *

    app.run(debug=True)
