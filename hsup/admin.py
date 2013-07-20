from django.contrib import admin
from hsup.models import *

class FeedAdmin(admin.ModelAdmin):
    pass

admin.site.register(Feed, FeedAdmin)
