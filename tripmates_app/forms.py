from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, User, Post, Comment

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["username", "email", "password",]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["biography", "picture",]

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['media_type', 'image', 'video']
    
    def clean(self):
        cleaned_data = super().clean()
        media_type = cleaned_data.get('media_type')
        image = cleaned_data.get('image')
        video = cleaned_data.get('video')

        if media_type == 'image' and not image:
            self.add_error('image', 'Please upload an image.')
        elif media_type == 'video' and not video:
            self.add_error('video', 'Please upload a video.')
        elif media_type not in ['image', 'video']:
            self.add_error('media_type', 'Invalid media type.')

        return cleaned_data
    
class CommentForm(forms.modelForm):
    class Meta:
        model = Comment
        fields = ["content"]