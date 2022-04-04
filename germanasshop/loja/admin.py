from django.contrib import admin
from .models import Compra, CompraProduto, Reclamacao, Produto,Carrinho, Favorito

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'categoria')

@admin.register(Reclamacao)
class ReclamacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_pergunta', 'data_resposta')

@admin.register(Carrinho)
class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ('id_produto', 'id_usuario', 'quantidade')

@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'id_produto', 'data_adicao')

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'data', 'total')

@admin.register(CompraProduto)
class CompraProduto(admin.ModelAdmin):
    list_display = ('id_produto', 'id_compra',)

