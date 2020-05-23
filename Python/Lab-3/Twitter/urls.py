from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include, register_converter
from django.contrib import admin
from . import views
from .converter import NegativeIntConverter

app_name = 'twitterApp'

register_converter(NegativeIntConverter, 'negint')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    path('accounts/', include('accounts.urls')),
    path('search/', views.search, name='search'),
    path('like/<int:id>/', views.like_view),

    path('twit/<int:twit_id>/', views.twit_details, name='twit_detail'),
    path('twit/create/', views.create_twit, name='create_twit'),
    path('twit/get/<int:take>/<negint:start_from_id>', views.get_twits, name='get_twits'),
    path('twit/delete/<int:twit_id>', views.delete_twit, name='delete_twit'),
    path('twit/restore/<int:twit_id>', views.restore_twit, name='restore_twit'),
    path('twit/liked/<int:take>/<negint:start_from_id>/<int:user_id>', views.get_liked_twits, name='liked_twits'),
    path('twit/media/<int:take>/<negint:start_from_id>/<int:user_id>', views.get_media_twits, name='get_media_twits'),
    path('twit/get/<int:take>/<negint:start_from_id>/<int:user_id>', views.get_user_twits),

    path('twit/comments/create/<int:twit_id>', views.create_comment, name='create_comment'),
    path('comment/get/<int:twit_id>/<int:take>/<negint:start_from_id>', views.get_comments, name='get_comments'),
    path('comment/get_user_comments/<int:take>/<negint:start_from_id>/<int:user_id>', views.get_user_comments, name='user_comments'),

    path('bookmarks/', views.bookmarks, name='bookmarks'),
    path('bookmarks/add/<int:twit_id>', views.add_bookmark, name='add_bookmark'),
    path('bookmarks/remove/<int:twit_id>', views.remove_bookmark, name='remove_bookmark'),

    path('search/find-by/name', views.find_users_by_name, name='find_by_name'),
    path('search/find-by/username', views.find_users_by_username, name='find_by_username'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
