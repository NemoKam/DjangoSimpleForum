from django.db import models
# translation
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


# UserProfileModel
class ProfileUser(AbstractUser):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'мужской'),
        (FEMALE, 'женский')
    )
    activation_key = models.CharField(max_length=128, blank=True)
    birthday = models.DateField(_('birthday'), default=None, null=True)
    gender = models.CharField(_('gender'), max_length=1, choices=GENDER_CHOICES, default='M')
    avatar = models.ImageField(upload_to='users/avatars', blank=True, default="users/avatars/default_user_icon.png")
    about = models.CharField(_('about'), max_length=128, null=True)
    pre_friends = models.ManyToManyField("self", blank=True, related_name=_("maybe_friends"), symmetrical=False)
    friends = models.ManyToManyField("self", blank=True, related_name=_("friends"))
    
    def __str__(self):
        return self.username

class Post(models.Model):
    author = models.ForeignKey('ProfileUser', on_delete=models.CASCADE)
    text = models.CharField(max_length=4000)
    img = models.ImageField(upload_to='posts/', blank=True, null=True)
    likes = models.ManyToManyField("ProfileUser", blank=True, related_name='post_likes')
    comments = models.ManyToManyField("Comment", blank=True, related_name='post_comments')
    warned = models.ManyToManyField("ProfileUser", blank=True, related_name='post_warned')
    created_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    author = models.ForeignKey('ProfileUser', on_delete=models.CASCADE, related_name='comment_author')
    text = models.CharField(max_length=4000)
    img = models.ImageField(upload_to='comments/avatars', blank=True, null=True)
    likes = models.ManyToManyField("ProfileUser", blank=True, related_name='comment_likes')
    warned = models.ManyToManyField("ProfileUser", blank=True, related_name='comment_warned')
    created_at = models.DateTimeField(auto_now=True)