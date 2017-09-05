from rest_framework import serializers
from .models import lightStatus
from .models import rotorColorCount
from .models import elecColorCount,elecTimeCount,rotorTimeCount,fireProSys,airMach,autoSwitch,pipe,boiler,waterTower
from .models import factoryData
# from .models import temperatureFac,humidityFac,sunFac,co2Fac,PMFac,waterpressureFac
from .models import configwater,configsun,configtemp,switchcontrol1,switchcontrol3,switchcontrol2,switchcontrol4,runningtime


class fireProSysSerlizer(serializers.ModelSerializer):
        class Meta:
            model = fireProSys
            fields = ('waterpressure','now')

class autoSwitchSerlizer(serializers.ModelSerializer):
        class Meta:
            model = autoSwitch
            fields = ('light','water','elec','fan','now')

class airMachSerlizer(serializers.ModelSerializer):
        class Meta:
            model = airMach
            fields = ('airpressure','now')

class pipesSerlizer(serializers.ModelSerializer):
        class Meta:
            model = pipe
            fields = ('speed','pressure','now')

class boilerSerlizer(serializers.ModelSerializer):
        class Meta:
            model = boiler
            fields = ('temperature','airpressure','waterpressure','elec','now')

class waterTowerSerlizer(serializers.ModelSerializer):
        class Meta:
            model = waterTower
            fields = ('height','ph','flow','now')


class lightstatusSerlizer(serializers.ModelSerializer):
        class Meta:
            model = lightStatus
            fields = ('nid','status_change','now')

class factoryDataSerlizer(serializers.ModelSerializer):
        class Meta:
            model = factoryData
            fields = ('temperature','humidity','sun','co2','PM','waterpressure','now')

class rotorColorCountSerlizer(serializers.ModelSerializer):
        class Meta:
            model = rotorColorCount
            fields = ('red','yellow','blue','green','now')

class elecColorCountSerlizer(serializers.ModelSerializer):
        class Meta:
            model = elecColorCount
            fields = ('red','yellow','blue','green','now')

class rotorTimeCountSerilzer(serializers.ModelSerializer):
        class Meta:
            model = rotorTimeCount
            fields = ('red','yellow','blue','green')

class elecTimeCountSerilzer(serializers.ModelSerializer):
        class Meta:
            model = elecTimeCount
            fields = ('red','yellow','blue','green','randy')

class configSunSerilzer(serializers.ModelSerializer):
        class Meta:
            model = configsun
            fields = ('sunmax','sunmin','now')

class configWaterSerilzer(serializers.ModelSerializer):
        class Meta:
            model = configwater
            fields = ('waterpressuremax','waterpressuremin','now')

class configTempSerilzer(serializers.ModelSerializer):
        class Meta:
            model = configtemp
            fields = ('temperaturemax','temperaturemin','now')


class switchControl1Serilzer(serializers.ModelSerializer):
        class Meta:
            model = switchcontrol1
            fields = ('switch1','now')

class switchControl2Serilzer(serializers.ModelSerializer):
        class Meta:
            model = switchcontrol2
            fields = ('switch2','now')

class switchControl3Serilzer(serializers.ModelSerializer):
        class Meta:
            model = switchcontrol3
            fields = ('switch3','now')

class switchControl4Serilzer(serializers.ModelSerializer):
        class Meta:
            model = switchcontrol4
            fields = ('switch4','now')

class runningtimeSerilzer(serializers.ModelSerializer):
        class Meta:
            model = runningtime
            fields =('time','now')
# class temperatureFacSerilzer(serializers.ModelSerializer):
#        class Meta:
#             model = temperatureFac
#             fields = ('temperature','now')
#
# class humidityFacSerilzer(serializers.ModelSerializer):
#        class Meta:
#             model = humidityFac
#             fields = ('humidity','now')
#
# class sunFacSerilzer(serializers.ModelSerializer):
#        class Meta:
#             model = sunFac
#             fields = ('sun','now')
#
# class co2FacSerilzer(serializers.ModelSerializer):
#        class Meta:
#             model = co2Fac
#             fields = ('co2','now')
#
# class PMFacSerilzer(serializers.ModelSerializer):
#        class Meta:
#             model = PMFac
#             fields = ('PM','now')
#
# class waterpressureFacSerilzer(serializers.ModelSerializer):
#        class Meta:
#             model = waterpressureFac
#             fields = ('waterpressure','now')