import requests
import json
from django.shortcuts import render
from os import device_encoding
from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.regex_helper import Group, contains
import json, mysql.connector, datetime
from collections import defaultdict
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from sensor import auth
import sensor._function as func
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from sensor.api import elevator
from sensor.models import *
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.views import LoginView
from datetime import datetime
from django.db.models import Avg


# Create your views here.

class Dict(defaultdict):
    def _init_(self):
        defaultdict._init_(self, Dict)

    def _repr_(self):
        return dict._repr_(self)

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(uname=request.POST['username'],password = request.POST['password'],role = request.POST['role'])
        if user is not None:
            auth.login(request,user)
            request.session['username']=request.POST['username']
            
            return redirect('sensor/menu.html')
        else:
            return render (request,'sensor/login/login.html', {'error':'Username or password is incorrect!'})
    else:
        return render(request,'sensor/login/login.html')

def submit_login(request):
    if request.method=='POST':
        uname = request.POST['username']
        password = request.POST['password']
        print(uname)
        print(password)
        log = AuthUser(username=uname, password=password) 
        log = AuthenticationForm(data = request.POST)

        if log.is_valid():
            objUser = AuthUser.objects.get(username=uname)
            print(objUser.role.name)
            request.session['userid'] = objUser.id
            request.session['username'] = uname
            request.session['lvl'] = objUser.role.level
            print(objUser.id)
            return redirect ('menu')
        else:
            return HttpResponse ('Wrong username or password')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
    return redirect('home')

def home(request):
    if request.session._session:
        dryer=Dryer.objects.all()
        sens=Sens.objects.all()
        elevator=Elevator.objects.all()
        user=AuthUser.objects.all()
        cctv = Cctv.objects.all()

        content={
                'dryer': dryer,
                'sens': sens,
                'elevator': elevator,
                'user': user,
                'cctv' : cctv,
                'datenow' : datetime.now()
        }
        return render(request, 'sensor/track.html', content)
    else:
        return HttpResponseRedirect('/')

def menu(request):
    dryer=Dryer.objects.all()
    sens=Sens.objects.all()
    elevator=Elevator.objects.all()

    content={
            'dryer': dryer,
            'sens': sens,
            'elevator': elevator
    }
    return render(request, 'sensor/menu.html',content)

def jsonflood(request):
    site_mbusid = 'floodsensor'
    now = datetime.datetime.now()
    print("now =", now)
    dt_string = now.strftime("%Y-%m-%d")
    print("date and time =", dt_string)

    start = dt_string+' 00:0:00'
    end = dt_string+ ' 23:59:59'
    df = func.dataframeRaw(site_mbusid,start,end)
    datareal = []
    for d in df:
        print(d['floodsensor'])
        date_raw = datetime.datetime.timestamp(d['datecreated'])*1000
        date_str = round(date_raw,0)
        datareal.append([
            str(d['datecreated']).replace(' ','T')[:23]+'Z',
            d['floodsensor']
        ])
    return JsonResponse(datareal,safe=False)

def realtimedata(request):
    site_mbusid = 'floodsensor'
    now = datetime.datetime.now()
    print("now =", now)
    dt_string = now.strftime("%Y-%m-%d")
    print("date and time =", dt_string)
    start = dt_string +' 00:00:00'
    end = dt_string+' 23:59:59'
    df = func.dataframeRaw(site_mbusid,start,end)
    data = 0
    for d in df:
        data  = (921 - d['floodsensor'])
    return HttpResponse(data)

def dryer(request):
    dryer=Dryer.objects.all()
    sens=Sens.objects.all()
    elevator=Elevator.objects.all()

    content={
            'dryer': dryer,
            'sens': sens,
            'elevator': elevator
    }
    return render(request, 'sensor/dryer.html', content)

def dryerbyid(request,id):
    dryer=Dryer.objects.all().filter(dryer_id=id)
    content={
        'dryer': dryer
    }
    return render(request, 'sensor/dryer.html', content)


def sensorbyid(request,id):
    sens=Sens.objects.all().filter(dryer_id=id)
    dryer=Dryer.objects.all()
    elevator=Elevator.objects.all()
    content={
        'sens': sens,
        'dryer_id':id,
        'elevator': elevator,
        'dryer' : dryer
    }
    return render(request, 'sensor/sensor.html', content)

def sensors(request):
    dryer=Dryer.objects.all()
    sens=Sens.objects.all()
    elevator=Elevator.objects.all()

    content={
            'dryer': dryer,
            'sens': sens,
            'elevator': elevator
    }
    return render(request, 'sensor/sensor.html', content)

def ind(request, id):
    dryer=Dryer.objects.all()
    sensor = Sens.objects.all().get(sensor_id=id)
    obj = []
    obj = {
        'title' : 'Sensor Info',
        'sensor': sensor
    }
    return render(request, 'sensor/individual_sensor.html', obj)

def sensor3(request, id):
    dryer=Dryer.objects.all()
    sensor = Sens.objects.all().get(sensor_id=id)
    obj = []
    obj = {
        'title' : 'Sensor Info',
        'sensor': sensor,
        'dryer' : dryer
    }
    return render(request, 'sensor/sensor3.html', obj)

def current(request):
    station_id = 1
    dryer=Dryer.objects.all()
    sens=Sens.objects.all()
    elevator=Elevator.objects.all().filter(station_id=station_id)
    user=AuthUser.objects.all()

    content={
            'station_id': station_id,
            'dryer': dryer,
            'sens': sens,
            'elevator': elevator,
            'user': user,
            'datenow' : datetime.now()
    }
    return render(request, 'sensor/current.html', content)

def currentbyid(request,id):
    elevator=Elevator.objects.all().filter(elevator_id=id)
    dryer=Dryer.objects.all()
    sens=Sens.objects.all()
    elevator=Elevator.objects.all()
    content={

        'elevator': elevator,
        'elevator_id':id,
        'dryer' : dryer,
        'sensor' : sens
    }
    return render(request, 'sensor/current.html', content)

def cctvview(request):
    cctv = Cctv.objects.all()
    elevator=Elevator.objects.all()
    dryer=Dryer.objects.all()
    sens=Sens.objects.all()
    elevator=Elevator.objects.all()
    content={
        'cctv' : cctv,
        'elevator': elevator,
        'dryer' : dryer,
        'sensor' : sens
    }
    return render(request, 'sensor/cctv.html', content)

def cctvbyid(request,id):
    cctv = Cctv.objects.all().filter(cctv_id=id)
    elevator=Elevator.objects.all()
    dryer=Dryer.objects.all()
    sens=Sens.objects.all()
    elevator=Elevator.objects.all()
    content={
        'cctv' : cctv,
        'elevator': elevator,
        'dryer' : dryer,
        'sensor' : sens
    }
    return render(request, 'sensor/cctv.html', content)

def sampling(request):
    dryer = Dryer.objects.all()
    # sensor = Sens.objects.all()
    content = {
        'dryer' : dryer,
        # 'sensor' : sensor
    }
    return render(request, 'sensor/sampling.html', content)

def weight(request):
    dryer = Dryer.objects.all()
    content = {
        'dryer' : dryer,
    }
    return render(request, 'sensor/weight.html',content)

def history(request):
    sensor = Sens.objects.all()
    dryer = Dryer.objects.all()

    content = {
        'sensor':sensor,
        'dryer':dryer,
    }
    return render(request, 'sensor/home.html',content)

def time(request,id):
	api_url = "http://192.168.87.158:8080/api/item/"+ str(id) +"/batch"
	app_requests = requests.get(api_url)
	json_data = app_requests.json()
	data = []

	for i in range(len(json_data)):
		end = datetime.strptime(json_data[i]["end_datetime"], '%Y-%m-%d %H:%M:%S')
		start = datetime.strptime(json_data[i]["start_datetime"], '%Y-%m-%d %H:%M:%S')
		total = {'total':str(end - start)}
		data.append(total)

	print(data)
	
	content = {
		'data':data,
	}

	return render(request, 'sensor/time.html', content)