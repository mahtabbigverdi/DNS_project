from cryptography.hazmat.primitives.serialization import load_pem_private_key
from django.shortcuts import render
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
import datetime
import uuid
from apps.ca.models import *

def start_ca(request):
    one_day = datetime.timedelta(1, 0, 0)
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    builder = x509.CertificateBuilder()
    builder = builder.subject_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u'DNS CA'),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'Sharif'),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, u'University'),
    ]))
    builder = builder.issuer_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u'DNS CA'),
    ]))
    builder = builder.not_valid_before(datetime.datetime.today() - one_day)
    builder = builder.not_valid_after(datetime.datetime(2021, 12, 2))
    builder = builder.serial_number(int(uuid.uuid4()))
    builder = builder.public_key(public_key)
    builder = builder.add_extension(
        x509.BasicConstraints(ca=True, path_length=None), critical=True,
    )
    certificate = builder.sign(
        private_key=private_key, algorithm=hashes.SHA256(),
        backend=default_backend()
    )
    print(isinstance(certificate, x509.Certificate))

    with open("ca_private.key", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption(b"openstack-ansible")
        ))

    with open("ca_public.key", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.PKCS1,
        ))

    with open("ca_certificate.crt", "wb") as f:
        f.write(certificate.public_bytes(
            encoding=serialization.Encoding.PEM,
        ))


def load_private_key(filename):
    with open(filename, 'rb') as pem_in:
        pemlines = pem_in.read()
    key = load_pem_private_key(pemlines, None, default_backend())
    return key


def check_public(request):
    m = request.POST['data']
    print('heeeelllllllloooo%%%%%%%%%%%%%%%%%%%%%')
    print(m)
    data = m.split(',')
    one_day = datetime.timedelta(1, 0, 0)
    user_public_key= data[4].encode('')
    time = data[3]
    subject_name = data[0]
    organization = data[1]
    unit = data[2]

    now = datetime.datetime.now().timestamp()
    # if now - time > 10:
    #     # todo
    #     pass

    n = uuid.uuid4()
    user_public_key.encrypt(n)
    id = user_public_key.public_bytes() % 64
    NonceChecker.objects.create(val=n, id= id,name=subject_name)
    # todo send


def generate_ca(request):
    m = request.POST['data']
    data = m.split(',')
    one_day = datetime.timedelta(1, 0, 0)
    user_public_key= data[4].encode('')
    time = data[3]
    subject_name = data[0]
    organization = data[1]
    unit = data[2]
    nonce = data[5]

    id = user_public_key.public_bytes() % 64
    nonce_checker = NonceChecker.objects.filter(id=id, name=subject_name)[0]
    if nonce_checker.val != nonce:
        # todo
        pass

    now = datetime.datetime.now().timestamp()
    # if now - time > 10:
    #     # todo
    #     pass

    builder = x509.CertificateBuilder()
    builder = builder.subject_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, subject_name),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, unit),
    ]))
    builder = builder.issuer_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u'DNS CA'),
    ]))
    builder = builder.not_valid_before(datetime.datetime.today() - one_day)
    builder = builder.not_valid_after(datetime.datetime(2021, 12, 2))
    builder = builder.serial_number(int(uuid.uuid4()))
    builder = builder.public_key(user_public_key)
    builder = builder.add_extension(
        x509.BasicConstraints(ca=True, path_length=None), critical=True,
    )
    ca_private_key = load_private_key('ca_private.key')
    certificate = builder.sign(
        private_key=ca_private_key, algorithm=hashes.SHA256(),
        backend=default_backend()
    )