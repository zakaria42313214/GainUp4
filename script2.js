// Affiche le formulaire
function showForm() {
  const card = document.getElementById("formCard");
  if (!card) return;

  card.style.display = "block";
  card.scrollIntoView({ behavior: "smooth" });
}

// Validation code promo en direct et affichage icône
function setupPromoValidation() {
  const promoInput = document.getElementById("promoCode");
  const promoIcon = document.getElementById("promoIcon");
  if (!promoInput || !promoIcon) return;

  promoInput.addEventListener("input", () => {
    const val = promoInput.value.trim().toUpperCase();
    if (val === "KILIAN10") {
      promoIcon.textContent = "✅";
      promoIcon.style.color = "#16a34a";
    } else if (val.length === 0) {
      promoIcon.textContent = "";
    } else {
      promoIcon.textContent = "❌";
      promoIcon.style.color = "#dc2626";
    }
  });
}

// Validation + envoi serveur
async function validateAndContinue() {
  const name1 = document.getElementById("name1");
  const name2 = document.getElementById("name2");
  const name3 = document.getElementById("name3");
  const promoInput = document.getElementById("promoCode");
  const error = document.getElementById("error");

  if (!name1 || !name2 || !name3 || !promoInput || !error) {
    console.error("Éléments HTML manquants");
    return;
  }

  const n1 = name1.value.trim();
  const n2 = name2.value.trim();
  const n3 = name3.value.trim();
  const promo = promoInput.value.trim();

  // Vérification champs vides
  if (n1 === "" || n2 === "" || n3 === "") {
    error.textContent = "Veuillez remplir les trois premiers champs.";
    error.style.display = "block";
    return;
  }

  // Validation code promo (vide ou KILIAN10)
  if (promo !== "" && promo.toUpperCase() !== "KILIAN10") {
    error.textContent = "Code promo invalide.";
    error.style.display = "block";
    return;
  }

  error.style.display = "none";

  try {
    const response = await fetch("/send-names", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        name1: n1,
        name2: n2,
        name3: n3,
        promoCode: promo
      })
    });

    if (!response.ok) {
      throw new Error("Réponse serveur invalide");
    }

    const result = await response.json();

    if (result.success === true) {
      // ✅ Validation OK → redirection
      window.location.href = "main.html";
    } else {
      error.textContent = "Une erreur est survenue. Veuillez réessayer.";
      error.style.display = "block";
    }

  } catch (err) {
    console.error(err);
    error.textContent = "Impossible de contacter le serveur.";
    error.style.display = "block";
  }
}

// Initialisation de la validation promo au chargement de la page
document.addEventListener("DOMContentLoaded", () => {
  setupPromoValidation();
});
