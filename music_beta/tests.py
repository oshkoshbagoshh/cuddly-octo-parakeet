from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from music_beta.models import (
    Genre, Artist, Album, Track, User, AdCampaign, ServiceRequest
)
import datetime


class GenreModelTest(TestCase):
    """Test case for the Genre model."""

    def setUp(self):
        """Set up test data."""
        self.genre = Genre.objects.create(name="Rock")

    def test_genre_creation(self):
        """Test that a genre can be created."""
        self.assertEqual(self.genre.name, "Rock")

    def test_genre_string_representation(self):
        """Test the string representation of a genre."""
        self.assertEqual(str(self.genre), "Rock")


class ArtistModelTest(TestCase):
    """Test case for the Artist model."""

    def setUp(self):
        """Set up test data."""
        self.artist = Artist.objects.create(
            name="Test Artist",
            bio="This is a test artist bio."
        )

    def test_artist_creation(self):
        """Test that an artist can be created."""
        self.assertEqual(self.artist.name, "Test Artist")
        self.assertEqual(self.artist.bio, "This is a test artist bio.")

    def test_artist_string_representation(self):
        """Test the string representation of an artist."""
        self.assertEqual(str(self.artist), "Test Artist")


class AlbumModelTest(TestCase):
    """Test case for the Album model."""

    def setUp(self):
        """Set up test data."""
        self.artist = Artist.objects.create(name="Test Artist")
        self.genre = Genre.objects.create(name="Rock")
        self.album = Album.objects.create(
            title="Test Album",
            artist=self.artist,
            release_date=datetime.date(2023, 1, 1)
        )
        self.album.genre.add(self.genre)

    def test_album_creation(self):
        """Test that an album can be created."""
        self.assertEqual(self.album.title, "Test Album")
        self.assertEqual(self.album.artist, self.artist)
        self.assertEqual(self.album.release_date, datetime.date(2023, 1, 1))
        self.assertEqual(self.album.genre.count(), 1)
        self.assertEqual(self.album.genre.first(), self.genre)

    def test_album_string_representation(self):
        """Test the string representation of an album."""
        self.assertEqual(str(self.album), "Test Album")


class TrackModelTest(TestCase):
    """Test case for the Track model."""

    def setUp(self):
        """Set up test data."""
        self.artist = Artist.objects.create(name="Test Artist")
        self.album = Album.objects.create(
            title="Test Album",
            artist=self.artist
        )
        self.track = Track.objects.create(
            title="Test Track",
            album=self.album,
            artist=self.artist,
            duration="3:45"
        )

    def test_track_creation(self):
        """Test that a track can be created."""
        self.assertEqual(self.track.title, "Test Track")
        self.assertEqual(self.track.album, self.album)
        self.assertEqual(self.track.artist, self.artist)
        self.assertEqual(self.track.duration, "3:45")

    def test_track_string_representation(self):
        """Test the string representation of a track."""
        self.assertEqual(str(self.track), "Test Track")


class UserModelTest(TestCase):
    """Test case for the User model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create(
            username="testuser",
            email="test@example.com",
            password="password123"
        )

    def test_user_creation(self):
        """Test that a user can be created."""
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.password, "password123")
        self.assertTrue(isinstance(self.user.date_joined, datetime.datetime))

    def test_user_string_representation(self):
        """Test the string representation of a user."""
        self.assertEqual(str(self.user), "testuser")


class ServiceRequestModelTest(TestCase):
    """Test case for the ServiceRequest model."""

    def setUp(self):
        """Set up test data."""
        self.service_request = ServiceRequest.objects.create(
            name="Test User",
            email="test@example.com",
            company="Test Company",
            service_type="media_solutions",
            message="This is a test message."
        )

    def test_service_request_creation(self):
        """Test that a service request can be created."""
        self.assertEqual(self.service_request.name, "Test User")
        self.assertEqual(self.service_request.email, "test@example.com")
        self.assertEqual(self.service_request.company, "Test Company")
        self.assertEqual(self.service_request.service_type, "media_solutions")
        self.assertEqual(self.service_request.message, "This is a test message.")
        self.assertTrue(isinstance(self.service_request.created_at, datetime.datetime))

    def test_service_request_string_representation(self):
        """Test the string representation of a service request."""
        self.assertEqual(str(self.service_request), "Test User - Test Company - Media Solutions")


class AdCampaignModelTest(TestCase):
    """Test case for the AdCampaign model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        self.genre = Genre.objects.create(name="Rock")
        self.ad_campaign = AdCampaign.objects.create(
            title="Test Campaign",
            description="This is a test campaign.",
            genre=self.genre,
            mood="happy",
            target_audience="general",
            user=self.user
        )

    def test_ad_campaign_creation(self):
        """Test that an ad campaign can be created."""
        self.assertEqual(self.ad_campaign.title, "Test Campaign")
        self.assertEqual(self.ad_campaign.description, "This is a test campaign.")
        self.assertEqual(self.ad_campaign.genre, self.genre)
        self.assertEqual(self.ad_campaign.mood, "happy")
        self.assertEqual(self.ad_campaign.target_audience, "general")
        self.assertEqual(self.ad_campaign.user, self.user)
        self.assertTrue(isinstance(self.ad_campaign.created_at, datetime.datetime))

    def test_ad_campaign_string_representation(self):
        """Test the string representation of an ad campaign."""
        self.assertEqual(str(self.ad_campaign), "Test Campaign")