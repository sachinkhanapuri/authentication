# Generated by Django 3.0.8 on 2020-07-24 06:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authrestapi', '0003_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]