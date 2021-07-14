from django.conf.urls import url
from django.urls import path, include
from apps.bank import views


app_name = "buyer"
urlpatterns = [
    path('create/', views.create),
]


