# app.py
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy 
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drankkaart.db'
db = SQLAlchemy(app)
session = session
app.config['SECRET_KEY'] = "AMT2610web"

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

@app.route('/')
def index():
    drinks = Drink.query.all()
    return render_template('index.html', drinks=drinks)

@app.route('/add_balance', methods=['POST'])
def add_balance():
    rfid = request.form['rfid']
    amount = float(request.form['amount'])
    code = request.form['code']
    admin = User.query.filter_by(code=code).first()
    if admin:
        card = Card.query.filter_by(rfid=rfid).first()
        if card:
            account = Account.query.get(card.account_id)
            account.balance += amount
            db.session.commit()
            return jsonify({"status": "success", "new_balance": account.balance})
    return jsonify({"status": "error", "message": "Ongeldige kaart of admin code"})

@app.route('/buy_drink', methods=['POST'])
def buy_drink():
    rfid = request.form['rfid']
    drink_id = int(request.form['drink_id'])
    card = Card.query.filter_by(rfid=rfid).first()
    drink = Drink.query.get(drink_id)
    if card and drink:
        account = Account.query.get(card.account_id)
        if account.balance >= drink.price:
            account.balance -= drink.price
            transaction = Transaction(card_id=card.id, drink_id=drink.id)
            db.session.add(transaction)
            db.session.commit()
            return jsonify({"status": "success", "new_balance": account.balance})
        else:
            return jsonify({"status": "error", "message": "Onvoldoende saldo"})
    return jsonify({"status": "error", "message": "Ongeldige kaart of drankje"})

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('admin_login.html')
    if request.method == 'POST':
        code = request.form['code']
        user = User.query.filter_by(code=code).first()
        if user:
            session['admin'] = True
            return redirect(url_for('admin_menu'))
        else:
            return render_template('admin_relogin.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('index'))
    
@app.route('/admin/menu')
def admin_menu():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    return render_template('admin_menu.html')

@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect(url_for('admin_menu'))
    return render_template('admin_menu.html')

# Route to display and process the add_balance form
@app.route('/admin/add_balance', methods=['GET', 'POST'])
def admin_add_balance():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    card = None
    account = None
    user = None
    error = None

    if request.method == 'POST':
        rfid = request.form['rfid']
        card = Card.query.filter_by(rfid=rfid).first()
        if not card:
            error = "Card not found. Please try again."
        account = Account.query.get(card.account_id)
        user = User.query.get(card.user_id)

    return render_template('add_balance.html', card=card, account=account, error=error, user=user)

# Route to handle balance update
@app.route('/admin/update_balance', methods=['POST'])
def update_balance():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    card_id = request.form['card_id']
    new_balance = float(request.form['new_balance'])

    card = Card.query.get(card_id)
    if card:
        account = Account.query.get(card.account_id)
        account.balance = new_balance
        db.session.commit()
        return redirect(url_for('admin_add_balance'))
    else:
        flash("Card not found or update failed.", "danger")
        return redirect(url_for('admin_add_balance'))

@app.route('/admin/drinks')
def admin_drinks():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    drinks = Drink.query.all()
    return render_template('admin_drinks.html', drinks=drinks)

@app.route('/admin/drinks/add', methods=['GET', 'POST'])
def add_drink():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        image_url = request.form['image_url']
        new_drink = Drink(name=name, price=price, image_url=image_url)
        db.session.add(new_drink)
        db.session.commit()
        return redirect(url_for('admin_drinks'))
    return render_template('add_drink.html')

@app.route('/admin/drinks/edit/<int:id>', methods=['GET', 'POST'])
def edit_drink(id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    drink = Drink.query.get_or_404(id)
    if request.method == 'POST':
        drink.name = request.form['name']
        drink.price = request.form['price']
        drink.image_url = request.form['image_url']
        db.session.commit()
        return redirect(url_for('admin_drinks'))
    return render_template('edit_drink.html', drink=drink)

@app.route('/admin/drinks/delete/<int:id>', methods=['POST'])
def delete_drink(id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    drink = Drink.query.get_or_404(id)
    db.session.delete(drink)
    db.session.commit()
    return redirect(url_for('admin_drinks'))

@app.route('/admin/users')
def admin_users():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    users = User.query.all()
    current_user = User.query.get(session.get('user_id'))  # Assuming you have a user_id in session
    return render_template('admin_users.html', users=users, current_user=current_user)

@app.route('/admin/users/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    user = User.query.get_or_404(id)
    if user.id == session.get('user_id'):  # Prevent editing currently logged-in admin
        return redirect(url_for('admin_users'))
    if request.method == 'POST':
        user.name = request.form['name']
        # Exclude admin code from being edited
        db.session.commit()
        return redirect(url_for('admin_users'))
    return render_template('edit_user.html', user=user)

@app.route('/admin/users/delete/<int:id>', methods=['POST'])
def delete_user(id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    user_to_delete = User.query.get_or_404(id)
    if user_to_delete.id == session.get('user_id'):  # Prevent deleting currently logged-in admin
        return redirect(url_for('admin_users'))
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect(url_for('admin_users'))
      
@app.route('/admin/add_user', methods=['POST'])
def add_user_api():
    code = request.form['code']
    new_user_name = request.form['name']
    new_user_code = request.form['code']
    new_user_role = request.form['role']
    new_user_organization = requestform['organization']        
    super_admin = User.query.filter_by(code=code).first()
    if super_admin:
        new_user = User(name=new_user_name, code=new_user_code, role=role, organization=organization)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Ongeldige super admin code"})

@app.route('/admin/users/add', methods=['GET', 'POST'])
def add_user():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        name = request.form['name']
        organization = request.form['organization']
        role = request.form['role']
        code = request.form['code']
        
        rfid = request.form['rfid']
        balance = float(request.form['balance'])

        new_user = User(name=name, organization=organization, role=role, code=code)
        db.session.add(new_user)
        db.session.commit()

        new_account = Account(balance=balance)
        db.session.add(new_account)
        db.session.commit()

        new_card = Card(rfid=rfid, account_id=new_account.id, user_id=new_user.id)
        db.session.add(new_card)
        db.session.commit()

        return redirect(url_for('admin_users'))
    return render_template('add_user.html')
    
@app.route('/admin/accounts')
def admin_accounts():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    try:
        accounts = Account.query.all()
    except:
    	account = null
    return render_template('admin_accounts.html', accounts=accounts)

@app.route('/admin/accounts/add', methods=['GET', 'POST'])
def add_account():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        balance = float(request.form['balance'])
        print(request.form['user_id'])
        user_id = int(request.form['user_id'])  # Assuming you have a way to select the user
        new_account = Account(balance=balance, user_id=user_id)
        db.session.add(new_account)
        db.session.commit()
        return redirect(url_for('admin_accounts'))
    return render_template('add_account.html')
    
@app.route('/admin/search_users', methods=['GET'])
def search_users():
    query = request.args.get('query')
    users = User.query.filter(User.name.like(f'%{query}%')).all()
    user_list = [{"id": user.id, "name": user.name} for user in users]
    return jsonify(user_list)
    
@app.route('/admin/accounts/edit/<int:id>', methods=['GET', 'POST'])
def edit_account(id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    account = Account.query.get_or_404(id)
    if request.method == 'POST':
        account.balance = float(request.form['balance'])
        db.session.commit()
        return redirect(url_for('admin_accounts'))
    return render_template('edit_account.html', account=account)
    
@app.route('/admin/accounts/delete/<int:id>', methods=['POST'])
def delete_account(id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    account = Account.query.get_or_404(id)
    db.session.delete(account)
    db.session.commit()
    return redirect(url_for('admin_accounts'))

@app.route('/admin/cards', methods=['GET'])
def admin_cards():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    else:
        cards = Card.query.all()
        for card in cards:
            user = User.query.get(card.user_id)
            account = Account.query.get(card.account_id)
        return render_template('admin_cards.html', cards=cards, user=user, account=account)
    return jsonify({"status": "error", "message": "Ongeldige super admin code"})

@app.route('/admin/cards/add', methods=['GET', 'POST'])
def add_card():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        rfid = request.form['rfid']
        user_id = int(request.form['user_id'])
        account_id = int(request.form['account_id'])
        new_card = Card(rfid=rfid, user_id=user_id, account_id=account_id)
        db.session.add(new_card)
        db.session.commit()
        return redirect(url_for('admin_cards'))
    return render_template('add_card.html')

@app.route('/admin/cards/edit/<int:id>', methods=['GET', 'POST'])
def edit_card(id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    card = Card.query.get_or_404(id)
    if card != None:
        user = User.query.get(card.user_id)
        account = Account.query.get(card.account_id)
    if request.method == 'POST':
        card.rfid = request.form['rfid']
        card.user_id = int(request.form['user_id'])
        card.account_id = int(request.form['account_id'])
        db.session.commit()
        return redirect(url_for('admin_cards'))
    return render_template('edit_card.html', card=card, user=user, account=account)

@app.route('/admin/cards/delete/<int:id>', methods=['POST'])
def delete_card(id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    card = Card.query.get_or_404(id)
    db.session.delete(card)
    db.session.commit()
    return redirect(url_for('admin_cards'))

@app.route('/admin/logs', methods=['GET'])
def view_logs():
    code = request.args.get('code')
    super_admin = User.query.filter_by(code=code).first()
    if super_admin:
        transactions = Transaction.query.all()
        log_data = []
        for transaction in transactions:
            card = Card.query.get(transaction.card_id)
            drink = Drink.query.get(transaction.drink_id)
            log_data.append({
                "card_id": card.rfid,
                "drink": drink.name,
                "timestamp": transaction.timestamp
            })
        return jsonify(log_data)
    return jsonify({"status": "error", "message": "Ongeldige super admin code"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
