from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from django.http import HttpResponse
from django.shortcuts import render
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from apps.blockchain.models import *


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
def delegation(request):
    m = request.POST['data']
    data = m.split(',')
    buyer_id = data[0]
    timestamp = data[1]
    count = data[2]
    range = data[3]
    time = data[4]
    receiver = data[5]
    bank_public_key = load_pem_public_key(data[6].encode('utf-8'))
    buyer_public_key = load_pem_public_key(data[7].encode('utf-8'))

    signed = request.POST['sign']
    try:
        buyer_public_key.verify(signed.encode('iso-8859-1'), m.encode('utf-8'), padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH),
                                hashes.SHA256())
        print('signature validated')
    except Exception as e:
        print(e)
        return HttpResponse('failed')
    de = Delegation.objects.create(range=range, time_in_minutes=time, count=count, receiver_id_in_bank=receiver)
    return HttpResponse('successfully created delegation record.')
