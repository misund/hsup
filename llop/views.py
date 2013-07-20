from django.http import HttpResponse
from llop.models import Feed

def home(request):
    response = ""

    for feed in Feed.objects.all():
        try:
            response += str(feed.update())
        except TypeError as error:
            response += str(error)

    response += "Oppdaterte alle feeds."

    return HttpResponse( response )

