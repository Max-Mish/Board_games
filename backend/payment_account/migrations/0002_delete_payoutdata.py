# Generated by Django 5.0.1 on 2024-02-29 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment_account', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PayoutData',
        ),
    ]