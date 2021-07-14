from django.conf.urls import url
from django.urls import path, include
from apps.buyer import views


app_name = "buyer"
urlpatterns = [
    path('create_user/', views.create_user),
    path('decode_nonce/', views.decode_nonce),
    path('save_ca/', views.save_ca),
    path('bank_account/', views.create_account),
    path('delegation/', views.send_delegation_req),
    path('buy/', views.buy),
    path('confirm_buy/', views.confirm_buy),

]


