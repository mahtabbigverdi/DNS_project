from django.shortcuts import render
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from django.http import HttpResponse
from django.shortcuts import render
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
import datetime
import uuid
from cryptography.hazmat.primitives.asymmetric import padding
import zlib
import random
from django.views.decorators.csrf import csrf_exempt
import requests
from apps.merchant.models import *

def load_pub_key(filename):
    with open(filename, 'rb') as pem_in:
        pemlines = pem_in.read()
    key = load_pem_public_key(pemlines, None)
    return key


def load_private_key(filename):
    with open(filename, 'rb') as pem_in:
        pemlines = pem_in.read()
    key = load_pem_private_key(pemlines,b"openstack-ansible", default_backend())
    return key

@csrf_exempt
def start_merchant(request):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=512,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    with open("merchant_private.key", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption(b"openstack-ansible")
        ))

    with open("merchant_public.key", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.PKCS1,
        ))

    r = requests.post('http://127.0.0.1:8001/bank/create_m/', verify=False)
    return HttpResponse('Keys generated for merchant.')


@csrf_exempt
def bank_account(request):
    id = request.POST['account_id']
    password = request.POST['password']
    Merchant.objects.create(id_in_bank=id, password_in_bank=password)
    print('your account created successfully! (Merchant)')
    return HttpResponse('')


@csrf_exempt
def sell(request):
    m = request.POST['data']
    data = m.split(',')
    signed = request.POST['sign']
    time = data[0]
    x = data[1]
    buyer_id = data[2]
    merchant_id = Merchant.objects.first().id_in_bank
    buyer_public_key = load_pem_public_key(data[3].encode('utf-8'))
    merchant_public_key = load_pub_key('merchant_public.key')
    merchant_private_key = load_private_key('merchant_private.key')

    try:
        buyer_public_key.verify(signed.encode('iso-8859-1'), m.encode('utf-8'), padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH),
                                hashes.SHA256())
        print('signature validated')
    except Exception as e:
        print(e)
        return HttpResponse('failed')

    if x == 'potato':
        price = 100
    elif x == 'tomato':
        price = 200

    t = datetime.datetime.now().timestamp()
    message = str(t) + ',' + x + ',' + buyer_id + ',' + merchant_id + ',' + str(price) + ',' + merchant_public_key.public_bytes(encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.PKCS1).decode('utf-8')
    signed = merchant_private_key.sign(message.encode('utf-8'), padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH),
                              hashes.SHA256())
    r = requests.post('http://127.0.0.1:8000/buyer/confirm_buy/', {'data': message, 'sign': signed.decode('iso-8859-1')}, verify=False)
    return HttpResponse('')
