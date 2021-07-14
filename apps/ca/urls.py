from django.conf.urls import url
from django.urls import path, include
from apps.ca import views


app_name = "ca"
urlpatterns = [
    path('start_ca/', views.start_ca),
    path('check_public/', views.check_public),
    path('generate_ca/', views.generate_ca),
]


