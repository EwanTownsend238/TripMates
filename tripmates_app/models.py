from django.contrib.auth.models import User
from django.db import models

max_textbox_length = 200

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # additional attributes to include
    biography = models.CharField(max_length=max_textbox_length, blank=True)
    picture = models.ImageField(upload_to="profile_images", blank=True)

    def __str__(self):
        return self.user.username
    
    def follow(self, other_user):
        if self.user != other_user:  # Prevent following yourself
            Follow.objects.get_or_create(follower=self.user, followed=other_user)

    def unfollow(self, other_user):
        Follow.objects.filter(follower=self.user, followed=other_user).delete()

    def is_following(self, other_user):
        return Follow.objects.filter(follower=self.user, followed=other_user).exists()

    def followers_count(self):
        return self.user.followers.count()

    def following_count(self):
        return self.user.following.count()

class Post(models.Model):
    media_types = [("image", "Image"), ("video", "Video"),]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=max_textbox_length)
    description = models.CharField(max_length=max_textbox_length)
    date_uploaded = models.DateField(auto_now_add=True)
    media_type = models.CharField(max_length=10, choices=media_types)
    image = models.ImageField(upload_to="posts/images", blank=True, null=True)
    video = models.FileField(upload_to="posts/videos", blank=True, null=True)
    likes = models.IntegerField(default = 0)

    def __str__(self):
        return f'Post by {self.author} - {self.media_type}'

    def is_image(self):
        return self.media_type == 'image' and self.image

    def is_video(self):
        return self.media_type == 'video' and self.video
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delte = models.CASCADE)
    content = models.CharField(max_length=max_textbox_length)
    date_uploaded = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
    
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')  # Prevent duplicate follows

    def __str__(self):
        return f"{self.follower} follows {self.followed}"