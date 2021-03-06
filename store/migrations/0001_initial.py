# Generated by Django 3.0.8 on 2020-07-25 14:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import localflavor.us.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=100)),
                ('street_address', models.CharField(max_length=100)),
                ('suite_address', models.CharField(max_length=100)),
                ('state', localflavor.us.models.USStateField(max_length=2)),
                ('zip', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('weight', models.FloatField(blank=True, null=True)),
                ('measurement', models.CharField(blank=True, choices=[('OZ', 'ounce'), ('LB', 'pound'), ('FLOZ', 'fluid ounce')], max_length=4, null=True)),
                ('description', models.CharField(default='Enter description for item', max_length=500)),
                ('label', models.CharField(blank=True, choices=[('P', 'primary'), ('S', 'secondary'), ('D', 'danger')], max_length=1, null=True)),
                ('featured', models.BooleanField(default=False)),
                ('slug', models.SlugField()),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='store.Category')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('quantity', models.IntegerField(default=1)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('ordered_date', models.DateTimeField()),
                ('delivery_date', models.DateTimeField(null=True)),
                ('ordered', models.BooleanField(default=False)),
                ('billing_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.BillingAddress')),
                ('items', models.ManyToManyField(to='store.OrderItem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='store.SubCategory'),
        ),
    ]
