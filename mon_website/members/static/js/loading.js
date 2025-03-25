document.addEventListener("DOMContentLoaded", function () {
    let count = 0;
    const counterElement = document.getElementById("counter");

    // Fonction pour incrémenter le compteur chaque seconde
    function startCounter() {
        setInterval(() => {
            count++;
            counterElement.textContent = count;
        }, 1000);
    }

    startCounter(); // Démarrer le compteur

    fetch("/page1")  // Appel AJAX pour générer le contenu
        .then(response => response.text()) // Attendre la réponse complète
        .then(() => {
            window.location.href = "/page1";  // Redirection vers la page générée
        })
        .catch(error => console.error("Erreur lors de la génération:", error));
});
