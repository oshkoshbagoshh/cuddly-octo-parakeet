#  Copyright (c) 2025. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

from django import forms
from .models import ArtistProfile
from music_beta.models import Track

class ArtistProfileForm(forms.ModelForm):
    """Form for artist profile management."""
    class Meta:
        model = ArtistProfile
        fields = [
            'profile_picture', 'bio', 'contact_email', 'phone', 'website',
            'facebook', 'twitter', 'instagram', 'spotify', 'soundcloud', 'youtube',
            'featured_track'
        ]
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Tell us about yourself'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Contact Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website URL'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Facebook Profile URL'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Twitter Profile URL'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Instagram Profile URL'}),
            'spotify': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Spotify Profile URL'}),
            'soundcloud': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'SoundCloud Profile URL'}),
            'youtube': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'YouTube Channel URL'}),
            'featured_track': forms.Select(attrs={'class': 'form-control'})
        }
    
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Filter featured_track choices to only include tracks by this artist
            self.fields['featured_track'].queryset = Track.objects.filter(artist__user=user)