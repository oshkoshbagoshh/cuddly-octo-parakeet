from django.test import TestCase, Client
from django.urls import reverse
from music_beta.models import User, Track, Artist
from .models import ArtistProfile
import json

class ArtistProfileTest(TestCase):
    """Test case for artist profile functionality."""

    def setUp(self):
        """Set up test data."""
        # Create a test artist user
        self.artist_user = User.objects.create(
            username='testartist',
            email='artist@example.com',
            password='password123',
            user_type='artist',
            agreed_to_terms=True,
            agreed_to_privacy=True
        )

        # Create a test client user
        self.client_user = User.objects.create(
            username='testclient',
            email='client@example.com',
            password='password123',
            user_type='client',
            agreed_to_terms=True,
            agreed_to_privacy=True
        )

        # Create a test artist
        self.artist = Artist.objects.create(
            name='Test Artist',
            bio='This is a test artist bio.'
        )

        # Create a test artist profile
        self.profile = ArtistProfile.objects.create(
            user=self.artist_user,
            bio='This is my artist bio.',
            contact_email='contact@example.com',
            phone='123-456-7890',
            website='https://example.com'
        )

        # Create a test client
        self.client = Client()

    def test_artist_profile_view_authenticated_artist(self):
        """Test that an authenticated artist can view their profile."""
        # Log in as the artist
        session = self.client.session
        session['user_id'] = self.artist_user.id
        session['username'] = self.artist_user.username
        session['user_type'] = self.artist_user.user_type
        session.save()

        # Access the artist profile page
        response = self.client.get(reverse('artist_profile'))

        # Check that the page loads successfully
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is my artist bio.')
        self.assertContains(response, 'contact@example.com')

    def test_artist_profile_view_unauthenticated(self):
        """Test that an unauthenticated user cannot view the artist profile page."""
        # Access the artist profile page without logging in
        response = self.client.get(reverse('artist_profile'))

        # Check that the user is redirected to the login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/artist/profile/')

    def test_artist_profile_view_authenticated_client(self):
        """Test that an authenticated client cannot view the artist profile page."""
        # Log in as the client
        session = self.client.session
        session['user_id'] = self.client_user.id
        session['username'] = self.client_user.username
        session['user_type'] = self.client_user.user_type
        session.save()

        # Access the artist profile page
        response = self.client.get(reverse('artist_profile'))

        # Check that the user is redirected to the home page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_artist_profile_update(self):
        """Test that an artist can update their profile."""
        # Log in as the artist
        session = self.client.session
        session['user_id'] = self.artist_user.id
        session['username'] = self.artist_user.username
        session['user_type'] = self.artist_user.user_type
        session.save()

        # Update the profile
        response = self.client.post(reverse('artist_profile'), {
            'bio': 'Updated bio',
            'contact_email': 'updated@example.com',
            'phone': '987-654-3210',
            'website': 'https://updated.com'
        })

        # Check that the profile was updated
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('artist_profile'))

        # Refresh the profile from the database
        self.profile.refresh_from_db()

        # Check that the profile was updated correctly
        self.assertEqual(self.profile.bio, 'Updated bio')
        self.assertEqual(self.profile.contact_email, 'updated@example.com')
        self.assertEqual(self.profile.phone, '987-654-3210')
        self.assertEqual(self.profile.website, 'https://updated.com')

    def test_artist_public_profile_view(self):
        """Test that anyone can view an artist's public profile."""
        # Access the artist's public profile page
        response = self.client.get(reverse('artist_public_profile', args=[self.artist_user.username]))

        # Check that the page loads successfully
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is my artist bio.')
        self.assertContains(response, 'contact@example.com')
