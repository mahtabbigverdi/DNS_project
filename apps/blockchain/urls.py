from django.conf.urls import url
from django.urls import path, include
from apps.blockchain import views


app_name = "blockchain"
urlpatterns = [
    path('delegation/', views.delegation),
]


