# Generated by Django 5.0.2 on 2024-04-24 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MIaC', '0019_subscriptiondetail_miac_subscr_trainin_0e9cc8_idx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpayment',
            name='payment_type',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='userpayment',
            name='provider',
            field=models.CharField(max_length=255),
        ),
    ]
