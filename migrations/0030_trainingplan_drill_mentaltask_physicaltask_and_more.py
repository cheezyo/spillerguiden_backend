# Generated by Django 5.0.2 on 2025-02-21 09:47

import django.db.models.deletion
import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_remove_diagnosis_situation_delete_biochainpart'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Drill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', tinymce.models.HTMLField()),
                ('video_url', models.URLField(blank=True, null=True)),
                ('picture_url', models.URLField(blank=True, null=True)),
                ('suggested_time', models.PositiveIntegerField(default=10)),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='drills', to='core.task')),
                ('technical_level_task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='technical_drills', to='core.technicalleveltasks')),
            ],
        ),
        migrations.CreateModel(
            name='MentalTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', tinymce.models.HTMLField()),
                ('category', models.CharField(choices=[('In-match', 'In-match'), ('Pre-match', 'Pre-match'), ('Gameplan', 'Gameplan')], max_length=50)),
                ('drills', models.ManyToManyField(blank=True, to='core.drill')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mental_tasks', to='core.level')),
            ],
        ),
        migrations.CreateModel(
            name='PhysicalTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', tinymce.models.HTMLField()),
                ('category', models.CharField(choices=[('Endurance', 'Endurance'), ('Strength', 'Strength'), ('Mobility', 'Mobility')], max_length=50)),
                ('drills', models.ManyToManyField(blank=True, to='core.drill')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='physical_tasks', to='core.level')),
            ],
        ),
        migrations.CreateModel(
            name='TrainingPlanDrill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_allocated', models.PositiveIntegerField()),
                ('drill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='drill_plans', to='core.drill')),
                ('training_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plan_drills', to='core.trainingplan')),
            ],
        ),
    ]
