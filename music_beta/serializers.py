#  Copyright (c) 2025. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

from rest_framework import serializers
from .models import Genre, Artist, Album, Track, User, AdCampaign, Copyright, ServiceRequest

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name', 'bio', 'image', 'image_url']

class AlbumSerializer(serializers.ModelSerializer):
    artist = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all())
    genre = serializers.PrimaryKeyRelatedField(many=True, queryset=Genre.objects.all())

    class Meta:
        model = Album
        fields = ['id', 'title', 'artist', 'genre', 'release_date', 'cover_image', 'cover_image_url', 'copyright']

class TrackSerializer(serializers.ModelSerializer):
    album = serializers.PrimaryKeyRelatedField(queryset=Album.objects.all())
    artist = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all())

    class Meta:
        model = Track
        fields = ['id', 'title', 'album', 'artist', 'audio_file', 'duration', 'play_count', 
                 'last_played', 'year', 'genre_tag', 'composer', 'track_number', 
                 'bitrate', 'sample_rate', 'copyright']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'agreed_to_terms', 
                 'agreed_to_privacy', 'receive_marketing', 'agreement_date',
                 'user_type', 'is_active', 'last_login']
        extra_kwargs = {'password': {'write_only': True}}

class AdCampaignSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all())

    class Meta:
        model = AdCampaign
        fields = ['id', 'title', 'description', 'video', 'video_url', 'genre', 
                 'mood', 'target_audience', 'user', 'created_at']

class CopyrightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Copyright
        fields = ['id', 'holder', 'license_type', 'license_url', 'credits', 
                 'year', 'document', 'album', 'track']

class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = ['id', 'name', 'email', 'company', 'service_type', 'message', 'created_at']
