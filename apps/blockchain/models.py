from django.db import models

# Create your models here.

class Delegation(models.Model):
    range = models.IntegerField(max_length=5, null=False, blank=False)
    count = models.IntegerField(max_length=2, null=False, blank=False)
    time_in_minutes = models.IntegerField(max_length=2, null=False, blank=False)
    receiver_id_in_bank = models.CharField(max_length=10)  #todo cheeeeck
