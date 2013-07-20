from django.http import HttpResponse
from llop.models import Feed

def push_it_baby(self, entry):
    push_to_twitter(entry);
    return str(entry)

def home(request):
    response = ""

    for feed in Feed.objects.all():
        try:
            response += str(feed.update(push_it_baby))
        except TypeError as error:
            response += str(error)

    response += "Oppdaterte alle feeds."

    return HttpResponse( response )

def push_to_twitter(entry):
    pass
