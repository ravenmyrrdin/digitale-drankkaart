from flask import render_template, redirect, url_for, request, session
from app import app, db
from models import Card

@app.route('/admin/cards')
def admin_cards():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    cards = Card.query.all()
    return render_template('admin_cards.html', cards=cards)

@app.route('/admin/cards/add', methods=['GET', 'POST'])
def add_card():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        rfid = request.form['rfid']
        account_id = request.form['account_id']
        user_id = request.form['user_id']
        new_card = Card(rfid=rfid, account_id=account_id, user_id=user_id)
        db.session.add(new_card)
        db.session.commit()
        return redirect(url_for('admin_cards'))
    return render_template('add_card.html')

@app.route('/admin/cards/edit/<int:id>', methods=['GET', 'POST'])
def edit_card(id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    card = Card.query.get_or_404(id)
    if request.method == 'POST':
        card.rfid = request.form['rfid']
        card.account_id = request.form['account_id']
        card.user_id = request.form['user_id']
        db.session.commit()
        return redirect(url_for('admin_cards'))
    return render_template('edit_card.html', card=card)

@app.route('/admin/cards/delete/<int:id>', methods=['POST'])
def delete_card(id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    card = Card.query.get_or_404(id)
    db.session.delete(card)
    db.session.commit()
    return redirect(url_for('admin_cards'))
