#!/bin/bash

kubectl delete pod --all -n my-app

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