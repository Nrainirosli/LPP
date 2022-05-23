from tkinter import S
from sensor.models import *
from bson.json_util import dumps
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from ast import literal_eval
import sensor._function as func
import json
from rest_framework import status
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
import sensor._function as func
from datetime import datetime, timedelta

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def dryer(request,id):

    now = datetime.now()
    # print("now =", now)
    dt_string = now.strftime("%Y-%m-%d")
    # print("date and time =", dt_string)

    start = '2021-01-01 00:0:00'
    end = dt_string+ ' 23:59:59'
    sensor = Sens.objects.filter(dryer_id=id)

    datareal = []
    for s in sensor:
        tablename = 'dryer_'+str(s.site_id) + '_' + str(s.dryer_id) + '_' + str(s.sensor_id)
        print(tablename)
        df = func.dataframeOneSite(tablename,start,end)
        print(df)

        if df:
            for d in df:
                print('............')
                print(d) 
                print(d['sensor_type'])
                if d['sensor_type'] == 1:
                
                    data = {
                        "ts":str(d['datecreated']),
                        "site_id": 1000,
                        "dryer_id": s.dryer_id,
                        "station_id":s.station_id,
                        "sensor_type":s.sensor_type,
                        "sensor_name":s.name,
                        "sensor_id":s.sensor_id,
                        "temperature": d['temperature'],
                        "humidity": d["humidity"]
                    }

                elif d['sensor_type'] == 2: 
                    data = {
                        "ts":str(d['datecreated']),
                        "site_id": 1000,
                        "dryer_id": s.dryer_id,
                        "station_id":s.station_id,
                        "sensor_type":s.sensor_type,
                        "sensor_name":s.name,
                        "sensor_id":s.sensor_id,
                        "distance": d["distance"],
                    }


                elif d['sensor_type'] == 3:
                
                    data = {
                        "ts":str(d['datecreated']),
                        "site_id": 1000,
                        "dryer_id": s.dryer_id,
                        "station_id":s.station_id,
                        "sensor_type":s.sensor_type,
                        "sensor_name":s.name,
                        "sensor_id":s.sensor_id,
                        "temperature": d['temperature'],
                    }

                datareal.append(data)
    
    return Response(datareal, status=HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def dryerhistory(request,id):

    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d")
    start = '2021-01-01 00:0:00'
    end = dt_string+ ' 23:59:59'
    sensor = Sens.objects.filter(dryer_id=id)

    datareal = []

    for s in sensor:
        tablename = 'dryer_'+str(s.site_id) + '_' + str(s.dryer_id) + '_' + str(s.sensor_id)
        print(tablename)
        df = func.dataframeOneSite(tablename,start,end)
        print(df)
        try: 
            sensor = Sens.objects.filter(dryer_id=id)
        except sensor.DoesNotExist: 
            return JsonResponse({'message': 'Dryer does not exist'}, status=status.HTTP_404_NOT_FOUND) 
        if df:
            for d in df:
                if d['sensor_type'] == 1:
                    data = {
                        'start':['gte', 'lte', 'exact', 'gt', 'lt'],
                        'sensor_id':['exact'],
                        'sensor_type':['exact'],
                        'start_time':['exact'],
                        'end':['exact'],
                        'end_time':['exact'],
                        'temperature':['gte', 'lte', 'exact', 'gt', 'lt'],
                        'humidity':['gte', 'lte', 'exact', 'gt', 'lt'],
                    }
                elif d['sensor_type'] == 2: 
                    data = {
                        'start':['gte', 'lte', 'exact', 'gt', 'lt'],
                        'sensor_id':['exact'],
                        'sensor_type':['exact'],
                        'start_time':['exact'],
                        'end':['exact'],
                        'end_time':['exact'],
                        'distance':['gte', 'lte', 'exact', 'gt', 'lt'],
                    }
                elif d['sensor_type'] == 3:
                    data = {
                        'start':['gte', 'lte', 'exact', 'gt', 'lt'],
                        'sensor_id':['exact'],
                        'sensor_type':['exact'],
                        'start_time':['exact'],
                        'end':['exact'],
                        'end_time':['exact'],
                        'temperature':['gte', 'lte', 'exact', 'gt', 'lt'],
                    }
            datareal.append(data)

    return Response(datareal, status=HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def elevator(request,id):

    now = datetime.now()
    print("now =", now)
    dt_string = now.strftime("%Y-%m-%d")
    print("date and time =", dt_string)

    start = '2021-01-01 00:0:00'
    end = dt_string+ ' 23:59:59'
    elevator = Elevator.objects.filter(station_id=id)

    datareal1 = []
    for e in elevator:
        df = func.dataframeOneSite('elevator_'+str(e.site_id) + '_' + str(e.elevator_id) + '_' + str(e.sensor_address),start,end)
        print(df)

        if df:
            for d in df:

                    data = {
                        "ts":str(d['datecreated']),
                        "site_id": 1000,
                        "elevator_id":e.elevator_id,    
                        "current":d["current"],
                        "station_id":e.station_id,
                        "sensor_address":e.sensor_address,
                    }

                    datareal1.append(data)
    
    return Response(datareal1, status=HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,IsAuthenticated))
def controldryer(request):
    if request.method == 'POST':
        message = 'success'
        # dryerid = request.data['dryer_id']
        name = request.data['name']
        status = request.data['status']

        d = Dryer.objects.get(name=name)
        d.flag = status
        d.save()
        func.publishMQTT(name, status)
            
        return Response({'message':'Success '+status+''})
    return Response({"message": "Error not ajax"})

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,IsAuthenticated))
def controlelevator(request):
    if request.method == 'POST':
        message = 'success'
        name = request.data['name']
        status = request.data['status']

        e = Elevator.objects.get(name=name)
        e.flag = status
        e.save()
        func.publishMQTT(name,status)

        return Response({'message':'Success '+status+''})
    return Response({"message": "Error not ajax"})

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def dryer_status(request):

    datenow = datetime.now()
    dryer = Dryer.objects.all()
    jsondr=[]
    for d in dryer:
        name = d.name
        status = ''
        if d.name == name:
            check = True       
            if check == True:
                if d.flag == 1:
                    status = 'ON'
                elif d.flag == 0:
                    status = 'OFF'
            else:
                status = 'OFFLINE'
            # print(status)
            data = {
                'Dryer':name,
                'Status':status,
            }
            jsondr.append(data)

    return Response(jsondr, status=HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def elevator_status(request):

    datenow = datetime.now()
    elevator = Elevator.objects.all()
    jsondr=[]
    for e in elevator:
        name = e.name
        status = ''
        if e.name == name:
            check = True       
            if check == True:
                if e.flag == 1:
                    status = 'ON'
                elif e.flag == 0:
                    status = 'OFF'
            else:
                status = 'OFFLINE'
            # print(status)
            data = {
                'Elevator':name,
                'Status':status,
            }
            jsondr.append(data)

    return Response(jsondr, status=HTTP_200_OK)

#API new combined
@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def api_get_value(request):

    batch_collection = 'current_value_setting' 

    new_batch_collection = func.checkDatabase(batch_collection)

    dataset = []

    for i in new_batch_collection.find():
        data = {
            'elevator': i['elevator'],
            'limit': i['limit'],
            }
        dataset.append(data)
    return Response(dataset, status=HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def api_get_status_dryer(request):

    batch_collection = 'status_dryer' 

    new_batch_collection = func.checkDatabase(batch_collection)

    dataset = []

    for i in new_batch_collection.find():
        data = {
            'dryer_id': i['dryer_id'],
            'status': i['status'],
            }
        dataset.append(data)

    return Response(dataset, status=HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def api_get_weightset(request, dryer_id, sensor_id):

    batch_collection = 'weight_set'

    new_batch_collection = func.checkDatabase(batch_collection)

    query = {"dryer_id": dryer_id, "sensor_id": sensor_id}
    mydoc = new_batch_collection.find(query)

    dataset = []

    for i in mydoc:
        data = {
            'height_order': i['height_order'],
            'weight_est': i['weight_est']
            }
        dataset.append(data)

    return Response(dataset, status=HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def api_get_timer(request, dryer_id):
    batch_collection = 'batch_dryer_' + str(dryer_id)

    new_batch_collection = func.checkDatabase(batch_collection)

    ctme = 'test'
    on = 'ON'
    off = 'OFF'
    now = datetime.now()
    # print(now)
    # formatteddate =  datetime.strptime(now[i],["i"],'%Y-%m-%d %H:%M:%S.%f')

    dataset = []

    for i in new_batch_collection.find():
        data = {
            'batch_id': i['batch_id'],
            'start_datetime': str(i['srt_datetime']),
            'end_datetime': str(i['end_datetime']),
            'total_current_time' : None if i['end_datetime'] != None else str(now - i['srt_datetime']),
            'total_finished_time' : None if i['end_datetime'] == None else str(i['end_datetime'] - i['srt_datetime']),
            'status' : on if i['end_datetime'] == None else off
        }
        # print(now - datetime.strptime(data['start_datetime'], '%Y-%m-%d %H:%M:%S'))
        # 2022-01-19 00:00:00
        dataset.append(data)

    return Response(dataset, status=HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def api_get_historical(request, dryer_id, batch_id):
    sensor = Sens.objects.filter(dryer_id=dryer_id)

    batch_time_coll_name = 'batch_dryer_' + str(dryer_id)
    batch_time_collection = func.checkDatabase(batch_time_coll_name)

    temp_batch_id = batch_time_collection.find().sort('batch_id', 1)

    try:
        start_time = temp_batch_id[batch_id-1]['srt_datetime']
        end_time = temp_batch_id[batch_id-1]['end_datetime']

        per_dataset = []

        for sens in sensor:
            batch_hist_coll_name = 'dryer_' + str(sens.site_id) + '_' + str(sens.dryer_id) + '_' + str(sens.sensor_id)
            batch_hist_collection = func.checkDatabase(batch_hist_coll_name)

            for i in batch_hist_collection.find({'datecreated':{'$gte': start_time, '$lt': end_time}}):
                # if i['sensor_type'] == 3:
                #   if 'temperature' not in i:
                #       print('as')
                #   else:
                #       print('sa')

                if i['sensor_type'] == 1:
                    data = {
                        "timestamp": str(i['datecreated']),
                        "site_id": i['payload']['site_id'],
                        "dryer_id": dryer_id,
                        "station_id": i['payload']['station_id'],
                        "sensor_id": i['sensor_id'],
                        "sensor_type": i['sensor_type'],
                        "temperature": i['temperature'],
                        "humidity": i['humidity'],
                    }

                elif i['sensor_type'] == 2:
                    sensor_name = None

                    if 'temperature' not in i:
                        sensor_name = 'distance'

                    else:
                        sensor_name = 'temperature'

                    data = {
                        "timestamp": str(i['datecreated']),
                        "site_id": i['payload']['site_id'],
                        "dryer_id": dryer_id,
                        "station_id": i['payload']['station_id'],
                        "sensor_id": i['sensor_id'],
                        "sensor_type": i['sensor_type'],
                        "distance": i[sensor_name]
                    }

                elif i['sensor_type'] == 3:
                    sensor_name = None

                    if 'temperature' not in i:
                        sensor_name = 'distance'

                    else:
                        sensor_name = 'temperature'

                    data = {
                        "timestamp": str(i['datecreated']),
                        "site_id": i['payload']['site_id'],
                        "dryer_id": dryer_id,
                        "station_id": i['payload']['station_id'],
                        "sensor_id": i['sensor_id'],
                        "sensor_type": i['sensor_type'],
                        "temperature": i[sensor_name],
                    }

                per_dataset.append(data)

        return Response(per_dataset, status=HTTP_200_OK)

    except Exception:
        return Response([])

@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def api_get_timer_per_batch(request, dryer_id, batch_id):
    batch_collection = 'batch_dryer_' + str(dryer_id)

    new_batch_collection = func.checkDatabase(batch_collection)

    dataset = []

    temp_data = new_batch_collection.find()

    data = {
        'batch_id': temp_data[batch_id-1]['batch_id'],
        'start_datetime': str(temp_data[batch_id-1]['srt_datetime']),
        'end_datetime': str(temp_data[batch_id-1]['end_datetime'])
    }

    return Response(data, status=HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def api_post_start_time(request, dryer_id):
    srt_time = datetime.strptime(request.query_params['start_time'], '%Y-%m-%d %H:%M:%S.%f')

    batch_collection = 'batch_dryer_' + str(dryer_id)
    status_collection = 'status_dryer'

    new_batch_collection = func.checkDatabase(batch_collection)

    batch_id = None

    if new_batch_collection.find_one() == None:
        batch_id = 1
 
    else:
        temp_batch_id = new_batch_collection.find().sort('batch_id', -1)
        new_batch_id = temp_batch_id[0]['batch_id']
        new_batch_id += 1
        batch_id = new_batch_id

    now = datetime.now
    batch_details = {
        'batch_id': batch_id,
        'srt_datetime': srt_time,
        'end_datetime': None,
    }

    func.insertDataframe(batch_details, batch_collection)

    on = 'ON'
    off = 'OFF'

    new_status_collection = func.checkDatabase(status_collection)

    # old_value = {'dryer_id': dryer_id}
    # newvalues = {'$set': {'status': on}}

    # db_mongo.updateOneItem(old_value, newvalues, status_collection)

    func.updateOneItem({'dryer_id': dryer_id}, {'$set': {'status': on}}, status_collection)

    return Response(dumps(batch_details), status=HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def api_post_end_time(request, dryer_id):
    end_time = datetime.strptime(request.query_params['end_time'], '%Y-%m-%d %H:%M:%S.%f')
    batch_collection = 'batch_dryer_' + str(dryer_id)
    status_collection = 'status_dryer'

    new_batch_collection = func.checkDatabase(batch_collection)

    temp_batch_id = new_batch_collection.find().sort('batch_id', -1)
    new_batch_id = temp_batch_id[0]['batch_id']
    new_srt_time = temp_batch_id[0]['srt_datetime']

    old_value = {'end_datetime': None}
    new_value = {'$set': {'end_datetime': end_time}}

    on = 'ON'
    off = 'OFF'

    batch_details = {
        'batch_id': new_batch_id,
        'srt_datetime': new_srt_time,
        'end_datetime': end_time,
    }

    func.updateOneItem(old_value, new_value, batch_collection)
    func.updateOneItem({'dryer_id': dryer_id}, {'$set': {'status': off}}, status_collection)

    return Response(dumps(batch_details), status=HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def api_post_sampling(request, dryer_id, sampledata):

    batch_collection = 'sampling_data'
    check_batch_collection = 'batch_dryer_' + str(dryer_id)

    new_batch_collection = func.checkDatabase(check_batch_collection)

    temp_batch_id = new_batch_collection.find().sort('batch_id', -1)
    new_batch_id = temp_batch_id[0]['batch_id']

    datasampling = {
        'dryer_id': dryer_id,
        'data': sampledata,
        'batch': new_batch_id,
    }

    func.insertDataframe(datasampling, batch_collection)

    return Response(dumps(datasampling), status=HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def api_get_sampling(request, dryer_id):

    batch_collection = 'sampling_data'

    new_batch_collection = func.checkDatabase(batch_collection)

    query = {"dryer_id": dryer_id}
    mydoc = new_batch_collection.find(query)

    dataset = []

    for i in mydoc:
        data = {
            'data': i['data'],
            'batch': i['batch']
            }
        dataset.append(data)

    return Response(dataset, status=HTTP_200_OK)

@csrf_exempt
@api_view(['PUT'])
@permission_classes((AllowAny,))
def api_edit_current_value(request, elevator_id, limitset):

    batch_collection = 'current_value_setting' 

    new_batch_collection = func.checkDatabase(batch_collection)

    func.updateOneItem({'elevator': elevator_id}, {'$set': {'limit': limitset}}, batch_collection)
    return Response({"message": "Success"})
    
#API new combined
