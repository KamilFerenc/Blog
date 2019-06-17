from django.contrib import admin

from posts.models import PostImages, Post


class PostAdmin(admin.ModelAdmin):

    list_display = ('title', 'created')
    list_filter = ('created',)
    ordering = ('created',)
    search_fields = ('title',)


class PostImageAdmin(admin.ModelAdmin):

    list_display = ('name',)


admin.site.register(Post, PostAdmin)
admin.site.register(PostImages, PostImageAdmin)
