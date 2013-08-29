from datetime import datetime, timedelta
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from llop.models import Feed, Callback

import dateutil.parser
import feedparser
import json
import logging
import urllib2

def _get_callbacks(feed):
    return Callback.objects.all().filter(feed_id=feed.id)

def _is_callback_duplicate(callback_url, feed_url):
    callbacks = Callback.objects.all().filter(url=callback_url)

    if len(callbacks) == 0:
        return False

    for callback in callbacks:
        old_feed_url = callback.feed.url
        if old_feed_url == feed_url:
            return True

    return False

def _update_feed(feed):
    logging.info("Update started.")
    old_limit = timezone.make_aware( datetime.now(), timezone.get_default_timezone() ) - timedelta( seconds = feed.update_interval )
    if feed.last_updated is not None and old_limit < feed.last_updated:
        logging.info("Update not needed.")
        #return # Commented out for testing purposes.

    parsed_feed = feedparser.parse(feed.url)

    if parsed_feed['status'] != 200:
        logging.warning("Feed '{url}' errored with message '{msg}'".format(url=feed.url, msg=str(parsed_feed['bozo_exception']).strip()))

    for entry in parsed_feed['entries']:
        published = dateutil.parser.parse(entry['published'])
        if feed.last_pubdate is None or published > feed.last_pubdate:
            logging.info('Update added new post: '+entry['guid'])
            feed.last_pubdate = timezone.make_aware(published, timezone.get_default_timezone())
            for callback in _get_callbacks(feed):
                urllib2.urlopen(callback.url, str(entry))

    feed.last_updated = timezone.make_aware(datetime.now(), timezone.get_default_timezone())
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

@csrf_exempt
def add_feed(request):
    if request.method.lower() != "post":
        return HttpResponse("Wrong method: " +str(request.method)) #TODO return 404
        
    try:
        data = json.loads(request.body)
        feed_url = data['feed_url']
        callback_url = data['callback_url']

        if _is_callback_duplicate(callback_url, feed_url):
            return HttpResponse("Already exists.") # TODO Return correct statuscode.

        f = Feed(url=feed_url)
        f.save()

        cb = Callback(url=callback_url, feed=f)
        cb.save()

        return HttpResponse("Added connection: {feed} -> {cb}".format(feed=feed_url, cb=callback_url))
    except (ValueError, KeyError) as err:
        return HttpResponse("No data in body or invalid JSON. Error: " +str(err)) #TODO return correct statuscode

