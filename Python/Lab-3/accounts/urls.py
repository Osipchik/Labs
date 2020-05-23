from django.urls import path, register_converter

from Twitter.converter import NegativeIntConverter
from . import views

app_name = 'accounts'

register_converter(NegativeIntConverter, 'negint')

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('profile/<int:id>/', views.profile_view, name='profile'),
    path('profile/personalize/update-image/<str:image_type>/', views.update_user_image, name='update_image'),
    path('profile/personalize/change-description', views.change_description, name='change_description'),

    path('profile/follow/<int:author_id>', views.follow_view, name='follow'),
    path('profile/unfollow/<int:author_id>', views.unfollow_view, name='unfollow'),

    path('profile/followers/<int:user_id>', views.followers, name='followers'),
    path('profile/following/<int:user_id>', views.following, name='following')
]
