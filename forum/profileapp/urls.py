from django.urls import path
import profileapp.views as profileapp

app_name = 'profileapp'

urlpatterns = [
    path('', profileapp.user_profile, name='profile'),
    path('<str:username>', profileapp.user_other_profile, name='other_profile'),
    path('create/', profileapp.profile_create, name='profile_create'),
    path('edit/', profileapp.profile_edit, name='profile_edit'),
    path('friends/search/<str:username>', profileapp.friends_search, name='friends_search'),
    path('friends/add/<str:username>', profileapp.friends_add, name='friends_add'),
    path('friends/delete/<str:username>', profileapp.friends_delete, name='friends_delete'),
    path('friends/get/', profileapp.friends_get, name='friends_get'),
    path('friends/requested/', profileapp.friends_requested, name='friends_requested'),
    path('posts/create/', profileapp.posts_create, name='posts_create'),
    path('posts/<int:post_id>/like/', profileapp.posts_like, name='posts_like'),
    path('posts/<int:post_id>/warn/', profileapp.posts_warn, name='posts_warn'),
    path('posts/<int:post_id>/delete/', profileapp.posts_delete, name='posts_delete'),
    path('posts/<int:post_id>/edit/', profileapp.posts_edit, name='posts_edit'),
    path('posts/<int:post_id>/comments/', profileapp.posts_comments, name='posts_comments'),
    path('posts/<int:post_id>/comments/create/', profileapp.posts_comments_create, name='posts_comments_create'),
    path('posts/<int:post_id>/comments/<int:comment_id>/like/', profileapp.posts_comments_like, name='posts_comments_like'),
    path('posts/<int:post_id>/comments/<int:comment_id>/warn/', profileapp.posts_comments_warn, name='posts_comments_warn'),
]