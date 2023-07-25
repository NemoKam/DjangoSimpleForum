from django.contrib import admin
from profileapp.models import ProfileUser, Post, Comment

from .filters import IDFilter, UsernameFilter

class ProfileUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'get_friends_cnt', 'last_login', 'is_active']
    ordering = ['id']
    list_display_links = ['username']
    list_filter = [IDFilter, UsernameFilter, 'is_active']

    def get_friends_cnt(self, obj):
        return obj.friends.count()
    
    get_friends_cnt.short_description = 'FRIENDS'
    get_friends_cnt.admin_order_field = 'friends'

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'get_likes_cnt', 'get_comments_cnt', 'get_warned_cnt', 'created_at']
    ordering = ['id']
    list_display_links = ['author']
    list_filter = [IDFilter, UsernameFilter]

    def get_likes_cnt(self, obj):
        return obj.likes.count()
    
    def get_comments_cnt(self, obj):
        return obj.comments.count()
    
    def get_warned_cnt(self, obj):
        return obj.warned.count()

    get_likes_cnt.short_description = 'LIKES'
    get_likes_cnt.admin_order_field = 'likes'
    get_comments_cnt.short_description = 'COMMENTS'
    get_comments_cnt.admin_order_field = 'comments'
    get_warned_cnt.short_description = 'WARNED'
    get_warned_cnt.admin_order_field = 'warned'

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'get_likes_cnt', 'get_warned_cnt', 'created_at']
    ordering = ['id']
    list_display_links = ['author']
    list_filter = [IDFilter, UsernameFilter]

    def get_likes_cnt(self, obj):
        return obj.likes.count()
    
    def get_warned_cnt(self, obj):
        return obj.warned.count()

    get_likes_cnt.short_description = 'LIKES'
    get_likes_cnt.admin_order_field = 'likes'
    get_warned_cnt.short_description = 'WARNED'
    get_warned_cnt.admin_order_field = 'warned'


admin.site.register(ProfileUser, ProfileUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)