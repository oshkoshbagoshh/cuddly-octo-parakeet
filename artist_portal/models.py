from django.db import models
from music_beta.models import User, Track
import uuid
import os

def artist_profile_image_path(instance, filename):
    """
    Generate a unique file path for artist profile images.

    Args:
        instance (Model instance): The ArtistProfile model instance.
        filename (str): The original filename of the uploaded image.

    Returns:
        str: The file path with a UUID as filename inside 'artist_profiles' directory.
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('artist_profiles', filename)

class ArtistProfile(models.Model):
    """
    Represents an artist's profile with additional information.

    Fields:
        user (ForeignKey): The user associated with this profile.
        profile_picture (FileField): The artist's profile picture.
        bio (TextField): A detailed biography of the artist.
        contact_email (EmailField): Contact email for the artist.
        phone (CharField): Contact phone number for the artist.
        website (URLField): Artist's website URL.
        facebook (URLField): Artist's Facebook profile URL.
        twitter (URLField): Artist's Twitter profile URL.
        instagram (URLField): Artist's Instagram profile URL.
        spotify (URLField): Artist's Spotify profile URL.
        soundcloud (URLField): Artist's SoundCloud profile URL.
        youtube (URLField): Artist's YouTube channel URL.
        featured_track (ForeignKey): A track featured on the artist's profile.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='artist_profile')
    profile_picture = models.FileField(upload_to=artist_profile_image_path, blank=True, null=True)
    bio = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)

    # Social media links
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    spotify = models.URLField(blank=True)
    soundcloud = models.URLField(blank=True)
    youtube = models.URLField(blank=True)

    # Featured track
    featured_track = models.ForeignKey(Track, on_delete=models.SET_NULL, null=True, blank=True, related_name='featured_on_profiles')

    def __str__(self):
        return f"{self.user.username}'s Artist Profile"

    @property
    def profile_picture_url(self):
        """
        Returns the URL for the artist's profile picture.
        If no image is set or accessible, returns a fallback placeholder image URL.

        Returns:
            str: URL to the artist's profile picture or a fallback image.
        """
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            try:
                # Access URL to ensure file exists
                _ = self.profile_picture.url
                return self.profile_picture.url
            except Exception:
                # Fall back to placeholder if image access fails
                pass
        # Fallback placeholder URL with random image keyed by user id
        return f'https://picsum.photos/300?random={self.user.id}'
