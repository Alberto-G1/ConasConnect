from django import forms
from .models import Content, Category, Comment

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'description', 'content_type', 'category', 'file', 'image', 'video_url']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content_type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
        }
