from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from vinyl.models import Album, Artist, Genre, Collection, User


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ["title", "artist", "year", "created_by", "created_at", ]
    list_filter = ["artist", ]
    search_fields = ["title", ]


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("country", )
    fieldsets = UserAdmin.fieldsets + (("Additional info", {"fields": ("country", )}),)


admin.site.register(Artist)
admin.site.register(Genre)
admin.site.register(Collection)
