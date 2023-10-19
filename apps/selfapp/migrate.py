from selfapp.models import usuario_pergunta, selfapp_pergunta

def migrate_perguntas():
    perguntas = usuario_pergunta.objects.all()
    
    for pergunta in perguntas:
        nova_pergunta = selfapp_pergunta(texto=pergunta.texto)  # Copie os campos relevantes
        nova_pergunta.save()
        pergunta.delete()

if __name__ == '__main__':
    migrate_perguntas()
