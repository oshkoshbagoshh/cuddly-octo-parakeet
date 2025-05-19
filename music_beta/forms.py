from django import forms
from django.core.validators import RegexValidator
from django.core.files.storage import default_storage
import os

from .models import Genre, Track
from .utils import extract_audio_metadata

class ServiceRequestForm(forms.Form):
    """Form for service requests."""
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}))
    company = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Company'}))
    service_type = forms.ChoiceField(choices=[
        ('', 'Select Service Type'),
        ('media_solutions', 'Media Solutions'),
        ('music_services', 'Music Services')
    ], required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 4}), required=False)

class UserSignupForm(forms.Form):
    """Form for user signup."""
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    # Terms and conditions agreement
    agree_terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='I agree to the Terms and Conditions and Privacy Policy',
        error_messages={'required': 'You must agree to the Terms and Conditions and Privacy Policy to sign up.'}
    )

    # Marketing emails opt-in
    receive_marketing = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='I would like to receive marketing emails about new features and promotions'
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        # Ensure terms are agreed to
        if not cleaned_data.get('agree_terms'):
            raise forms.ValidationError("You must agree to the Terms and Conditions and Privacy Policy to sign up.")

        return cleaned_data

class AdCampaignForm(forms.Form):
    """Form for ad campaign upload."""
    title = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Campaign Title'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Campaign Description', 'rows': 3}))
    video = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'video/*'}), required=False)
    # youtube_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'YouTube URL (preferred)'}))
    video_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Video URL (preferred)'}))
    genre = forms.ModelChoiceField(queryset=Genre.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    mood = forms.ChoiceField(choices=[
        ('', 'Select Mood'),
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('energetic', 'Energetic'),
        ('calm', 'Calm'),
        ('inspirational', 'Inspirational'),
        ('dramatic', 'Dramatic')
    ], widget=forms.Select(attrs={'class': 'form-control'}))
    target_audience = forms.ChoiceField(choices=[
        ('', 'Select Target Audience'),
        ('general', 'General'),
        ('youth', 'Youth'),
        ('adults', 'Adults'),
        ('seniors', 'Seniors'),
        ('professionals', 'Professionals')
    ], widget=forms.Select(attrs={'class': 'form-control'}))

    def clean(self):
        """Validate the form data."""
        cleaned_data = super().clean()
        video = cleaned_data.get('video')
        youtube_url = cleaned_data.get('youtube_url')

        # Check if either video or youtube_url is provided
        if not video and not youtube_url:
            raise forms.ValidationError("Either a video file or YouTube URL must be provided.")

        # Check if both video and youtube_url are provided
        if video and youtube_url:
            raise forms.ValidationError("Please provide either a video file or YouTube URL, not both.")

        # Check video file size (max 50MB)
        if video and video.size > 50 * 1024 * 1024:  # 50MB in bytes
            raise forms.ValidationError("Video file size must be less than 50MB. Please use a YouTube URL for larger videos.")

        return cleaned_data

class TrackForm(forms.ModelForm):
    """Form for track creation/editing."""
    # Add duration validation with RegexValidator to ensure format MM:SS
    duration = forms.CharField(
        max_length=10,
        required=False,  # Not required as it can be extracted from the audio file
        validators=[
            RegexValidator(
                regex=r'^\d+:\d{2}$',
                message='Duration must be in format minutes:seconds (e.g., 3:45)',
                code='invalid_duration'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Duration (e.g., 3:45)'
        })
    )

    class Meta:
        model = Track
        fields = ['title', 'album', 'artist', 'audio_file', 'duration', 'year', 'genre_tag', 'composer', 'track_number']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Track Title'}),
            'album': forms.Select(attrs={'class': 'form-control'}),
            'artist': forms.Select(attrs={'class': 'form-control'}),
            'audio_file': forms.FileInput(attrs={'class': 'form-control', 'accept': 'audio/*'}),
            'year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Year'}),
            'genre_tag': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Genre Tag'}),
            'composer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Composer'}),
            'track_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Track Number'}),
        }

    def save(self, commit=True):
        """
        Override the save method to extract metadata from the audio file.
        """
        instance = super().save(commit=False)

        # Check if an audio file was uploaded
        if self.cleaned_data.get('audio_file'):
            # Get the file path
            file_path = default_storage.path(self.cleaned_data['audio_file'].name)

            # Extract metadata
            metadata = extract_audio_metadata(file_path)

            # Update instance with metadata
            if metadata:
                # Only update fields that are not already set
                if not instance.title and 'title' in metadata:
                    instance.title = metadata['title']

                if not instance.duration and 'duration' in metadata:
                    instance.duration = metadata['duration']

                if not instance.year and 'year' in metadata:
                    instance.year = metadata['year']

                if not instance.genre_tag and 'genre_tag' in metadata:
                    instance.genre_tag = metadata['genre_tag']

                if not instance.composer and 'composer' in metadata:
                    instance.composer = metadata['composer']

                if not instance.track_number and 'track_number' in metadata:
                    instance.track_number = metadata['track_number']

                if 'bitrate' in metadata:
                    instance.bitrate = metadata['bitrate']

                if 'sample_rate' in metadata:
                    instance.sample_rate = metadata['sample_rate']

        if commit:
            instance.save()

        return instance
