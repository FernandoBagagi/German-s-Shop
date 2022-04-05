from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.conf import settings
from audioop import reverse
from django.http import HttpResponseRedirect    
from django.core.mail import send_mail
import random

def cadastro(request):
    if request.method == 'POST':
        try:
            nome = request.POST['nome']
            email = request.POST['email']
            senha = request.POST['senha']
            confirmar = request.POST['confirmar']
        except (KeyError):
            return HttpResponseRedirect('/cliente/erro')
        else:
            if(nome != '' and email != ''):
                if(senha == confirmar):
                    user = User.objects.create_user(nome, email=email, password=senha)
                    user.save()
                    return HttpResponseRedirect('/cliente/login')
                return HttpResponseRedirect('/clienteo/erro')
            return HttpResponseRedirect('/cliente/erro')
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
            return HttpResponseRedirect('/cliente/erro')
    return render(request, 'cadastro/login.html')


def recuperar_senha(request):
    if request.method == 'POST':
        try:
            nome = request.POST['nome']
            email = request.POST['email']
        except (KeyError):
            return HttpResponseRedirect('/cliente/erro')
        else:
            user = get_object_or_404(User, username=nome)
            if user:
                if user.email == email:
                    nova_senha = str(random.randrange(100000,999999))
                    mensagem = 'Olá, você optou por recuperar sua senha. Sua nova senha é ' + nova_senha + '.'
                    send_mail(
                        subject='Recuperação de senha',
                        message=mensagem,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[email]
                    )
                    user.set_password(nova_senha)
                    user.save()
                    return HttpResponseRedirect('/cliente/login')
            return HttpResponseRedirect('/cliente/erro')
    return render(request, 'cadastro/recuperar_senha.html')


def logout(request):
    if request.session.get('id_usuario', False):
        del request.session['id_usuario']
    return HttpResponseRedirect('/')


def erro(request):
     return render(request, 'cadastro/erro.html')