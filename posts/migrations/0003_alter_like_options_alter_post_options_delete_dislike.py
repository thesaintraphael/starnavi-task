# Generated by Django 4.1 on 2022-08-14 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0002_like_dislike"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="like",
            options={"ordering": ("-id",)},
        ),
        migrations.AlterModelOptions(
            name="post",
            options={"ordering": ("-id",)},
        ),
        migrations.DeleteModel(
            name="Dislike",
        ),
    ]
