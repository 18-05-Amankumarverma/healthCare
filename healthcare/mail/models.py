from django.db import models
from datetime import datetime

# Create your models here.
class Mails(models.Model):
    mailId = models.AutoField(primary_key=True)
    senderEmail = models.CharField(max_length=200)
    senderName = models.CharField(max_length=30)
    recevierEmail = models.CharField(max_length=200)
    recevierName = models.CharField(max_length=30)
    mailBody = models.CharField(max_length=500)
    createdAt = models.DateTimeField(default=datetime.now,blank=True)


