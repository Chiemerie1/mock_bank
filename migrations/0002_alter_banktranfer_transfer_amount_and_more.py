# Generated by Django 4.0.3 on 2022-11-10 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cladexallied', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banktranfer',
            name='transfer_amount',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='customers',
            name='account_number',
            field=models.IntegerField(default=1217541057),
        ),
        migrations.AlterField(
            model_name='receivedfunds',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]
