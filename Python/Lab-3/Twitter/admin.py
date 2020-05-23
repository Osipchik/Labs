from django.contrib import admin

from accounts.models import Contact, UserProfile
from .models import Tweet, Comment, Like, Bookmark

admin.site.register(Tweet)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Bookmark)

admin.site.register(UserProfile)
admin.site.register(Contact)
