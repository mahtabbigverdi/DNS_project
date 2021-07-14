# from django.shortcuts import render
# import Crypto.PublicKey.RSA as RSA
# from Crypto.Signature import *
# from apps.buyer.models import *
# import datetime
# from Crypto.Hash import SHA256
#
#
# # Create your views here.
#

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from cryptography.x509.oid import NameOID
import datetime
from cryptography.hazmat.primitives.asymmetric import padding
import uuid
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import zlib
from apps.buyer.models import *
from cryptography.hazmat.primitives import hashes


def load_pub_key(filename):
    with open(filename, 'rb') as pem_in:
        pemlines = pem_in.read()
    key = load_pem_public_key(pemlines, None)
    return key


def load_private_key(filename):
    with open(filename, 'rb') as pem_in:
        pemlines = pem_in.read()
    key = load_pem_private_key(pemlines, b"openstack-ansible", default_backend())
    return key


@csrf_exempt
def create_user(request):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=512,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    with open("buyer_private.key", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption(b"openstack-ansible")
        ))

    with open("buyer_public.key", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.PKCS1,
        ))

    t = datetime.datetime.now().timestamp()
    name = 'buyer1'
    organization = 'DNS LAB'
    unit_name = 'LAB'
    m = name + ',' + organization + ',' + unit_name + ',' + str(t) + ',' + public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.PKCS1).decode('utf-8')
    m = zlib.compress(m.encode('utf-8'), -1)
    ca_public_key = load_pub_key('ca_public.key')
    cipher = ca_public_key.encrypt(m, padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA1()),
        algorithm=hashes.SHA1(),
        label=None))

    r = requests.post('http://127.0.0.1:8004/ca/check_public/', {'data': cipher.decode('iso-8859-1')}, verify=False)

    #  lets go to the bank (pay attention: hozori!!)
    r = requests.post('http://127.0.0.1:8001/bank/create/', verify=False)

    return HttpResponse('')


@csrf_exempt
def decode_nonce(request):
    n = request.POST['data'].encode('iso-8859-1')
    private_key = load_private_key('buyer_private.key')
    nonce = private_key.decrypt(n, padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA1()),
        algorithm=hashes.SHA1(),
        label=None
    )).decode('utf-8')
    print('buuuuuuuuuyyyyyyyyyyyyyyyerrrrrrrr', nonce)
    public_key = load_pub_key('buyer_public.key')
    t = datetime.datetime.now().timestamp()
    name = 'buyer1'
    organization = 'DNS LAB'
    unit_name = 'LAB'
    m = name + ',' + organization + ',' + unit_name + ',' + str(t) + ',' + public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.PKCS1).decode('utf-8') + ',' + nonce
    m = zlib.compress(m.encode('utf-8'), -1)
    ca_public_key = load_pub_key('ca_public.key')
    cipher = ca_public_key.encrypt(m, padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA1()),
        algorithm=hashes.SHA1(),
        label=None))

    r = requests.post('http://127.0.0.1:8004/ca/generate_ca/', {'data': cipher.decode('iso-8859-1')}, verify=False)
    return HttpResponse('')


@csrf_exempt
def save_ca(request):
    n = request.POST['data'].encode('iso-8859-1')
    with open("buyer_certificate.crt", "wb") as f:
        f.write(n)
    return HttpResponse('')


@csrf_exempt
def create_account(request):
    id = request.POST['account_id']
    password = request.POST['password']
    Buyer.objects.create(id_in_bank=id, password_in_bank=password)
    print('your account created successfully! (Buyer)')
    return HttpResponse('')


@csrf_exempt
def send_delegation_req(request):
    count = 10
    range = 100
    time = 5
    receiver = 10
    policy = str(count) + ',' + str(range) + ',' + str(time) + ',' + str(receiver)
    buyer_id = Buyer.objects.first().id_in_bank
    t = datetime.datetime.now().timestamp()
    private_key = load_private_key('buyer_private.key')
    bank_pubic_key = load_pub_key('bank_public.key')
    public_key = load_pub_key('buyer_public.key')

    m = buyer_id + ',' + str(t) + ',' + policy + ',' + bank_pubic_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                                                   format=serialization.PublicFormat.PKCS1).decode(
        'utf-8') + ',' + public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                 format=serialization.PublicFormat.PKCS1).decode('utf-8')

    signed = private_key.sign(m.encode('utf-8'), padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH),
                              hashes.SHA256())
    r = requests.post('http://127.0.0.1:8002/bc/delegation/', {'data': m, 'sign': signed.decode('iso-8859-1')},
                      verify=False)
    return HttpResponse('')


@csrf_exempt
def buy(request):
    x = 'potato'
    t = datetime.datetime.now().timestamp()
    buyer_id = Buyer.objects.first().id_in_bank
    public_key = load_pub_key('buyer_public.key')
    private_key = load_private_key('buyer_private.key')
    m = str(t) + ',' + x + ',' + buyer_id + ',' + public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                                          format=serialization.PublicFormat.PKCS1).decode(
        'utf-8')
    signed = private_key.sign(m.encode('utf-8'), padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH),
                              hashes.SHA256())
    r = requests.post('http://127.0.0.1:8003/merchant/sell/', {'data': m, 'sign': signed.decode('iso-8859-1')},
                      verify=False)
    return HttpResponse('')


@csrf_exempt
def confirm_buy(request):
    m = request.POST['data']
    signed = request.POST['sign']
    data = m.split(',')
    time = data[0]
    x = data[1]
    buyer_id = data[2]
    merchant_id = data[3]
    price = data[4]
    merchant_public_key = load_pem_public_key(data[5].encode('utf-8'))
    try:
        merchant_public_key.verify(signed.encode('iso-8859-1'), m.encode('utf-8'), padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH),
                                   hashes.SHA256())
        print('signature validated')
    except Exception as e:
        print(e)
        return HttpResponse('failed')

    if x != 'potato':
        return HttpResponse('failed')

    t = datetime.datetime.now().timestamp()
    buyer_public_key = load_pub_key('buyer_public.key')
    message = str(t) + ',' + price + ',' + merchant_id + ',' + buyer_id + ',' + buyer_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.PKCS1).decode('utf-8')

    buyer_private_key = load_private_key('buyer_private.key')
    signed = buyer_private_key.sign(m.encode('utf-8'), padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH),
                              hashes.SHA256())
    r = requests.post('http://127.0.0.1:8001/bank/buy_req/', {'data': message, 'sign': signed.decode('iso-8859-1')},
                      verify=False)
    return HttpResponse('.')
