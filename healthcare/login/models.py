from django.db import models

class Patient(models.Model):
    patientId = models.AutoField(primary_key=True)
    patientName = models.CharField(max_length=40)
    patientEmail = models.CharField(max_length=100)
    patientPhoneNo = models.IntegerField(max_length=12)
    patientPassword = models.CharField(max_length=30)

    
class Doctor(models.Model):
    doctortId = models.AutoField(primary_key=True)
    doctorName = models.CharField(max_length=40)
    doctorEmail = models.CharField(max_length=100)
    doctorPhoneNo = models.IntegerField(max_length=12)
    specializedIn = models.CharField(max_length=50)
    doctorPassword = models.CharField(max_length=30)
