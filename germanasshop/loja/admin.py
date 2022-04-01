from django.contrib import admin

from .models import Compra, CompraProduto, Reclamacao, Produto,Carrinho, Favorito

admin.site.register(Produto)
admin.site.register(Reclamacao)
admin.site.register(Carrinho)
admin.site.register(Favorito)
admin.site.register(Compra)
admin.site.register(CompraProduto)