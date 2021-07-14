from django.db import models


class NonceChecker(models.Model):
    val = models.CharField(max_length = 100)
    id_PB = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)