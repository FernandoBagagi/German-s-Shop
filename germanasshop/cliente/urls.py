from django.urls import path
from django.contrib.auth import views as auth_view
from . import views

app_name = 'cliente'
urlpatterns = [
    path("cadastro/", views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    
]
