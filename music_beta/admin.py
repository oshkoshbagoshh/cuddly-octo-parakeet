from django.contrib import admin
from .models import Genre, Artist, Album, Track, ServiceRequest, User, Copyright


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'bio')
    search_fields = ('name',)
    list_filter = ()  # Add filters if applicable
    autocomplete_fields = ()  # Add if there are ForeignKeys or ManyToMany you want autocompleted
    ordering = ('name',)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_date')
    list_filter = ('genre', 'release_date')
    search_fields = ('title', 'artist__name')
    filter_horizontal = ('genre',)  # For ManyToMany genre field for better usability
    date_hierarchy = 'release_date'
    ordering = ('release_date', 'title')


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album', 'duration')
    list_filter = ('album__genre', 'artist')
    search_fields = ('title', 'artist__name', 'album__title')
    ordering = ('album', 'title')


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'company', 'service_type', 'created_at')
    list_filter = ('service_type', 'created_at')
    search_fields = ('name', 'email', 'company')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'




@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined')
    search_fields = ('username', 'email')
    # list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined')
    ordering = ('username',)
    readonly_fields = ('date_joined',)

# legal
@admin.register(Copyright)
class CopyrightAdmin(admin.ModelAdmin):
    pass
    # TODO : add administrative views for copyright management


