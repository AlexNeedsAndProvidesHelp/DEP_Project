from django.shortcuts import render, redirect
from .models import GeneratedText
from django.http import HttpResponse
import requests, os
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib import messages

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import Http404

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

def signin_view(request):
    return render(request, "signin.html")  # Affiche calendar.html

def calendar_view(request):
    return render(request, "calendar.html")  # Affiche calendar.html

def user_view(request, id):
    
    # Récupérer tous les textes de l'utilisateur triés par date de création
    texts = GeneratedText.objects.filter(user_id=request.user).order_by('created_at')
    total_texts = texts.count()

    # Vérifier s'il y a des textes et si l'ID est valide
    if total_texts == 0 or id < 1 or id > total_texts:
        raise Http404("Objet non trouvé")

    # Récupérer l'élément correspondant
    generated_text = texts[id-1]  # Liste indexée à partir de 0

    # Calculer les IDs précédent et suivant en mode circulaire
    previous_id = total_texts if id == 1 else id - 1
    next_id = 1 if id == total_texts else id + 1

    context = {
        "ai_title": generated_text.title,
        "subtitle": generated_text.subtitle,
        "question": generated_text.question,
        "com1": generated_text.com1,
        "com2": generated_text.com2,
        "com3": generated_text.com3,
        "theme1": generated_text.theme1,
        "theme2": generated_text.theme2,
        "theme3": generated_text.theme3,
        "previous_id": previous_id,
        "next_id": next_id,
    }

    return render(request, "user_view.html", context)

def signin_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Ajouter un message de succès
            messages.success(request, f"Welcome, {user.username}! You have successfully logged in.")
            
            return redirect('home')  # Redirige vers la page d'accueil
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('signin')  # Redirige vers la page de connexion

    return render(request, 'signin.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('signup')
        
        # Création de l'utilisateur
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False  # L'utilisateur est inactif par défaut
        user.save()

        # Générer un token pour l'activation
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(str(user.pk).encode())

        # Envoyer un email de confirmation
        subject = "Activate your account"
        message = render_to_string(
            'activation_email.html', {
                'user': user,
                'domain': get_current_site(request).domain,
                'uid': uid,
                'token': token,
            }
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )

        messages.success(request, 'Account created successfully. Please check your email to activate your account.')
        return redirect('signin')

    return render(request, 'signin.html')

def activate_user(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True  # Activer l'utilisateur
        user.save()
        messages.success(request, 'Your account has been activated successfully.')
        return redirect('signin')
    else:
        messages.error(request, 'Invalid activation link.')
        return redirect('signup')

def logout_view(request):
    logout(request)  # Déconnecter l'utilisateur
    return redirect('home')  # Rediriger vers la page d'accueil

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
        #"question": f"Génère une question en rapport avec le titre : '{ai_title}'. Ne mentionne rien d'autres que la question",
        #"com1": f"Donne moi trois mots au hasard en rapport avec le titre : '{ai_title}'. Ne mentionne rien d'autres que les trois mots",
        #"com2": f"Donne moi trois mots au hasard en rapport avec le titre : '{ai_title}'. Ne mentionne rien d'autres que les trois mots",
        #"com3": f"Donne moi trois mots au hasard en rapport avec le titre : '{ai_title}'. Ne mentionne rien d'autres que les trois mots",
        #"theme1": f"Génère un thème en rapport avec le titre : '{ai_title}'. Ne mentionne rien d'autres que le thème",
        #"theme2": f"Génère un autre thème en rapport avec le titre : '{ai_title}'. Ne mentionne rien d'autres que le thème",
        #"theme3": f"Génère un autre thème en rapport avec le titre : '{ai_title}'. Ne mentionne rien d'autres que le thème",
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
        question="",#ai_texts["question"],
        com1="",#ai_texts["com1"],
        com2="",#ai_texts["com2"],
        com3="",#ai_texts["com3"],
        theme1="",#ai_texts["theme1"],
        theme2="",#ai_texts["theme2"],
        theme3="",#ai_texts["theme3"],
        user_id = request.user,
    )

    print("🔍 Données envoyées au template:", ai_texts)

    return render(request, "page1.html", ai_texts)

def loading_view(request):
    return render(request, "loading.html")

