#  Copyright (c) 2025. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

from rest_framework import viewsets, permissions
from .models import Genre, Artist, Album, Track, User, AdCampaign, Copyright, ServiceRequest
from .serializers import (
    GenreSerializer, ArtistSerializer, AlbumSerializer, TrackSerializer,
    UserSerializer, AdCampaignSerializer, CopyrightSerializer, ServiceRequestSerializer
)

class GenreViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows genres to be viewed or edited.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ArtistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows artists to be viewed or edited.
    """
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AlbumViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows albums to be viewed or edited.
    """
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TrackViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tracks to be viewed or edited.
    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    Users can only access their own data unless they are admin.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        Filter queryset to return only the current user's data unless the user is admin.
        """
        user_id = self.request.session.get('user_id')
        if not user_id:
            return User.objects.none()

        # Check if user is admin (for simplicity, we're just checking if user_id is 1)
        if user_id == 1:
            return User.objects.all()

        # Regular users can only see their own data
        return User.objects.filter(id=user_id)

    def get_permissions(self):
        """
        Custom permissions:
        - List/Retrieve: Allow if user is authenticated and requesting their own data
        - Create/Update/Delete: Admin only
        """
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

class AdCampaignViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ad campaigns to be viewed or edited.
    """
    queryset = AdCampaign.objects.all()
    serializer_class = AdCampaignSerializer
    permission_classes = [permissions.IsAuthenticated]

class CopyrightViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows copyright information to be viewed or edited.
    """
    queryset = Copyright.objects.all()
    serializer_class = CopyrightSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ServiceRequestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows service requests to be viewed or edited.
    """
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    permission_classes = [permissions.IsAdminUser]
