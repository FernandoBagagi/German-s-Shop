from datetime import datetime
from functools import total_ordering
from django.db import models
from django.contrib.auth.models import User


class Produto(models.Model):
    nome = models.CharField('Nome', max_length=100)
    preco = models.DecimalField('Preço', max_digits=7, decimal_places=2)
    descricao = models.TextField('Descrição')
    url_imagem = models.URLField('Url Imagem')
    categoria = models.CharField('Categoria', max_length=50)

    def __str__(self):
        return str(self.pk)


class Reclamacao(models.Model):
    titulo = models.CharField('Título', max_length=100)
    reclamacao = models.TextField('Reclamação')
    resposta = models.TextField('Resposta', null=True)
    data_pergunta = models.DateTimeField('Data Pergunta', default=datetime.now())
    data_resposta = models.DateTimeField('Data Resposta', null=True)

    def __str__(self):
        return str(self.pk) + ' ' + self.titulo


class Carrinho(models.Model):
    id_produto = models.ForeignKey(Produto, on_delete = models.CASCADE)
    id_usuario = models.ForeignKey(User, on_delete =  models.CASCADE)
    quantidade = models.CharField('Quantidade',max_length=100)

    def __str__(self):
        return str(self.id_produto) + ' ' + str(self.id_usuario) + ' ' + str(self.quantidade)


class Favorito(models.Model):
    id_usuario = models.ForeignKey(User, on_delete = models.CASCADE)
    id_produto = models.ForeignKey(Produto, on_delete = models.CASCADE)
    data_adicao = models.DateTimeField('Data da Adição na lista',default=datetime.now())
    
    def __str__(self):
        return str(self.id_usuario) + ' favoritou ' + str(self.id_produto)


class Compra(models.Model):
    id_usuario = models.ForeignKey(User, on_delete = models.CASCADE)
    data = models.DateTimeField("Data da compra", default= datetime.now())
    total = models.DecimalField('Total', max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.pk)


class CompraProduto(models.Model):
    id_produto = models.ForeignKey(Produto, on_delete = models.CASCADE)
    id_compra = models.ForeignKey(Compra, on_delete = models.CASCADE)
