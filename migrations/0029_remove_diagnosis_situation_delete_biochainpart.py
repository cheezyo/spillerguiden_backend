# Generated by Django 5.0.2 on 2025-02-21 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_remove_diagnosis_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diagnosis',
            name='situation',
        ),
        migrations.DeleteModel(
            name='BioChainPart',
        ),
    ]
