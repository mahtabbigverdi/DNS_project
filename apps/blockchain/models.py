from django.db import models

# Create your models here.

class Delegation(models.Model):
    range = models.IntegerField(null=False, blank=False)
    count = models.IntegerField(null=False, blank=False)
    time_in_minutes = models.IntegerField( null=False, blank=False)
    receiver_id_in_bank = models.CharField(max_length=10)  #todo cheeeeck
