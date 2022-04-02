
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def cadastro(request):
    try:
        nome = request.POST['nome']
        cpf = request.POST['cpf']
        email = request.POST['email']
        senha = request.POST['senha']
        confirmar = request.POST['confirmar']
    except (KeyError):
        return render(request, 'cadastro/cadastro.html')
    else:
        if(nome != '' and cpf  != '' and email != ''):
            if(senha == confirmar):
                user = User.objects.create_user(nome, email=email, password=senha)
                user.save()
                print(nome, email, senha)
        return render(request, 'cadastro/login.html')
    
def login(request):
    if request.method == 'POST':
        try:
            nome = request.POST['nome']
            senha = request.POST['senha']
        except (KeyError):
            return render(request, 'cadastro/erro.html')
        else:
            user = authenticate(username=nome, password=senha)
            if user:
                request.session['id_usuario'] = user.id
                return render(request, 'cadastro/carregando.html')
            return render(request, 'cadastro/erro.html')
    return render(request, 'cadastro/login.html')
