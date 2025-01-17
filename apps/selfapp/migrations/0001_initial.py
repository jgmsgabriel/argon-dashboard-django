# Generated by Django 3.2.6 on 2023-10-17 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dominio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_Dominio', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Fase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_fases', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Pergunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_pergunta', models.TextField(max_length=300)),
                ('dominio_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dominio', to='selfapp.dominio')),
            ],
        ),
        migrations.AddField(
            model_name='dominio',
            name='fases_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fase', to='selfapp.fase'),
        ),
        migrations.CreateModel(
            name='Alternativa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_alternativa', models.TextField(max_length=300)),
                ('rating', models.TextField(default='TESTE', max_length=50)),
                ('pergunta_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pergunta', to='selfapp.pergunta')),
            ],
        ),
    ]
