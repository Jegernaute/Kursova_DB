# Generated by Django 5.0.2 on 2024-04-23 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MIaC', '0011_userpayment_miac_userpa_user_id_10272b_idx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddress',
            name='city',
            field=models.CharField(max_length=255),
        ),
        migrations.AddIndex(
            model_name='useraddress',
            index=models.Index(fields=['user', 'city', 'address_line_1'], name='MIaC_userad_user_id_7d78b4_idx'),
        ),
    ]
