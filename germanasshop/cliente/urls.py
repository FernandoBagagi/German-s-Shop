from django.urls import path
from django.contrib.auth import views as auth_view
from . import views

app_name = 'cliente'
urlpatterns = [
    path("cadastro/", views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('recuperar_senha/', views.recuperar_senha, name='recuperar_senha'),
    path('erro/', views.erro, name='erro'),
    path('logout/', views.logout, name='logout'),
]
