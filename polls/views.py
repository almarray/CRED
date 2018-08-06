from django.shortcuts import render
from django.http import HttpResponse
from .models import Pompe


def index(request):
    pompes = Pompe.objects.all()
    context = {'pompes': pompes}
    return render(request, 'polls/index.html', context)


def log(request, pompe_id):
    return HttpResponse("This is the logs for the pompe " + pompe_id)
# Create your views here.
