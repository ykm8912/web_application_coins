from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
def signalTime(request):
    return render(request, 'iframe/signalDay.html', {})

@xframe_options_exempt
def signalDay(request):
    return render(request, 'iframe/signalTime.html', {})