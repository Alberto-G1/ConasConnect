from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Content(models.Model):
    CONTENT_TYPES = (
        ('free', 'Free Content'),
        ('premium', 'Premium Content'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES, default='free')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='contents')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contents')
    file = models.FileField(upload_to='content_files/', null=True, blank=True)
    image = models.ImageField(upload_to='content_images/', null=True, blank=True)
    video_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def can_user_access(self, user):
        """Check if user can access this content"""
        if self.content_type == 'free':
            return True
        return user.can_access_premium_content()

class ContentView(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='content_views')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('content', 'user')

class Comment(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.content.title}"
