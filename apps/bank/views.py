from django.http import HttpResponse
from django.shortcuts import render
import random
import requests
# Create your views here.
from apps.bank.models import *
def create():
    account_id = random.randint(10**2,10**3)
    password = random.randint(10**10,10**11)
    Customer.objects.create(id_in_bank=account_id, password=password)
    r =  requests.post('http://127.0.0.1:8000/buyer/bank_account/', {'account_id':account_id, 'password': password}, verify=False)
    return HttpResponse('')