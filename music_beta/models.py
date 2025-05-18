from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import os
import uuid

def artist_image_path(instance, filename):
    """Generate file path for artist images."""
    # Get the file extension
    ext = filename.split('.')[-1]
    # Generate a new filename with UUID
    filename = f"{uuid.uuid4()}.{ext}"
    # Return the path
    return os.path.join('artists', filename)

def album_cover_path(instance, filename):
    """Generate file path for album cover images."""
    # Get the file extension
    ext = filename.split('.')[-1]
    # Generate a new filename with UUID
    filename = f"{uuid.uuid4()}.{ext}"
    # Return the path
    return os.path.join('albums', filename)

def track_audio_path(instance, filename):
    """Generate file path for track audio files."""
    # Get the file extension
    ext = filename.split('.')[-1]
    # Generate a new filename with UUID
    filename = f"{uuid.uuid4()}.{ext}"
    # Return the path
    return os.path.join('tracks', filename)

def ad_video_path(instance, filename):
    """Generate file path for ad campaign videos."""
    # Get the file extension
    ext = filename.split('.')[-1]
    # Generate a new filename with UUID
    filename = f"{uuid.uuid4()}.{ext}"
    # Return the path
    return os.path.join('ads', filename)

# Create your models here.
class ServiceRequest(models.Model):
    """Model representing a service request."""
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
        """String for representing the Model object."""
        return f"{self.name} - {self.company} - {self.get_service_type_display()}"
class Genre(models.Model):
    """Model representing a music genre."""
    name = models.CharField(max_length=200, help_text='Enter a music genre (e.g. Rock, Jazz, Hip Hop)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Artist(models.Model):
    """Model representing a music artist."""
    name = models.CharField(max_length=200, help_text='Enter the artist name')
    bio = models.TextField(max_length=1000, help_text='Enter a brief bio of the artist', blank=True)
    image = models.FileField(upload_to=artist_image_path, help_text='Artist image', blank=True, null=True)

    @property
    def image_url(self):
        """Return the URL for the artist image with a fallback to a default image."""
        if self.image and hasattr(self.image, 'url'):
            try:
                # Try to access the URL to check if the file exists
                self.image.url
                return self.image.url
            except:
                # If there's an error accessing the URL, use the fallback
                pass
        # Fallback to a default image from picsum.photos
        return f'https://picsum.photos/300?random={self.id}'

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Album(models.Model):
    """Model representing a music album."""
    title = models.CharField(max_length=200, help_text='Enter the album title')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this album')
    release_date = models.DateField(null=True, blank=True)
    cover_image = models.FileField(upload_to=album_cover_path, help_text='Album cover image', blank=True, null=True)

    @property
    def cover_image_url(self):
        """Return the URL for the album cover image with a fallback to a default image."""
        if self.cover_image and hasattr(self.cover_image, 'url'):
            try:
                # Try to access the URL to check if the file exists
                self.cover_image.url
                return self.cover_image.url
            except:
                # If there's an error accessing the URL, use the fallback
                pass
        # Fallback to a default image from picsum.photos
        return f'https://picsum.photos/300?random={self.id}'

    def __str__(self):
        """String for representing the Model object."""
        return self.title

class Track(models.Model):
    """Model representing a music track."""
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

    def __str__(self):
        """String for representing the Model object."""
        return self.title

class User(models.Model):
    """Model representing a user."""
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # In a real app, this would be hashed
    date_joined = models.DateTimeField(default=timezone.now)

    # User agreements and preferences
    agreed_to_terms = models.BooleanField(default=False, help_text='User has agreed to Terms and Conditions')
    agreed_to_privacy = models.BooleanField(default=False, help_text='User has agreed to Privacy Policy')
    receive_marketing = models.BooleanField(default=False, help_text='User has opted in to marketing emails')
    agreement_date = models.DateTimeField(null=True, blank=True, help_text='When the user agreed to terms')

    def __str__(self):
        """String for representing the Model object."""
        return self.username

class AdCampaign(models.Model):
    """Model representing an ad campaign."""
    MOOD_CHOICES = [
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('energetic', 'Energetic'),
        ('calm', 'Calm'),
        ('inspirational', 'Inspirational'),
        ('dramatic', 'Dramatic'),
    ]

    TARGET_AUDIENCE_CHOICES = [
        ('general', 'General'),
        ('youth', 'Youth'),
        ('adults', 'Adults'),
        ('seniors', 'Seniors'),
        ('professionals', 'Professionals'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    video = models.FileField(upload_to=ad_video_path, help_text='Video file (max 50MB)', blank=True, null=True)
    youtube_url = models.URLField(help_text='YouTube video URL (preferred)', blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    target_audience = models.CharField(max_length=20, choices=TARGET_AUDIENCE_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ad_campaigns')
    created_at = models.DateTimeField(default=timezone.now)

    def clean(self):
        """Validate that either video or youtube_url is provided, but not both."""
        if not self.video and not self.youtube_url:
            raise ValidationError('Either a video file or YouTube URL must be provided.')

        if self.video and self.youtube_url:
            raise ValidationError('Please provide either a video file or YouTube URL, not both.')

    def __str__(self):
        """String for representing the Model object."""
        return self.title
