from flask import render_template, redirect, url_for, request, session, jsonify
from app import app, db
from models import User

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
    user = User.query.get_or_404(id)
    if user.id == session.get('user_id'):  # Prevent deleting currently logged-in admin
        return redirect(url_for('admin_users'))
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin_users'))