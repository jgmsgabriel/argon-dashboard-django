from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import requests
from django.shortcuts import render,redirect
from .models import Fase, Dominio, Pergunta, Alternativa, Respostas
from decimal import Decimal


def testeself(request):
    return render(request, "selfapp/test-app.html")
    #return render(request, "accounts/login.html")

# Testes Self Assessment...


@login_required(login_url='/auth/login')
def list_fase(request):
    # Vamos puxar todos os dados que estao em Dominio.
    nom_fase = Fase.objects.all()
    # Vamos passar todos os dados para o template, passando nome da variavel e o valor que será passado para ela.
    lista_de_dominios = []

    # Vamos puxar todos os dados que estao em Dominio.
    dominio_tex = Dominio.objects.all()
    todas_respostas = Respostas.objects.all()
    if request.user.is_authenticated:
        usuario_id = request.user
    else:
        usuario_id = "Nao logado"
    respostas_por_usuario = todas_respostas.filter(id_usuario=usuario_id)
    numero_de_perguntas_respondidas = 0
    for res in respostas_por_usuario:
        if res.estado_atual !=None and res.estado_desejado != None:
            numero_de_perguntas_respondidas+=2
        elif res.estado_atual ==None and res.estado_desejado != None:
            numero_de_perguntas_respondidas+=1
        elif res.estado_atual !=None and res.estado_desejado == None:
            numero_de_perguntas_respondidas+=1
    
    final = []
    aux = []
    todas_perguntas = Pergunta.objects.all()
    numero_de_perguntas_total = len(todas_perguntas) * 2
    total_porcento_concluido = (numero_de_perguntas_respondidas/numero_de_perguntas_total)*100
    for item in dominio_tex:
        obj_dom_aux = {
            "id_dominio": item.id,
            "nome_dominio": item.nom_Dominio
        }
        lista_de_dominios.append(obj_dom_aux)
        pergunta_por_dominio = todas_perguntas.filter(dominio_id = item)
        for perg in pergunta_por_dominio:
            respostas_por_dominio = respostas_por_usuario.filter(id_pergunta =perg)
            aux_numero_de_respostas = 0
            if respostas_por_dominio:
                if respostas_por_dominio[0].estado_atual !=None and respostas_por_dominio[0].estado_desejado !=None:
                    aux_numero_de_respostas += 2
                    obj={
                        "valor_rating": respostas_por_dominio[0].estado_atual.valor_rating,
                        "rating_desejado": respostas_por_dominio[0].estado_desejado.valor_rating,
                        "pergunta": respostas_por_dominio[0].id_pergunta.text_pergunta,
                        "dominio": respostas_por_dominio[0].id_pergunta.dominio_id.nom_Dominio,
                        "dominio_id": respostas_por_dominio[0].id_pergunta.dominio_id.id,
                        "numero_perguntas_total": len(pergunta_por_dominio)
                    }
                elif respostas_por_dominio[0].estado_atual == None and respostas_por_dominio[0].estado_desejado !=None:
                    aux_numero_de_respostas += 1
                    obj={
                        "valor_rating": 0,
                        "rating_desejado": respostas_por_dominio[0].estado_desejado.valor_rating,
                        "pergunta": respostas_por_dominio[0].id_pergunta.text_pergunta,
                        "dominio": respostas_por_dominio[0].id_pergunta.dominio_id.nom_Dominio,
                        "dominio_id": respostas_por_dominio[0].id_pergunta.dominio_id.id,
                        "numero_perguntas_total": len(pergunta_por_dominio)
                    }
                elif respostas_por_dominio[0].estado_atual != None and respostas_por_dominio[0].estado_desejado ==None:
                    aux_numero_de_respostas += 1
                    obj={
                        "valor_rating": respostas_por_dominio[0].estado_atual.valor_rating,
                        "rating_desejado": 0,
                        "pergunta": respostas_por_dominio[0].id_pergunta.text_pergunta,
                        "dominio": respostas_por_dominio[0].id_pergunta.dominio_id.nom_Dominio,
                        "dominio_id": respostas_por_dominio[0].id_pergunta.dominio_id.id,
                        "numero_perguntas_total": len(pergunta_por_dominio)
                    }
                elif respostas_por_dominio[0].estado_atual == None and respostas_por_dominio[0].estado_desejado ==None:
                    obj={
                        "valor_rating": 0,
                        "rating_desejado": 0,
                        "pergunta": respostas_por_dominio[0].id_pergunta.text_pergunta,
                        "dominio": respostas_por_dominio[0].id_pergunta.dominio_id.nom_Dominio,
                        "dominio_id": respostas_por_dominio[0].id_pergunta.dominio_id.id,
                        "numero_perguntas_total": len(pergunta_por_dominio)
                    }
                obj['respostas']= aux_numero_de_respostas
                aux.append(obj)
        final.append(aux)
        aux=[]
    fin = []
    cont =0
    for resp_por_dominio in final:
        cont+=1
        somatoria_atual = 0
        somatoria_desejado = 0
        aux_perg_total = 1
        dominio_id = 0
        nome_dominio = ""
        respostas_por_dominio_percento=0
        if resp_por_dominio:
            for resp in resp_por_dominio:
                respostas_por_dominio_percento += resp["respostas"]
                somatoria_atual += resp["valor_rating"]
                somatoria_desejado += resp["rating_desejado"]
                aux_perg_total = resp["numero_perguntas_total"]
                dominio_id = resp["dominio_id"]
                nome_dominio = resp["dominio"]
        else:
            #respostas_por_dominio_percento += resp["respostas"]
            dominio_id = lista_de_dominios[cont-1]["id_dominio"]
            nome_dominio = lista_de_dominios[cont-1]["nome_dominio"]

        aux_response = (respostas_por_dominio_percento/(aux_perg_total*2))*100
        porcentagem_atual = somatoria_atual/(aux_perg_total*4)
        porcentagem_desejado = somatoria_desejado/(aux_perg_total*4)
        dado_grafico_atual = porcentagem_atual*4
        dado_grafico_desejado = porcentagem_desejado*4
        estado_cliente = ""
        if porcentagem_atual < 0.25:
            estado_cliente = "Foundational"
        elif porcentagem_atual < 0.5:
            estado_cliente = "Crawl"
        elif porcentagem_atual < 0.75:
            estado_cliente = "Walk"
        else:
            estado_cliente = "Run"
        
        obj = {
            "porcentagem": round(porcentagem_atual*100,2),
            "estado_cliente": estado_cliente,
            "somatoria_atual": somatoria_atual,
            "dominio_id": dominio_id,
            "nome_dominio": nome_dominio,
            "dado_grafico_atual": round(dado_grafico_atual,2),
            "dado_grafico_desejado": round(dado_grafico_desejado,2),
            "porcentagem_respondida": round(aux_response,2)
        }
        fin.append(obj)
    total_porcento_concluido = round(total_porcento_concluido,2)
    
    porcentagem_por_fase=[]
    
    for fas in nom_fase:
        cont_pos=0
        aux_cont_por_fase =0
        for item in fin:
            dominio_atual = Dominio.objects.all()
            dominio_atual = dominio_atual.filter(id=item['dominio_id'])
            if dominio_atual:
                if dominio_atual[0].fases_id == fas:
                    cont_pos+=1
                    aux_cont_por_fase += Decimal(item['porcentagem'])

        aux_cont_por_fase = aux_cont_por_fase/cont_pos
        estado_cliente = ""
        if aux_cont_por_fase < 25:
            estado_cliente = "Foundational"
        elif aux_cont_por_fase < 50:
            estado_cliente = "Crawl"
        elif aux_cont_por_fase < 75:
            estado_cliente = "Walk"
        else:
            estado_cliente = "Run"
        obj_porc_fase={
            'porcentagem': round(aux_cont_por_fase,2),
            "estado_cliente": estado_cliente,
            'fase': fas.nom_fases,
            'id_fase': fas.id,
            'dado_grafico': round(aux_cont_por_fase*4/100,2),
        }
        porcentagem_por_fase.append(obj_porc_fase)

    porcentagem_total = 0
    cont_pos = 0
    for item in porcentagem_por_fase:
        cont_pos += 1
        porcentagem_total += item['porcentagem']
    
    porcentagem_total = round(porcentagem_total/cont_pos,2)
    estado_cliente = ""
    if porcentagem_total < 25:
        estado_cliente = "Foundational"
    elif porcentagem_total < 50:
        estado_cliente = "Crawl"
    elif porcentagem_total < 75:
        estado_cliente = "Walk"
    else:
        estado_cliente = "Run"
    dados_organizacional = {
        'porcentagem': porcentagem_total,
        'estado_cliente': estado_cliente
    }


    data = Respostas.objects.all()

    # Vamos passar todos os dados para o template, passando nome da variavel e o valor que será passado para ela.
    #return render(request, 'dominio.html', {"nom_dominio": dominio_tex, "teste_respostas": fin} )
    return render(request, 'selfapp/selfpage.html', {'teste':data,'porcentagem_total':dados_organizacional,'porcentagem_por_fase':porcentagem_por_fase,"nom_dominio": dominio_tex, "home_respostas": fin, "nom_fase": nom_fase, "porcento_concluido": total_porcento_concluido})



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
    dominio_anterior = -1
    dominio_proximo = -1
    dominio_anterior_nom = ""
    dominio_proximo_nom = ""
    cont = 0
    tam = len(nom_dominio)
    for item in nom_dominio:
        if item.id == dominio_tex.id:
            break
        dominio_anterior = item.id
        dominio_anterior_nom = item.nom_Dominio
        cont += 1

    if cont+1 < tam:
        dominio_proximo = nom_dominio[cont+1].id
        dominio_proximo_nom = nom_dominio[cont+1].nom_Dominio

    link_botoes = {
        'dominio_anterior': dominio_anterior,
        'dominio_anterior_nom': dominio_anterior_nom,
        'proximo_dominio': dominio_proximo,
        'dominio_proximo_nom': dominio_proximo_nom
    }


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
    return render(request, 'selfapp/pergunta.html', {"paginacao": link_botoes,"resposta": resposta, "dominio_tex": dominio_tex})
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
            
           # aux = str(timezone.now)
            #aux = strptime(aux, "YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]")
            #existem_dados_cadastrais.data_time = aux
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