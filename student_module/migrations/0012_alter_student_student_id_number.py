# Generated by Django 4.2.5 on 2023-09-25 10:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("student_module", "0011_rename_course_student_courses_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="student_id_number",
            field=models.CharField(default="65dc0d", max_length=255),
        ),
    ]
