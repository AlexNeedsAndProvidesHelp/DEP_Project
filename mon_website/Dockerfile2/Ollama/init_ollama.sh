#!/bin/bash

# Vérifier si le modèle llama3 est déjà téléchargé
if [ ! -d "/root/.ollama/models/llama3" ]; then
    echo "Modèle llama3 non trouvé, téléchargement..."
    ollama pull llama3
else
    echo "Modèle llama3 déjà présent."
fi

# Démarrer le service Ollama
echo "Lancement du service Ollama..."
ollama serve
