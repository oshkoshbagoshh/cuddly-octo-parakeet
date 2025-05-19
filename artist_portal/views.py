from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseForbidden
from music_beta.models import User, Track
from .models import ArtistProfile
from .forms import ArtistProfileForm

def artist_profile(request):
    """
    View function for the artist's profile page.
    Only accessible to users with user_type='artist'.
    """
    # Check if user is logged in and is an artist
    if 'user_id' not in request.session:
        messages.error(request, 'You must be logged in to view your artist profile.')
        return redirect('login')

    user_id = request.session['user_id']
    try:
        user = User.objects.get(id=user_id)
        if user.user_type != 'artist':
            messages.error(request, 'You must be an artist to access this page.')
            return redirect('home')
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('login')

    # Get or create artist profile
    profile, created = ArtistProfile.objects.get_or_create(user=user)

    # Handle form submission
    if request.method == 'POST':
        form = ArtistProfileForm(user=user, instance=profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('artist_profile')
    else:
        form = ArtistProfileForm(user=user, instance=profile)

    # Get artist's tracks
    tracks = Track.objects.filter(artist__user=user)

    context = {
        'user': user,
        'profile': profile,
        'form': form,
        'tracks': tracks,
    }

    return render(request, 'artist_portal/artist_profile.html', context)

def artist_public_profile(request, username):
    """
    View function for the public view of an artist's profile.
    Accessible to all users.
    """
    user = get_object_or_404(User, username=username, user_type='artist')
    profile = get_object_or_404(ArtistProfile, user=user)
    tracks = Track.objects.filter(artist__user=user)

    context = {
        'user': user,
        'profile': profile,
        'tracks': tracks,
    }

    return render(request, 'artist_portal/artist_public_profile.html', context)
