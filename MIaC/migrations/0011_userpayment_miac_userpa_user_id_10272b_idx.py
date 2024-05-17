# Generated by Django 5.0.2 on 2024-04-23 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MIaC', '0010_alter_paymentdetails_payment_date'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='userpayment',
            index=models.Index(fields=['user', 'payment_type', 'provider'], name='MIaC_userpa_user_id_10272b_idx'),
        ),
    ]
