#!/bin/bash

# Vérifier que le namespace est spécifié
if [ -z "$1" ]; then
    echo "❌ Aucun namespace spécifié. Veuillez fournir le namespace."
    exit 1
fi

namespace=$1

# Vérifier l'état des pods dans le namespace
echo "🔍 Vérification de l'état des pods dans le namespace $namespace..."
kubectl get pods -n "$namespace"

# Identifier le pod lié au déploiement Django
POD_NAME=$(kubectl get pods -n "$namespace" -l app=django -o jsonpath='{.items[0].metadata.name}')

if [ -z "$POD_NAME" ]; then
    echo "❌ Aucun pod trouvé pour le déploiement django dans le namespace $namespace."
    exit 1
fi

echo "🔍 Vérification des logs du pod $POD_NAME..."
kubectl logs "$POD_NAME" -n "$namespace"

# Vérifier les événements Kubernetes dans le namespace pour trouver des erreurs
echo "🔍 Vérification des événements Kubernetes dans le namespace $namespace..."
kubectl get events -n "$namespace"

# Vérifier les ressources allouées pour le pod
echo "🔍 Vérification des ressources (CPU, mémoire) du pod $POD_NAME..."
kubectl describe pod "$POD_NAME" -n "$namespace" | grep -A 10 "Resources"

# Vérifier les conditions du pod
echo "🔍 Vérification des conditions du pod $POD_NAME..."
kubectl describe pod "$POD_NAME" -n "$namespace" | grep "State" -A 10

# Vérification des problèmes potentiels de déploiement
echo "🔍 Vérification des détails du déploiement Django..."
kubectl describe deployment django-deployment -n "$namespace"

# Vérifier les logs du conteneur (par exemple, si Django ne démarre pas)
echo "🔍 Vérification des logs du conteneur (s'il y en a)..."
kubectl logs "$POD_NAME" -n "$namespace" -c django

# Vérification de la résolution du nom DNS pour MailHog via curl
echo "🔍 Vérification de la résolution du nom DNS pour 'mailhog-service' depuis le pod Django..."
kubectl exec -it "$POD_NAME" -n "$namespace" -- curl -s mailhog-service:8025
if [ $? -eq 0 ]; then
    echo "✅ Le nom 'mailhog-service' est correctement résolu et le service MailHog est accessible."
else
    echo "❌ Le nom 'mailhog-service' n'a pas pu être résolu ou le service MailHog n'est pas accessible."
fi



# Suggestion d'actions en fonction des erreurs possibles
echo "--------------------------"
echo "✅ Suggestions d'actions :"
echo "1. Si vous avez des erreurs liées à l'image Docker, assurez-vous que l'image est correctement construite et disponible."
echo "2. Si vous avez des erreurs liées à la base de données, assurez-vous que le service PostgreSQL est prêt et accessible."
echo "3. Vérifiez les ressources CPU et mémoire allouées au pod. Augmentez-les si nécessaire."
echo "4. Si le pod reste dans un état 'CrashLoopBackOff', vérifiez les logs pour plus de détails sur la cause."
echo "5. Si la résolution du nom DNS pour 'mailhog-service' échoue, assurez-vous que le service MailHog est en ligne et correctement exposé dans le même namespace."

echo "--------------------------"
echo "🔚 Fin du débogage."
