from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import requests
from django.shortcuts import render,redirect
from .models import Fase, Dominio, Pergunta, Alternativa, Respostas


def testeself(request):
    return render(request, "selfapp/test-app.html")
    #return render(request, "accounts/login.html")

# Testes Self Assessment...


def list_fase(request):
    # Vamos puxar todos os dados que estao em Dominio.
    nom_fase = Fase.objects.all()
    # Vamos passar todos os dados para o template, passando nome da variavel e o valor que será passado para ela.
    return render(request, 'selfapp/fase.html', {"nom_fase": nom_fase})


def list_dominio(request, id):
    # Vamos puxar todos os dados que estao em Dominio.
    nom_dominio = Dominio.objects.all()
    dominio_tex = nom_dominio.filter(fases_id=id)
    # Vamos passar todos os dados para o template, passando nome da variavel e o valor que será passado para ela.
    return render(request, 'selfapp/dominio.html', {"nom_dominio": dominio_tex})


@login_required(login_url='/auth/login')
def list_pergunta(request, id):
    # Vamos puxar todos os dados que estao em Dominio.
    nom_dominio = Dominio.objects.all()
    # filtrar dominio pelo id
    dominio_tex = nom_dominio.get(id=id)
    # Vamos puxar todos os dados que estao em Pergunta.
    pergunta_tex = Pergunta.objects.all()
    # filtrar perguntas pelo id
    pergunta_id = pergunta_tex.filter(dominio_id=id)
    # Retornando todas as alternativas
    alternativa = Alternativa.objects.all()

    resposta = []
    todas_respostas = Respostas.objects.all()
    if request.user.is_authenticated:
        usuario_id = request.user
    else:
        usuario_id = "Nao logado"

    # Percorrendo todas perguntas que ja estao filtradas por dominio, utilziando variavel ( pergunta_id )
    for item in pergunta_id:
        # Aqui estamos recebendo a pergunta que ja esta filtranda ( pergunta.id ), e usando o ID dessas perguntas ( item.id ) para retornar as alternativas referentes a essa pergunta
        alternativas_item = alternativa.filter(pergunta_id=item.id)
        obj = {
                "Pergunta": item,
                "Alternativas":alternativas_item,
                "Historico": ""
            }
        if(todas_respostas):
            historico = todas_respostas.filter(id_usuario=usuario_id.id)
            obj = {
                    "Pergunta": item,
                    "Alternativas": alternativas_item,
                    "Historico": historico
                }
        
        # print(alternativas_item)
        # print("---")
        resposta.append(obj)
        # print(resposta)
        # print("---")
        # print(dominio_tex)
    return render(request, 'selfapp/pergunta.html', {"resposta": resposta, "dominio_tex": dominio_tex})
    #return HttpResponse(historico)

@login_required(login_url='/auth/login')
def cad_resposta(request, id):
    # Vamos puxar todos os dados que estao em Pergunta.
    pergunta_tex = Pergunta.objects.all()
    # filtrar perguntas pelo id
    perguntas_por_dominio = pergunta_tex.filter(dominio_id=id)

    if request.user.is_authenticated:
        usuario_id = request.user
    else:
        usuario_id = "Nao logado"
    for item in perguntas_por_dominio:
        # Aqui estamos buscando no HTML os valores de rating referentes as perguntas que foram listadas anteriomente.

        existem_dados_cadastrais = Respostas.objects.filter(id_usuario=usuario_id, id_pergunta=item.id)
        if(existem_dados_cadastrais):
            existem_dados_cadastrais = Respostas.objects.get(id_usuario=usuario_id, id_pergunta=item.id)
            Atual_input = request.POST.get("atual-"+str(item.id))
            Desejado_input = request.POST.get("desejado-"+str(item.id))
            if(Atual_input == None and Desejado_input == None):
                existem_dados_cadastrais.estado_atual = None
                existem_dados_cadastrais.estado_desejado = None
            if(Atual_input != None and Desejado_input != None):
                Atual = Alternativa.objects.all()
                Atual = Atual.get(id=Atual_input)
                Desejado = Alternativa.objects.all()
                Desejado = Desejado.get(id=Desejado_input)
                existem_dados_cadastrais.estado_desejado = Desejado
                existem_dados_cadastrais.estado_atual = Atual

            if(Atual_input != None and Desejado_input == None):
                Atual = Alternativa.objects.all()
                Atual = Atual.get(id=Atual_input)
                existem_dados_cadastrais.estado_atual = Atual
                existem_dados_cadastrais.estado_desejado = None

            if(Atual_input == None and Desejado_input != None):
                Desejado = Alternativa.objects.all()
                Desejado = Desejado.get(id=Desejado_input)
                existem_dados_cadastrais.estado_desejado = Desejado
                existem_dados_cadastrais.estado_atual = None
            # Vamos dizer a pessoa que pegamos, que seu novo NOME e o valor contido em Vnome.
            
            # Salvo
            existem_dados_cadastrais.save()
        else:
            Atual_input = request.POST.get("atual-"+str(item.id))
            Desejado_input = request.POST.get("desejado-"+str(item.id))
            if(Atual_input != None and Desejado_input != None):
                Atual = Alternativa.objects.all()
                Atual = Atual.get(id=Atual_input)
                Desejado = Alternativa.objects.all()
                Desejado = Desejado.get(id=Desejado_input)
                Respostas.objects.create(
                    id_usuario=usuario_id, estado_atual=Atual, estado_desejado=Desejado,id_pergunta=item)

            if(Atual_input != None and Desejado_input == None):
                Atual = Alternativa.objects.all()
                Atual = Atual.get(id=Atual_input)
                Respostas.objects.create(id_usuario=usuario_id, estado_atual=Atual,id_pergunta=item)

            if(Atual_input == None and Desejado_input != None):
                Desejado = Alternativa.objects.all()
                Desejado = Desejado.get(id=Desejado_input)
                Respostas.objects.create(
                    id_usuario=usuario_id, estado_desejado=Desejado,id_pergunta=item)
            
            
            

    return redirect('fase')