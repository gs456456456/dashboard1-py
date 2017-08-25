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

from app1 import models
import datetime


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



# def modelsave(modelname):
#     models.modelname.objects.create(temperature='1111')
#     return

def test(request):
    # modelsave(temperatureFac)
    # models.waterTower.objects.create(height=0.001,ph=1,flow=2)
    sun_switch = models.configsun.objects.order_by('-now').values_list('sunmax')
    print(list(sun_switch))
    return HttpResponse('OK!')

def fan(request):
    print('1111')
    return render(request,'mainpage.html')


