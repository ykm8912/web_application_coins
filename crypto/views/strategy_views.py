from django.shortcuts import render
from crypto.views.base_views import handle, handleChart

def strategy(request):
    resultDict = handle(request, 'strategy')

    return render(request, 'strategy/strategy.html', {'volList' : resultDict['resultList'],
                                                'page' : resultDict['page'],
                                                "pageCount" : resultDict['pageCount'],
                                                'pageRange' : resultDict['pageRange'],
                                                'keyword' : resultDict['keyword'],
                                                'startDate' : resultDict['startDate'],
                                                'endDate' : resultDict['endDate']})

def strategyChart(request):
    resultDict = handleChart(request, 'strategy')

    return render(request, 'strategy/strategyChart.html', {'labels': resultDict['labels'],
                                                    'data': resultDict['data'],
                                                    'isReverse' : resultDict['isReverse'],
                                                    'itemCount' : resultDict['itemCount'],
                                                    'startDate' : resultDict['startDate'],
                                                    'endDate' : resultDict['endDate']})