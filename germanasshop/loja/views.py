from audioop import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from matplotlib.style import context
from .models import Carrinho, Favorito, Produto, Reclamacao
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
            secoes.append(Secao(titulo=produto.categoria,
                          lista_produtos=[produto]))
        else:
            for secao in secoes:
                if secao.titulo == produto.categoria:
                    secao.lista_produtos.append(produto)
    autenticado = False
    user = None
    if request.session.get('id_usuario', False):
        autenticado = True
        user = get_object_or_404(User, pk=request.session['id_usuario'])
        print(request.session['id_usuario'])
        lista_favoritos = []
        favoritos = Favorito.objects.order_by('data_adicao')
        for favorito in favoritos:
            if favorito.id_usuario.username == user.username:
                produto_aux = get_object_or_404(Produto, pk=favorito.id_produto.pk)
                lista_favoritos.append(produto_aux)
        secoes.insert(0, Secao(titulo='Seus favoritos', lista_produtos=lista_favoritos))
    context = {'secoes': secoes, 'autenticado':autenticado, 'user':user}
    return render(request, 'loja/index.html', context)


def forum(request):
    reclamacoes = Reclamacao.objects.order_by('data_pergunta').reverse()
    context = {'reclamacoes': reclamacoes}
    try:
        titulo = request.POST['titulo']
        reclamacao = request.POST['reclamacao']
    except (KeyError):
        print('Entra aqui')
        return render(request, 'loja/forum.html', context)
    else:
        nova_reclamacao = Reclamacao(titulo=titulo, reclamação=reclamacao, resposta= None, data_resposta=None)
        print(nova_reclamacao)
        nova_reclamacao.save()
        reclamacoes = Reclamacao.objects.order_by('data_pergunta').reverse()
        context = {'reclamacoes': reclamacoes}
        return render(request, 'loja/forum.html', context)


def cesta(request):     
    if  request.session.get('id_usuario', False):
        user = get_object_or_404(User, pk=request.session['id_usuario'])
        carrinho = Carrinho.objects.all() 
        lista_produtos = []
        
        for items in carrinho:
            if items.id_usuario.username == user.username:
                produto_aux = get_object_or_404(Produto, pk=items.id_produto.pk)
                lista_produtos.append(produto_aux)
        context = {'lista_produtos':lista_produtos}
        return render(request, 'loja/cesta.html',context)
    return render(request,'cadastro/login.html') 
     
def cadastro_produto(request,id_produto):
    if request.session.get('id_usuario', False):
         produto = get_object_or_404(Produto, pk=id_produto)
         user = get_object_or_404(User, pk=request.session['id_usuario'])
         C = Carrinho(id_produto=produto, id_usuario = user,quantidade=1)
         C.save()
         context= {'id_produto':id_produto}
         return render(request, 'loja/cesta.html')
    return render(request,'cadastro/login.html')

def produto(request, id_produto):
    produto = get_object_or_404(Produto, pk=id_produto)
    context = {}
    context['produto'] = produto
    return render(request, 'loja/produto.html', context)

def historico(request):
    return render(request, 'loja/historico.html')

def logout(request):
    if  request.session.get('id_usuario', False):
        del request.session['id_usuario']
    return HttpResponseRedirect('/')