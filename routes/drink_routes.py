from flask import request, jsonify, render_template, redirect, url_for
from app import app, db
from models import Drink, Card, Account, Transaction

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