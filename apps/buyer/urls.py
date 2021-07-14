from django.conf.urls import url
from django.urls import path, include
from apps.buyer import views


app_name = "buyer"
urlpatterns = [
    path('create_user/', views.create_user),
    path('decode_nonce/', views.decode_nonce),
    path('save_ca/', views.save_ca),
    path('create_account/', views.create_account),
]


