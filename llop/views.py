from datetime import datetime, timedelta
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from llop.models import Feed, Callback

import dateutil.parser
import feedparser
import logging
import urllib2

def _get_callbacks(feed):
    return Callback.objects.all().filter(feed_id=feed.id)

def _update_feed(feed):
    logging.info("Update started.")
    old_limit = timezone.make_aware( datetime.now(), timezone.get_default_timezone() ) - timedelta( seconds = feed.update_interval )
    if feed.last_updated is not None and old_limit < feed.last_updated:
        logging.info("Update not needed.")
        #return

    parsed_feed = feedparser.parse(feed.url)

    for entry in parsed_feed['entries']:
        published = dateutil.parser.parse(entry['published'])
        if feed.last_pubdate is None or published > feed.last_pubdate:
            logging.info('Update added new post: '+entry['guid'])
            feed.last_pubdate = published
            for callback in _get_callbacks(feed):
                urllib2.urlopen(callback.url, str(entry))

    feed.last_updated = datetime.now()
    feed.save()


def home(request):
    response = ""

    for feed in Feed.objects.all():
        try:
            _update_feed(feed)
        except TypeError as error:
            response += "ERROR ({}): url = {}<br/>".format(str(error), feed.url)

    response += "Oppdaterte alle feeds."

    return HttpResponse( response )

@csrf_exempt
def post(request):
    print request.POST
    return HttpResponse("Success!")
