# Generated by Django 5.0 on 2024-05-22 09:22

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("department", "0006_alter_userdepartment_options_department_head_user"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name="UserDepartment",
            new_name="DepartMember",
        ),
        migrations.AlterModelOptions(
            name="department",
            options={"ordering": ["created"]},
        ),
    ]
