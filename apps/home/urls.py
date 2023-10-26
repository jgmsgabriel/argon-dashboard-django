from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('testhome/', views.testhome, name='testhome'),
    path('home_portal/', views.home_portal, name='home_portal'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]