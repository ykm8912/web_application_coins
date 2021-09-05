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

def handle(request, col):
    page = request.GET.get('page', 1)
    page = int(page or 1)
    pageSize = 30
    pageBarSize = 10
    keyword = request.GET.get('keyword', '')
    type = request.GET.get('type', '')
    startDateReq = request.GET.get('startDate', '')
    endDateReq= request.GET.get('endDate', '')

    if endDateReq:
        endDate = []
        endDate.append(endDateReq)
        endDate.append("23:59:59")
        endDate = ' '.join(endDate)
        
    if page <= 0:
        page = 1
    
    if col == 'pumping':
        dbm = MongoDbManager('pumping')
    elif col == 'strategy':
        dbm = MongoDbManager('vol')
    elif col == 'cross':
        dbm = MongoDbManager('cross')

    if keyword or type or (startDateReq and endDateReq):
        qr = {}
        if keyword:
            qr = {"$or" : [{"coinCode" : {"$regex" : keyword}}, {"englishName" : {"$regex" : keyword}}, {"koreaName" : {"$regex" : keyword}}]}
        if type:
            qr["$and"] = [{"type" : type}]
        if startDateReq and endDateReq:
            startDate = datetime.strptime(startDateReq, '%Y-%m-%d')
            endDate = datetime.strptime(endDate, '%Y-%m-%d %H:%M:%S')
            qr["createdTime"] = {"$gte" : startDate, "$lte" : endDate}

        resultList = list(dbm.col.find(qr).sort('createdTime', -1).skip((page - 1) * pageSize).limit(pageSize))
        totalCount = dbm.col.find(qr).count()
    else:
        resultList = list(dbm.col.find().sort('createdTime', -1).skip((page - 1) * pageSize).limit(pageSize))
        totalCount = totalCount = dbm.col.find().count()

    pageCount = math.ceil(totalCount / pageSize)
    startIndex = int(page / pageBarSize) * pageBarSize
    endIndex = startIndex + pageBarSize
    
    if endIndex >= pageCount:
        endIndex = pageCount

    return {'resultList' : resultList,
            'page' : page,
            'pageCount' : pageCount,
            'pageRange' : range(startIndex, endIndex + 1),
            'keyword' : keyword,
            'startDate' : startDateReq,
            'endDate' : endDateReq,
            'type': type}


def handleChart(request, col):
    isReverse = request.GET.get('isReverse', True)
    isReverse = bool(isReverse)
    itemCount = request.GET.get('itemCount', 5)
    itemCount = int(itemCount)
    coinCodeList = []
    coinCodeDict = {}
    startDateReq = request.GET.get('startDate', '')
    endDateReq= request.GET.get('endDate', '')

    if endDateReq:
        endDate = []
        endDate.append(endDateReq)
        endDate.append("23:59:59")
        endDate = ' '.join(endDate)

    qr = {}
    if startDateReq and endDateReq:
        startDate = datetime.strptime(startDateReq, '%Y-%m-%d')
        endDate = datetime.strptime(endDate, '%Y-%m-%d %H:%M:%S')
        qr["createdTime"] = {"$gte" : startDate, "$lte" : endDate}
    
    if col == 'pumping':
        dbm = MongoDbManager('pumping')
    elif col == 'strategy':
        dbm = MongoDbManager('vol')
    elif col == 'cross':
        dbm = MongoDbManager('cross')

    resultList = list(dbm.col.find(qr).sort('createdTime', -1))
     
    for result in resultList:
        coinCodeList.append(result['coinCode'])
    
    coinCodeSet = set(coinCodeList)
    coinCodeSetList = list(coinCodeSet)

    for coinCode in coinCodeSetList:
        count = coinCodeList.count(coinCode)
        coinCodeDict[coinCode] = count

    sortedcoinCodeTup = sorted(coinCodeDict.items(), key=operator.itemgetter(1), reverse=isReverse)[:itemCount]
    sortedcoinCodeDict = dict((x, y) for x, y in sortedcoinCodeTup)

    labels = list(sortedcoinCodeDict.keys())
    dat = list(sortedcoinCodeDict.values())

    resultDict = {}
    resultDict['labels'] = labels
    resultDict['data'] = dat
    resultDict['isReverse'] = isReverse
    resultDict['itemCount'] = itemCount
    resultDict['startDate'] = startDateReq
    resultDict['endDate'] = endDateReq
    
    return resultDict

def findWithoutCondition(col):
    if col == 'pumping':
        dbm = MongoDbManager('pumping')
    elif col == 'strategy':
        dbm = MongoDbManager('vol')
    elif col == 'cross':
        dbm = MongoDbManager('cross')

    resultList = list(dbm.col.find().sort('createdTime', -1))

    return resultList