from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth


def cadastro (request):
    #print(request.META)
    #return HttpResponse('Olá mundo!')
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    
    elif request.method == 'POST':
        #print(request.POST)
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not senha == confirmar_senha:
            #print('AS SENHAS DIGITADAS NÃO CONFEREM!')
            messages.add_message(request, constants.ERROR, 'AS SENHAS DIGITADAS NÃO CONFEREM!')
            
            return redirect('/usuarios/cadastro')
        
        if len(senha) < 6:
            #print('TAMANHO DE SENHA MENOR DO 6 DÍGITOS!')
            messages.add_message(request, constants.ERROR, 'TAMANHO DE SENHA MENOR DO QUE 6 DÍGITOS!')

            return redirect('/usuarios/cadastro')
        
        users = User.objects.filter(username=username)
        
        if users.exists():
            #print('USUÁRIO JÁ EXISTE NO BANCO DE DADOS!')
            messages.add_message(request, constants.ERROR, 'USUÁRIO JÁ EXISTE NO BANCO DE DADOS!')

            return redirect('/usuarios/cadastro')
        
        user = User.objects.create_user(
            username=username,
            password=senha,

        )
        
        return redirect('/usuarios/logar')


def logar (request):
    if request.method == 'GET':
        return render(request, 'logar.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = auth.authenticate(request, username=username, password=senha)

        if user:
            auth.login(request, user)

            return redirect('/empresarios/cadastrar_empresa')
        
        messages.add_message(request, constants.ERROR, 'USUÁRIO E/OU SENHA INVÁLIDO(S)!')

        return redirect('/usuarios/logar')
