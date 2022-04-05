from django.urls import path
from . import views

app_name = 'loja'
urlpatterns = [
    path('', views.index, name='inicio'),
    path('produto/<int:id_produto>/cadastrar/',views.cadastro_produto,name='cadastro_produto'),
    path('forum/', views.forum, name='forum'),
    path('cesta/', views.cesta, name='cesta'),
    path('produto/<int:id_produto>/', views.produto, name='produto'),
    path('produto/json/', views.produto_json, name='produto_json'),
    path('produto/json/<int:id_produto>', views.produto_json_by_id, name='produto_json_by_id'),
    path('historico/', views.historico, name='historico'),
    path('comprar/', views.compras,name='comprar'),
    path('favoritar/<int:id_produto>', views.favoritar,name='favoritar'),
    path('logout/', views.logout, name='logout'),
]