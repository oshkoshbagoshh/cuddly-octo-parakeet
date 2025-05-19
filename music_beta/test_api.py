#  Copyright (c) 2025. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Genre, Artist, Album, Track, User, Copyright, ServiceRequest, AdCampaign
from .serializers import (
    GenreSerializer, ArtistSerializer, AlbumSerializer, TrackSerializer,
    UserSerializer, CopyrightSerializer, ServiceRequestSerializer, AdCampaignSerializer
)
import datetime

class GenreAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.genre1 = Genre.objects.create(name='Rock')
        self.genre2 = Genre.objects.create(name='Jazz')
        
    def test_get_all_genres(self):
        """Test retrieving all genres"""
        response = self.client.get(reverse('genre-list'))
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_single_genre(self):
        """Test retrieving a single genre"""
        response = self.client.get(reverse('genre-detail', kwargs={'pk': self.genre1.pk}))
        genre = Genre.objects.get(pk=self.genre1.pk)
        serializer = GenreSerializer(genre)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ArtistAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.artist1 = Artist.objects.create(name='Artist 1', bio='Bio 1')
        self.artist2 = Artist.objects.create(name='Artist 2', bio='Bio 2')
        
    def test_get_all_artists(self):
        """Test retrieving all artists"""
        response = self.client.get(reverse('artist-list'))
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_single_artist(self):
        """Test retrieving a single artist"""
        response = self.client.get(reverse('artist-detail', kwargs={'pk': self.artist1.pk}))
        artist = Artist.objects.get(pk=self.artist1.pk)
        serializer = ArtistSerializer(artist)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class AlbumAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.artist = Artist.objects.create(name='Test Artist')
        self.genre = Genre.objects.create(name='Test Genre')
        self.album = Album.objects.create(
            title='Test Album',
            artist=self.artist,
            release_date=datetime.date.today()
        )
        self.album.genre.add(self.genre)
        
    def test_get_all_albums(self):
        """Test retrieving all albums"""
        response = self.client.get(reverse('album-list'))
        albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_single_album(self):
        """Test retrieving a single album"""
        response = self.client.get(reverse('album-detail', kwargs={'pk': self.album.pk}))
        album = Album.objects.get(pk=self.album.pk)
        serializer = AlbumSerializer(album)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TrackAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.artist = Artist.objects.create(name='Test Artist')
        self.genre = Genre.objects.create(name='Test Genre')
        self.album = Album.objects.create(
            title='Test Album',
            artist=self.artist,
            release_date=datetime.date.today()
        )
        self.album.genre.add(self.genre)
        self.track = Track.objects.create(
            title='Test Track',
            album=self.album,
            artist=self.artist,
            duration='3:45'
        )
        
    def test_get_all_tracks(self):
        """Test retrieving all tracks"""
        response = self.client.get(reverse('track-list'))
        tracks = Track.objects.all()
        serializer = TrackSerializer(tracks, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_single_track(self):
        """Test retrieving a single track"""
        response = self.client.get(reverse('track-detail', kwargs={'pk': self.track.pk}))
        track = Track.objects.get(pk=self.track.pk)
        serializer = TrackSerializer(track)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_update_play_count(self):
        """Test updating a track's play count"""
        initial_play_count = self.track.play_count
        response = self.client.patch(
            reverse('track-detail', kwargs={'pk': self.track.pk}),
            {'play_count': initial_play_count + 1},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.track.refresh_from_db()
        self.assertEqual(self.track.play_count, initial_play_count + 1)