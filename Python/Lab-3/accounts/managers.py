# from django.db import models
#
#
# class FollowingManager(models.Manager):
#     use_for_related_fields = True
#
#     def is_remembered(self, tweet, user_id):
#         return self.get_queryset().filter(tweet=tweet, user_id=user_id).exists()
