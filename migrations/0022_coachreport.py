# Generated by Django 5.0.2 on 2025-02-14 14:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_biochainpart_diagnosis'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoachReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coach_name', models.CharField(max_length=255)),
                ('player_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('diagnoses', models.ManyToManyField(to='core.diagnosis')),
                ('tasks', models.ManyToManyField(to='core.technicalleveltasks')),
                ('technical_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.technicallevel')),
            ],
        ),
    ]
