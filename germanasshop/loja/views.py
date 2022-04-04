from audioop import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from matplotlib.style import context
from .models import Carrinho, Compra, CompraProduto, Favorito, Produto, Reclamacao
from django.contrib.auth.models import User


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
    autenticado = False
    user = None
    if request.session.get('id_usuario', False):
        autenticado = True
        user = get_object_or_404(User, pk=request.session['id_usuario'])
        lista_favoritos = []
        favoritos = Favorito.objects.order_by('data_adicao')
        for favorito in favoritos:
            if favorito.id_usuario.username == user.username:
                produto_aux = get_object_or_404(Produto, pk=favorito.id_produto.pk)
                lista_favoritos.append(produto_aux)
        secoes.insert(0, Secao(titulo='Seus favoritos', lista_produtos=lista_favoritos))
    context = {'secoes': secoes, 'autenticado': autenticado, 'user': user}
    return render(request, 'loja/index.html', context)


def forum(request):
    reclamacoes = Reclamacao.objects.order_by('data_pergunta').reverse()
    context = {'reclamacoes': reclamacoes}
    try:
        titulo = request.POST['titulo']
        reclamacao = request.POST['reclamacao']
    except (KeyError):
        return render(request, 'loja/forum.html', context)
    else:
        nova_reclamacao = Reclamacao(
            titulo=titulo, reclamação=reclamacao, resposta=None, data_resposta=None)
        print(nova_reclamacao)
        nova_reclamacao.save()
        reclamacoes = Reclamacao.objects.order_by('data_pergunta').reverse()
        context = {'reclamacoes': reclamacoes}
        return render(request, 'loja/forum.html', context)


def cesta(request):
    if request.session.get('id_usuario', False):
        user = get_object_or_404(User, pk=request.session['id_usuario'])
        carrinho = Carrinho.objects.all()
        lista_produtos = []

        for items in carrinho:
            if items.id_usuario.username == user.username:
                produto_aux = get_object_or_404(
                    Produto, pk=items.id_produto.pk)
                lista_produtos.append(produto_aux)
        context = {'lista_produtos': lista_produtos}
        return render(request, 'loja/cesta.html', context)
    return HttpResponseRedirect('/cliente/login/')


def cadastro_produto(request, id_produto):
    if request.session.get('id_usuario', False):
        produto = get_object_or_404(Produto, pk=id_produto)
        user = get_object_or_404(User, pk=request.session['id_usuario'])
        C = Carrinho(id_produto=produto, id_usuario=user, quantidade=1)
        C.save()
        return HttpResponseRedirect('/cesta')
    return HttpResponseRedirect('/cliente/login/')


def produto(request, id_produto):
    produto = get_object_or_404(Produto, pk=id_produto)
    context = {'produto': produto}
    user_id = request.session.get('id_usuario', None)
    context['user_id'] = user_id
    estaFavoritado = False
    if user_id:
        user = get_object_or_404(User, pk=request.session['id_usuario'])
        favoritos_usuario = Favorito.objects.filter(id_usuario=user)
        for favs in favoritos_usuario:
            if favs.id_produto == produto:
                estaFavoritado = True
    context['estaFavoritado'] = estaFavoritado
    return render(request, 'loja/produto.html', context)


def logout(request):
    if request.session.get('id_usuario', False):
        del request.session['id_usuario']
    return HttpResponseRedirect('/')


class CompraModel:
    def __init__(self, total, data, lista_produtos):
        self.total = total
        self.data = data
        self.lista_produtos = lista_produtos


def historico(request):
    if request.session.get('id_usuario', False):
        lista_compras = []
        user = get_object_or_404(User, pk=request.session['id_usuario'])
        compras = Compra.objects.all()
        for compra in compras:
            if compra.id_usuario.username == user.username:
                CP_list = CompraProduto.objects.all()
                lista_produtos = []
                for CP in CP_list:
                    if CP.id_compra.pk == compra.pk:
                        produto = get_object_or_404(
                            Produto, pk=CP.id_produto.pk)
                        lista_produtos.append(produto)
                c = CompraModel(total=compra.total, data=compra.data,
                                lista_produtos=lista_produtos)
                lista_compras.append(c)

        context = {"compras": lista_compras}
        return render(request, 'loja/historico.html', context=context)
    return HttpResponseRedirect('/cliente/login/')


def compras(request):
    if request.session.get('id_usuario', False):
        user = get_object_or_404(User, pk=request.session['id_usuario'])
        carrinho = Carrinho.objects.all()
        lista_produtos = []

        for items in carrinho:
            if items.id_usuario.username == user.username:
                produto_aux = get_object_or_404(
                    Produto, pk=items.id_produto.pk)
                lista_produtos.append(produto_aux)
        total_compra = 0.0
        for prod in lista_produtos:
            total_compra += float(prod.preco)
        compra = Compra(id_usuario=user, total=total_compra)
        compra.save()
        for produto in lista_produtos:
            compra_produto = CompraProduto(
                id_produto=produto, id_compra=compra)
            compra_produto.save()
        Carrinho.objects.filter(id_usuario=user).delete()
        return HttpResponseRedirect('/historico/')
    return HttpResponseRedirect('/cliente/login/')


def favoritar(request, id_produto):
    if request.session.get('id_usuario', False):
        user = get_object_or_404(User, pk=request.session['id_usuario'])
        produto = get_object_or_404(Produto, pk=id_produto)
        favoritos_usuario = Favorito.objects.filter(id_usuario=user)
        for favs in favoritos_usuario:
            if favs.id_produto == produto:
                favs.delete()
                break
        else:
            favorito = Favorito(id_produto=produto, id_usuario=user)
            favorito.save()
        return HttpResponseRedirect('/produto/' + str(id_produto))
    else:
        print('Não Favorita')
        return HttpResponseRedirect('/cliente/login/')
