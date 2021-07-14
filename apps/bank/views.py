from django.http import HttpResponse
from django.shortcuts import render
import random
import requests
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from apps.bank.models import *
from cryptography.hazmat.primitives import hashes

@csrf_exempt
def create(request):
    account_id = random.randint(10**2,10**3)
    password = str(random.randint(10**10,10**11))
    h = hashes.Hash(hashes.SHA256())
    hashed_pass = h.update(password.encode('utf-8'))
    hashed_pass = h.finalize()
    Customer.objects.create(id_in_bank=account_id, password=hashed_pass)
    r = requests.post('http://127.0.0.1:8000/buyer/bank_account/', {'account_id':account_id, 'password': password}, verify=False)
    return HttpResponse('')