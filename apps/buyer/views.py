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
