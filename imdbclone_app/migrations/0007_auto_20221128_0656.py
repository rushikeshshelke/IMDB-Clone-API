# Generated by Django 2.2.28 on 2022-11-28 06:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imdbclone_app', '0006_auto_20221128_0654'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchlist',
            old_name='total_ratings',
            new_name='total_reviews',
        ),
    ]