from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from .forms import CopyrightForm, LoginForm
from io import BytesIO
import hashlib
import json
import os

# Try to import requests, but provide a fallback if it's not available
try:
    import requests
except ImportError:
    # Create a simple mock for the requests module
    class MockResponse:
        def __init__(self, status_code=200):
            self.status_code = status_code
            self.json_data = {"photos": []}

        def json(self):
            return self.json_data

    class MockRequests:
        @staticmethod
        def get(url, headers=None):
            return MockResponse()

    requests = MockRequests()

from .models import Genre, Artist, Album, Track, User, AdCampaign, ServiceRequest
from .forms import UserSignupForm, AdCampaignForm, ServiceRequestForm, LoginForm

# Create your views here.
def home(request):
    """
    View function for the home page of the site.
    """
    signup_form = UserSignupForm()
    ad_campaign_form = AdCampaignForm()

    context = {
        'signup_form': signup_form,
        'ad_campaign_form': ad_campaign_form,
    }

    return render(request, 'music_beta/home.html', context)

@csrf_exempt
def signup(request):
    """
    View function for user signup.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            user_type = data.get('user_type', 'client')  # Default to client if not specified
            agree_terms = data.get('agree_terms', False)
            receive_marketing = data.get('receive_marketing', False)

            # Check if user already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': 'Username already exists'})
            if User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'Email already exists'})

            # Check if terms are agreed to
            if not agree_terms:
                return JsonResponse({'success': False, 'message': 'You must agree to the Terms and Conditions and Privacy Policy to sign up.'})

            # Validate user_type
            if user_type not in ['client', 'artist']:
                return JsonResponse({'success': False, 'message': 'Invalid user type. Must be either "client" or "artist".'})

            # Create new user
            user = User.objects.create(
                username=username,
                email=email,
                password=password,  # In a real app, this would be hashed
                user_type=user_type,
                agreed_to_terms=True,
                agreed_to_privacy=True,
                receive_marketing=receive_marketing,
                agreement_date=timezone.now()
            )

            # Set up session
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session['user_type'] = user.user_type

            return JsonResponse({
                'success': True, 
                'message': 'User created successfully',
                'user_id': user.id,
                'user_type': user.user_type
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def upload_ad_campaign(request):
    """
    View function for ad campaign upload.
    """
    if request.method == 'POST':
        try:
            # Handle form data (including file uploads)
            form = AdCampaignForm(request.POST, request.FILES)

            if form.is_valid():
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                video = form.cleaned_data.get('video')
                genre = form.cleaned_data['genre']
                mood = form.cleaned_data['mood']
                target_audience = form.cleaned_data['target_audience']
                username = request.POST.get('username')

                # Get user
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    return JsonResponse({'success': False, 'message': 'User not found'})

                # Create new ad campaign
                ad_campaign = AdCampaign.objects.create(
                    title=title,
                    description=description,
                    video=video,
                    genre=genre,
                    mood=mood,
                    target_audience=target_audience,
                    user=user
                )

                return JsonResponse({
                    'success': True, 
                    'message': 'Ad campaign created successfully',
                    'campaign_id': ad_campaign.id
                })
            else:
                return JsonResponse({'success': False, 'message': 'Invalid form data', 'errors': form.errors})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def search(request):
    """
    View function for search functionality.
    """
    if request.method == 'GET':
        query = request.GET.get('q', '')

        if not query:
            return JsonResponse({'success': False, 'message': 'No search query provided'})

        # Search for artists, albums, tracks, and ad campaigns
        artists_queryset = Artist.objects.filter(name__icontains=query)
        albums_queryset = Album.objects.filter(title__icontains=query)
        tracks = Track.objects.filter(title__icontains=query).values('id', 'title', 'artist__name', 'album__title')
        ad_campaigns = AdCampaign.objects.filter(title__icontains=query).values('id', 'title', 'description', 'video_url', 'mood')

        # Convert querysets to lists with custom properties
        artists = []
        for artist in artists_queryset:
            artists.append({
                'id': artist.id,
                'name': artist.name,
                'image': artist.image.url if artist.image else None,
                'image_url': artist.image_url,
            })

        albums = []
        for album in albums_queryset:
            albums.append({
                'id': album.id,
                'title': album.title,
                'artist__name': album.artist.name,
                'cover_image': album.cover_image.url if album.cover_image else None,
                'cover_image_url': album.cover_image_url,
            })

        results = {
            'artists': artists,
            'albums': albums,
            'tracks': list(tracks),
            'ad_campaigns': list(ad_campaigns),
        }

        return JsonResponse({'success': True, 'results': results})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def get_pexels_images(request):
    """
    View function to fetch images from Pexels API.
    """
    if request.method == 'GET':
        query = request.GET.get('q', 'music')

        # Get Pexels API key from environment variables
        api_key = os.environ.get('PEXELS_API_KEY', '')

        if not api_key:
            # Return SVG placeholder images if no API key is available
            svg_placeholders = [
                f'/static/images/blog-{i+1}.svg' for i in range(3)
            ] * 4  # Repeat to get 12 images
            return JsonResponse({'success': True, 'images': svg_placeholders[:10]})

        try:
            # Make request to Pexels API
            headers = {
                'Authorization': api_key
            }
            response = requests.get(f'https://api.pexels.com/v1/search?query={query}&per_page=10', headers=headers)

            if response.status_code == 200:
                data = response.json()
                images = [photo['src']['medium'] for photo in data['photos']]
                return JsonResponse({'success': True, 'images': images})
            else:
                # Return SVG placeholder images if API request fails
                svg_placeholders = [
                    f'/static/images/blog-{i+1}.svg' for i in range(3)
                ] * 4  # Repeat to get 12 images
                return JsonResponse({'success': True, 'images': svg_placeholders[:10]})
        except Exception as e:
            # Return SVG placeholder images if there's an exception
            svg_placeholders = [
                f'/static/images/blog-{i+1}.svg' for i in range(3)
            ] * 4  # Repeat to get 12 images
            return JsonResponse({'success': True, 'images': svg_placeholders[:10], 'error': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def service_request(request):
    """
    View function for handling service requests.
    """
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            # Save the service request to the database
            service_request = ServiceRequest.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                company=form.cleaned_data['company'],
                service_type=form.cleaned_data['service_type'],
                message=form.cleaned_data['message']
            )

            # Send email notification
            subject = f"New Service Request: {form.cleaned_data['service_type']}"
            message = f"""
            New service request received:

            Name: {form.cleaned_data['name']}
            Email: {form.cleaned_data['email']}
            Company: {form.cleaned_data['company']}
            Service Type: {form.cleaned_data['service_type']}
            Message: {form.cleaned_data['message']}
            """
            # Use development email from settings
            recipient_email = getattr(settings, 'DEVELOPER_EMAIL', settings.DEFAULT_FROM_EMAIL)
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [recipient_email],
                fail_silently=False,
            )

            # Return success message
            return render(request, 'music_beta/service_request.html', {
                'form': ServiceRequestForm(),
                'success': True,
                'message': 'Your service request has been submitted successfully. We will contact you soon.'
            })
    else:
        form = ServiceRequestForm()

    return render(request, 'music_beta/service_request.html', {'form': form})

def music_platform(request):
    """
    View function for the CTV Music platform demo.
    """
    # Get all genres, artists, albums, and tracks
    genres = Genre.objects.all()
    artists = Artist.objects.all()
    albums = Album.objects.all().prefetch_related('genre', 'tracks')
    tracks = Track.objects.all().select_related('artist', 'album')

    # If no data exists, create placeholder data
    if not genres.exists():
        # Create genres
        rock = Genre.objects.create(name='Rock')
        pop = Genre.objects.create(name='Pop')
        hiphop = Genre.objects.create(name='Hip Hop')
        jazz = Genre.objects.create(name='Jazz')
        electronic = Genre.objects.create(name='Electronic')

        # Create artists
        artist1 = Artist.objects.create(
            name='Sample Artist 1',
            bio='Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        )
        artist2 = Artist.objects.create(
            name='Sample Artist 2',
            bio='Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
        )

        # Create albums
        album1 = Album.objects.create(
            title='Sample Album 1',
            artist=artist1,
            release_date='2023-01-01',
            cover_image='https://picsum.photos/300'
        )
        album1.genre.add(rock, pop)

        album2 = Album.objects.create(
            title='Sample Album 2',
            artist=artist2,
            release_date='2023-02-01',
            cover_image='https://picsum.photos/300'
        )
        album2.genre.add(hiphop, electronic)

        # Create tracks
        Track.objects.create(
            title='Sample Track 1',
            album=album1,
            artist=artist1,
            audio_file='https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3',
            duration='3:45'
        )
        Track.objects.create(
            title='Sample Track 2',
            album=album1,
            artist=artist1,
            audio_file='https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3',
            duration='4:12'
        )
        Track.objects.create(
            title='Sample Track 3',
            album=album2,
            artist=artist2,
            audio_file='https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3',
            duration='3:22'
        )
        Track.objects.create(
            title='Sample Track 4',
            album=album2,
            artist=artist2,
            audio_file='https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3',
            duration='5:01'
        )

        # Refresh querysets
        genres = Genre.objects.all()
        artists = Artist.objects.all()
        albums = Album.objects.all().prefetch_related('genre', 'tracks')
        tracks = Track.objects.all().select_related('artist', 'album')

    # Get trending tracks (top 5 by play count)
    trending_tracks = Track.objects.all().order_by('-play_count')[:5]

    context = {
        'genres': genres,
        'artists': artists,
        'albums': albums,
        'tracks': tracks,
        'trending_tracks': trending_tracks,
    }

    return render(request, 'music_beta/music_platform.html', context)

@csrf_exempt
def update_play_count(request, track_id):
    """
    View function to update the play count for a track.
    """
    if request.method == 'POST':
        try:
            track = get_object_or_404(Track, id=track_id)
            track.play_count += 1
            track.last_played = timezone.now()
            track.save()
            return JsonResponse({'success': True, 'play_count': track.play_count})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

# copyright pdf gen
def generate_copyright_pdf(request):
    # Example: Accept form data via GET or POST, here static for demo
    holder = "Your Company Name"
    license_type = "All Rights Reserved"
    year = "2024"

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, "Copyright and License Agreement")

    p.setFont("Helvetica", 12)
    p.drawString(100, 760, f"Copyright Holder: {holder}")
    p.drawString(100, 740, f"License Type: {license_type}")
    p.drawString(100, 720, f"Year: {year}")

    p.drawString(100, 680, "Terms and Conditions:")
    p.setFont("Helvetica", 10)
    text = p.beginText(100, 660)
    text.textLines("""
This document certifies that the copyright holder owns the rights to the work.
Any use beyond the scope of this license requires written permission.
Please read the full terms on our website or contact legal@yourcompany.com.
    """)
    p.drawText(text)

    p.showPage()
    p.save()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="copyright_boilerplate.pdf"'
    return response

# end copyright pdf gen

# download copyright boilerplate
def download_copyright_boilerplate(request):
    filepath = os.path.join(settings.MEDIA_ROOT, 'copyright_docs', 'copyright_boilerplate.pdf')
    if not os.path.exists(filepath):
        raise Http404("Boilerplate document not found.")

    return FileResponse(open(filepath, 'rb'), as_attachment=True, filename='copyright_boilerplate.pdf')


def generate_pdf_bytes(holder, license_type, year, additional_notes):
    buffer = BytesIO()

    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - 100, "Copyright and License Agreement")

    c.setFont("Helvetica", 12)
    lines = [
        f"Copyright Holder: {holder}",
        f"License Type: {license_type or 'N/A'}",
        f"Year: {year or 'N/A'}",
        "",
        "Terms and Conditions:",
        "This document certifies the copyright holder owns all rights to this work.",
        "Any use beyond the scope of this license requires written permission.",
        "Please contact legal@tfnms.co with questions or to request authorization.",
        "",
        "Additional Notes:",
        additional_notes or "None",
    ]

    y = height - 150
    for line in lines:
        c.drawString(72, y, line)
        y -= 18

    c.save()
    buffer.seek(0)
    return buffer


def copyright_request_view(request):
    if request.method == 'POST':
        form = CopyrightForm(request.POST)
        if form.is_valid():
            holder = form.cleaned_data['holder']
            license_type = form.cleaned_data.get('license_type', '')
            year = form.cleaned_data.get('year', '')
            additional_notes = form.cleaned_data.get('additional_notes', '')
            sender_email = form.cleaned_data['email']

            pdf_file = generate_pdf_bytes(holder, license_type, year, additional_notes)

            # Prepare email
            email = EmailMessage(
                subject="New Copyright Boilerplate Request",
                body="Please find attached the copyright boilerplate generated from the form.",
                from_email=sender_email,
                to=["legal@tfnms.co"],
            )
            email.attach("copyright_boilerplate.pdf", pdf_file.read(), "application/pdf")
            email.send()

            return HttpResponse("Your request has been sent to legal@tfnms.co. Thank you.")
    else:
        form = CopyrightForm()

    return render(request, "copyright_form.html", {"form": form})

def login_view(request):
    """
    View function for user login.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)

            try:
                user = User.objects.get(username=username)

                # In a real app, use a secure password hashing method
                # For now, we're just comparing plaintext passwords
                if user.password == password:
                    # Set session data
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    request.session['user_type'] = user.user_type

                    # Update last login time
                    user.last_login = timezone.now()
                    user.save()

                    # Set session expiry if remember_me is checked
                    if remember_me:
                        # Session will expire in 2 weeks
                        request.session.set_expiry(1209600)
                    else:
                        # Session will expire when browser is closed
                        request.session.set_expiry(0)

                    messages.success(request, f'Welcome back, {username}!')

                    # Redirect based on user type
                    if user.user_type == 'artist':
                        return redirect('artist_profile')
                    else:  # client
                        return redirect('client_dashboard')
                else:
                    messages.error(request, 'Invalid password.')
            except User.DoesNotExist:
                messages.error(request, 'User does not exist.')
        else:
            messages.error(request, 'Invalid form data.')
    else:
        form = LoginForm()

    return render(request, 'music_beta/login.html', {'form': form})

def logout_view(request):
    """
    View function for user logout.
    """
    # Clear session data
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'username' in request.session:
        del request.session['username']
    if 'user_type' in request.session:
        del request.session['user_type']

    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

def client_dashboard(request):
    """
    View function for the client dashboard.
    Only accessible to users with user_type='client'.
    """
    # Check if user is logged in and is a client
    if 'user_id' not in request.session:
        messages.error(request, 'You must be logged in to view your dashboard.')
        return redirect('login')

    user_id = request.session['user_id']
    try:
        user = User.objects.get(id=user_id)
        if user.user_type != 'client':
            messages.error(request, 'You must be a client to access this page.')
            return redirect('home')
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('login')

    # Get user's campaigns
    campaigns = ClientCampaign.objects.filter(user=user).order_by('-created_at')

    # Get or create user's cart
    cart, created = Cart.objects.get_or_create(user=user)

    context = {
        'user': user,
        'campaigns': campaigns,
        'cart': cart,
    }

    return render(request, 'music_beta/client_dashboard.html', context)

def campaign_detail(request, campaign_id):
    """
    View function for campaign detail.
    Only accessible to the campaign owner.
    """
    # Check if user is logged in
    if 'user_id' not in request.session:
        messages.error(request, 'You must be logged in to view campaign details.')
        return redirect('login')

    user_id = request.session['user_id']
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('login')

    # Get campaign and check ownership
    campaign = get_object_or_404(ClientCampaign, id=campaign_id)
    if campaign.user.id != user.id:
        messages.error(request, 'You do not have permission to view this campaign.')
        return redirect('client_dashboard')

    context = {
        'user': user,
        'campaign': campaign,
    }

    return render(request, 'music_beta/campaign_detail.html', context)

def create_campaign(request):
    """
    View function for creating a new campaign.
    Only accessible to users with user_type='client'.
    """
    # Check if user is logged in and is a client
    if 'user_id' not in request.session:
        messages.error(request, 'You must be logged in to create a campaign.')
        return redirect('login')

    user_id = request.session['user_id']
    try:
        user = User.objects.get(id=user_id)
        if user.user_type != 'client':
            messages.error(request, 'You must be a client to create a campaign.')
            return redirect('home')
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('login')

    # Handle form submission
    if request.method == 'POST':
        form = ClientCampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.user = user
            campaign.save()
            messages.success(request, 'Campaign created successfully.')
            return redirect('campaign_detail', campaign_id=campaign.id)
    else:
        form = ClientCampaignForm()

    context = {
        'user': user,
        'form': form,
    }

    return render(request, 'music_beta/create_campaign.html', context)

def edit_campaign(request, campaign_id):
    """
    View function for editing a campaign.
    Only accessible to the campaign owner.
    """
    # Check if user is logged in
    if 'user_id' not in request.session:
        messages.error(request, 'You must be logged in to edit a campaign.')
        return redirect('login')

    user_id = request.session['user_id']
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('login')

    # Get campaign and check ownership
    campaign = get_object_or_404(ClientCampaign, id=campaign_id)
    if campaign.user.id != user.id:
        messages.error(request, 'You do not have permission to edit this campaign.')
        return redirect('client_dashboard')

    # Handle form submission
    if request.method == 'POST':
        form = ClientCampaignForm(request.POST, instance=campaign)
        if form.is_valid():
            form.save()
            messages.success(request, 'Campaign updated successfully.')
            return redirect('campaign_detail', campaign_id=campaign.id)
    else:
        form = ClientCampaignForm(instance=campaign)

    context = {
        'user': user,
        'campaign': campaign,
        'form': form,
    }

    return render(request, 'music_beta/edit_campaign.html', context)

def add_to_cart(request, track_id):
    """
    View function for adding a track to the cart.
    Only accessible to users with user_type='client'.
    """
    # Check if user is logged in and is a client
    if 'user_id' not in request.session:
        messages.error(request, 'You must be logged in to add tracks to your cart.')
        return redirect('login')

    user_id = request.session['user_id']
    try:
        user = User.objects.get(id=user_id)
        if user.user_type != 'client':
            messages.error(request, 'You must be a client to add tracks to your cart.')
            return redirect('home')
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('login')

    # Get or create user's cart
    cart, created = Cart.objects.get_or_create(user=user)

    # Get track and add to cart
    track = get_object_or_404(Track, id=track_id)
    cart.tracks.add(track)
    cart.save()

    messages.success(request, f'"{track.title}" has been added to your cart.')

    # Redirect back to the referring page or to the music platform
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect('music_platform')

def remove_from_cart(request, track_id):
    """
    View function for removing a track from the cart.
    Only accessible to the cart owner.
    """
    # Check if user is logged in
    if 'user_id' not in request.session:
        messages.error(request, 'You must be logged in to remove tracks from your cart.')
        return redirect('login')

    user_id = request.session['user_id']
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('login')

    # Get user's cart
    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        messages.error(request, 'Cart not found.')
        return redirect('client_dashboard')

    # Get track and remove from cart
    track = get_object_or_404(Track, id=track_id)
    cart.tracks.remove(track)
    cart.save()

    messages.success(request, f'"{track.title}" has been removed from your cart.')

    # Redirect back to the referring page or to the client dashboard
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect('client_dashboard')
