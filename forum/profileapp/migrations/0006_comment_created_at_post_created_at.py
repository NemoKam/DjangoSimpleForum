# Generated by Django 4.2.2 on 2023-07-15 12:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profileapp", "0005_post_comment"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="created_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="post",
            name="created_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
