from django.contrib import admin
from llop.models import *

class FeedAdmin(admin.ModelAdmin):
    pass

admin.site.register(Feed, FeedAdmin)
