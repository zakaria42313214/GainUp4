import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import sgMail from '@sendgrid/mail';

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

sgMail.setApiKey(process.env.SENDGRID_API_KEY);

app.post('/send-names', async (req, res) => {
  const { name1, name2, name3, promoCode } = req.body;

  if (!name1 || !name2 || !name3) {
    return res.status(400).json({ success: false, message: "Veuillez remplir les trois premiers champs." });
  }

  // Optionnel : tu peux vérifier promoCode ici si tu veux, ex:
  // if (promoCode && promoCode.toUpperCase() !== "KILIAN10") {
  //   return res.status(400).json({ success: false, message: "Code promo invalide." });
  // }

  const msg = {
    to: process.env.EMAIL_TO,
    from: process.env.EMAIL_FROM,
    subject: 'Nouvelle demande de parrainage',
    text: `
Noms soumis :

1) ${name1}
2) ${name2}
3) ${name3}

Code promo : ${promoCode || "Aucun"}

Merci de vérifier la conformité (insultes, contenu).
    `
  };

  try {
    await sgMail.send(msg);
    res.json({ success: true });
  } catch (error) {
    console.error("Erreur SendGrid:", error);
    res.status(500).json({ success: false, message: "Erreur lors de l’envoi de l’email." });
  }
});

app.listen(3000, () => {
  console.log('Serveur lancé sur http://localhost:3000');
});
