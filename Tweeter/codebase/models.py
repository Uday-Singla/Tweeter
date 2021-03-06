from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

User._meta.get_field('email')._unique = False

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dp = models.ImageField(default='default.jpg', blank=True,  upload_to='profile_pics')
    bio = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    dob = models.DateField(null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='user_follows', blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='user_following', blank=True)
    subscribed = models.ManyToManyField('self', symmetrical=False, related_name='user_subscribed_to', blank=True)
    subscribers = models.ManyToManyField('self', symmetrical=False, related_name='user_subscribed', blank=True)
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        for follower in self.followers.all():
            follower.following.add(Profile.objects.filter(user=self.user).get())
        for follows in self.following.all():
            follows.followers.add(Profile.objects.filter(user=self.user).get())
        
        for subscriber in self.subscribers.all():
            subscriber.subscribed.add(Profile.objects.filter(user=self.user).get())
        for subscriber in self.subscribed.all():
            subscriber.subscribers.add(Profile.objects.filter(user=self.user).get())

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} Profile"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True)
    image = models.ImageField(blank=True,  upload_to='post_pics')
    date = models.DateTimeField(default = timezone.now, editable=False)

    def __str__(self):
         return f"{self.user.username} PostID:{self.pk}"

class EditHistory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True)
    image = models.ImageField(blank=True,  upload_to='post_pics_edited')
    date = models.DateTimeField(default = timezone.now, editable=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        if self.post:
            return f"PostID:{self.post.pk} EditID:{self.pk}"

    class Meta:
        verbose_name_plural = "Edit Histories"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} PostID:{self.post.pk} CommentID:{self.pk}"