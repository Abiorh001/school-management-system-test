# Generated by Django 4.2.5 on 2023-09-22 14:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("student_module", "0004_alter_student_student_id_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="student_id_number",
            field=models.CharField(default="a23bef", max_length=255),
        ),
    ]
