from django.conf.urls import url
from django.urls import path, include
from apps.bank import views


app_name = "bank"
urlpatterns = [
    path('create/', views.create_account),
    path('start_bank/', views.start_bank),
    path('create_m/', views.create_account_for_merchant),
    path('buy_req/', views.buy_request),
]


