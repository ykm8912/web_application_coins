from django.shortcuts import render
from db.DatabaseManager import MongoDbManager
from datetime import datetime
from crypto.views.base_views import handle, handleChart
import operator

def cross(request):
    resultDict = handle(request=request, col=request.GET.get('col', 'day_yet_golden_cross'))
    
    return render(request, 'cross/cross.html', {'crossList' : resultDict['resultList'],
                                            'page' : resultDict['page'],
                                            'pageCount' : resultDict['pageCount'],
                                            'pageRange' : resultDict['pageRange'],
                                            'keyword' : resultDict['keyword'],
                                            'startDate' : resultDict['startDate'],
                                            'endDate' : resultDict['endDate'],
                                            'col' : resultDict['col'],
                                            })


def crossChart(request):
    resultDict = handleChart(request=request, col=request.GET.get('col', 'day_yet_golden_cross'))
    
    return render(request, 'cross/crossChart.html', {'labels': resultDict['labels'],
                                                    'data': resultDict['data'],
                                                    'isReverse' : resultDict['isReverse'],
                                                    'itemCount' : resultDict['itemCount'],
                                                    'startDate' : resultDict['startDate'],
                                                    'endDate' : resultDict['endDate'],
                                                    'col' : resultDict['col']})