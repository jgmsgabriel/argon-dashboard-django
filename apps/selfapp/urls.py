from django.urls import path
from apps.selfapp import views

urlpatterns = [

    path('testeself/', views.testeself, name='testeself'),
    path('fase/', views.list_fase, name='fase'),
    path('dominio/<int:id>', views.list_dominio, name='dominio'),
    path('pergunta_por_dominio/<int:id>', views.list_pergunta, name='pergunta_por_dominio'),

]
