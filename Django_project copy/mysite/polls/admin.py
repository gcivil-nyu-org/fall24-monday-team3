from django.contrib import admin
from .models import Post, Rating

class RatingInline(admin.TabularInline):
    model = Rating
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_preview', 'average_rating')
    list_filter = ('average_rating',)
    search_fields = ('content',)
    inlines = [RatingInline]

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'value')
    list_filter = ('value',)
    search_fields = ('post__content',)