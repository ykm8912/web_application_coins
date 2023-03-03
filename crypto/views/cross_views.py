from django.shortcuts import render
from db.DatabaseManager import MongoDbManager
from datetime import datetime
from crypto.views.base_views import handle, handleChart, findWithoutCondition
import operator

def cross(request):
    resultDict = handle(request, 'cross')
    crossList = resultDict['resultList']
    makeGcCrossRemark(crossList)
    makeDcCrossRemark(crossList)
    
    return render(request, 'cross/cross.html', {'crossList' : resultDict['resultList'],
                                            'page' : resultDict['page'],
                                            'pageCount' : resultDict['pageCount'],
                                            'pageRange' : resultDict['pageRange'],
                                            'keyword' : resultDict['keyword'],
                                            'startDate' : resultDict['startDate'],
                                            'endDate' : resultDict['endDate'],
                                            'type' : resultDict['type']})

def makeGcCrossRemark(crossList):
    # gcList = list(filter(lambda x: x['type'] == 'goldencross', crossList))
    gcList = [cross for cross in crossList if cross['type'] == 'goldencross']

    pumpingList = findWithoutCondition('pumping')

    # gcCodeList = []
    # for gc in gcList:
    #     for pumping in pumpingList:
    #         if gc['coinCode'] == pumping['coinCode'] and gc['createdTime'] <= pumping['createdTime']:
    #             gcCodeList.append(gc['crossCode'])
    gcCodeList = [gc['crossCode'] for gc in gcList for pumping in pumpingList if gc['coinCode'] == pumping['coinCode'] and gc['createdTime'] <= pumping['createdTime']]

    for gc in gcList:
        for gcCode in gcCodeList:
            if gc['crossCode'] == gcCode:
                gc['remark'] = '골든크로스 후 펌핑'
    

def makeDcCrossRemark(crossList):
    # dcList = list(filter(lambda x: x['type'] == 'deadcross', crossList))
    dcList = [cross for cross in crossList if cross['type'] == 'deadcross']

    # gcList = list(filter(lambda x: x['type'] == 'goldencross', findWithoutCondition('cross')))
    gcList = [cross for cross in findWithoutCondition('cross') if cross['type'] == 'goldencross']

    # dcCodeList = []
    # for dc in dcList:
    #     for gc in gcList:
    #         if dc['coinCode'] == gc['coinCode'] and dc['createdTime'] <= gc['createdTime']:
    #             dcCodeList.append(dc['crossCode'])
    dcCodeList = [dc['crossCode'] for dc in dcList for gc in gcList if dc['coinCode'] == gc['coinCode'] and dc['createdTime'] <= gc['createdTime']]

    for dc in dcList:
        for dcCode in dcCodeList:
            if dc['crossCode'] == dcCode:
                dc['remark'] = '데드크로스 후 골든크로스'


def crossChart(request):
    startDateReq = request.GET.get('startDate', '')
    endDateReq = request.GET.get('endDate', '')

    if endDateReq:
        # endDate = []
        # endDate.append(endDateReq)
        # endDate.append("23:59:59")
        endDate = [endDateReq, "23:59:59"]
        endDate = ' '.join(endDate)

    qr = {}
    if startDateReq and endDateReq:
        startDate = datetime.strptime(startDateReq, '%Y-%m-%d')
        endDate = datetime.strptime(endDate, '%Y-%m-%d %H:%M:%S')
        qr["createdTime"] = {"$gte" : startDate, "$lte" : endDate}

    isReverseGc = request.GET.get('isReverseGc', True)
    isReverseGc = bool(isReverseGc)
    itemCountGc = request.GET.get('itemCountGc', 5)
    itemCountGc = int(itemCountGc)
    gcLabels, gcDat = makeGcList(isReverseGc, itemCountGc, qr)

    isReverseDc = request.GET.get('isReverseDc', True)
    isReverseDc = bool(isReverseDc)
    itemCountDc = request.GET.get('itemCountDc', 5)
    itemCountDc = int(itemCountDc)
    dcLabels, dcDat = makeDcList(isReverseDc, itemCountDc, qr)

    return render(request, 'cross/crossChart.html', {'gcLabels': gcLabels,
                                                    'gcData': gcDat,
                                                    'dcLabels' : dcLabels,
                                                    'dcData' : dcDat,
                                                    'isReverseGc' : isReverseGc,
                                                    'itemCountGc' : itemCountGc,
                                                    'isReverseDc' : isReverseDc,
                                                    'itemCountDc' : itemCountDc,
                                                    'startDate' : startDateReq,
                                                    'endDate' : endDateReq})
    
def makeGcList(isReverse, itemCount, qr):
    # coinCodeList = []
    coinCodeDict = {}
    dbm = MongoDbManager('cross')
    
    # ctype = "goldencross"
    qr["type"] = "goldencross"
    gcList = list(dbm.col.find(qr).sort('createdTime', -1))
     
    # for gc in gcList:
    #     coinCodeList.append(gc['coinCode'])
    coinCodeList = [gc['coinCode'] for gc in gcList]
    
    coinCodeSet = set(coinCodeList)
    coinCodeSetList = list(coinCodeSet)

    for coinCode in coinCodeSetList:
        count = coinCodeList.count(coinCode)
        coinCodeDict[coinCode] = count

    sortedcoinCodeTup = sorted(coinCodeDict.items(), key=operator.itemgetter(1), reverse=isReverse)[:itemCount]
    sortedcoinCodeDict = dict((x, y) for x, y in sortedcoinCodeTup)

    gcLabels = list(sortedcoinCodeDict.keys())
    gcDat = list(sortedcoinCodeDict.values())
    
    return gcLabels, gcDat

def makeDcList(isReverse, itemCount, qr):
    # coinCodeList = []
    coinCodeDict = {}
    dbm = MongoDbManager('cross')

    # ctype = "deadcross"
    qr["type"] = "deadcross"
    dcList = list(dbm.col.find(qr).sort('createdTime', -1))
     
    # for dc in dcList:
    #     coinCodeList.append(dc['coinCode'])
    coinCodeList = [dc['coinCode'] for dc in dcList]

    coinCodeSet = set(coinCodeList)
    coinCodeSetList = list(coinCodeSet)

    for coinCode in coinCodeSetList:
        count = coinCodeList.count(coinCode)
        coinCodeDict[coinCode] = count

    sortedcoinCodeTup = sorted(coinCodeDict.items(), key=operator.itemgetter(1), reverse=isReverse)[:itemCount]
    sortedcoinCodeDict = dict((x, y) for x, y in sortedcoinCodeTup)

    dcLabels = list(sortedcoinCodeDict.keys())
    dcDat = list(sortedcoinCodeDict.values())
    
    return dcLabels, dcDat
