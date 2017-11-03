from django.db import models
import datetime
from django.utils import timezone
from datetime import datetime
# class light(models.Model):
#     name = models.TextField()
#     def __str__(self):
#         return self.name


class lightStatus(models.Model):
    nid = models.IntegerField()
    status_change = models.TextField()
    now = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return self.status_change

##factory data fenkai
class factoryData(models.Model):
    temperature = models.DecimalField(max_digits=4, decimal_places=1)
    humidity = models.DecimalField(max_digits=4, decimal_places=1)
    sun = models.IntegerField()
    co2= models.IntegerField()
    PM = models.DecimalField(max_digits=3, decimal_places=1)
    waterpressure = models.DecimalField(max_digits=4, decimal_places=3)
    # waterpressure = models.IntegerField()
    now = models.DateTimeField(default=datetime.now)


# class temperatureFac(models.Model):
#     temperature = models.CharField(max_length=10)
#     now = models.DateTimeField(default=timezone.now)
#     def __str__(self):
#         return self.temperature
#
# class humidityFac(models.Model):
#     humidity = models.CharField(max_length=10)
#     now = models.DateTimeField(default=timezone.now)
#
# class sunFac(models.Model):
#     sun = models.CharField(max_length=10)
#     now = models.DateTimeField(default=timezone.now)
#
# class co2Fac(models.Model):
#     co2= models.CharField(max_length=10)
#     now = models.DateTimeField(default=timezone.now)
#
# class PMFac(models.Model):
#     PM = models.CharField(max_length=10)
#     now = models.DateTimeField(default=timezone.now)
#
# class waterpressureFac(models.Model):
#     waterpressure = models.CharField(max_length=10)
#     now = models.DateTimeField(default=timezone.now)

class autoSwitch(models.Model):
    light = models.IntegerField()
    water = models.IntegerField()
    elec = models.IntegerField()
    fan = models.IntegerField()
    now = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return self.light

class elecMachline(models.Model):
    status = models.TextField()
    daily = models.IntegerField()
    total = models.IntegerField()
    disrate = models.IntegerField()
    totaltime = models.IntegerField()
    stoptime = models.IntegerField()
    alerttimes = models.IntegerField()
    repairtime = models.IntegerField()
    def __str__(self):
        return self.status


class rotorLine(models.Model):#time时间 times次数
    runtime = models.IntegerField()
    runtimes = models.IntegerField()
    wrongtime = models.IntegerField()
    wrongtimes = models.IntegerField()
    repairtime = models.IntegerField()
    repairtimes = models.IntegerField()
    waittime = models.IntegerField()
    waittimes = models.IntegerField()

class waterTower(models.Model):
     height = models.DecimalField(max_digits=4, decimal_places=3)
     # height = models.IntegerField()
     ph = models.IntegerField()
     flow = models.IntegerField()
     now = models.DateTimeField(default=datetime.now)

class airMach(models.Model):
    airpressure = models.IntegerField()
    now = models.DateTimeField(default=datetime.now)

class pipe(models.Model):
    speed = models.IntegerField()
    pressure = models.IntegerField()
    now = models.DateTimeField(default=datetime.now)

class boiler(models.Model):
    temperature = models.IntegerField()
    airpressure = models.IntegerField()
    waterpressure = models.IntegerField()
    elec = models.IntegerField()
    now = models.DateTimeField(default=datetime.now)


class fireProSys(models.Model):
    waterpressure = models.IntegerField()
    now = models.DateTimeField(default=datetime.now)

class rotorColorCount(models.Model):
    red = models.TextField()
    yellow = models.TextField()
    blue = models.TextField()
    green = models.TextField()
    now = models.DateTimeField(default=datetime.now)


class elecColorCount(models.Model):
    red = models.CharField(max_length=30)
    yellow = models.CharField(max_length=30)
    blue = models.CharField(max_length=30)
    green = models.CharField(max_length=30)
    now = models.DateTimeField(default=datetime.now)

class rotorTimeCount(models.Model):
    red = models.CharField(max_length=30)
    yellow = models.CharField(max_length=30)
    blue = models.CharField(max_length=30)
    green = models.CharField(max_length=30)
    now = models.DateTimeField(default=datetime.now)


class elecTimeCount(models.Model):
    red = models.CharField(max_length=30)
    yellow = models.CharField(max_length=30)
    blue = models.CharField(max_length=30)
    green = models.CharField(max_length=30)
    randy = models.CharField(max_length=30)
    now = models.DateTimeField(default=datetime.now)

class topicGet(models.Model):
    nid = models.CharField(max_length=10)
    ch = models.CharField(max_length=10)
    m = models.CharField(max_length=10)
    ts = models.DateTimeField()
    s = models.CharField(max_length=10)

class configtemp(models.Model):
    temperaturemax = models.DecimalField('温度上限',max_digits=4, decimal_places=1)
    temperaturemin = models.DecimalField('温度下限',max_digits=4, decimal_places=1)
    now = models.DateTimeField('设置时间',default=datetime.now)
    def __str__(self):
        return '温度设置'
    class Meta:
        verbose_name = '温度设置'

class configsun(models.Model):
    sunmax = models.IntegerField('光照上限')
    sunmin = models.IntegerField('光照下限')
    now = models.DateTimeField('设置时间',default=datetime.now)
    def __str__(self):
        return '光照设置'
    class Meta:
        verbose_name = '光照设置'

class configwater(models.Model):
    waterpressuremax = models.DecimalField('水压上限',max_digits=10, decimal_places=5)
    waterpressuremin = models.DecimalField('水压下限',max_digits=10, decimal_places=5)
    now = models.DateTimeField('设置时间',default=datetime.now)
    def __str__(self):
        return '水压设置'
    class Meta:
        verbose_name = '水压设置'

class switchcontrol1(models.Model):
    switch1 = models.IntegerField(default=2)
    now = models.DateTimeField(default=datetime.now)

class switchcontrol2(models.Model):
    switch2 = models.IntegerField(default=2)
    now = models.DateTimeField(default=datetime.now)

class switchcontrol3(models.Model):
    switch3 = models.IntegerField(default=2)
    now = models.DateTimeField(default=datetime.now)

class switchcontrol4(models.Model):
    switch4 = models.IntegerField(default=2)
    now = models.DateTimeField(default=datetime.now)

class sendtomqtt(models.Model):
    s1 = models.CharField(max_length=6)
    s2 = models.CharField(max_length=6)
    s3 = models.CharField(max_length=6)
    s4 = models.CharField(max_length=6)
    now = models.DateTimeField(default=datetime.now)
<<<<<<< HEAD
# Create your models here.
=======

class switchget(models.Model):
    pass

>>>>>>> 3d7178659a3e057061599664f7b0168540cb2ada

class runningtime(models.Model):
    time = models.CharField(max_length=30)
    now = models.DateTimeField(default=datetime.now)


###从id6读入数据
class id6_get(models.Model):
    s1 = models.CharField(max_length=6)
    s2 = models.CharField(max_length=6)
    s3 = models.CharField(max_length=6)
    s4 = models.CharField(max_length=6)
    now = models.DateTimeField(default=datetime.now)


# Create your models here.
