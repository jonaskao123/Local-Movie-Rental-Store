# Generated by Django 5.0.6 on 2024-06-04 07:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0005_rating_remove_movie_language_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="movie",
            options={"ordering": ["title", "director"]},
        ),
    ]
