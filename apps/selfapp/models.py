from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.
#Testes Self Assessment...
# 1 - Criando as tabelas.
class Fase(models.Model):
    nom_fases = models.CharField(max_length=100)

    def __str__(self):
        return self.nom_fases

# Estamos definindo relacionamentos entre as tabelas de 1 : N 
# related_name permite que façamos pesquisas inversas mais facilmente.
class Dominio(models.Model):
    nom_Dominio = models.CharField(max_length=100)
    fases_id = models.ForeignKey("Fase", on_delete=models.CASCADE, related_name='fase')

    def __str__(self):
        return self.nom_Dominio

class Pergunta(models.Model):
    text_pergunta = models.TextField(max_length=300)
    dominio_id = models.ForeignKey("Dominio", on_delete=models.CASCADE, related_name='dominio')
    descricao = models.TextField(max_length=400,null=True,default="Descrição - Pergunta")
    link_doc = models.TextField(max_length=300,null=True,default="https://www.z-act.io/")

    def __str__(self):
        return self.text_pergunta

class Alternativa(models.Model):
    text_alternativa = models.TextField(max_length=300)
    pergunta_id = models.ForeignKey("Pergunta", on_delete=models.CASCADE, related_name='pergunta')
    rating = models.TextField(max_length=50,default="TESTE")
    valor_rating = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0.00))


    def __str__(self):
        return self.text_alternativa
    
class Respostas(models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_time = models.DateTimeField(auto_now=True)
    id_pergunta = models.ForeignKey("Pergunta", on_delete=models.CASCADE, related_name='pergunta_resposta', null=True)
    estado_atual = models.ForeignKey("Alternativa", on_delete=models.CASCADE, related_name='alternativa_atual',null=True)
    estado_desejado = models.ForeignKey("Alternativa", on_delete=models.CASCADE, related_name='alternativa_desejada',null=True)

    def __str__(self):
        return self.id_pergunta.text_pergunta