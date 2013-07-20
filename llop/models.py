from django.db import models

import dateutil.parser
import feedparser
import logging

class Feed(models.Model):
    url = models.URLField(max_length=255)
    last_updated = models.DateTimeField(blank=True, null=True)
    last_pubdate = models.DateTimeField(blank=True, null=True)
    update_interval = models.IntegerField(default=3600)

    def update(self, callback):
        logging.info("Update started.")
        old_limit = timezone.make_aware( datetime.now(), timezone.get_default_timezone() ) - timedelta( seconds = self.update_interval )
        if self.last_updated is not None and old_limit < self.last_updated:
            logging.info("Update not needed.")
            return
    
        feed = feedparser.parse(self.url)
    
        for entry in feed['entries']:
            published = dateutil.parser.parse(entry['published'])
            if self.last_pubdate is None or published > self.last_pubdate:
                logging.info('Update added new post: '+entry['guid'])
                self.last_pubdate = published
                callback(entry)
        
        self.last_updated = datetime.now()
        self.save()

# What to do when there are new entries
class Callback(models.Model):
    url = models.URLField(max_length=255)
    feed = models.ForeignKey('Feed')
