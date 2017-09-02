from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import lightStatus
from .serializers import lightstatusSerlizer,factoryData,switchControl1Serilzer,switchControl3Serilzer,switchControl2Serilzer,switchControl4Serilzer
from .serializers import rotorColorCountSerlizer,elecColorCountSerlizer,elecTimeCountSerilzer,rotorTimeCountSerilzer,factoryDataSerlizer
from .models import lightStatus,rotorColorCount,elecColorCount,elecTimeCount,rotorTimeCount,configtemp,configsun,configwater
# from .models import temperatureFac,humidityFac,co2Fac,PMFac,waterpressureFac,sunFac,factoryData
# from .serializers import temperatureFacSerilzer,humidityFacSerilzer,co2FacSerilzer,waterpressureFacSerilzer,sunFacSerilzer,PMFacSerilzer
from django.http import HttpResponse
from .models import pipe,fireProSys,airMach,autoSwitch,waterTower,boiler
from .serializers import pipesSerlizer,fireProSysSerlizer,airMachSerlizer,autoSwitchSerlizer,waterTowerSerlizer,boilerSerlizer,configSunSerilzer,configWaterSerilzer,configTempSerilzer
import json
from datetime import datetime
from app1 import models
import datetime
from django.db.models import Q
import re
from django.shortcuts import redirect
import pytz
from django.http import HttpResponseRedirect
# Create your views here.




def testview(request):
    return render(request,'test1.html')


def chartview(request):
    return render(request,'chart.html')

class fireProSysViewset(ReadOnlyModelViewSet):
    queryset = fireProSys.objects.order_by('-now')
    serializer_class = fireProSysSerlizer

class pipeViewset(ReadOnlyModelViewSet):
    queryset = pipe.objects.order_by('-now')
    serializer_class = pipesSerlizer

class airMachViewset(ReadOnlyModelViewSet):
    queryset = airMach.objects.order_by('-now')
    serializer_class = airMachSerlizer

class autoSwitchViewset(ReadOnlyModelViewSet):
    queryset = autoSwitch.objects.order_by('-now')
    serializer_class = autoSwitchSerlizer

class waterTowerViewset(ReadOnlyModelViewSet):
    queryset = waterTower.objects.order_by('-now')
    serializer_class = waterTowerSerlizer

class boilerViewset(ReadOnlyModelViewSet):
    queryset = boiler.objects.order_by('-now')
    serializer_class = boilerSerlizer


class statusViewset(ReadOnlyModelViewSet):
    queryset = lightStatus.objects.all()
    serializer_class = lightstatusSerlizer

class statusFive(ReadOnlyModelViewSet):
    queryset = lightStatus.objects.order_by('-now')
    serializer_class = lightstatusSerlizer

class colorCountViewset(ReadOnlyModelViewSet):
    queryset = rotorColorCount.objects.order_by('-now')
    serializer_class = rotorColorCountSerlizer

class elecCountViewset(ReadOnlyModelViewSet):
    queryset = elecColorCount.objects.order_by('-now')
    serializer_class = elecColorCountSerlizer

class elecTimeViewset(ReadOnlyModelViewSet):
    queryset = elecTimeCount.objects.order_by('-now')
    serializer_class = elecTimeCountSerilzer

class rotorTimeViewset(ReadOnlyModelViewSet):
    queryset = rotorTimeCount.objects.order_by('-now')
    serializer_class = rotorTimeCountSerilzer

class switchControl1Viewset(ReadOnlyModelViewSet):
    queryset = models.switchcontrol1.objects.order_by('-now')
    serializer_class = switchControl1Serilzer

class switchControl2Viewset(ReadOnlyModelViewSet):
    queryset = models.switchcontrol2.objects.order_by('-now')
    serializer_class = switchControl2Serilzer

class switchControl3Viewset(ReadOnlyModelViewSet):
    queryset = models.switchcontrol3.objects.order_by('-now')
    serializer_class = switchControl3Serilzer

class switchControl4Viewset(ReadOnlyModelViewSet):
    queryset = models.switchcontrol4.objects.order_by('-now')
    serializer_class = switchControl4Serilzer
# class temperatureFacViewset(ReadOnlyModelViewSet):
#     queryset = temperatureFac.objects.order_by('-now')
#     serializer_class = temperatureFacSerilzer
#
# class humidityFacViewset(ReadOnlyModelViewSet):
#     queryset = humidityFac.objects.order_by('-now')
#     serializer_class = humidityFacSerilzer
#
# class co2FacViewset(ReadOnlyModelViewSet):
#     queryset = co2Fac.objects.order_by('-now')
#     serializer_class = co2FacSerilzer
#
#
# class PMFacViewset(ReadOnlyModelViewSet):
#     queryset = PMFac.objects.order_by('-now')
#     serializer_class = PMFacSerilzer
#
# class sunFacViewset(ReadOnlyModelViewSet):
#     queryset = sunFac.objects.order_by('-now')
#     serializer_class = sunFacSerilzer
#
# class waterpressureFacViewset(ReadOnlyModelViewSet):
#     queryset = waterpressureFac.objects.order_by('-now')
#     serializer_class = waterpressureFacSerilzer

class factoryDataViewset(ReadOnlyModelViewSet):
    queryset = factoryData.objects.order_by('-now')
    serializer_class = factoryDataSerlizer

class configTempViewset(ReadOnlyModelViewSet):
    queryset = configtemp.objects.order_by('-now')
    serializer_class = configTempSerilzer

class configWaterViewset(ReadOnlyModelViewSet):
    queryset = configwater.objects.order_by('-now')
    serializer_class = configWaterSerilzer

class configSunViewset(ReadOnlyModelViewSet):
    queryset = configsun.objects.order_by('-now')
    serializer_class = configSunSerilzer

def detail(request):
    a = models.lightStatus.objects.order_by('-now')[:200]
    num = 3
    if request.method == 'GET':
        #####line
        if request.GET.get('st') or request.GET.get('et') or request.GET.get('line') or request.GET.get('status'):
            default_line = request.GET.get('line')
            numlist = re.findall(r'\d+',default_line)
            print(default_line)
            num = int(numlist[0])
            ####status
            default_status = request.GET.get('status')
            if default_status == '运行':
                default_status = 4
            elif default_status == '故障':
                default_status = 1
            elif default_status == '检修':
                default_status = 3
            elif default_status == '待机':
                default_status = 2

            ####时间
            tz = pytz.timezone('Asia/Shanghai')
            default_st = request.GET.get('st')
            d = json.loads(default_st)
            default_et = request.GET.get('et')
            e = json.loads(default_et)
            dtstart = datetime.datetime(year = d['year'],month=d['month'],day=d['date'],hour=d['hours'],minute=d['minutes'],second=d['seconds'])
            dtend = datetime.datetime(year = e['year'],month=e['month'],day=e['date'],hour=e['hours'],minute=e['minutes'],second=e['seconds'])
            print(default_status)
            a = models.lightStatus.objects.filter(Q(now__range=(dtstart,dtend)),Q(nid=default_status),Q(status_change=num)).order_by('-now')
            return render(request,'detailpage.html',context={'a':a})
        else:
            return render(request,'detailpage.html',context={'a':a})
# def modelsave(modelname):
#     models.modelname.objects.create(temperature='1111')
#     return

def test(request):
    # modelsave(temperatureFac)
    # models.waterTower.objects.create(height=0.001,ph=1,flow=2)
    # sun_switch = models.configsun.objects.order_by('-now').values_list('sunmax')
    # print(list(sun_switch))
    a  = list(models.switchcontrol1.objects.order_by('-now').values_list('switch1'))
    for x in a:
        print('SSSSSSSSSS')
        print(x[0])
    return HttpResponse('ok')


def switchget(request):
    if request.method == 'POST':
        s1 = request.POST['s1']
        s2 = request.POST['s2']
        s3 = request.POST['s3']
        s4 = request.POST['s4']
        # models.sendtomqtt.objects.create(s1=s1,s2=s2,s3=s3,s4=s4)
        return HttpResponse('OK')
    elif request.method == 'GET':
        return HttpResponse('OK')

def changepage(request):
    print(type(request.POST['changepage']))
    if request.POST['changepage'] == '1':
        return HttpResponseRedirect('/detail/')
    # if request.method == 'GET':
    return HttpResponse('OK')

def fan(request):
    return render(request,'mainpage.html')


