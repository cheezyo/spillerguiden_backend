# Generated by Django 5.0.2 on 2025-01-31 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_level_short_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='level',
            name='short_desc',
            field=models.CharField(default=' ', max_length=200),
        ),
    ]
