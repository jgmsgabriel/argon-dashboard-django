# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from decimal import Decimal
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from apps.selfapp.models import Fase, Dominio, Pergunta, Alternativa, Respostas

def testhome(request):
    #return render(request, "home/test-home.html")
    return HttpResponse("test2")

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))



@login_required(login_url="/login/")
def home_portal(request):
    if request.user.is_authenticated:
        usuario_id = request.user
    else:
        usuario_id = "Nao logado"
    fases = Fase.objects.all()
    dominios = Dominio.objects.all()
    perguntas = Pergunta.objects.all()
    respostas = Respostas.objects.all()
    qtd_respostas = 0
    dados_fase = []
    for fase in fases:
        dominios_fase = dominios.filter(fases_id=fase.id)
        qtd_perguntas_fase = 0
        qtd_pontos_fase = 0
        for dominio in dominios_fase:
            pergunta_dominio = perguntas.filter(dominio_id=dominio.id)
            for pergunta in pergunta_dominio:
                qtd_perguntas_fase+=1
                resposta = respostas.filter(id_pergunta=pergunta.id, id_usuario=usuario_id)
                if resposta:
                    if resposta[0].estado_atual!=None:
                        qtd_pontos_fase += resposta[0].estado_atual.valor_rating
                        qtd_respostas +=1

        porcentagem_fase = qtd_pontos_fase/(qtd_perguntas_fase*4)*100
        estado_cliente = ""
        if porcentagem_fase < 25:
            estado_cliente = "Foundational"
        elif porcentagem_fase < 50:
            estado_cliente = "Crawl"
        elif porcentagem_fase < 75:
            estado_cliente = "Walk"
        else:
            estado_cliente = "Run"
        obj = {
            "Fase": fase.nom_fases,
            "Porcentagem": round(porcentagem_fase,2),
            "Estado": estado_cliente
        }
        dados_fase.append(obj)
    
    porcentagem_org =0
    for dado in dados_fase:
        porcentagem_org+=Decimal(dado['Porcentagem'])
    porcentagem_org = porcentagem_org/len(dados_fase)
    estado_cliente_org = ""
    if porcentagem_fase < 25:
        estado_cliente_org = "Foundational"
    elif porcentagem_fase < 50:
        estado_cliente_org = "Crawl"
    elif porcentagem_fase < 75:
        estado_cliente_org = "Walk"
    else:
        estado_cliente_org = "Run"
    
    dados_organizacao = {
        "Fase": "ORGANIZATIONAL MATURITY",
        "Porcentagem": round(porcentagem_org,2),
        "Estado": estado_cliente_org
    }
    
    return render(request,'home/home-portal.html', {'dados_fase': dados_fase,'dados_org':dados_organizacao, 'cond_bloco_asses':qtd_respostas})


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
