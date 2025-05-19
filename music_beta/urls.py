from django.urls import path, include
from . import views
from .views import copyright_request_view
from rest_framework.routers import DefaultRouter
from .api import (
    GenreViewSet, ArtistViewSet, AlbumViewSet, TrackViewSet,
    UserViewSet, AdCampaignViewSet, CopyrightViewSet, ServiceRequestViewSet
)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'genres', GenreViewSet)
router.register(r'artists', ArtistViewSet)
router.register(r'albums', AlbumViewSet)
router.register(r'tracks', TrackViewSet)
router.register(r'users', UserViewSet)
router.register(r'ad-campaigns', AdCampaignViewSet)
router.register(r'copyrights', CopyrightViewSet)
router.register(r'service-requests', ServiceRequestViewSet)

# app_name = 'music_beta'
urlpatterns = [
    path('', views.home, name='home'),
    path('music/', views.music_platform, name='music_platform'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('upload-ad-campaign/', views.upload_ad_campaign, name='upload_ad_campaign'),
    path('search/', views.search, name='search'),
    path('pexels-images/', views.get_pexels_images, name='pexels_images'),
    path('service-request/', views.service_request, name='service_request'),
    path('update-play-count/<int:track_id>/', views.update_play_count, name='update_play_count'),
    path('legal/generate_copyright_pdf/', views.generate_copyright_pdf, name='generate_copyright_pdf'),
    path('legal/download_copyright_boilerplate/', views.download_copyright_boilerplate, name='download_copyright_boilerplate'),
    path('legal/copyright_request/', copyright_request_view, name='copyright_request'),

    # Client dashboard URLs
    path('client/dashboard/', views.client_dashboard, name='client_dashboard'),
    path('client/campaign/<int:campaign_id>/', views.campaign_detail, name='campaign_detail'),
    path('client/campaign/create/', views.create_campaign, name='create_campaign'),
    path('client/campaign/<int:campaign_id>/edit/', views.edit_campaign, name='edit_campaign'),
    path('client/cart/add/<int:track_id>/', views.add_to_cart, name='add_to_cart'),
    path('client/cart/remove/<int:track_id>/', views.remove_from_cart, name='remove_from_cart'),

    # API URLs
    path('api/', include(router.urls)),

    # Include artist_portal URLs
    path('artist/', include('artist_portal.urls')),
]
