# Generated by Django 4.1 on 2022-08-13 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="activation_code",
            field=models.CharField(blank=True, max_length=6),
        ),
        migrations.AddField(
            model_name="user",
            name="reset_code",
            field=models.CharField(blank=True, max_length=6),
        ),
    ]