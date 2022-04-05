from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Carrinho, Compra, CompraProduto, Favorito, Produto, Reclamacao
from django.contrib.auth.models import User
import requests

class Secao:
    def __init__(self, titulo, lista_produtos=[]):
        self.titulo = titulo
        self.lista_produtos = lista_produtos


def index(request):
    produtos = Produto.objects.all()
    secoes = []
    for produto in produtos:
        nomes_secoes = [secao.titulo for secao in secoes]
        if not produto.categoria in nomes_secoes:
            secoes.append(Secao(titulo=produto.categoria, lista_produtos=[produto]))
        else:
            for secao in secoes:
                if secao.titulo == produto.categoria:
                    secao.lista_produtos.append(produto)
    user = None
    if request.session.get('id_usuario', False):
        user = get_object_or_404(User, pk=request.session['id_usuario'])
        lista_favoritos = []
        favoritos = Favorito.objects.filter(id_usuario=user.pk).order_by('data_adicao').reverse()
        for favorito in favoritos:
            produto_aux = get_object_or_404(Produto, pk=favorito.id_produto.pk)
            lista_favoritos.append(produto_aux)
        secoes.insert(0, Secao(titulo='Seus favoritos', lista_produtos=lista_favoritos))
    context = {'secoes': secoes, 'user': user}
    return render(request, 'loja/index.html', context)


def forum(request):
    if request.method == 'POST':
        try:
            titulo = request.POST['titulo']
            reclamacao = request.POST['reclamacao']
        except (KeyError):
            return HttpResponseRedirect('/clienteo/erro')
        else:
            nova_reclamacao = Reclamacao(titulo=titulo, reclamacao=reclamacao, resposta=None, data_resposta=None)
            nova_reclamacao.save()
    reclamacoes = Reclamacao.objects.order_by('data_pergunta').reverse()    
    context = {'reclamacoes': reclamacoes}
    return render(request, 'loja/forum.html', context)


def cesta(request):
    if request.session.get('id_usuario', False):
        user = get_object_or_404(User, pk=request.session['id_usuario'])
        carrinho = Carrinho.objects.filter(id_usuario = user.pk)
        lista_produtos = []
        for item in carrinho:
            produto = get_object_or_404(Produto, pk=item.id_produto.pk)
            lista_produtos.append(produto)
        context = {'lista_produtos': lista_produtos}
        return render(request, 'loja/cesta.html', context)
    return HttpResponseRedirect('/cliente/login/')


def cadastro_produto(request, id_produto):
    if request.session.get('id_usuario', False):
        produto = get_object_or_404(Produto, pk=id_produto)
        user = get_object_or_404(User, pk=request.session['id_usuario'])
        carrinho = Carrinho(id_produto=produto, id_usuario=user, quantidade=1)
        carrinho.save()
        return HttpResponseRedirect('/cesta')
    return HttpResponseRedirect('/cliente/login/')


def produto(request, id_produto):
    produto = get_object_or_404(Produto, pk=id_produto)
    user_id = request.session.get('id_usuario', None)
    estaFavoritado = False
    if user_id:
        user = get_object_or_404(User, pk=request.session['id_usuario'])
        favoritos_usuario = Favorito.objects.filter(id_usuario=user)
        for favorito in favoritos_usuario:
            if favorito.id_produto == produto:
                estaFavoritado = True
    #API Cotação de Moedas
    response = requests.get('http://economia.awesomeapi.com.br/json/last/USD-BRL')
    cotacao = (float(response.json()['USD']['high']) + float(response.json()['USD']['low'])) / 2.0
    preco_dolar = float(produto.preco) / cotacao
    preco_dolar = format(preco_dolar,'.2f')
    context = {'produto': produto, 'user_id' : user_id, 'estaFavoritado' : estaFavoritado, 'preco_dolar': preco_dolar}
    return render(request, 'loja/produto.html', context)


class CompraModel:
    def __init__(self, pk, total, data, lista_produtos):
        self.pk = pk
        self.total = total
        self.data = data
        self.lista_produtos = lista_produtos


def historico(request):
    if request.session.get('id_usuario', False):
        lista_compras = []
        user = get_object_or_404(User, pk=request.session['id_usuario'])
        compras = Compra.objects.filter(id_usuario=user.pk).order_by('data').reverse()
        for compra in compras:
            produtos_compra = CompraProduto.objects.filter(id_compra=compra.pk)
            ids_produtos = [produto_compra.id_produto for produto_compra in produtos_compra]
            lista_produtos = []
            for id_produto in ids_produtos:
                produto = get_object_or_404(Produto, pk=id_produto.pk)
                lista_produtos.append(produto)
            nova_compra = CompraModel(pk=compra.pk, total=compra.total, data=compra.data,lista_produtos=lista_produtos)
            lista_compras.append(nova_compra)
        context = {"compras": lista_compras}
        return render(request, 'loja/historico.html', context=context)
    return HttpResponseRedirect('/cliente/login/')


def compras(request):
    if request.session.get('id_usuario', False):
        user = get_object_or_404(User, pk=request.session['id_usuario'])
        carrinho = Carrinho.objects.filter(id_usuario = user.pk)
        ids_produtos = [produto_compra.id_produto for produto_compra in carrinho]
        lista_produtos = []
        for id_produto in ids_produtos:
            produto = get_object_or_404(Produto, pk=id_produto.pk)
            lista_produtos.append(produto)
        total_compra = 0.0
        for produto in lista_produtos:
            total_compra += float(produto.preco)
        compra = Compra(id_usuario=user, total=total_compra)
        compra.save()
        for produto in lista_produtos:
            compra_produto = CompraProduto(id_produto=produto, id_compra=compra)
            compra_produto.save()
        carrinho.delete()
        return HttpResponseRedirect('/historico/')
    return HttpResponseRedirect('/cliente/login/')


def favoritar(request, id_produto):
    if request.session.get('id_usuario', False):
        user = get_object_or_404(User, pk=request.session['id_usuario'])
        produto = get_object_or_404(Produto, pk=id_produto)
        favoritos_usuario = Favorito.objects.filter(id_usuario=user)
        for favoritos in favoritos_usuario:
            if favoritos.id_produto == produto:
                favoritos.delete()
                break
        else:
            favorito = Favorito(id_produto=produto, id_usuario=user)
            favorito.save()
        return HttpResponseRedirect('/produto/' + str(id_produto))
    else:
        return HttpResponseRedirect('/cliente/login/')


def produto_json(request):
    data = {'produtos':list(Produto.objects.values())}
    return JsonResponse(data, safe=False)


def produto_json_by_id(request, id_produto):
    data = {'produto':list(Produto.objects.filter(pk=id_produto).values())}
    return JsonResponse(data, safe=False)
