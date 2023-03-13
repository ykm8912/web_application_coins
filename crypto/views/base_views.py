from django.shortcuts import render
from db.DatabaseManager import MongoDbManager
from datetime import datetime
import math
import operator

def index(request):
    dbm = MongoDbManager('pumping')
    pumpingList = list(dbm.col.find().sort('createdTime', -1).limit(10))

    dbm = MongoDbManager('vol')
    volList = list(dbm.col.find().sort('createdTime', -1).limit(10))

    dbm = MongoDbManager('cross')
    crossList = list(dbm.col.find().sort('createdTime', -1).limit(10))

    return render(request, 'index.html', {'pumpingList' : pumpingList,
                                            'crossList' : crossList,
                                            'volList' : volList})

def handle(request=None, col=None):
    page = request.GET.get('page', 1)
    page = int(page or 1)
    pageSize = 30
    pageBarSize = 10
    keyword = request.GET.get('keyword', '')
    startDateReq = request.GET.get('startDate', '')
    endDateReq= request.GET.get('endDate', '')

    if endDateReq:
        endDate = [endDateReq, "23:59:59"]
        endDate = ' '.join(endDate)
        
    if page <= 0:
        page = 1
    
    if col == 'pumping':
        dbm = MongoDbManager('day_pumping')
        timeField = 'createdTime'
    elif col == 'strategy':
        dbm = MongoDbManager('day_vol')
        timeField = 'createdTime'
    elif col == 'day_yet_golden_cross':
        dbm = MongoDbManager('day_yet_golden_cross')
        timeField = 'goldenCrossTime'
    elif col == 'day_not_yet_golden_cross':
        dbm = MongoDbManager('day_not_yet_golden_cross')
        timeField = 'deadCrossTime'
    elif col == 'day_pumping_yet':
        dbm = MongoDbManager('day_pumping_yet')
        timeField = 'pumpingTime'
    elif col == 'day_pumping_not_yet':
        dbm = MongoDbManager('day_pumping_not_yet')
        timeField = 'lastPumpingTime'
    else:
        raise Exception('col is not valid')

    if keyword or (startDateReq and endDateReq):
        qr = dict()
        if keyword:
            qr = {"$or" : [{"coinCode" : {"$regex" : keyword}}, {"englishName" : {"$regex" : keyword}}, {"koreaName" : {"$regex" : keyword}}]}
        if startDateReq and endDateReq:
            startDate = datetime.strptime(startDateReq, '%Y-%m-%d')
            endDate = datetime.strptime(endDate, '%Y-%m-%d %H:%M:%S')
            qr[timeField] = {"$gte" : startDate, "$lte" : endDate}

        resultList = list(dbm.col.find(qr).sort(timeField, -1).skip((page - 1) * pageSize).limit(pageSize))
        totalCount = dbm.col.find(qr).count()
    else:
        resultList = list(dbm.col.find().sort(timeField, -1).skip((page - 1) * pageSize).limit(pageSize))
        totalCount = totalCount = dbm.col.find().count()

    pageCount = math.ceil(totalCount / pageSize)
    startIndex = int(page / pageBarSize) * pageBarSize
    endIndex = startIndex + pageBarSize
    
    if endIndex >= pageCount:
        endIndex = pageCount

    return {
            'resultList' : resultList,
            'page' : page,
            'pageCount' : pageCount,
            'pageRange' : range(startIndex, endIndex + 1),
            'keyword' : keyword,
            'startDate' : startDateReq,
            'endDate' : endDateReq,
            'col' : col,
            }


def handleChart(request=None, col=None):
    isReverse = request.GET.get('isReverse', True)
    isReverse = bool(isReverse)
    itemCount = request.GET.get('itemCount', 5)
    itemCount = int(itemCount)
    coinCodeList = list()
    coinCodeDict = dict()
    startDateReq = request.GET.get('startDate', '')
    endDateReq= request.GET.get('endDate', '')

    if endDateReq:
        endDate = [endDateReq, "23:59:59"]
        endDate = ' '.join(endDate)

    qr = dict()
    if startDateReq and endDateReq:
        startDate = datetime.strptime(startDateReq, '%Y-%m-%d')
        endDate = datetime.strptime(endDate, '%Y-%m-%d %H:%M:%S')
        qr["createdTime"] = {"$gte" : startDate, "$lte" : endDate}
    
    if col == 'pumping':
        dbm = MongoDbManager('day_pumping')
    elif col == 'strategy':
        dbm = MongoDbManager('day_vol')
    elif col == 'day_yet_golden_cross':
        dbm = MongoDbManager('day_yet_golden_cross')
    elif col == 'day_not_yet_golden_cross':
        dbm = MongoDbManager('day_not_yet_golden_cross')
    elif col == 'day_pumping_yet':
        dbm = MongoDbManager('day_pumping_yet')
    elif col == 'day_pumping_not_yet':
        dbm = MongoDbManager('day_pumping_not_yet')
    else:
        raise Exception('col is not valid')

    resultList = list(dbm.col.find(qr).sort('createdTime', -1))

    coinCodeList = [result['coinCode'] for result in resultList]
    
    coinCodeSet = set(coinCodeList)
    coinCodeSetList = list(coinCodeSet)

    for coinCode in coinCodeSetList:
        count = coinCodeList.count(coinCode)
        coinCodeDict[coinCode] = count

    sortedcoinCodeTup = sorted(coinCodeDict.items(), key=operator.itemgetter(1), reverse=isReverse)[:itemCount]
    sortedcoinCodeDict = dict((x, y) for x, y in sortedcoinCodeTup)

    labels = list(sortedcoinCodeDict.keys())
    dat = list(sortedcoinCodeDict.values())

    return {
            'labels' : labels,
            'data' : dat,
            'isReverse' : isReverse,
            'itemCount' : itemCount,
            'startDate' : startDateReq,
            'endDate' : endDateReq,
            'col' : col,
            }

def findWithoutCondition(col):
    if col == 'pumping':
        dbm = MongoDbManager('pumping')
    elif col == 'strategy':
        dbm = MongoDbManager('vol')
    elif col == 'cross':
        dbm = MongoDbManager('cross')

    resultList = list(dbm.col.find().sort('createdTime', -1))

    return resultList