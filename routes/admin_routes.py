from flask import render_template, redirect, url_for, request, session
from app import app, db
from models import User, Card, Account

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