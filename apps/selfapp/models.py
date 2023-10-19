from django.db import models

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

    def __str__(self):
        return self.text_pergunta

class Alternativa(models.Model):
    text_alternativa = models.TextField(max_length=300)
    pergunta_id = models.ForeignKey("Pergunta", on_delete=models.CASCADE, related_name='pergunta')
    rating = models.TextField(max_length=50,default="TESTE")

    def __str__(self):
        return self.text_alternativa
