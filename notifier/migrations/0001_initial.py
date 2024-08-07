# Generated by Django 5.0.6 on 2024-07-10 19:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="YouTubeChannel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("channel_link", models.URLField(unique=True)),
                ("channel_name", models.CharField(max_length=64)),
                ("channel_img", models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name="YouTubeQuery",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("query", models.CharField(max_length=500, unique=True)),
                ("last_fetched", models.DateTimeField(auto_now=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="YouTubeVideo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("video_id", models.CharField(max_length=22, unique=True)),
                ("link", models.URLField()),
                ("title", models.CharField(max_length=100)),
                ("thumbnail", models.URLField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "youtube_channel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="youtube_videos",
                        to="notifier.youtubechannel",
                    ),
                ),
                (
                    "youtube_query",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="youtube_videos",
                        to="notifier.youtubequery",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="youtubequery",
            name="latest",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="youtube_queries",
                to="notifier.youtubevideo",
            ),
        ),
    ]
