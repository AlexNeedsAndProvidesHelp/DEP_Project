# Utiliser l'image de base d'Ollama
FROM ollama/ollama:latest

# Définir le répertoire de travail
WORKDIR /root/.ollama

# Copier le script d'initialisation dans l'image
COPY ./Ollama/init_ollama.sh /root/init_ollama.sh

# Rendre le script exécutable
RUN chmod +x /root/init_ollama.sh

# Exposer le port sur lequel Ollama écoutera (si nécessaire)
EXPOSE 11434

# Commande d'entrée pour lancer le script d'initialisation
ENTRYPOINT ["/root/init_ollama.sh"]
