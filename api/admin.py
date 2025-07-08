from django.contrib import admin
from .models import UserProfile
from django.utils.html import format_html

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'email', 'phone', 'gender', 'dob',
        'age', 'city', 'profession', 'education',
        'interests', 'photo_preview'
    )
    search_fields = ('name', 'email', 'phone', 'city', 'profession', 'education')
    list_filter = ('gender', 'city', 'profession', 'education')

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" />', obj.photo.url)
        return "No Photo"

    photo_preview.short_description = "Photo"
