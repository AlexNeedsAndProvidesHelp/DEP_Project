#!/bin/bash

# Supprimer tous les pods dans le namespace my-app
kubectl delete pod --all -n my-app

# Supprimer le registre Docker s'il existe
docker rm -f registry 2>/dev/null

#Construire l'image
docker compose build

# Démarrer le registre Docker
docker run -d -p 5000:5000 --name registry registry:2

# Vérifier si le registre est opérationnel (attente pour s'assurer que le registre est prêt)
echo "Vérification du registre Docker..."
sleep 5  # Attendre que le registre soit prêt

# Pousser la dernière image de mon_website
docker tag mon_website-web:latest localhost:5000/mon_website-web:latest
docker push localhost:5000/mon_website-web:latest

# Afficher les images disponibles dans le registre local
echo "Images disponibles dans le registre local :"
curl -s http://localhost:5000/v2/_catalog

# Fonction pour relancer tous les déploiements
relancer_deployments() {
    local namespace=$1

    # Application des volumes persistants
    kubectl apply -f postgres-pvc.yaml -n my-app

    # Application des ConfigMaps et Configurations
    kubectl apply -f configmap.yaml
    kubectl apply -f postgres-config.yaml

    # Appliquer les déploiements
    kubectl apply -f db-deployment.yaml -n "$namespace"
    kubectl apply -f ollama-server-deployment.yaml -n "$namespace"
    kubectl apply -f mailhog-deployment.yaml -n "$namespace"
    kubectl apply -f web-deployment.yaml -n "$namespace"
    sleep 1

    echo "Tous les déploiements ont été relancés dans le namespace $namespace."
}

# Appel de la fonction avec le namespace "my-app"
relancer_deployments "my-app"

#services disponibles
echo "services crées : "
kubectl get svc -n my-app

echo "pods crées : "
kubectl get pods -n my-app
