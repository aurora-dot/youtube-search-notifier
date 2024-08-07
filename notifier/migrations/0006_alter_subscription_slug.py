# Generated by Django 5.0.6 on 2024-07-18 14:15

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("notifier", "0005_subscription_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="slug",
            field=models.SlugField(
                default=uuid.UUID("3acada70-d8db-4d72-ae6d-91ee6a355e44"),
                editable=False,
                unique=True,
            ),
        ),
    ]
