from django.conf.urls import url
from django.urls import path, include
from apps.merchant import views


app_name = "merchant"
urlpatterns = [
    path('start_merchant/', views.start_merchant),
    path('bank_account/', views.bank_account),
    path('sell/', views.sell),
]


