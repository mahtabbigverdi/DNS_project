from django.db import models


class NonceChecker(models.Model):
    val = models.CharField()
    id = models.CharField()
    name = models.CharField()