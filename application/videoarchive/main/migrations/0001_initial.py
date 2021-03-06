# Generated by Django 3.1.7 on 2021-03-27 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Video",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.TextField()),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("raw_path", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Thumbnail",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("format", models.TextField(choices=[("jpg", "Jpg")])),
                ("width", models.IntegerField()),
                ("height", models.IntegerField()),
                ("path", models.TextField()),
                (
                    "video",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.video"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EncodedVideo",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "format",
                    models.TextField(choices=[("webm", "Webm"), ("mp4", "Mp4")]),
                ),
                ("width", models.IntegerField()),
                ("height", models.IntegerField()),
                ("path", models.TextField()),
                (
                    "video",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.video"
                    ),
                ),
            ],
        ),
    ]
