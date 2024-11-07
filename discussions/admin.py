# discussions/admin.py
from django.contrib import admin
from .models import Topic, Discussion, Reply, Vote


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')


@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'author', 'topic', 'created_at', 'updated_at', 'views'
    )
    list_filter = ('topic', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'author__username')
    raw_id_fields = ('author',)
    date_hierarchy = 'created_at'


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('discussion', 'author', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('content', 'author__username', 'discussion__title')
    raw_id_fields = ('author', 'discussion')


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'discussion', 'value', 'created_at')
    list_filter = ('value', 'created_at')
    raw_id_fields = ('user', 'discussion')
