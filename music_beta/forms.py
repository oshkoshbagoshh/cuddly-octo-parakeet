from django import forms
from django.core.validators import RegexValidator
from django.core.files.storage import default_storage
import os

from .models import Genre, Track, ClientCampaign
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

    # User type selection
    user_type = forms.ChoiceField(
        choices=[
            ('client', 'I am a client looking for music for my ad campaign'),
            ('artist', 'I am an artist looking to manage my artist profile')
        ],
        required=True,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='client'
    )

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

# AdCampaignForm removed as per requirements - users only need to browse music

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

    # Add BPM field
    bpm = forms.FloatField(
        required=False,  # Not required as it can be extracted from the audio file
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'BPM (e.g., 120.5)',
            'step': '0.01'
        })
    )

    # Add key field
    key = forms.CharField(
        max_length=10,
        required=False,  # Not required as it can be extracted from the audio file
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Key (e.g., C major)'
        })
    )

    # Add mood field
    mood = forms.CharField(
        max_length=100,
        required=False,  # Not required as it can be extracted from the audio file
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mood/Emotion'
        })
    )

    class Meta:
        model = Track
        fields = ['title', 'album', 'artist', 'audio_file', 'duration', 'year', 
                 'genre_tag', 'composer', 'track_number', 'bpm', 'key', 'mood']
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

                # New fields from librosa analysis
                if not instance.bpm and 'bpm' in metadata:
                    instance.bpm = metadata['bpm']

                if not instance.key and 'key' in metadata:
                    instance.key = metadata['key']

                if not instance.mood and 'mood' in metadata:
                    instance.mood = metadata['mood']

        # Ensure copyright is set
        if not instance.copyright:
            # Create a new Copyright instance with default values
            from .models import Copyright
            copyright_instance = Copyright.objects.create()
            instance.copyright = copyright_instance

        if commit:
            instance.save()

        return instance

# copyright form
class CopyrightForm(forms.ModelForm):
    """Form for copyright information."""
    class Meta:
        model = Copyright
        fields = ['license_type', 'license_url', 'credits', 'document']
        widgets = {
            'license_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'License Type'}),
            'license_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'License URL'}),
            'credits': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Credits/Notes'}),
            'document': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add a note explaining that copyright holder is always the organization
        self.fields['license_type'].help_text = "Copyright holder is always set to our organization."

    def save(self, commit=True):
        """Override save method to ensure holder is always set to the organization."""
        instance = super().save(commit=False)
        # Ensure holder is always set to the organization
        instance.holder = "TFN Music"
        # Set year to current year if not provided
        if not instance.year:
            from django.utils import timezone
            instance.year = timezone.now().year

        if commit:
            instance.save()

        return instance

class LoginForm(forms.Form):
    """Form for user login."""
    username = forms.CharField(max_length=100, required=True, 
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    remember_me = forms.BooleanField(required=False, 
                                    widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                                    label='Remember me')

# ClientCampaignForm removed as per requirements - users only need to browse music
