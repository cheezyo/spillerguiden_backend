# Generated by Django 5.0.2 on 2025-02-27 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_alter_drill_situation_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keypoint',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
