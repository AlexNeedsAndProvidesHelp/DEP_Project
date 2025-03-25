#!/bin/bash

# Suppression et recréation du namespace
kubectl delete namespace my-app --ignore-not-found=true
kubectl create namespace my-app
echo "✅ Namespace my-app recréé."

# Pull de l'image PostgreSQL
echo "📦 Docker pull de PostgreSQL..."
docker pull postgres:15

# Application des volumes persistants
kubectl apply -f postgres-pvc.yaml -n my-app
kubectl apply -f ollama-pvc.yaml -n my-app

# Application des ConfigMaps et Configurations
kubectl apply -f configmap.yaml
kubectl apply -f postgres-config.yaml

# Application des déploiements
kubectl apply -f db-deployment.yaml -n my-app
kubectl apply -f ollama-server-deployment.yaml -n my-app
kubectl apply -f mailhog-deployment.yaml -n my-app
kubectl apply -f web-deployment.yaml -n my-app

echo "-------------------------- "
echo "✅ Attente que tous les pods soient prêts..."

# Attendre que tous les pods soient en état "Ready"
kubectl wait --for=condition=Ready pod --all -n my-app --timeout=180s

echo "✅ Tous les pods sont prêts."
echo "-------------------------- "

# Exécuter `ollama pull llama3` dans le pod du serveur Ollama
echo "🔄 Téléchargement du modèle Llama 3 sur le serveur Ollama..."
OLLAMA_POD=$(kubectl get pod -n my-app -l app=ollama -o jsonpath="{.items[0].metadata.name}")
kubectl exec -n my-app $OLLAMA_POD -- ollama pull llama3
echo "✅ Modèle Llama 3 téléchargé."

echo "-------------------------- "
echo "📜 Effectuer la migration Django..."
kubectl logs -n my-app -l app=django -c migrate
echo "-------------------------- "

# Voir les services en cours
echo "🔍 Services en cours :"
kubectl get svc -n my-app

# Voir le statut des pods
echo "🔍 Statut des pods :"
kubectl get pods -n my-app

# Afficher les logs des pods
echo "-------------------------- "
echo "📜 Affichage des logs des pods..."
echo "-------------------------- "
for pod in $(kubectl get pods -n my-app -o jsonpath='{.items[*].metadata.name}'); do
    echo " **** START LOG POD $pod **** "
    kubectl logs $pod -n my-app
    echo "                              "
done

# Lister les volumes montés
echo "-------------------------- "
echo "🗂️  Liste des volumes montés :"
kubectl get pvc -n my-app

# Lister les endpoints
echo "-------------------------- "
echo "🔗 Liste des endpoints :"
kubectl get endpoints -n my-app
echo "---------- FIN ------------- "
