# Generated by Django 4.2.2 on 2023-07-19 16:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profileapp", "0012_alter_comment_img"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="img",
            field=models.ImageField(blank=True, default="", upload_to="users/avatars"),
        ),
    ]
