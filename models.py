from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(50), unique=False, nullable=True)
    organization = db.Column(db.String(50), unique=True, nullable=False)
    role = db.Column(db.String(50), unique=False, nullable=False)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, default=0.0)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rfid = db.Column(db.String(50), unique=True, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    drink_id = db.Column(db.Integer, db.ForeignKey('drink.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())