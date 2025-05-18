import os
import random
import requests
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.files.base import ContentFile
from faker import Faker
from music_beta.models import (
    Genre, Artist, Album, Track, User, AdCampaign, ServiceRequest
)

class Command(BaseCommand):
    help = 'Generate fake data for the music_beta app'

    def add_arguments(self, parser):
        parser.add_argument('--genres', type=int, default=10, help='Number of genres to create')
        parser.add_argument('--artists', type=int, default=20, help='Number of artists to create')
        parser.add_argument('--albums', type=int, default=30, help='Number of albums to create')
        parser.add_argument('--tracks', type=int, default=100, help='Number of tracks to create')
        parser.add_argument('--users', type=int, default=15, help='Number of users to create')
        parser.add_argument('--ad_campaigns', type=int, default=10, help='Number of ad campaigns to create')
        parser.add_argument('--service_requests', type=int, default=5, help='Number of service requests to create')

    def handle(self, *args, **options):
        fake = Faker()

        # Create genres
        self.stdout.write(self.style.SUCCESS('Creating genres...'))
        genres = self.create_genres(options['genres'])

        # Create artists
        self.stdout.write(self.style.SUCCESS('Creating artists...'))
        artists = self.create_artists(options['artists'], fake)

        # Create albums
        self.stdout.write(self.style.SUCCESS('Creating albums...'))
        albums = self.create_albums(options['albums'], artists, genres, fake)

        # Create tracks
        self.stdout.write(self.style.SUCCESS('Creating tracks...'))
        self.create_tracks(options['tracks'], albums, artists, fake)

        # Create users
        self.stdout.write(self.style.SUCCESS('Creating users...'))
        users = self.create_users(options['users'], fake)

        # Create ad campaigns
        self.stdout.write(self.style.SUCCESS('Creating ad campaigns...'))
        self.create_ad_campaigns(options['ad_campaigns'], users, genres, fake)

        # Create service requests
        self.stdout.write(self.style.SUCCESS('Creating service requests...'))
        self.create_service_requests(options['service_requests'], fake)

        self.stdout.write(self.style.SUCCESS('Fake data generation completed!'))

    def create_genres(self, count):
        # List of common music genres
        genre_names = [
            'Rock', 'Pop', 'Hip Hop', 'R&B', 'Country', 'Jazz', 'Blues', 
            'Electronic', 'Classical', 'Reggae', 'Folk', 'Metal', 'Punk', 
            'Soul', 'Funk', 'Disco', 'Techno', 'House', 'Ambient', 'Indie'
        ]

        genres = []
        # Use existing genres or create new ones
        existing_genres = list(Genre.objects.all())

        if existing_genres:
            genres.extend(existing_genres)
            self.stdout.write(f'Found {len(existing_genres)} existing genres')

        # Create new genres if needed
        new_genres_needed = max(0, count - len(genres))
        if new_genres_needed > 0:
            # Shuffle the genre names to get random selection
            random.shuffle(genre_names)

            # Create new genres
            for i in range(min(new_genres_needed, len(genre_names))):
                genre, created = Genre.objects.get_or_create(name=genre_names[i])
                if created:
                    genres.append(genre)
                    self.stdout.write(f'Created genre: {genre.name}')

        return genres

    def create_artists(self, count, fake):
        artists = []
        # Use existing artists or create new ones
        existing_artists = list(Artist.objects.all())

        if existing_artists:
            artists.extend(existing_artists)
            self.stdout.write(f'Found {len(existing_artists)} existing artists')

        # Create new artists if needed
        new_artists_needed = max(0, count - len(artists))
        if new_artists_needed > 0:
            for i in range(new_artists_needed):
                # Generate artist data
                name = fake.name()
                bio = fake.paragraph(nb_sentences=5)

                # Get a random image from Unsplash
                image_url = f"https://source.unsplash.com/300x300/?musician,artist,singer&random={fake.uuid4()}"

                try:
                    # Create the artist
                    artist = Artist(name=name, bio=bio)

                    # Download and save the image
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        image_name = f"{fake.uuid4()}.jpg"
                        artist.image.save(image_name, ContentFile(response.content), save=False)

                    artist.save()
                    artists.append(artist)
                    self.stdout.write(f'Created artist: {artist.name}')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creating artist: {str(e)}'))

        return artists

    def create_albums(self, count, artists, genres, fake):
        albums = []
        # Use existing albums or create new ones
        existing_albums = list(Album.objects.all())

        if existing_albums:
            albums.extend(existing_albums)
            self.stdout.write(f'Found {len(existing_albums)} existing albums')

        # Create new albums if needed
        new_albums_needed = max(0, count - len(albums))
        if new_albums_needed > 0 and artists:
            for i in range(new_albums_needed):
                # Generate album data
                title = fake.sentence(nb_words=3).rstrip('.')
                artist = random.choice(artists)
                release_date = fake.date_between(start_date='-10y', end_date='today')

                # Get a random image from Unsplash
                image_url = f"https://source.unsplash.com/300x300/?album,music,cover&random={fake.uuid4()}"

                try:
                    # Create the album
                    album = Album(title=title, artist=artist, release_date=release_date)

                    # Download and save the image
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        image_name = f"{fake.uuid4()}.jpg"
                        album.cover_image.save(image_name, ContentFile(response.content), save=False)

                    album.save()

                    # Add random genres (1-3)
                    album_genres = random.sample(genres, min(random.randint(1, 3), len(genres)))
                    album.genre.set(album_genres)

                    albums.append(album)
                    self.stdout.write(f'Created album: {album.title} by {album.artist.name}')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creating album: {str(e)}'))

        return albums

    def create_tracks(self, count, albums, artists, fake):
        # Use existing tracks or create new ones
        existing_tracks = list(Track.objects.all())

        if existing_tracks:
            self.stdout.write(f'Found {len(existing_tracks)} existing tracks')

        # Create new tracks if needed
        new_tracks_needed = max(0, count - len(existing_tracks))
        if new_tracks_needed > 0 and albums:
            for i in range(new_tracks_needed):
                # Generate track data
                title = fake.sentence(nb_words=4).rstrip('.')
                album = random.choice(albums)
                artist = album.artist  # Use the album's artist

                # Generate a random duration (2-7 minutes)
                minutes = random.randint(2, 7)
                seconds = random.randint(0, 59)
                duration = f"{minutes}:{seconds:02d}"

                try:
                    # Create the track (without audio file for now)
                    track = Track(title=title, album=album, artist=artist, duration=duration)
                    track.save()
                    self.stdout.write(f'Created track: {track.title} on {album.title}')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creating track: {str(e)}'))

    def create_users(self, count, fake):
        users = []
        # Use existing users or create new ones
        existing_users = list(User.objects.all())

        if existing_users:
            users.extend(existing_users)
            self.stdout.write(f'Found {len(existing_users)} existing users')

        # Create new users if needed
        new_users_needed = max(0, count - len(users))
        if new_users_needed > 0:
            for i in range(new_users_needed):
                # Generate user data
                username = fake.user_name()
                email = fake.email()
                password = fake.password()

                try:
                    # Create the user
                    user = User(username=username, email=email, password=password)
                    user.save()
                    users.append(user)
                    self.stdout.write(f'Created user: {user.username}')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creating user: {str(e)}'))

        return users

    def create_ad_campaigns(self, count, users, genres, fake):
        # Use existing ad campaigns or create new ones
        existing_campaigns = list(AdCampaign.objects.all())

        if existing_campaigns:
            self.stdout.write(f'Found {len(existing_campaigns)} existing ad campaigns')

        # Create new ad campaigns if needed
        new_campaigns_needed = max(0, count - len(existing_campaigns))
        if new_campaigns_needed > 0 and users and genres:
            for i in range(new_campaigns_needed):
                # Generate ad campaign data
                title = fake.sentence(nb_words=4).rstrip('.')
                description = fake.paragraph(nb_sentences=3)
                user = random.choice(users)
                genre = random.choice(genres)

                # Random mood and target audience
                mood = random.choice(['happy', 'sad', 'energetic', 'calm', 'inspirational', 'dramatic'])
                target_audience = random.choice(['general', 'youth', 'adults', 'seniors', 'professionals'])

                # Create a YouTube URL placeholder
                youtube_url = f"https://www.youtube.com/watch?v={fake.uuid4()}"

                try:
                    # Create the ad campaign
                    campaign = AdCampaign(
                        title=title,
                        description=description,
                        genre=genre,
                        mood=mood,
                        target_audience=target_audience,
                        user=user,
                        youtube_url=youtube_url
                    )

                    campaign.save()
                    self.stdout.write(f'Created ad campaign: {campaign.title}')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creating ad campaign: {str(e)}'))

    def create_service_requests(self, count, fake):
        # Use existing service requests or create new ones
        existing_requests = list(ServiceRequest.objects.all())

        if existing_requests:
            self.stdout.write(f'Found {len(existing_requests)} existing service requests')

        # Create new service requests if needed
        new_requests_needed = max(0, count - len(existing_requests))
        if new_requests_needed > 0:
            for i in range(new_requests_needed):
                # Generate service request data
                name = fake.name()
                email = fake.email()
                company = fake.company()
                service_type = random.choice(['media_solutions', 'music_services'])
                message = fake.paragraph(nb_sentences=3)
                created_at = fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.get_current_timezone())

                try:
                    # Create the service request
                    service_request = ServiceRequest(
                        name=name,
                        email=email,
                        company=company,
                        service_type=service_type,
                        message=message,
                        created_at=created_at
                    )
                    service_request.save()
                    self.stdout.write(f'Created service request: {service_request.name} - {service_request.company}')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creating service request: {str(e)}'))
