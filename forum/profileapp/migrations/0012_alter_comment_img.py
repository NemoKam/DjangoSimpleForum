# Generated by Django 4.2.2 on 2023-07-18 21:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profileapp", "0011_alter_comment_img_alter_post_img"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="img",
            field=models.ImageField(blank=True, upload_to="users/avatars"),
        ),
    ]
