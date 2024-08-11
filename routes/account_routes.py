from flask import render_template, redirect, url_for, request, session
from app import app, db
from models import Account

@app.route('/admin/accounts')
def admin_accounts():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    accounts = Account.query.all()
    return render_template('admin_accounts.html', accounts=accounts)

@app.route('/admin/accounts/add', methods=['GET', 'POST'])
def add_account():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        new_account = Account(balance=0.0)
        db.session.add(new_account)
        db.session.commit()
        return redirect(url_for('admin_accounts'))
    return render_template('add_account.html')

@app.route('/admin/accounts/edit/<int:id>', methods=['GET', 'POST'])
def edit_account(id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    account = Account.query.get_or_404(id)
    if request.method == 'POST':
        account.balance = request.form['balance']
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