from django.http import HttpResponse
from hsup.models import Feed

def push_it_baby(self, entry):
    push_to_twitter(entry);
    return entry.tostring()

def home(request):
    response = ""

    for feed in Feed.objects.all():
	try:
            response = response.join( feed.update(push_it_baby) )
	except TypeError:
	    response = response.join( TypeError.tostring() )

    response = response.join( "Oppdaterte alle feeds." )

    return HttpResponse( response )

def push_to_twitter(entry):
    pass
