# Generated by Django 5.0.3 on 2024-03-07 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_alter_project_proj_total_rounds_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='round',
            options={'ordering': ['number']},
        ),
    ]
