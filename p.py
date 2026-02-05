import os
from flask import Flask, render_template, request, jsonify
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()  # Charge les variables d'environnement depuis .env

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

    # Validation optionnelle du code promo
    if promo_code and promo_code.upper() != "KILIAN10":
        return jsonify({"success": False, "message": "Code promo invalide."}), 400

    message = Mail(
        from_email=os.getenv('EMAIL_FROM'),
        to_emails=os.getenv('EMAIL_TO'),
        subject='Nouvelle demande de parrainage',
        plain_text_content=f"""
Noms soumis :

1) {name1}
2) {name2}
3) {name3}

Code promo : {promo_code or "Aucun"}

Merci de vérifier la conformité (insultes, contenu).
        """
    )

    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        if response.status_code >= 200 and response.status_code < 300:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "Erreur lors de l'envoi de l'email."}), 500
    except Exception as e:
        print("Erreur SendGrid:", e)
        return jsonify({"success": False, "message": "Erreur lors de l'envoi de l'email."}), 500

if __name__ == '__main__':
    app.run(debug=True)
