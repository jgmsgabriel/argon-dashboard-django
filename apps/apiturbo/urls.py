from django.urls import path, re_path
from apps.apiturbo import views

urlpatterns = [

    path('teste/', views.teste, name='teste'),

]
