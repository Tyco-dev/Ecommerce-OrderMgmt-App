# Generated by Django 3.0.8 on 2020-07-25 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20200725_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingaddress',
            name='delivery_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]