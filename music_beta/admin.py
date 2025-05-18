from django.contrib import admin
from .models import Genre, Artist, Album, Track, ServiceRequest

# Register your models here.
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_date')
    list_filter = ('genre', 'release_date')
    search_fields = ('title', 'artist__name')

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album', 'duration')
    list_filter = ('album__genre',)
    search_fields = ('title', 'artist__name', 'album__title')

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'company', 'service_type', 'created_at')
    list_filter = ('service_type', 'created_at')
    search_fields = ('name', 'email', 'company')
    readonly_fields = ('created_at',)
