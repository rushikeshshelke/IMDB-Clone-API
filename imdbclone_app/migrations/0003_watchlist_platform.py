# Generated by Django 2.2.28 on 2022-11-24 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imdbclone_app', '0002_auto_20221124_0800'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='platform',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='watchlist', to='imdbclone_app.StreamingPlatform'),
            preserve_default=False,
        ),
    ]
