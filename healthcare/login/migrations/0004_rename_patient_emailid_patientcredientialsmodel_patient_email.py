# Generated by Django 5.1.1 on 2025-02-20 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patientcredientialsmodel',
            old_name='patient_emailId',
            new_name='patient_email',
        ),
    ]
