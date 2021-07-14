from django.shortcuts import render
import Crypto.PublicKey.RSA as RSA
from Crypto.Signature import *
from apps.buyer.models import *
import datetime
# Create your views here.

def send_delegation_req(req):
    count = 10
    range = 100
    time = 5
    receiver = 10
    policy = str(count) + ',' + str(range) + ',' + str(time) + ',' + str(receiver)
    buyer_id = Buyer.objects.first()
    t = datetime.datetime.now().timestamp()
