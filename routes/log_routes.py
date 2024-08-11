from flask import render_template, redirect, url_for, request, session
from app import app, db
from models import Transaction

@app.route('/admin/log')
def admin_log():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    transactions = Transaction.query.all()
    return render_template('admin_log.html', transactions=transactions)