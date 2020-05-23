from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


def get_objects_or_none(obj, **kwargs):
    try:
        return obj.objects.filter(**kwargs)
    except ObjectDoesNotExist:
        return None


def set_likes(obj, user_id):
    obj.is_liked = bool(obj.likes.is_like_exist(obj, user_id))


def prepare_tweet(tweet, user_id):
    set_likes(tweet, user_id)
    tweet.is_remembered = tweet.bookmarks.is_remembered(tweet, user_id)
    return tweet


def set_load_link(obj, take, link, mark_name, *args):
    size = len(obj) if isinstance(obj, list) else obj.count()
    if size == take:
        obj[take // 2].mark_name = mark_name
        obj[take // 2].load_link = '/{}/{}/{}'.format(link, take, -obj[take - 1].id)
        for i in args:
            obj[take // 2].load_link += '/{}'.format(i)


def get_objects(obj, take, skip, **kwargs):
    take = 10 if take < 10 else take

    if skip < 0:
        objects = obj.get_queryset().filter(id__lt=-skip, **kwargs).order_by('-created_date')[:take]
    elif skip > 0:
        objects = obj.get_queryset().filter(id__gt=skip, **kwargs).order_by('-created_date')[:take]
    else:
        objects = obj.get_queryset().filter(**kwargs).order_by('-created_date')[:take]

    return objects


class LikeManager(models.Manager):
    use_for_related_fields = True

    def is_like_exist(self, obj, user_id):
        like = self.get_queryset().filter(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id,
                                          user_id=user_id)
        return like if like.exists() else None


class TweetManager(models.Manager):
    use_for_related_fields = True

    def get_twits(self, user, take, skip, **kwargs):
        if not isinstance(take, int) and not isinstance(skip, int):
            return None

        if user.is_authenticated:
            users = user.following.all() | get_objects_or_none(User, id=user.id)
            twits = get_objects(self, take, skip, user__in=users, **kwargs)
            for i in twits:
                prepare_tweet(i, user.id)
        else:
            twits = get_objects(self, take, skip, **kwargs)

        return twits

    def get_user_twits(self, user, take, skip, author_id, **kwargs):
        twits = get_objects(self, take, skip, user_id=author_id, **kwargs)

        if user.is_authenticated:
            for i in twits:
                prepare_tweet(i, user.id)

        return twits


class BookmarkManager(models.Manager):
    use_for_related_fields = True

    def is_remembered(self, tweet, user_id):
        return self.get_queryset().filter(tweet=tweet, user_id=user_id).exists()


class CommentManager(models.Manager):
    use_for_related_fields = True

    def get_comments(self, user, take, skip, **kwargs):
        comments = get_objects(self, take, skip, **kwargs)

        if user.is_authenticated:
            for i in comments:
                set_likes(i, user.id)

        return comments
