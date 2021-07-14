"""DNS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.ca import urls as ca_urls
from apps.buyer import urls as buyer_urls
from apps.bank import urls as bank_urls
from apps.blockchain import urls as bc_urls
from apps.merchant import urls as m_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ca/', include(ca_urls)),
    path('buyer/', include(buyer_urls)),
    path('bank/', include(bank_urls)),
    path('bc/', include(bc_urls)),
    path('merchant/', include(m_urls)),
]
