from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Pompe


def index(request):
    pompes = Pompe.objects.all()
    context = {'pompes': pompes}
    return render(request, 'polls/index.html', context)


def log(request, pompe_id):
    try:
        pompe = Pompe.objects.get(pk=pompe_id)
        context = {'pompe': pompe, 'logs': pompe.status_log()}
    except Pompe.DoesNotExist:
        raise Http404("Pompe object does not exist.")
    ## If pompe not found send 404
    return render(request, 'polls/log.html', context)
# Create your views here.
