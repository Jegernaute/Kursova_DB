# Generated by Django 5.0.2 on 2024-04-24 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MIaC', '0018_orderitem_miac_orderi_order_i_497373_idx'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='subscriptiondetail',
            index=models.Index(fields=['training', 'subscription', 'trainer'], name='MIaC_subscr_trainin_0e9cc8_idx'),
        ),
    ]
