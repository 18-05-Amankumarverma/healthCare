# Generated by Django 5.1.6 on 2025-03-01 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_appointment_patientemail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='patientEmail',
            field=models.EmailField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='patientPhoneNo',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
