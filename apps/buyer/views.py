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
# def send_delegation_req(req):
#     count = 10
#     range = 100
#     time = 5
#     receiver = 10
#     policy = str(count) + ',' + str(range) + ',' + str(time) + ',' + str(receiver)
#     buyer_id = Buyer.objects.first()
#     t = datetime.datetime.now().timestamp()
#
#     h = SHA256.new('test'.encode("utf8"))
#     with open('private.pem', 'r') as f:
#         private_key = RSA.import_key(f.read())
#     pkcs1_15.new(private_key).sign('test')

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from cryptography.x509.oid import NameOID
import datetime
import uuid


def load_pub_key(filename):
    with open(filename, 'rb') as pem_in:
        pemlines = pem_in.read()
    key = load_pem_public_key(pemlines, None, default_backend())
    return key


def load_private_key(filename):
    with open(filename, 'rb') as pem_in:
        pemlines = pem_in.read()
    key = load_pem_private_key(pemlines, None, default_backend())
    return key


def create_user(request):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
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
    m = name + ',' + organization + ',' + unit_name + ',' + t + ',' + public_key.public_bytes().decode('utf-8')

    ca_public_key = load_pub_key('ca_public.key')
    ca_public_key.encrypt(m)
    # todo


def decode_nonce(request):
    n = request.POST['data']
    private_key = load_private_key('buyer_private.key')
    public_key = load_pub_key('buyer_public.key')
    res = private_key.decrypt(n)

    t = datetime.datetime.now().timestamp()
    name = 'buyer1'
    organization = 'DNS LAB'
    unit_name = 'LAB'
    m = name + ',' + organization + ',' + unit_name + ',' + t + ',' + public_key.public_bytes().decode('utf-8') + ',' +res
    # todo


def save_certificate(request):
