from django.db import models
from datetime import datetime
# Create your models here.

class UserQuery(models.Model):
    user_id           = models.AutoField(primary_key=True)
    username          = models.CharField(max_length=40)
    user_query        = models.CharField(max_length=300)
    user_uploadedFile = models.ImageField(upload_to='media/disease')



class Appointment(models.Model):
    appointmentId= models.AutoField(primary_key=True)
    appointmentFor= models.CharField(max_length=100)
    doctorName= models.CharField(max_length=40)
    doctorEmail = models.EmailField(max_length=200,default='')
    patientName= models.CharField(max_length=40)    
    patientEmail = models.EmailField(max_length=200,default='')
    patientPhoneNo = models.CharField(max_length=10,default='')
    appointmentTime= models.CharField(max_length=40)
    appointmentDate= models.CharField(max_length=40)
    appointementStatus= models.BooleanField(default=False)
    createdAt = models.DateTimeField(default=datetime.now,blank=True)


class AppointmentGrant(models.Model):
    appointmentId= models.AutoField(primary_key=True)
    treatmentFor= models.CharField(max_length=100)
    patientName= models.CharField(max_length=40)    
    patientEmail = models.EmailField(max_length=200,default='')
    patientPhoneNo = models.CharField(max_length=10,default='')
    appointmentGrantDateTime = models.CharField(max_length=40)
    appointmentDateTime = models.CharField(max_length=40)
    appointementStatus= models.BooleanField(default=False)
    messageFromDoctor = models.CharField(max_length=200,default='test')
    createdAt = models.DateTimeField(default=datetime.now,blank=True)