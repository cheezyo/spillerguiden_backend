# Generated by Django 5.0.2 on 2025-02-06 11:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_task_picture_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='situation_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.situationtype'),
            preserve_default=False,
        ),
    ]
