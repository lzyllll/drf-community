# Generated by Django 5.0.6 on 2024-06-22 10:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("activity", "0004_campusactivity_planning_document"),
    ]

    operations = [
        migrations.AddField(
            model_name="campusactivity",
            name="score",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]