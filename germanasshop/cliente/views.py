
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from audioop import reverse
from django.http import HttpResponseRedirect    
def cadastro(request):
    if request.method == 'POST':
        try:
            nome = request.POST['nome']
            email = request.POST['email']
            senha = request.POST['senha']
            confirmar = request.POST['confirmar']
        except (KeyError):
            return render(request, 'cadastro/erro.html')
        else:
            if(nome != '' and email != ''):
                if(senha == confirmar):
                    user = User.objects.create_user(nome, email=email, password=senha)
                    user.save()
                    print(nome, email, senha)
                    return HttpResponseRedirect('/cliente/login')
                return render(request, 'cadastro/erro.html')
            return render(request, 'cadastro/erro.html')
    return render(request, 'cadastro/cadastro.html')
    
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
                return HttpResponseRedirect('/')
            return render(request, 'cadastro/erro.html')
    return render(request, 'cadastro/login.html')

def recuperar_senha(request):
    send_mail(
        'Teste',
        'ola',
        settings.EMAIL_HOST_USER,
        ['1234contasdejogos1234@gmail.com'],
        fail_silently=False,
    )