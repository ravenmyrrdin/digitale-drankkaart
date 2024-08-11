from flask import render_template
from app import app, db
from models import Drink

@app.route('/')
def index():
    drinks = Drink.query.all()
    return render_template('index.html', drinks=drinks)