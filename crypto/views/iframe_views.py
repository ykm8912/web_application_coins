from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from common.config import SUPERSET_URL

@xframe_options_exempt
def signalTime(request):
    return render(request, 'iframe/signalTime.html', {"SUPERSET_URL": SUPERSET_URL})

@xframe_options_exempt
def signalDay(request):
    return render(request, 'iframe/signalDay.html', {"SUPERSET_URL": SUPERSET_URL})