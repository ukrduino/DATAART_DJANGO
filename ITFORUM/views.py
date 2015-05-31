from django.shortcuts import render_to_response

# Create your views here.
from django.template import RequestContext


def start_page(request):
    return render_to_response("StartPage.html", context_instance=RequestContext(request))
