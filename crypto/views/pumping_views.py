from django.shortcuts import render
from crypto.views.base_views import handle, handleChart

def pumping(request):
    resultDict = handle(request, 'pumping')

    return render(request, 'pumping/pumping.html', {'pumpingList' : resultDict['resultList'],
                                                'page' : resultDict['page'],
                                                'pageCount' : resultDict['pageCount'],
                                                'pageRange' : resultDict['pageRange'],
                                                'keyword' : resultDict['keyword'],
                                                'startDate' : resultDict['startDate'],
                                                'endDate' : resultDict['endDate'],
                                                'type': resultDict['type']})

def pumpingChart(request):
    resultDict = handleChart(request, 'pumping')
    
    return render(request, 'pumping/pumpingChart.html', {'labels': resultDict['labels'],
                                                    'data': resultDict['data'],
                                                    'isReverse' : resultDict['isReverse'],
                                                    'itemCount' : resultDict['itemCount'],
                                                    'startDate' : resultDict['startDate'],
                                                    'endDate' : resultDict['endDate']})