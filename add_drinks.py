from app import app, db, User, Drink

# Creëer een applicatiecontext
with app.app_context():
    drink = Drink(id=1,name='Cola', price=1.0, image_url="https://google.com/")
    drink2 = Drink(id=2, name='Cola Zero', price=1.0, image_url="https://google.com/")

    db.session.add(drink)
    db.session.add(drink2)
    db.session.commit()

    print("drinks toegevoegd")
