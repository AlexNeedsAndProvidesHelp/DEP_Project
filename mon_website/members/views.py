from django.shortcuts import render
from .models import GeneratedText
from django.http import HttpResponse
import requests, os

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://ollama_server:11434")

def  home(request):
    data ={}
    return render(request,"index.html", data)

def logs_view(request):
    # Récupérer tous les membres depuis la base de données
    generated_texts = GeneratedText.objects.all()  # Récupère tous les textes générés

    # Passer les membres et les textes générés au template
    context = {
        'generated_texts': generated_texts
    }
    return render(request, "logs.html", context)

def help_view(request):
    return render(request, "help.html")  # Affiche calendar.html

def calendar_view(request):
    return render(request, "calendar.html")  # Affiche calendar.html

def generated_texts_view(request, id):
    # Récupérer le nombre total d'éléments dans la base de données
    total_texts = GeneratedText.objects.count()

    # Vérifier si l'id est dans la plage valide
    if id < 1 or id > total_texts:
        raise Http404("Objet non trouvé")

    # Récupérer le texte correspondant à l'id demandé (après tri)
    generated_text = GeneratedText.objects.all().order_by('id')[id - 1]

    # Préparer les données pour le template
    ai_texts = {
        "ai_title": generated_text.title,
        "subtitle": generated_text.subtitle,
        "question": generated_text.question,
        "com1": generated_text.com1,
        "com2": generated_text.com2,
        "com3": generated_text.com3,
        "theme1": generated_text.theme1,
        "theme2": generated_text.theme2,
        "theme3": generated_text.theme3,
    }
    
    return render(request, "page1.html", ai_texts)

def generate_text(prompt):
    """Appelle l'API Ollama pour générer un texte en fonction du prompt donné."""
    response = requests.post(
        f"{OLLAMA_API_URL}/api/generate",
        json={"model": "llama3", "prompt": prompt, "stream": False}  
    )

    if response.status_code == 200:
        return response.json().get('response', 'Aucune réponse générée.')
    return "Erreur avec l'API Ollama."


def page1_view(request):
    prompt1 = "Génère un titre de journal. Mentionne uniquement le titre que tu as choisi."
    ai_title = generate_text(prompt1)  # Générer le titre

    prompt2 = {
        "subtitle": f"Génère un sous-titre en rapport avec le titre : '{ai_title}'. Ne mentionne rien d'autres que le titre",
        "question": f"Génère une question en rapport avec le titre : '{ai_title}'. Ne mentionne rien d'autres que la question",
        "com1": f"Donne moi trois mots au hasard en rapport avec le titre : '{ai_title}'. Ne mentionne rien d'autres que les trois mots",
        "com2": f"Donne moi trois mots au hasard en rapport avec le titre : '{ai_title}'. Ne mentionne rien d'autres que les trois mots",
        "com3": f"Donne moi trois mots au hasard en rapport avec le titre : '{ai_title}'. Ne mentionne rien d'autres que les trois mots",
        "theme1": f"Génère un thème en rapport avec le titre : '{ai_title}'. Ne mentionne rien d'autres que le thème",
        "theme2": f"Génère un autre thème en rapport avec le titre : '{ai_title}'. Ne mentionne rien d'autres que le thème",
        "theme3": f"Génère un autre thème en rapport avec le titre : '{ai_title}'. Ne mentionne rien d'autres que le thème",
    }

    ai_texts = {key: generate_text(value) for key, value in prompt2.items()}  # Appeler l'API pour chaque texte
    ai_texts['ai_title'] = ai_title  # Ajouter le titre généré au contexte

    # Afficher les valeurs générées par l'IA dans la console
    print("🔍 Valeurs générées par l'IA :")
    for key, value in ai_texts.items():
        print(f"{key}: {value}")

    # Vérifier le nombre d'enregistrements dans la base de données
    num_generated_texts = GeneratedText.objects.count()

    # Si plus de 8 enregistrements, supprimer le plus ancien
    if num_generated_texts >= 8:
        oldest_text = GeneratedText.objects.order_by('created_at').first()  # Obtenir le texte le plus ancien
        print(f"🔍 Suppression du texte le plus ancien (ID: {oldest_text.id})")
        oldest_text.delete()  # Supprimer le plus ancien

    # Enregistrer dans la base de données
    print("🔍 Enregistrement dans la base de données..")
    generated_text = GeneratedText.objects.create(
        title=ai_title,
        subtitle=ai_texts["subtitle"],
        question=ai_texts["question"],
        com1=ai_texts["com1"],
        com2=ai_texts["com2"],
        com3=ai_texts["com3"],
        theme1=ai_texts["theme1"],
        theme2=ai_texts["theme2"],
        theme3=ai_texts["theme3"],
    )

    print("🔍 Données envoyées au template:", ai_texts)

    return render(request, "page1.html", ai_texts)