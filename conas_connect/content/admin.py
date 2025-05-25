from django.contrib import admin
from .models import Category, Content, Comment, ContentView

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'content_type', 'views_count', 'is_active', 'created_at']
    list_filter = ['content_type', 'category', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'author__username']
    readonly_fields = ['views_count']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'content', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'content__title', 'text']

@admin.register(ContentView)
class ContentViewAdmin(admin.ModelAdmin):
    list_display = ['user', 'content', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['user__username', 'content__title']
