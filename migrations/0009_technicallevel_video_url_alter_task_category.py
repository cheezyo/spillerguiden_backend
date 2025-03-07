# Generated by Django 5.0.2 on 2025-02-03 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_level_short_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='technicallevel',
            name='video_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='category',
            field=models.CharField(choices=[('Taktisk', 'Taktisk'), ('Mentalt', 'Mentalt'), ('Fysisk', 'Fysisk')], max_length=10),
        ),
    ]
