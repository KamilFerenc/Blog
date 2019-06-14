from django.contrib import admin

from posts.models import Post


class PostAdmin(admin.ModelAdmin):

    list_display = ('title', 'created')
    list_filter = ('created',)
    ordering = ('created',)
    search_fields = ('title',)


admin.site.register(Post, PostAdmin)
