from django.http import HttpResponse
import requests
from django.shortcuts import render

def testeturbo(request):
    response = requests.get('https://us-south.functions.appdomain.cloud/api/v1/web/c1e8f27c-3a2a-4d4e-aed8-20dc5e0b4005/Turbonomic/app-actions.json').json()
    return render(request, 'apiturbo/teste.html', {'response':response})

    #return render(request, "apiturbo/teste.html")
    #return render(request, "accounts/login.html")