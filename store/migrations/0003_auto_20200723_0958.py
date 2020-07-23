# Generated by Django 3.0.8 on 2020-07-23 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20200723_0930'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.CharField(default='Enter description for item', max_length=500),
        ),
        migrations.AddField(
            model_name='item',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='item',
            name='measurement',
            field=models.CharField(choices=[('OZ', 'ounce'), ('LB', 'pound'), ('FLOZ', 'fluid ounce')], default='OZ', max_length=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='weight',
            field=models.FloatField(default='0'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(blank=True, choices=[('P', 'primary'), ('S', 'secondary'), ('D', 'danger')], max_length=1, null=True),
        ),
    ]
