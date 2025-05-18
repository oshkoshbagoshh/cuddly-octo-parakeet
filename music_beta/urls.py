from django.urls import path
from . import views

# app_name = 'music_beta'
urlpatterns = [
    path('', views.home, name='home'),
    path('music/', views.music_platform, name='music_platform'),
    path('signup/', views.signup, name='signup'),
    path('upload-ad-campaign/', views.upload_ad_campaign, name='upload_ad_campaign'),
    path('search/', views.search, name='search'),
    path('pexels-images/', views.get_pexels_images, name='pexels_images'),
    path('service-request/', views.service_request, name='service_request'),
    path('update-play-count/<int:track_id>/', views.update_play_count, name='update_play_count'),
]
