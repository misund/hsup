from django.db import models

import dateutil.parser
import feedparser
import logging

class Feed(models.Model):
    url = models.URLField(max_length=255)
    last_updated = models.DateTimeField(blank=True, null=True)
    last_pubdate = models.DateTimeField(blank=True, null=True)
    update_interval = models.IntegerField(default=3600)

    def __unicode__(self):
        return str(self.url)

# What to do when there are new entries
class Callback(models.Model):
    url = models.URLField(max_length=255)
    feed = models.ForeignKey('Feed')

    def __unicode__(self):
        return "{feed} -> {callback}".format(callback=str(self.url), feed=str(self.feed))
