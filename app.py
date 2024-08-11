from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialiseer Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drankkaart.db'
app.config['SECRET_KEY'] = "AMT2610web"

# Initialiseer database
db = SQLAlchemy(app)

# Importeer routes
from routes.main_routes import *
from routes.admin_routes import *
from routes.drink_routes import *
from routes.user_routes import *
from routes.card_routes import *
from routes.account_routes import *
from routes.log_routes import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)