from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Pompe


def index(request):
    context = {'secteur': Pompe.get_by_code("SE"),
               'puisard': Pompe.get_by_code("PU"),
               'ph': Pompe.get_by_code("PH"),
               'pb': Pompe.get_by_code("PB"),
               'groupe': Pompe.get_by_code("GE"),
               'p12v': Pompe.get_by_code("12")
               }
    return render(request, 'polls/index.html', context)


def log(request, pompe_id):
    try:
        pompe = Pompe.objects.get(pk=pompe_id)
        context = {'pompe': pompe, 'logs': pompe.state_log()}
    except Pompe.DoesNotExist:
        raise Http404("Pompe object does not exist.")
    ## If pompe not found send 404
    return render(request, 'polls/log.html', context)
# Create your views here.
