# 🍻 Digitale Drankkaart

Een moderne en intuïtieve webapplicatie voor het beheren van een digitale drankkaart, perfect voor evenementen, clubs en andere gelegenheden waar drankjes worden verkocht.

![Flask](https://img.shields.io/badge/Flask-2.0.3-blue.svg) ![Python](https://img.shields.io/badge/Python-3.10-green.svg) ![SQLite](https://img.shields.io/badge/SQLite-3.35.4-blue.svg)

## 📜 Inhoudsopgave

- [Overzicht](#overzicht)
- [Installatie](#installatie)
- [Gebruik](#gebruik)
- [Projectstructuur](#projectstructuur)
- [Routes en Functies](#routes-en-functies)
- [Bijdragen](#bijdragen)
- [Licentie](#licentie)

## 📝 Overzicht

De Digitale Drankkaart-applicatie stelt gebruikers in staat om drankjes te kopen via RFID-kaarten. Beheerders kunnen gebruikers, kaarten, accounts en drankjes beheren via een beveiligd admin-paneel. De applicatie is gebouwd met Flask, een Python-webframework, en gebruikt een SQLite-database voor het opslaan van gegevens.

## 🚀 Installatie

Volg de onderstaande stappen om de applicatie lokaal op te zetten:

1. **Clone de repository:**

   ```bash
   git clone https://github.com/ravenmyrrdin/digitale-drankkaart.git
   cd digitale-drankkaart
   ```

   Maak een virtual environment aan en activeer deze:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

Installeer de vereiste Python-pakketten:

    ```bash
    pip install -r requirements.txt
    ```

Initialiseer de SQLite-database:

    ```bash
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

Start de applicatie:

    ```bash
    flask run
    ```

Open je browser en ga naar:

    ```bash
    http://127.0.0.1:5000/
    ```

📖 Gebruik
Gebruikersdashboard

    Bekijk beschikbare drankjes: Op de homepage kun je een overzicht zien van alle beschikbare drankjes en hun prijzen.
    Koop een drankje: Voer je RFID-kaartgegevens in en selecteer een drankje om het te kopen.

Admin-paneel

    Login: Voer de admin code in om toegang te krijgen tot het beheerdersdashboard.
    Gebruikers beheren: Voeg nieuwe gebruikers toe, bewerk of verwijder bestaande gebruikers.
    Drankjes beheren: Voeg nieuwe drankjes toe, bewerk of verwijder bestaande drankjes.
    Saldo beheren: Voeg saldo toe aan gebruikersaccounts en beheer de kaartinformatie.

📂 Projectstructuur

    ```plaintext
    digitale-drankkaart/
    │
    ├── app.py                  # Hoofdbestand dat de applicatie start
    ├── models.py               # Database-modellen voor gebruikers, kaarten, etc.
    ├── routes/
    │ ├── admin_routes.py       # Routes specifiek voor het admin-gedeelte
    │ └── user_routes.py        # Routes specifiek voor het gebruikersgedeelte
    ├── static/                 # Statische bestanden (CSS, JS, afbeeldingen)
    ├── templates/              # HTML-templates voor de weergave van pagina's
    └── README.md               # Dit bestand
    ```

🌐 Routes en Functies
Gebruikersroutes

    GET / - Startpagina met een overzicht van beschikbare drankjes.
    POST /buy_drink - Koopt een drankje op basis van RFID en drankje ID.

Admin Routes

    GET /admin/login - Login pagina voor beheerders.
    GET /admin/menu - Beheerdersmenu na succesvolle login.
    POST /admin/update_balance - Route om het saldo van een account bij te werken.
    GET/POST /admin/add_balance - Formulier om saldo toe te voegen aan een account.
    En meer... - Zie de broncode voor alle beschikbare beheerdersroutes.

🤝 Bijdragen

Voel je vrij om bij te dragen aan dit project! Je kunt een pull request indienen of een issue aanmaken als je bugs tegenkomt of nieuwe functies wilt toevoegen.
📜 Licentie

Dit project is gelicentieerd onder de MIT-licentie - zie het LICENSE bestand voor meer informatie.
