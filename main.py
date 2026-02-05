import os
from flask import Flask, render_template, request, jsonify
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/send-names', methods=['POST'])
def send_names():
    data = request.json
    name1 = data.get('name1')
    name2 = data.get('name2')
    name3 = data.get('name3')
    promo_code = data.get('promoCode', '')

    if not all([name1, name2, name3]):
        return jsonify({"success": False, "message": "Tous les noms doivent être remplis"}), 400

    # Récupération des variables d'environnement (configurées sur Render)
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    EMAIL_FROM = os.getenv('EMAIL_FROM')  # ex: no-reply@gainup.com
    EMAIL_TO = os.getenv('EMAIL_TO')      # ton email ou liste email

    if not SENDGRID_API_KEY or not EMAIL_FROM or not EMAIL_TO:
        return jsonify({"success": False, "message": "Configuration email manquante"}), 500

    # Préparation du contenu email (à adapter à ton besoin)
    subject = "Nouveau parrainage GainUp"
    content = f"""
    Nouveau parrainage reçu :

    Nom 1 : {name1}
    Nom 2 : {name2}
    Nom 3 : {name3}
    Code promo : {promo_code}
    """

    message = Mail(
        from_email=EMAIL_FROM,
        to_emails=EMAIL_TO,
        subject=subject,
        plain_text_content=content
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        if response.status_code >= 200 and response.status_code < 300:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "Erreur lors de l’envoi de l’email"}), 500
    except Exception as e:
        print("Erreur SendGrid:", e)
        return jsonify({"success": False, "message": "Erreur interne serveur"}), 500

if __name__ == '__main__':
    app.run(debug=True)
