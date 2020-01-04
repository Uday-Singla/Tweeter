from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dp = models.ImageField(default='default.jpg', blank=True,  upload_to='profile_pics')
    bio = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    dob = models.DateField(null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='user_follows', blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='user_following', blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        for follower in self.followers.all():
            follower.following.add(Profile.objects.filter(user=self.user).get())
        for follows in self.following.all():
            follows.followers.add(Profile.objects.filter(user=self.user).get())

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} Profile"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True)
    image = models.ImageField(blank=True,  upload_to='post_pics')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} PostID:{self.pk}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} PostID:{self.post.pk} CommentID:{self.pk}"