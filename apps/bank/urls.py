from django.conf.urls import url
from django.urls import path, include
from apps.bank import views


app_name = "bank"
urlpatterns = [
    path('create/', views.create),
]


