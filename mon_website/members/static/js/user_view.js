// Animation du compteur (juste pour montrer du mouvement)
let count = 0;
const counterElement = document.getElementById("counter");

function updateCounter() {
    count++;
    counterElement.textContent = count;
    setTimeout(updateCounter, 1000); // Augmente toutes les secondes
}

if (counterElement) {
    updateCounter();
}
