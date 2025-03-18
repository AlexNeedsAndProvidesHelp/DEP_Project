const typedTextSpan = document.querySelector(".typed-text");
const cursor = document.querySelector(".cursor");

const words = ["Article 1", "Article 2", "Article 3", "Article 4", "Article 5", "Article 6", "Article 7", "Article 8"];
const typingDelay = 100;
const erasingDelay = 50;
const newLetterDelay = 1000;
let index = 0;
let charIndex = 0;

document.addEventListener("DOMContentLoaded", () => {
    setTimeout(type, newLetterDelay);
});

const nextButton = document.getElementById("next");
nextButton.addEventListener("click", changeNext);

const prevButton = document.getElementById("prev");
prevButton.addEventListener("click", changePrev);

function changeNext() {
    erasePos();
}

function changePrev() {
    eraseNeg();
}

function type() {
    if (charIndex < words[index].length) {
        typedTextSpan.textContent += words[index].charAt(charIndex);
        charIndex++;
        setTimeout(type, typingDelay);
    }
}

function erasePos() {
    if (charIndex > 0) {
        typedTextSpan.textContent = words[index].substring(0, charIndex - 1);
        charIndex--;
        setTimeout(erasePos, erasingDelay);
    } else {
        index = (index + 1) % words.length;  // Incrémenter l'index et le remettre à zéro si on dépasse la longueur
        setTimeout(type, typingDelay);
    }
}

function eraseNeg() {
    if (charIndex > 0) {
        typedTextSpan.textContent = words[index].substring(0, charIndex - 1);
        charIndex--;
        setTimeout(eraseNeg, erasingDelay);
    } else {
        index = (index - 1 + words.length) % words.length;  // Décrémenter l'index et s'assurer qu'on revient au dernier élément si nécessaire
        setTimeout(type, typingDelay);
    }
}
