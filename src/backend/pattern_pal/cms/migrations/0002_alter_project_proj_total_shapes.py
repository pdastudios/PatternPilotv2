# Generated by Django 5.0.3 on 2024-03-07 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='proj_total_shapes',
            field=models.IntegerField(),
        ),
    ]
