from django.urls import path
from . import views
from .views import copyright_request_view

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
    path('legal/generate_copyright_pdf/', views.generate_copyright_pdf, name='generate_copyright_pdf'),
    path('legal/download_copyright_boilerplate/', views.download_copyright_boilerplate, name='download_copyright_boilerplate'),
    path('legal/copyright_request/', copyright_request_view, name='copyright_request'),


]
