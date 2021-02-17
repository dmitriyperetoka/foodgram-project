from django.contrib import admin

from .models import Follow


class FollowAdmin(admin.ModelAdmin):
    pass


admin.site.register(Follow, FollowAdmin)
