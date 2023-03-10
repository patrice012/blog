from django.contrib import admin

from .models import Post, Comment


# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug', 'is_publish', 'status')
    list_filter = ('status', 'author', 'created', 'release')
    prepopulated_fields ={'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = ('release')
    ordering = ('status', 'release')



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('username', 'email', 'body')
