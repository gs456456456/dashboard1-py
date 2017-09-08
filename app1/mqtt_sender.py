#!/usr/bin/env python
# -*- encoding=utf-8 -*-

########################################
# Copyright (c) 2017 Shanghai Kimstars #
########################################

import os,sys
sys.path.append('../../zigbee-dashboard/')
os.environ.setdefault('DJANGO_SETTINGS_MODULE','untitled16.settings') #设置环境变量
import django
django.setup() #导入数据

import time
import threading
import json
import random
import arrow
import queue
import paho.mqtt.client as mqtt
from paho.mqtt.client import connack_string
from app1.models import lightStatus
from app1 import models
from django.utils import timezone
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django.http import HttpResponse

MQTT_SERVER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60
MQTT_TOPIC_PREFIX = "/SwitchStatus"
# MQTT_TOPIC_PREFIX2 = "/iotgateway"
# MQTT_SEND_INTERVAL = 3
myqueue = queue.Queue()##### switchcontrol 数据库通信
# s1 = ''
# s2 = ''
# s3 = ''
# s4 = ''
# s5 = {}
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

class DeviceAgent(threading.Thread):
    """
    @brief      a Mqtt Client as connection manager interface
                connect to local broker
    """

    def __init__(self,q):
        super(DeviceAgent, self).__init__()
        self._stop = threading.Event()
        self._stop.clear()
        self.mqttc = None
        self.mqttp = None
        self.modbusc = None
        self.modbusp = None
        self.mqttConnected = False
        self.factorycache = {}
        self.targetlist1 = []
        self.targetlist2 = []
        self.targetlist3 = []
        self.targetlist4 = []
        self.targetlist5 = []
        self.targetlist6 = []
        self.threading = []
        self.q = q
        self.a_list = 0
        self.b_list = 0
        self.c_list = 0
        self.d_list = 0
        self.copya = 0
        self.copyb = 0
        self.copyc = 0
        self.copyd = 0
        self.redislist1 = {}
        self.redislist2 = {}
        self.redislist3 = {}
        self.redislist4 = {}
        self.copy1 = {}
        self.copy2 = {}
        self.copy3 = {}
        self.copy4 = {}


    def init_mqtt_client(self):
        self.mqttp = {}
        self.mqttp['host'] = MQTT_SERVER
        self.mqttp['port'] = MQTT_PORT
        self.mqttp['topicPrefix'] = MQTT_TOPIC_PREFIX
        self.mqttp['keepalive'] = MQTT_KEEPALIVE

        # init mqtt client
        self.mqttc = mqtt.Client(clean_session=True,
                                 protocol=mqtt.MQTTv311)
        self.mqttc.on_connect = self.r_on_connect
        self.mqttc.on_disconnect = self.r_on_disconnect
        self.mqttc.on_message = self.r_on_message
        self.mqttc.on_publish = self.r_on_publish

        # connect to Server
        try:
            self.mqttc.connect(self.mqttp['host'],
                               self.mqttp['port'],
                               self.mqttp['keepalive'])
        except Exception as e:
            print(e)
        # start another thread to run client.loop_forever()
        # self.mqttc.loop_start()
        # logger.warning('loop_start remote_mqtt_client')
        return True


    def run(self):
        # remote mqtt parameters
        if not self.init_mqtt_client():
            self.stop()
        # self.loop_forever_local_mqtt_client()
        while not self._stop.is_set():
            # read from modbus tcp server
            # if self.mqttConnected:
            #     self.sender_simulation()
            #     time.sleep(MQTT_SEND_INTERVAL)
            self.mqttc.loop_forever()
            # print(self.q)
            # self.random_interval()

            # self.switch_send()
            # if self.copy1 != self.redislist1:
            #     # print(1)
            #     jsonObject1 = self.redislist1
            #     topic = '/SwitchStatus'
            #     self.r_send(topic, jsonObject1)
            # self.copy1 = self.redislist1
            # self.redislist1 = {}
            #     # print(self.redislist1)


            # if self.copy2 != self.redislist2:
            #     jsonObject2 = self.redislist2
            #     topic = '/SwitchStatus'
            #     self.r_send(topic, jsonObject2)
            # self.copy2 = self.redislist2
            # self.redislist2 = {}
            #     # print(self.redislist2)


            # if self.copy3 != self.redislist3:
            #     jsonObject3 = self.redislist3
            #     topic = '/SwitchStatus'
            #     self.r_send(topic, jsonObject3)
            # self.copy3 = self.redislist3
            # self.redislist3 = {}
            #     # print(self.redislist3)


            # if self.copy4 != self.redislist4:
            #     jsonObject4 = self.redislist4
            #     topic = '/SwitchStatus'
            #     self.r_send(topic, jsonObject4)
            # self.copy4 = self.redislist4
            # self.redislist4 = {}
            #     # print(self.redislist4)
            # time.sleep(MQTT_SEND_INTERVAL)



    def stop(self):
        self._stop.set()
        if self.mqttc is not None:
            self.mqttc.disconnect()
            self.mqttc.loop_stop()

    ###### 存入数据库 #######
    def lightstatus_create(self,data):
        models.lightStatus.objects.create(nid=data['m'],status_change=data['s'],now=data['ts'])

    # def deviceswitch_create(self,data):
    #     models.autoSwitch.objects.create(light=data['sw1'],water=data['sw2'],elec=data['sw3'],fan=data['sw4'])

    def watertower_create(self,data):
        models.waterTower.objects.create(height=data['wthe'],ph=data['wtph'],flow=data['wtfl'])

    def air_create(self,data):
        models.airMach.objects.create(airpressure=data['airp'])

    def pipe_create(self,data):
        models.pipe.objects.create(speed=data['winds'],pressure=data['windp'])

    def boiler_create(self,data):
        models.boiler.objects.create(temperature=data['boilt'],airpressure=data['boilp'],waterpressure=data['boilwp'],elec=data['boile'])

    def firepro_create(self,data):
        models.fireProSys.objects.create(waterpressure=data['pipewp'])

    # def factory_create(self,factorycache):
    #     models.factoryData.objects.create(temperature=data['temp'],humidity=data['humi'],sun=data['sun'],co2=data['co2'],PM=data['pm'],waterpressure=data['waterpressure'])

    #


    def r_send(self, topic, data):
        if self.mqttc is None:
            return
        msg = json.dumps(data)
        # mqttMessageInfo = self.mqttc.publish(topic, msg, qos=2)
        self.mqttc.publish(topic, msg, qos=2)
        print("send: " + topic + " " + str(data) + "\n")



        # Thread=[]
    #     t1 = threading.Thread(target=self.lightstatus_create,args=(data,))
    #     Thread.append(t1)
    #     t2 = threading.Thread(target=self.deviceswitch_create,args=(data,))
    #     Thread.append(t2)
    #     t3 = threading.Thread(target=self.watertower_create,args=(data,))
    #     Thread.append(t3)
    #     t4 = threading.Thread(target=self.air_create,args=(data,))
    #     Thread.append(t4)
    #     t5 = threading.Thread(target=self.pipe_create,args=(data,))
    #     Thread.append(t5)
    #     t6 = threading.Thread(target=self.boiler_create,args=(data,))
    #     Thread.append(t6)
    #     t7 = threading.Thread(target=self.firepro_create,args=(data,))
    #     Thread.append(t7)
    #     for t in Thread:
    #         t.setDaemon(True)
    #         t.start()
    #



    ####接收mqtt数据并存入数据库
    def append_list(self,origlist,targetlist):
        for x in origlist:
            for y in x:
                targetlist.append(y)

    def cache(self,get_list,property_name,tar_length):
        if tar_length == 0 or tar_length <0:
            return
        factory_now = {property_name:get_list[tar_length-1]}
        self.factorycache.update(factory_now)
        # print(self.factorycache)
        if len(self.factorycache)<6:
            pass
        elif len(self.factorycache)==6:
            models.factoryData.objects.create(temperature=self.factorycache['temp'],humidity=self.factorycache['humi'],sun=self.factorycache['sun'],co2=self.factorycache['co2'],PM=self.factorycache['pm'],waterpressure=self.factorycache['waterpressure'])
            # models.factoryData.objects.create(temperature=0,humidity=0,sun=0,co2=self.factorycache['co2'],PM=self.factorycache['pm'],waterpressure=self.factorycache['waterpressure'])
            self.factorycache.clear()
        else:
            print('工厂数据错误!')


    def temp_mysql_save(self,jsonObject):
        # targetlist = []
        # self.append_list(jsonObject['m'],self.targetlist1)
        self.targetlist1.append(jsonObject['m'])
        self.cache(self.targetlist1,'temp',len(self.targetlist1))
        self.targetlist1 = []

    def humi_mysql_save(self,jsonObject):
        # targetlist = []
        # self.append_list(jsonObject['m'],self.targetlist2)
        self.targetlist2.append(jsonObject['m'])
        self.cache(self.targetlist2,'humi',len(self.targetlist2))
        self.targetlist2 = []

    def sun_mysql_save(self,jsonObject):
        # targetlist = []
        # sun = list(models.topicGet.objects.filter(nid='2',ch='3').values_list('m'))
        # self.append_list(jsonObject['m'],self.targetlist3)
        self.targetlist3.append(jsonObject['m'])
        self.cache(self.targetlist3,'sun',len(self.targetlist3))
        self.targetlist3 = []

    def pm_mysql_save(self,jsonObject):
        # targetlist = []
        # self.append_list(jsonObject['m'],self.targetlist4)
        self.targetlist4.append(jsonObject['m'])
        self.cache(self.targetlist4,'pm',len(self.targetlist4))
        self.targetlist4 = []

    def co2_mysql_save(self,jsonObject):
        # targetlist = []
        # self.append_list(jsonObject['m'],self.targetlist5)
        self.targetlist5.append(jsonObject['m'])
        self.cache(self.targetlist5,'co2',len(self.targetlist5))
        self.targetlist5 = []

    def pres_mysql_save(self, jsonObject):
        # targetlist = []
        # pres = list(models.topicGet.objects.filter(nid='1',ch='1').values_list('m'))
        # self.append_list(jsonObject['m'],self.targetlist6)
        self.targetlist6.append(jsonObject['m'])
        self.cache(self.targetlist6,'waterpressure',len(self.targetlist6))
        self.targetlist6 = []


    def lightmysql_save1(self,jsonObject):
        targetlist = []
        # g = list(models.topicGet.objects.filter(nid='5',ch='3').values_list('m'))
        g = jsonObject['m']
        # self.append_list(g,targetlist)
        targetlist.append(g)
        resultlist = []
        for x in targetlist:
            if str(x)=='True' or float(x)>=0.1:
                resultlist.append(3)
            # else:
            #     resultlist.append(4)
        for x in resultlist:
            models.lightStatus.objects.create(nid=x,status_change=3)

    def lightmysql_save2(self,jsonObject):
        targetlist = []
        # h = list(models.topicGet.objects.filter(nid='5',ch='1').values_list('m'))
        h = jsonObject['m']
        # self.append_list(h,targetlist)
        targetlist.append(h)
        resultlist = []
        for x in targetlist:
            # if str(x)=='True':
            if str(x)=='True' or float(x)>=0.1:
                # print(11111111)
                resultlist.append(4)
            else:
                pass
        # print(resultlist)
        for x in resultlist:
            models.lightStatus.objects.create(nid=x,status_change=3)

    def lightmysql_save3(self,jsonObject):
        targetlist = []
        # h = list(models.topicGet.objects.filter(nid='5',ch='2').values_list('m'))
        h = jsonObject['m']
        # self.append_list(h,targetlist)
        targetlist.append(h)
        resultlist = []
        for x in targetlist:
            if str(x)=='True' or float(x)>=0.1:
                resultlist.append(2)
            else:
                pass
        # print(resultlist)
        for x in resultlist:
            models.lightStatus.objects.create(nid=x,status_change=3)

    def lightmysql_save4(self,jsonObject):
        targetlist = []
        # h = list(models.topicGet.objects.filter(nid='5',ch='2').values_list('m'))
        h = jsonObject['m']
        # self.append_list(h,targetlist)
        targetlist.append(h)
        resultlist = []
        for x in targetlist:
            if str(x)=='True' or float(x)>=0.1:
                resultlist.append(1)
            else:
                pass
        # print(resultlist)
        for x in resultlist:
            models.lightStatus.objects.create(nid=x,status_change=3)


    def light2mysql_save1(self,jsonObject):
        # num = jsonObject['values'][0]['id']
        status = jsonObject['v']
        # if str(status) == 'True':
        #     status = 1
        # elif str(status) == 'False':
        #     status = 2
        # else:
        #     pass
        if status:
            models.lightStatus.objects.create(nid = 1,status_change=10)

    def light2mysql_save2(self,jsonObject):
        # num = jsonObject['values'][0]['id']
        status = jsonObject['v']
        # if str(status) == 'True':
        #     status = 1
        # elif str(status) == 'False':
        #     status = 2
        # else:
        #     pass
        if status:
            models.lightStatus.objects.create(nid = 2,status_change=10)


    def light2mysql_save3(self,jsonObject):
        # num = jsonObject['values'][0]['id']
        status = jsonObject['v']
        # if str(status) == 'True':
        #     status = 1
        # elif str(status) == 'False':
        #     status = 2
        # else:
        #     pass
        if status:
            models.lightStatus.objects.create(nid = 4,status_change=10)

    def light2mysql_save4(self,jsonObject):
        # num = jsonObject['values'][0]['id']
        status = jsonObject['v']
        # if str(status) == 'True':
        #     status = 1
        # elif str(status) == 'False':
        #     status = 2
        # else:
        #     pass
        if status:
            models.lightStatus.objects.create(nid = 3,status_change=10)

    def switch1_save(self,jsonObject):
        s1 = jsonObject['v']
        if s1:
            models.switchcontrol1.objects.create(switch1=1)
        else:
            models.switchcontrol1.objects.create(switch1=2)

    def switch2_save(self,jsonObject):
        s2 = jsonObject['v']
        if s2:
            models.switchcontrol2.objects.create(switch2=1)
        else:
            models.switchcontrol2.objects.create(switch2=2)

    def switch3_save(self,jsonObject):
        s3 = jsonObject['v']
        if s3:
            models.switchcontrol3.objects.create(switch3=1)
        else:
            models.switchcontrol3.objects.create(switch3=2)

    def switch4_save(self,jsonObject):
        s4 = jsonObject['v']
        if s4:
            models.switchcontrol4.objects.create(switch4=1)
        else:
            models.switchcontrol4.objects.create(switch4=2)

    def running_save(self,jsonObject):
        # time = jsonObject['values'][0]['v']
        time = jsonObject['v']
        # mytime = arrow.get(time)
        chartime = secchange(time)
        print(chartime)
        models.runningtime.objects.create(time=chartime)

    # The callback for when the client receives a CONNACK response from the
    # server.
    # def r_on_connect(self, client, userdata, flags, rc):
    #     host = self.mqttp['host']
    #     port = self.mqttp['port']
    #     msg = "connected to %s:%s with flags = %s and result_code = %d. %s" % (
    #         host, port, flags['session present'], rc, connack_string(rc))
    #     print(msg)
    #     self.mqttConnected = True

    def r_on_connect(self, client, userdata, flags, rc):
        host = self.mqttp['host']
        port = self.mqttp['port']
        msg = "connected to %s:%s with flags = %s and result_code = %d. %s" % (
        host, port, flags['session present'], rc, connack_string(rc))
        print(msg)
        self.mqttConnected = True
        topic = "/zigbee/#"
        topic2 = "/iotgateway"
        # self.mqttc.subscribe(topic)
        self.mqttc.subscribe([(topic, 0), (topic2, 2)])



    # called when the client disconnects from the broker
    def r_on_disconnect(self, client, userdata, rc):
        msg = "disconnected with result code %d. %s" % (
            rc, connack_string(rc))
        print(msg)
        self.mqttConnected = False



    # The callback for when a message that was to be sent using the
    # publish() call has completed transmission to the broker.
    def r_on_publish(self, client, userdata, mid):
        pass

    # The callback for when a PUBLISH message is received from the server.
    def r_on_message(self, client, userdata, msg):
        print("received: " + msg.topic + " " + str(msg.payload))
        # print("received: " + msg.topic2 + " " + str(msg.payload))
        # topicid = msg.topic[-5]
        # topicch = msg.topic[-1]
        try:
            jsonObject = json.loads(msg.payload.decode('utf-8'))
            t = msg.topic
            if "id1/ch1" in t:
                self.pres_mysql_save(jsonObject)
            elif "id2/ch1" in t:
                self.temp_mysql_save(jsonObject)
            elif "id2/ch2" in t:
                self.humi_mysql_save(jsonObject)
            elif "id2/ch3" in t:
                self.sun_mysql_save(jsonObject)
            elif "id3/ch1" in t:
                self.pm_mysql_save(jsonObject)
            elif "id4/ch1" in t:
                self.co2_mysql_save(jsonObject)
            elif "id5/ch3" in t:
                self.lightmysql_save3(jsonObject)
            elif "id5/ch1" in t:
                self.lightmysql_save1(jsonObject)
            elif "id5/ch2" in t:
                self.lightmysql_save2(jsonObject)
            elif "id5/ch4" in t:
                self.lightmysql_save4(jsonObject)
            elif "id6/ch1" in t:
                self.switch1_save(jsonObject)
            elif "id6/ch2" in t:
                self.switch2_save(jsonObject)
            elif "id6/ch3" in t:
                self.switch3_save(jsonObject)
            elif "id6/ch4" in t:
                self.switch4_save(jsonObject)
            elif "iotgateway" in t:
                for value in jsonObject['values']:
                    if not value['q']:
                        continue
                    if "x1" in value['id']:
                        self.light2mysql_save1(value)
                    elif "x2" in value['id']:
                        self.light2mysql_save2(value)
                    elif "x3" in value['id']:
                        self.light2mysql_save3(value)
                    elif "x4" in value['id']:
                        self.light2mysql_save4(value)
                    elif "plc_on_time" in value['id']:
                        self.running_save(value)
                    else:
                        pass
            else:
                pass

        except Exception as e:
            errStr = "JSON loads Exception from msg.payload: " + str(e)
            print(errStr)

            return
        # m = jsonObject['m']
        # ts = jsonObject['ts']
        # s = jsonObject['s']
        # models.topicGet.objects.create(nid=topicid,ch=topicch,m=m,ts=ts,s=s)
        # # print(jsonObject)
        # self.co2_mysql_save()



    def random_save(self,data):
        # self.deviceswitch_create(data)
        self.watertower_create(data)
        self.air_create(data)
        self.boiler_create(data)
        self.firepro_create(data)
        self.pipe_create(data)


    def sender_simulation(self):
        payload = {}
        tagName = 'SwitchStatus'
        topic = MQTT_TOPIC_PREFIX + "/"
        # status = payload['s'] = 4
        # payload['q'] = 192
        utc = arrow.utcnow()
        time = payload['ts'] = utc.format('YYYY-MM-DDTHH:mm:ss.SSSSSS') + "Z"#时间戳
        # s1 = models.switchcontrol1.objects.order_by('-now').values_list('switch1')
        # self.random_save(payload)
         # co2 = payload['co2'] = random.randint(300,1000)
        # temp = payload['temp'] =random.randint(20,33)
        # humidity = payload['humi']=random.randint(0,100)
        # sunshine = payload['sun']=random.randint(1000,2000)
        # PM = payload['pm']=random.randint(0,50)
        # # waterpressure = payload['waterpressure']=random.randint(0,10)
        # waterpressure = payload['waterpressure']=random.choice([0.002,0.001,-0.003])
        # switch1 = payload['sw1']=random.randint(1,2)
        # switch2 = payload['sw2']=random.randint(1,2)
        # switch3 = payload['sw3']=random.randint(1,2)
        # switch4 = payload['sw4']=random.randint(1,2)
        watertowerph = payload['wtph']=random.choice([3,6,9])
        # watertowerheight = payload['wthe']=random.randint(0,10)
        watertowerheight = payload['wthe']=random.choice([0.002,0.001,-0.003])
        watertowerflow= payload['wtfl']=random.choice([4,6,9])
        airpressure = payload['airp'] = random.randint(1000,2000)
        windspeed = payload['winds']=random.randint(10,20)
        windpressure = payload['windp']=random.randint(20,30)
        boilerpressure = payload['boilp']=random.randint(20,30)
        boilertemp = payload['boilt']=random.randint(20,30)
        boilerwaterpressure = payload['boilwp']=random.randint(1000,2000)
        boilerelec = payload['boile']=random.randint(30,40)
        pipewaterpressure = payload['pipewp']=random.randint(300,500)
        self.random_save(payload)

    def switch_append_list(self,origlist,targetlist):
        for x in origlist:
            targetlist.append(x)


    def append_last_list(self,origlist,targetlist):
        print(origlist[0][0])
        for x in origlist:
            print(x[0])
            targetlist.append(x[0])
            # for y in x:
            #     print(y)
            # for y in x[0]:
            #     targetlist=y
        # print(origlist[0])

    def switch_send(self):
        a  = list(models.switchcontrol1.objects.order_by('-now').values_list('switch1'))
        b = list(models.switchcontrol2.objects.order_by('-now').values_list('switch2'))
        c = list(models.switchcontrol3.objects.order_by('-now').values_list('switch3'))
        d = list(models.switchcontrol4.objects.order_by('-now').values_list('switch4'))
        if a:
            # self.append_last_list(a,self.a_list)
            self.a_list = a[0][0]
            if self.a_list == 1:
                self.a_list = True
            elif self.a_list == 2:
                self.a_list = False
            else:
                pass
        if b:
            # self.append_last_list(b,self.b_list)
            self.b_list = b[0][0]
            if self.b_list == 1:
                self.b_list = True
            elif self.b_list == 2:
                self.b_list = False
            else:
                pass
        if c:
            # self.append_last_list(c,self.c_list)
            self.c_list = c[0][0]
            if self.c_list == 1:
                self.c_list = True
            elif self.c_list == 2:
                self.c_list = False
            else:
                pass
        if d:
            # self.append_last_list(d,self.d_list)
            self.d_list = d[0][0]
            if self.d_list == 1:
                self.d_list = True
            elif self.d_list == 2:
                self.d_list = False
            else:
                pass


        if self.copya != self.a_list:
            # if self.a_list:
            self.redislist1 = {'values':[{"id":"s1","v":self.a_list,"q":True}]}
                # models.switchcontrol1.objects.all().delete()
        self.copya = self.a_list
        # print(self.copya)

        if self.copyb != self.b_list:
            # if self.b_list:
            self.redislist2 = {'values':[{"id":"s2","v":self.b_list,"q":True}]}
                # models.switchcontrol2.objects.all().delete()
        self.copyb = self.b_list

        if self.copyc != self.c_list:
            # if self.c_list:
                self.redislist3 = {'values':[{"id":"s3","v":self.c_list,"q":True}]}
                # models.switchcontrol3.objects.all().delete()
        self.copyc = self.c_list

        if self.copyd != self.d_list:
            # if self.d_list:
                self.redislist4 ={'values':[{"id":"s4","v":self.d_list,"q":True}]}
                # models.switchcontrol4.objects.all().delete()
        self.copyd  =self.d_list


    def random_interval(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.sender_simulation,trigger='interval', seconds=2)
        # scheduler.add_job(self.switch_send,trigger='interval', seconds=1)
        # scheduler.add_job(self.switch_send,trigger='interval', seconds=1)
        scheduler.start()


if __name__ == "__main__":
    da = DeviceAgent(myqueue)
    da.start()
    da.join()

#
#     do = False
# last_do = False
#
# if (do and not last_do) or (not do and last_do):
#     pass
#
# do_last = do