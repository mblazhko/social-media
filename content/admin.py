from django.contrib import admin

from content.models import Post, Tag, PostImage

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(PostImage)
