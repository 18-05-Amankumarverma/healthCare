# Generated by Django 5.1.6 on 2025-03-02 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_appointmentgrant'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentgrant',
            name='messageFromDoctor',
            field=models.CharField(default='test', max_length=200),
        ),
    ]
