from django.urls import path
from apps.apiturbo import views

urlpatterns = [

    path('testeturbo/', views.testeturbo, name='testeturbo'),

]
