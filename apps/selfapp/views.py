from django.http import HttpResponse
import requests
from django.shortcuts import render,redirect
from .models import Fase, Dominio, Pergunta, Alternativa


def testeself(request):
    return render(request, "selfapp/test-app.html")
    #return render(request, "accounts/login.html")

#Testes Self Assessment...

def list_fase(request):
    #Vamos puxar todos os dados que estao em Dominio.
    nom_fase = Fase.objects.all()
    #Vamos passar todos os dados para o template, passando nome da variavel e o valor que será passado para ela.
    return render(request, 'selfapp/fase.html', {"nom_fase": nom_fase})


def list_dominio(request, id):
    #Vamos puxar todos os dados que estao em Dominio.
    nom_dominio = Dominio.objects.all()
    dominio_tex = nom_dominio.filter(fases_id=id)
    #Vamos passar todos os dados para o template, passando nome da variavel e o valor que será passado para ela.
    return render(request, 'selfapp/dominio.html', {"nom_dominio": dominio_tex})

def list_pergunta(request, id):
    #Vamos puxar todos os dados que estao em Dominio.
    nom_dominio = Dominio.objects.all()
    #filtrar dominio pelo id
    dominio_tex = nom_dominio.get(id=id)
    #Vamos puxar todos os dados que estao em Pergunta.
    pergunta_tex = Pergunta.objects.all()
    #filtrar perguntas pelo id
    pergunta_id = pergunta_tex.filter(dominio_id=id)
    #Retornando todas as alternativas
    alternativa = Alternativa.objects.all()

    resposta = []
    #Percorrendo todas perguntas que ja estao filtradas por dominio, utilziando variavel ( pergunta_id )
    for item in pergunta_id:
        #Aqui estamos recebendo a pergunta que ja esta filtranda ( pergunta.id ), e usando o ID dessas perguntas ( item.id ) para retornar as alternativas referentes a essa pergunta
        alternativas_item = alternativa.filter(pergunta_id=item.id)
        obj = {
            "Pergunta": item,
            "Alternativas": alternativas_item
        }
        #print(alternativas_item)
        #print("---")
        resposta.append(obj)
        #print(resposta)
        #print("---")
        #print(dominio_tex)
    return render(request, 'selfapp/pergunta.html', {"resposta": resposta,"dominio_tex": dominio_tex})
    
    
    #return HttpResponse(resposta)
    #Vamos passar todos os dados para o template, passando nome da variavel e o valor que será passado para ela.
    #return render(request, 'pergunta.html', {"pergunta_tex": pergunta_tex})
