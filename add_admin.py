from app import app, db, User

# Creëer een applicatiecontext
with app.app_context():
    # Voeg een standaard admin gebruiker toe
    admin_user = User(name='Admin User', code='admin123', organization='AMT', role="admin")

    db.session.add(admin_user)
    db.session.commit()

    print("Admin gebruiker toegevoegd met admin_code: admin123")
