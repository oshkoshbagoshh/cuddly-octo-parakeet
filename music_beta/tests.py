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


# TODO: add tests for audio player, uploading images, tracks, videos, etc for music library
# TODO: add tests to check for deadlinks, misc pages, etc.
# TODO: test for media library filenames


class ClientCampaignTest(TestCase):
    """Test case for client campaign functionality."""

    def setUp(self):
        """Set up test data."""
        # Create a test client user
        self.client_user = User.objects.create(
            username='testclient',
            email='client@example.com',
            password='password123',
            user_type='client',
            agreed_to_terms=True,
            agreed_to_privacy=True
        )

        # Create a test artist user
        self.artist_user = User.objects.create(
            username='testartist',
            email='artist@example.com',
            password='password123',
            user_type='artist',
            agreed_to_terms=True,
            agreed_to_privacy=True
        )

        # Create a test artist
        self.artist = Artist.objects.create(
            name='Test Artist',
            bio='This is a test artist bio.'
        )

        # Create a test genre
        self.genre = Genre.objects.create(name='Rock')

        # Create a test album
        self.album = Album.objects.create(
            title='Test Album',
            artist=self.artist,
            release_date=datetime.date(2023, 1, 1)
        )
        self.album.genre.add(self.genre)

        # Create test tracks
        self.track1 = Track.objects.create(
            title='Test Track 1',
            album=self.album,
            artist=self.artist,
            duration='3:45'
        )

        self.track2 = Track.objects.create(
            title='Test Track 2',
            album=self.album,
            artist=self.artist,
            duration='4:30'
        )

        # Create a test campaign
        self.campaign = ClientCampaign.objects.create(
            user=self.client_user,
            name='Test Campaign',
            description='This is a test campaign.',
            budget=1000.00,
            start_date=datetime.date(2023, 1, 1),
            end_date=datetime.date(2023, 12, 31)
        )
        self.campaign.tracks.add(self.track1)

        # Create a test cart
        self.cart = Cart.objects.create(user=self.client_user)
        self.cart.tracks.add(self.track2)

        # Create a test client
        self.client = Client()

        # Log in as the client user
        session = self.client.session
        session['user_id'] = self.client_user.id
        session['username'] = self.client_user.username
        session['user_type'] = self.client_user.user_type
        session.save()

    def test_client_dashboard_view(self):
        """Test that a client can view their dashboard."""
        response = self.client.get(reverse('client_dashboard'))

        # Check that the page loads successfully
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Campaign')
        self.assertContains(response, 'Test Track 2')

    def test_campaign_detail_view(self):
        """Test that a client can view campaign details."""
        response = self.client.get(reverse('campaign_detail', args=[self.campaign.id]))

        # Check that the page loads successfully
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Campaign')
        self.assertContains(response, 'This is a test campaign.')
        self.assertContains(response, 'Test Track 1')

    def test_create_campaign(self):
        """Test that a client can create a campaign."""
        response = self.client.post(reverse('create_campaign'), {
            'name': 'New Campaign',
            'description': 'This is a new campaign.',
            'budget': 2000.00,
            'start_date': '2024-01-01',
            'end_date': '2024-12-31'
        })

        # Check that the campaign was created
        self.assertEqual(response.status_code, 302)

        # Check that the campaign was created in the database
        campaign = ClientCampaign.objects.get(name='New Campaign')
        self.assertEqual(campaign.description, 'This is a new campaign.')
        self.assertEqual(campaign.budget, 2000.00)
        self.assertEqual(campaign.start_date, datetime.date(2024, 1, 1))
        self.assertEqual(campaign.end_date, datetime.date(2024, 12, 31))
        self.assertEqual(campaign.user, self.client_user)

    def test_edit_campaign(self):
        """Test that a client can edit a campaign."""
        response = self.client.post(reverse('edit_campaign', args=[self.campaign.id]), {
            'name': 'Updated Campaign',
            'description': 'This is an updated campaign.',
            'budget': 1500.00,
            'start_date': '2023-02-01',
            'end_date': '2023-11-30'
        })

        # Check that the campaign was updated
        self.assertEqual(response.status_code, 302)

        # Refresh the campaign from the database
        self.campaign.refresh_from_db()

        # Check that the campaign was updated correctly
        self.assertEqual(self.campaign.name, 'Updated Campaign')
        self.assertEqual(self.campaign.description, 'This is an updated campaign.')
        self.assertEqual(self.campaign.budget, 1500.00)
        self.assertEqual(self.campaign.start_date, datetime.date(2023, 2, 1))
        self.assertEqual(self.campaign.end_date, datetime.date(2023, 11, 30))

    def test_add_to_cart(self):
        """Test that a client can add a track to their cart."""
        response = self.client.get(reverse('add_to_cart', args=[self.track1.id]))

        # Check that the track was added to the cart
        self.assertEqual(response.status_code, 302)

        # Refresh the cart from the database
        self.cart.refresh_from_db()

        # Check that the track was added to the cart
        self.assertIn(self.track1, self.cart.tracks.all())
        self.assertIn(self.track2, self.cart.tracks.all())

    def test_remove_from_cart(self):
        """Test that a client can remove a track from their cart."""
        response = self.client.get(reverse('remove_from_cart', args=[self.track2.id]))

        # Check that the track was removed from the cart
        self.assertEqual(response.status_code, 302)

        # Refresh the cart from the database
        self.cart.refresh_from_db()

        # Check that the track was removed from the cart
        self.assertNotIn(self.track2, self.cart.tracks.all())


class AuthenticationTest(TestCase):
    """Test case for authentication functionality."""

    def setUp(self):
        """Set up test data."""
        self.client_user_data = {
            'username': 'testclient',
            'email': 'client@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'user_type': 'client',
            'agree_terms': True,
            'receive_marketing': False
        }

        self.artist_user_data = {
            'username': 'testartist',
            'email': 'artist@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'user_type': 'artist',
            'agree_terms': True,
            'receive_marketing': False
        }

        # Create a test user for login tests
        self.existing_user = User.objects.create(
            username='existinguser',
            email='existing@example.com',
            password='password123',
            user_type='client',
            agreed_to_terms=True,
            agreed_to_privacy=True
        )

    def test_signup_client(self):
        """Test client user signup."""
        response = self.client.post('/signup/', 
                                   data=self.client_user_data, 
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])

        # Check that the user was created in the database
        user = User.objects.get(username='testclient')
        self.assertEqual(user.email, 'client@example.com')
        self.assertEqual(user.user_type, 'client')
        self.assertTrue(user.agreed_to_terms)
        self.assertTrue(user.agreed_to_privacy)
        self.assertFalse(user.receive_marketing)

    def test_signup_artist(self):
        """Test artist user signup."""
        response = self.client.post('/signup/', 
                                   data=self.artist_user_data, 
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])

        # Check that the user was created in the database
        user = User.objects.get(username='testartist')
        self.assertEqual(user.email, 'artist@example.com')
        self.assertEqual(user.user_type, 'artist')
        self.assertTrue(user.agreed_to_terms)
        self.assertTrue(user.agreed_to_privacy)
        self.assertFalse(user.receive_marketing)

    def test_login(self):
        """Test user login."""
        response = self.client.post('/login/', {
            'username': 'existinguser',
            'password': 'password123'
        })

        # Check that the user is redirected after login
        self.assertEqual(response.status_code, 302)

        # Check that the session contains the user data
        self.assertEqual(self.client.session['username'], 'existinguser')
        self.assertEqual(self.client.session['user_type'], 'client')

    def test_logout(self):
        """Test user logout."""
        # First login
        self.client.post('/login/', {
            'username': 'existinguser',
            'password': 'password123'
        })

        # Then logout
        response = self.client.get('/logout/')

        # Check that the user is redirected after logout
        self.assertEqual(response.status_code, 302)

        # Check that the session no longer contains the user data
        self.assertNotIn('username', self.client.session)
        self.assertNotIn('user_type', self.client.session)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        response = self.client.post('/login/', {
            'username': 'existinguser',
            'password': 'wrongpassword'
        })

        # Check that the login page is rendered again with an error message
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid password')

    def test_login_nonexistent_user(self):
        """Test login with a nonexistent user."""
        response = self.client.post('/login/', {
            'username': 'nonexistentuser',
            'password': 'password123'
        })

        # Check that the login page is rendered again with an error message
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User does not exist')
