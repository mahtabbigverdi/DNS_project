from django.conf.urls import url
from django.urls import path, include
from apps.buyer import views


app_name = "buyer"
urlpatterns = [
    path('create_user/', views.create_user),
]


