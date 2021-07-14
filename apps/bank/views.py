from apps.bank.models import *
from django.http import HttpResponse
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import random
from django.views.decorators.csrf import csrf_exempt
import requests


@csrf_exempt
def create_account(request):
    account_id = random.randint(10**2,10**3)
    password = str(random.randint(10**10,10**11))
    h = hashes.Hash(hashes.SHA256())
    hashed_pass = h.update(password.encode('utf-8'))
    hashed_pass = h.finalize()
    Customer.objects.create(id_in_bank=account_id, password=hashed_pass)
    r = requests.post('http://127.0.0.1:8000/buyer/bank_account/', {'account_id':account_id, 'password': password}, verify=False)
    return HttpResponse('')


@csrf_exempt
def create_account_for_merchant(request):
    account_id = random.randint(10**2,10**3)
    password = str(random.randint(10**10,10**11))
    h = hashes.Hash(hashes.SHA256())
    hashed_pass = h.update(password.encode('utf-8'))
    hashed_pass = h.finalize()
    Customer.objects.create(id_in_bank=account_id, password=hashed_pass)
    r = requests.post('http://127.0.0.1:8003/merchant/bank_account/', {'account_id':account_id, 'password': password}, verify=False)
    return HttpResponse('')


@csrf_exempt
def start_bank(request):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=512,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    with open("bank_private.key", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption(b"openstack-ansible")
        ))

    with open("bank_public.key", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.PKCS1,
        ))
    return HttpResponse('Keys generated for bank.')


@csrf_exempt
def buy_request(request):
    print('hello we are in buy request')
    return HttpResponse('.')
