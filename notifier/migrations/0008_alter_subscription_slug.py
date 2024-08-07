# Generated by Django 5.0.6 on 2024-07-19 12:23

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("notifier", "0007_alter_subscription_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="slug",
            field=models.SlugField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
