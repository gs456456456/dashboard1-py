"""untitled16 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app1 import views
from rest_framework.urlpatterns import format_suffix_patterns
from app1.models import lightStatus
from app1.models import factoryData as factorymodel
from apscheduler.schedulers.background import BackgroundScheduler
import time
from django.shortcuts import render
from django.http import HttpResponse
from app1.models import rotorColorCount as rotorcolormodel
from app1.models import elecColorCount as eleccolormodel
from app1.models import elecTimeCount as electimemodel
from app1.models import rotorTimeCount as rotortimemodel
from app1.models import configsun as sunmodel
from app1.models import configwater as watermodel
from app1.models import configtemp as tempmodel
from app1.models import switchcontrol1 as switch1model
from app1.models import switchcontrol2 as switch2model
from app1.models import switchcontrol3 as switch3model
from app1.models import switchcontrol4 as switch4model
# from app1.models import temperatureFac as temperaturemodel
# from app1.models import co2Fac as co2model
# from app1.models import PMFac as PMmodel
# from app1.models import waterpressureFac as waterpressuremodel
# from app1.models import humidityFac as humiditymodel
# from app1.models import sunFac as sunmodel
from app1.views import *


def fan(request):
    # print('1111')
    # print(red,yellow,blue,green)
    # global red
    # global yellow
    # global blue
    # global green
    return render(request,'mainpage.html')

status = statusViewset.as_view({
    'get':'list',
})

configsun = configSunViewset.as_view({
    'get':'list',
})

configwater = configWaterViewset.as_view({
    'get':'list',
})

configtemp = configTempViewset.as_view({
    'get':'list',
})

factorydata= factoryDataViewset.as_view({
    'get':'list',
})

rotorcolorcount = colorCountViewset.as_view({
    'get':'list',
})


statusfive = statusFive.as_view({
    'get':'list',
})

eleccolorcount = elecCountViewset.as_view({
    'get':'list',
})

electimecount = elecTimeViewset.as_view({
    'get':'list',
})

rotortimecount = rotorTimeViewset.as_view({
    'get':'list',
})

switchcontrol1 = switchControl1Viewset.as_view({
    'get':'list',
})

switchcontrol2 = switchControl2Viewset.as_view({
    'get':'list',
})

switchcontrol3 = switchControl3Viewset.as_view({
    'get':'list',
})

switchcontrol4 = switchControl4Viewset.as_view({
    'get':'list',
})
# temperatureFac = temperatureFacViewset.as_view({
#     'get':'list'
# })
#
# PMFac = PMFacViewset.as_view({
#     'get':'list'
# })
#
# co2Fac = co2FacViewset.as_view({
#     'get':'list'
# })
#
# waterpressureFac = waterpressureFacViewset.as_view({
#     'get':'list'
# })
#
# humidityFac = humidityFacViewset.as_view({
#     'get':'list'
# })
#
# sunFac = sunFacViewset.as_view({
#     'get':'list'
# })


boiler = boilerViewset.as_view({
    'get':'list',
})

autoSwitch = autoSwitchViewset.as_view({
    'get':'list',
})

airMach = airMachViewset.as_view({
    'get':'list',
})

pipe = pipeViewset.as_view({
    'get':'list',
})

fireProSys = fireProSysViewset.as_view({
    'get':'list',
})

waterTower = waterTowerViewset.as_view({
    'get':'list',
})

urlpatterns = format_suffix_patterns([
    url(r'^admin/', admin.site.urls),
    # url(r'^$',views.testview),
    url(r'chart/$',views.chartview),
    url(r'^status/$',status,name='status'),
    url(r'^rotorcolorcount/$',rotorcolorcount,name='rotorcolorcount'),
    url(r'^eleccolorcount/$',eleccolorcount,name='eleccolorcount'),
    url(r'^rotortimecount/$',rotortimecount,name='rotortimecount'),
    url(r'^electimecount/$',electimecount,name='electimecount'),
    url(r'^statusfive/$',statusfive,name='statusfive'),
    url(r'^factorydata/$',factorydata,name='factorydata'),
    # url(r'^temperatureFac/$',temperatureFac,name='temperatureFac'),
    # url(r'^PMFac/$',PMFac,name='PMFac'),
    # url(r'^co2Fac/$',co2Fac,name='co2Fac'),
    # url(r'^waterpressureFac/$',waterpressureFac,name='waterpressureFac'),
    # url(r'^humidityFac/$',humidityFac,name='humidityFac'),
    # url(r'^sunFac/$',sunFac,name='sunFac'),
    url(r'^boiler/$',boiler,name='boiler'),
    url(r'^autoSwitch/$',autoSwitch,name='autoSwitch'),
    url(r'^airMach/$',airMach,name='airMach'),
    url(r'^pipe/$',pipe,name='pipe'),
    url(r'^fireProSys/$',fireProSys,name='fireProSys'),
    url(r'^waterTower/$',waterTower,name='waterTower'),
    url(r'^configsun/$',configsun,name='configsun'),
    url(r'^configwater/$',configwater,name='configwater'),
    url(r'^configtemp/$',configtemp,name='configtemp'),
    url(r'^switchcontrol1/$',switchcontrol1,name='switchcontrol1'),
    url(r'^switchcontrol2/$',switchcontrol2,name='switchcontrol2'),
    url(r'^switchcontrol3/$',switchcontrol3,name='switchcontrol3'),
    url(r'^switchcontrol4/$',switchcontrol4,name='switchcontrol4'),
    url(r'^$',fan),
    url(r'test/$',test),
])

######加载定时器
def append_list(origlist,targetlist):
    for x in origlist:
        for y in x:
            targetlist.append(y)

def secchange(secs):
    if secs>=3600:
        hours = int(secs/3600)
        minutes = int((secs%3600)/60)
        seconds = secs%3600%60
        a = '{}小时{}分钟{}秒'.format(hours,minutes,seconds)
        return a
    elif 60<=secs<3600:
        minutes = int(secs/60)
        seconds = secs%60
        a = '{}分钟{}秒'.format(minutes,seconds)
        return a
    elif 0<=secs<60:
        a = '{}秒'.format(secs)
        return a
    else:
        return 'pasttimewrong'


def colorcountfx(n):###总共花的次数
    red = 0
    yellow = 0
    blue = 0
    green = 0
    randy = 0
    lightcolor = list(lightStatus.objects.filter(status_change=n).values_list('nid'))
    lightcolorlist = []
    append_list(lightcolor,lightcolorlist)
    for item in lightcolorlist:
        if item == 1:
            red += 1
            randy += 1
        elif item == 2:
            yellow += 1
        elif item == 3:
            blue +=1
        elif item == 4:
            green +=1
        else:
            print('color wrong!')
    # colormodel.objects.order_by('-now')
    if n==4:
        rotorcolormodel.objects.create(red=red,yellow=yellow,blue=blue,green=green)
    elif n==3:
        eleccolormodel.objects.create(red=red,yellow=yellow,blue=blue,green=green)
    else:
        print('line is wrong!')
    return


def timecaculate(mylist):
    timelist = []
    total_time = 0
    mytimelist = []#对应颜色所对的时间戳
    a = list(lightStatus.objects.all().values_list('now'))
    append_list(a,timelist)
    # print(timelist)
    # print(len(timelist))
    for x in mylist:
        mytimelist.append(timelist[x])
    # if len(mytimelist) == 1:
    #     total_time = 0
    # else:
    for x in range(1,len(mytimelist)):
        timecost = mytimelist[x]-mytimelist[x-1]
        total_time += timecost.seconds
    timestr = secchange(total_time)
    return timestr

def randytimecaculate(mylist):
    timelist = []
    total_time = 0
    mytimelist = []#对应颜色所对的时间戳
    a = list(lightStatus.objects.all().values_list('now'))
    append_list(a,timelist)
    # print(timelist)
    # print(len(timelist))
    for x in mylist:
        mytimelist.append(timelist[x])
    # if len(mytimelist) == 1:
    #     total_time = 0
    # else:
    for x in range(1,len(mytimelist)):
        timecost = mytimelist[x]-mytimelist[x-1]
        total_time += timecost.seconds
    return total_time

def timecountfx(n):###总共花的时间
    redtime = 0
    yellowtime = 0
    bluetime = 0
    greentime = 0
    b = list(lightStatus.objects.filter(status_change=n).values_list('nid'))
    lightcolorlist = []
    redlist = []
    yellowlist = []
    bluelist = []
    greenlist = []
    # randylist = []
    # yellowandred = []
    append_list(b,lightcolorlist)
    for num,item in enumerate(lightcolorlist):
        if item == 1:
            redlist.append(num)
            # randylist.append(num)
        elif item == 2:
            yellowlist.append(num)
            # randylist.append(num)
        elif item == 3:
            bluelist.append(num)
        elif item == 4:
            greenlist.append(num)

    # print(len(redlist))
    redtotal = timecaculate(redlist)
    # print(redtotal)
    yellowtotal = timecaculate(yellowlist)
    bluetotal = timecaculate(bluelist)
    greentotal = timecaculate(greenlist)
    randytotal_time = randytimecaculate(redlist)+randytimecaculate(yellowlist)
    randytotal = secchange(randytotal_time)

    # print(randytotal)
    if n==4:
        rotortimemodel.objects.create(red=redtotal,yellow=yellowtotal,blue=bluetotal,green=greentotal)
    elif n==3:
        electimemodel.objects.create(red=redtotal,yellow=yellowtotal,blue=bluetotal,green=greentotal,randy=randytotal)
    else:
        print('continus time wrong!')
    return

##开关设置

# def switch_get():
#     sun_list_open=[]
#     sun_list_close=[]
#     water_list_open=[]
#     elec_list_open=[]
#     fan_list_open=[]
#     fan_list_close=[]
#     sun_switch_open = models.configsun.objects.order_by('-now').values_list('sunmin')
#     if sun_switch_open:
#         sun_min = append_list(sun_switch_open,sun_list_open)[0]
#     sun_switch_close = models.configsun.objects.order_by('-now').values_list('sunmax')
#     if sun_switch_close:
#         sun_max = append_list(sun_switch_close,sun_list_close)[0]
#     fan_switch_open = models.configtemp.objects.order_by('-now').values_list('temperaturemax')
#     if fan_switch_open:
#         fan_max = append_list(fan_switch_open,fan_list_open)[0]
#     fan_switch_close = models.configsun.objects.order_by('-now').values_list('temperaturemin')
#     if fan_switch_close:
#         fan_min = append_list(fan_switch_close,fan_list_close)[0]
#     water_switch_open = models.configwater.objects.order_by('-now').values_list('waterpressuremin')
#     if water_switch_open:
#         water_min = append_list(water_switch_open,water_list_open)[0]
#     elec_switch_open = models.configsun.objects.order_by('-now').values_list('waterpressuremax')
#     if elec_switch_open:
#         elec_max= append_list(elec_switch_open,elec_list_open)[0]
#     switch_judge(sun_min,sun_max,fan_max,fan_min,water_min,elec_max)
#     return



def switch_depend_list(val):
    targetlist = []
    a = list(models.factoryData.objects.order_by('-now').values_list(val))
    append_list(a,targetlist)
    target = targetlist[0]
    return target


def switch1_get():
    sun_list_open=[]
    sun_list_close=[]
    sun_switch_open = list(models.configsun.objects.order_by('-now').values_list('sunmin'))
    sun_switch_close = list(models.configsun.objects.order_by('-now').values_list('sunmax'))
    if sun_switch_open and sun_switch_close:
        append_list(sun_switch_open,sun_list_open)
        sun_min = sun_list_open[0]
        targetsun = switch_depend_list('sun')
        if float(targetsun)<sun_min:
            models.switchcontrol1.objects.create(switch1=1)
        else:
            models.switchcontrol1.objects.create(switch1=2)


def switch2_get():
    water_list_open=[]
    water_list_close=[]
    water_switch_open = list(models.configwater.objects.order_by('-now').values_list('waterpressuremin'))
    water_switch_close = list(models.configwater.objects.order_by('-now').values_list('waterpressuremax'))
    if water_switch_open and water_switch_close:
        append_list(water_switch_open,water_list_open)
        water_min = water_list_open[0]
        targetwater = switch_depend_list('waterpressure')
        if float(targetwater)<water_min:
            models.switchcontrol2.objects.create(switch2=1)
        else:
            models.switchcontrol2.objects.create(switch2=2)

def switch3_get():
    elec_list_open=[]
    elec_list_close=[]
    elec_switch_close = list(models.configwater.objects.order_by('-now').values_list('waterpressuremin'))
    elec_switch_open = list(models.configwater.objects.order_by('-now').values_list('waterpressuremax'))
    if elec_list_open and elec_list_close:
        append_list(elec_switch_open,elec_list_open)
        elec_max = elec_list_open[0]
        targetwater = switch_depend_list('waterpressure')
        if float(targetwater)>elec_max:
            models.switchcontrol3.objects.create(switch3=1)
        else:
            models.switchcontrol3.objects.create(switch3=2)

def switch4_get():
    fan_list_open=[]
    fan_list_close=[]
    fan_switch_open = list(models.configtemp.objects.order_by('-now').values_list('temperaturemax'))
    fan_switch_close = list(models.configtemp.objects.order_by('-now').values_list('temperaturemin'))
    if fan_switch_open and fan_switch_close:
        append_list(fan_switch_open,fan_list_open)
        temp_min = fan_list_open[0]
        targetfan = switch_depend_list('temperature')
        if float(targetfan)<temp_min:
            models.switchcontrol4.objects.create(switch4=1)
        else:
            models.switchcontrol4.objects.create(switch4=2)


# def switch_judge(sun_min,sun_max,fan_max,fan_min,water_min,elec_max):
#     targetsun = switch_depend_list('sun')
#     targettemp = switch_depend_list('temperature')
#     targetwater = switch_depend_list('waterpressure')
#     if float(targetsun)<sun_min:
#         if float(targettemp)<fan_min:
#             if float(targetwater)<water_min:
#                 models.switchcontrol.objects.create(switch1=1,switch2=1,switch3=2,switch4=2)
#             elif float(targetwater)>elec_max:
#                 models.switchcontrol.objects.create(switch1=1,switch2=2,switch3=1,switch4=2)
#             else:
#                 models.switchcontrol.objects.create(switch1=1,switch2=2,switch3=2,switch4=2)
#         elif float(targettemp)>fan_max:
#             if float(targetwater)<water_min:
#                 models.switchcontrol.objects.create(switch1=1,switch2=1,switch3=2,switch4=1)
#             elif float(targetwater)>elec_max:
#                 models.switchcontrol.objects.create(switch1=1,switch2=2,switch3=1,switch4=1)
#             else:
#                 models.switchcontrol.objects.create(switch1=1,switch2=2,switch3=2,switch4=1)
#         else:
#             if float(targetwater)<water_min:
#                 models.switchcontrol.objects.create(switch1=1,switch2=1,switch3=2,switch4=2)
#             elif float(targetwater)>elec_max:
#                 models.switchcontrol.objects.create(switch1=1,switch2=2,switch3=1,switch4=2)
#             else:
#                 models.switchcontrol.objects.create(switch1=1,switch2=2,switch3=2,switch4=2)
#
#     else:
#         if float(targettemp)<fan_min:
#             if float(targetwater)<water_min:
#                 models.switchcontrol.objects.create(switch1=2,switch2=1,switch3=2,switch4=2)
#             elif float(targetwater)>elec_max:
#                 models.switchcontrol.objects.create(switch1=2,switch2=2,switch3=1,switch4=2)
#             else:
#                 models.switchcontrol.objects.create(switch1=2,switch2=2,switch3=2,switch4=2)
#         elif float(targettemp)>fan_max:
#              if float(targetwater)<water_min:
#                 models.switchcontrol.objects.create(switch1=2,switch2=1,switch3=2,switch4=1)
#              elif float(targetwater)>elec_max:
#                 models.switchcontrol.objects.create(switch1=2,switch2=2,switch3=1,switch4=1)
#              else:
#                 models.switchcontrol.objects.create(switch1=2,switch2=2,switch3=2,switch4=1)
#         else:
#             if float(targetwater)<water_min:
#                 models.switchcontrol.objects.create(switch1=2,switch2=1,switch3=2,switch4=2)
#             elif float(targetwater)>elec_max:
#                 models.switchcontrol.objects.create(switch1=2,switch2=2,switch3=1,switch4=2)
#             else:
#                 models.switchcontrol.objects.create(switch1=2,switch2=2,switch3=2,switch4=2)



def test():
    switch1_get()
    switch2_get()
    switch3_get()
    switch4_get()

def mysch():
    scheduler = BackgroundScheduler()
    scheduler.add_job(colorcountfx,args=(3,),trigger='interval', seconds=4)
    # scheduler.add_job(colorcountfx,args=(4,),trigger='interval', seconds=4)
    scheduler.add_job(timecountfx,args=(3,),trigger='interval', seconds=4)
    scheduler.add_job(switch1_get,trigger='interval', seconds=60)
    scheduler.add_job(switch2_get,trigger='interval', seconds=60)
    scheduler.add_job(switch3_get,trigger='interval', seconds=60)
    scheduler.add_job(switch4_get,trigger='interval', seconds=60)
    # scheduler.add_job(timecountfx,args=(4,),trigger='interval', seconds=4)#间隔5秒钟执行一次

    scheduler.start()    #这里的调度任务是独立的一个线程
        # print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    # try:
    #     # This is here to simulate application activity (which keeps the main thread alive).
    #     while True:
    #         time.sleep(2)    #其他任务是独立的线程执行
    #         print('sleep!')
    # except (KeyboardInterrupt, SystemExit):
    #     # Not strictly necessary if daemonic mode is enabled but should be done if possible
    #     scheduler.shutdown()
    #     print('Exit The Job!')
    return

mysch()

