# Generated by Django 5.0.2 on 2025-02-11 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_tournamenttype_short_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='technicallevel',
            name='order_number',
            field=models.IntegerField(default=0),
        ),
    ]
