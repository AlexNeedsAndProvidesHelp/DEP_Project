from django.urls import path
from . import views

urlpatterns =[
    
    path("",views.home,name="home"),
    path("home",views.home),
    path("calendar", views.calendar_view, name='calendar'),
    path("page1", views.page1_view, name="page1"),
    path("logs", views.logs_view, name="logs"),
    path("generated_texts/<int:id>", views.generated_texts_view, name="generated_texts"),
    path("help", views.help_view, name="help"),

]