# Generated by Django 5.2.1 on 2025-05-12 21:58

import music_beta.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_beta', '0002_servicerequest_user_artist_image_adcampaign'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adcampaign',
            name='video_url',
        ),
        migrations.AddField(
            model_name='adcampaign',
            name='video',
            field=models.FileField(blank=True, help_text='Video file', null=True, upload_to=music_beta.models.ad_video_path),
        ),
        migrations.AlterField(
            model_name='album',
            name='cover_image',
            field=models.FileField(blank=True, help_text='Album cover image', null=True, upload_to=music_beta.models.album_cover_path),
        ),
        migrations.AlterField(
            model_name='artist',
            name='image',
            field=models.FileField(blank=True, help_text='Artist image', null=True, upload_to=music_beta.models.artist_image_path),
        ),
        migrations.AlterField(
            model_name='track',
            name='audio_file',
            field=models.FileField(blank=True, help_text='Audio file', null=True, upload_to=music_beta.models.track_audio_path),
        ),
    ]
