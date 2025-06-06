from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import os
import uuid


def artist_image_path(instance, filename):
    """
    Generate a unique file path for artist images to avoid filename collisions.

    Args:
        instance (Model instance): The Artist model instance.
        filename (str): The original filename of the uploaded image.

    Returns:
        str: The file path with a UUID as filename inside 'artists' directory.
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('artists', filename)


def album_cover_path(instance, filename):
    """
    Generate a unique file path for album cover images.

    Args:
        instance (Model instance): The Album model instance.
        filename (str): The original filename of the uploaded image.

    Returns:
        str: The file path with a UUID as filename inside 'albums' directory.
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('albums', filename)


def track_audio_path(instance, filename):
    """
    Generate a unique file path for track audio files.

    Args:
        instance (Model instance): The Track model instance.
        filename (str): The original filename of the uploaded audio.

    Returns:
        str: The file path with a UUID as filename inside 'tracks' directory.
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('tracks', filename)


# ad_video_path function removed as AdCampaign model is no longer needed


class ServiceRequest(models.Model):
    """
    Represents a request for a service from the user.

    Fields:
        name (str): Name of the person making the request.
        email (str): Email address of the requester.
        company (str): Company name of the requester.
        service_type (str): Type of service requested chosen from predefined options.
        message (str): Optional detailed message concerning the request.
        created_at (datetime): Timestamp when the request was created.
    """
    SERVICE_TYPE_CHOICES = [
        ('media_solutions', 'Media Solutions'),
        ('music_services', 'Music Services'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    company = models.CharField(max_length=100)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} - {self.company} - {self.get_service_type_display()}"


class Genre(models.Model):
    """
    Represents a musical genre.

    Fields:
        name (str): The genre name (e.g. Rock, Jazz, Hip Hop).
    """
    name = models.CharField(max_length=200, help_text='Enter a music genre (e.g. Rock, Jazz, Hip Hop)')
    objects = None  # Placeholder - consider Django's default manager or custom managers as needed

    def __str__(self):
        return self.name


class Artist(models.Model):
    """
    Represents a music artist with related information.

    Fields:
        name (str): Artist's name.
        bio (str): Short biography about the artist.
        image (file): Image file representing the artist.
    """
    name = models.CharField(max_length=200, help_text='Enter the artist name')
    bio = models.TextField(max_length=1000, help_text='Enter a brief bio of the artist', blank=True)
    image = models.FileField(upload_to=artist_image_path, help_text='Artist image', blank=True, null=True)

    @property
    def image_url(self):
        """
        Returns the URL for the artist image.
        If no image is set or accessible, returns a fallback placeholder image URL.

        Returns:
            str: URL to the artist image or a fallback image.
        """
        if self.image and hasattr(self.image, 'url'):
            try:
                # Access URL to ensure file exists
                _ = self.image.url
                return self.image.url
            except Exception:
                # Fall back to placeholder if image access fails
                pass
        # Fallback placeholder URL with random image keyed by artist id
        return f'https://picsum.photos/300?random={self.id}'

    def __str__(self):
        return self.name


class Album(models.Model):
    """
    Represents a music album by an artist.

    Fields:
        title (str): Album title.
        artist (ForeignKey): Artist who created the album.
        genre (ManyToMany): Genre(s) this album belongs to.
        release_date (date): Date of album release.
        cover_image (file): Cover image for the album.
    """
    title = models.CharField(max_length=200, help_text='Enter the album title')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this album')
    release_date = models.DateField(null=True, blank=True)
    cover_image = models.FileField(upload_to=album_cover_path, help_text='Album cover image', blank=True, null=True)
    copyright = models.ForeignKey('Copyright', on_delete=models.SET_NULL, null=True, blank=True, related_name='albums')



    @property
    def cover_image_url(self):
        """
        Returns the URL for the album cover image.
        If no image is set or accessible, returns a fallback placeholder image URL.

        Returns:
            str: URL to the album cover image or a fallback image.
        """
        if self.cover_image and hasattr(self.cover_image, 'url'):
            try:
                _ = self.cover_image.url
                return self.cover_image.url
            except Exception:
                # TODO: Upload default fallback images for album covers
                pass
        return f'https://picsum.photos/300?random={self.id}'

    def __str__(self):
        return self.title


class Track(models.Model):
    """
    Represents an individual music track.

    Fields:
        title (str): Track title.
        album (ForeignKey): Album that the track belongs to.
        artist (ForeignKey): Artist who performed the track.
        audio_file (file): Audio file associated with the track.
        duration (str): Length/duration of the track (e.g. "3:45").
        play_count (int): Total number of times the track was played.
        last_played (datetime): Last played timestamp.
        year (str): Release year from ID3 metadata.
        genre_tag (str): Genre tag from ID3 metadata.
        composer (str): Composer info from ID3 metadata.
        track_number (str): Track number from ID3 metadata.
        bitrate (int): Bitrate of audio in kbps.
        sample_rate (int): Sample rate of audio in Hz.
        bpm (float): Beats per minute of the track.
        key (str): Musical key of the track.
        mood (str): Mood/emotion of the track from DEAM dataset.
    """
    title = models.CharField(max_length=200, help_text='Enter the track title')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='tracks')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='tracks')
    audio_file = models.FileField(upload_to=track_audio_path, help_text='Audio file', blank=True, null=True)
    duration = models.CharField(max_length=10, help_text='Duration of the track (e.g. 3:45)', blank=True)
    play_count = models.IntegerField(default=0, help_text='Number of times the track has been played')
    last_played = models.DateTimeField(null=True, blank=True, help_text='When the track was last played')

    # ID3 metadata fields
    year = models.CharField(max_length=4, blank=True, null=True, help_text='Year of release')
    genre_tag = models.CharField(max_length=100, blank=True, null=True, help_text='Genre from ID3 tag')
    composer = models.CharField(max_length=200, blank=True, null=True, help_text='Composer from ID3 tag')
    track_number = models.CharField(max_length=10, blank=True, null=True, help_text='Track number from ID3 tag')
    bitrate = models.IntegerField(blank=True, null=True, help_text='Bitrate in kbps')
    sample_rate = models.IntegerField(blank=True, null=True, help_text='Sample rate in Hz')

    # Audio analysis fields (from librosa)
    bpm = models.FloatField(blank=True, null=True, help_text='Beats per minute')
    key = models.CharField(max_length=10, blank=True, null=True, help_text='Musical key (e.g. C major, A minor)')

    # DEAM dataset mood field
    # Placeholder for DEAM dataset integration
    mood = models.CharField(max_length=100, blank=True, null=True, help_text='Mood/emotion from DEAM dataset')

    # legal
    copyright = models.ForeignKey('Copyright', on_delete=models.SET_NULL, null=True, blank=True, related_name='tracks')

    def __str__(self):
        return self.title


class User(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser.

    This model inherits all the authentication functionality from Django's built-in User model
    while adding custom fields for our application.

    Fields (inherited from AbstractUser):
        username (str): Unique username of the user.
        email (str): Email address.
        password (str): Hashed user password.
        first_name (str): User's first name.
        last_name (str): User's last name.
        is_active (bool): Whether the user account is active.
        is_staff (bool): Whether the user can access the admin site.
        is_superuser (bool): Whether the user has all permissions.
        date_joined (datetime): Timestamp user registered.
        last_login (datetime): Timestamp of the user's last login.

    Additional Fields:
        agreed_to_terms (bool): Whether user agreed to terms and conditions.
        agreed_to_privacy (bool): Whether user agreed to privacy policy.
        receive_marketing (bool): Whether user opted to receive marketing emails.
        agreement_date (datetime): Timestamp when user agreed to terms/privacy policies.
        user_type (str): Type of user - 'client' or 'artist'.
    """
    USER_TYPE_CHOICES = [
        ('client', 'Client'),
        ('artist', 'Artist'),
    ]

    # Make email required and unique
    email = models.EmailField(unique=True)

    # Custom fields
    agreed_to_terms = models.BooleanField(default=False, help_text='User has agreed to Terms and Conditions')
    agreed_to_privacy = models.BooleanField(default=False, help_text='User has agreed to Privacy Policy')
    receive_marketing = models.BooleanField(default=False, help_text='User has opted in to marketing emails')
    agreement_date = models.DateTimeField(null=True, blank=True, help_text='When the user agreed to terms')
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='client', 
                                help_text='Type of user - client or artist')


# AdCampaign model removed as per requirements - users only need to browse music


# TODO: add copyright class to models.py for copyright / license of current track / album
    # want to view credits, etc.
class Copyright(models.Model):
    """
    Represents copyright and licensing information for a track or album.

    Copyright always belongs to the organization.
    """
    # Default holder is the organization
    holder = models.CharField(max_length=200, default="TFN Music", 
                             help_text='Name of copyright holder (always our organization)')
    license_type = models.CharField(max_length=200, help_text='License type (e.g. Creative Commons)')
    license_url = models.URLField(blank=True, null=True, help_text='Link to the license or terms')
    credits = models.TextField(blank=True, null=True, help_text='Credits/notes related to authorship, contributors, etc.')
    year = models.PositiveIntegerField(default=timezone.now().year, 
                                      help_text='Copyright or License Year')
    document = models.FileField(upload_to='copyright_docs/', blank=True, null=True,
                                help_text="Upload copyright/license document PDF")

    # relationships / foreign keys. One track can have one copyright. One album can have one copyright (one to one)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='copyrights')
    track = models.ForeignKey(Track, on_delete=models.SET_NULL, null=True, blank=True, related_name='copyrights')

    def __str__(self):
        return f"{self.holder} ({self.year or 'Year Unknown'}) - {self.license_type or 'License Info'}"


# ClientCampaign model removed as per requirements - users only need to browse music


class Cart(models.Model):
    """
    Represents a client's shopping cart for tracks.

    Fields:
        user (ForeignKey): The client user who owns this cart.
        tracks (ManyToManyField): Tracks in the cart.
        created_at (DateTimeField): When the cart was created.
        updated_at (DateTimeField): When the cart was last updated.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    tracks = models.ManyToManyField(Track, related_name='in_carts', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"
