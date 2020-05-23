from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.utils import timezone
from django.utils.timesince import timesince

from Twitter.managers import LikeManager, TweetManager, BookmarkManager, CommentManager
from Twitter.validators import validate_image_file


class Like(models.Model):
    user = models.ForeignKey(User, related_name='like', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, related_name='likes', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeManager()


class Tweet(models.Model):
    content = models.TextField(max_length=235)
    image = models.ImageField(upload_to='tweet_images/', blank=True, validators=[validate_image_file])

    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='twits')
    likes = GenericRelation(Like, related_name='likes')
    is_deleted = models.BooleanField(default=False)

    objects = TweetManager()

    def get_time_diff(self):
        return timesince(self.created_date, timezone.now())


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=235)
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    likes = GenericRelation(Like, related_name='likes')

    objects = CommentManager()

    def get_time_diff(self):
        return timesince(self.created_date, timezone.now())


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='bookmarks')

    objects = BookmarkManager()
