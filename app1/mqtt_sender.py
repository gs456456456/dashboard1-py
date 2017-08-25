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
import paho.mqtt.client as mqtt
from paho.mqtt.client import connack_string
from app1.models import lightStatus
from app1 import models
from django.utils import timezone
import datetime
from apscheduler.schedulers.background import BackgroundScheduler


MQTT_SERVER = "192.168.1.2"
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60
MQTT_TOPIC_PREFIX = "/zigbee/"
MQTT_SEND_INTERVAL = 1


class DeviceAgent(threading.Thread):
    """
    @brief      a Mqtt Client as connection manager interface
                connect to local broker
    """

    def __init__(self):
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
        self.mqttc.loop_start()
        # logger.warning('loop_start remote_mqtt_client')
        return True

    def run(self):
        # remote mqtt parameters
        if not self.init_mqtt_client():
            self.stop()

        # self.loop_forever_local_mqtt_client()
        while not self._stop.is_set():
            # read from modbus tcp server
            if self.mqttConnected:
                self.random_interval()
                # self.sender_simulation()
                # time.sleep(MQTT_SEND_INTERVAL)
                self.mqttc.loop_forever()

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
    # def r_send(self, topic, data):
    #     if self.mqttc is None:
    #         return
    #     Thread=[]
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
    #     msg = json.dumps(data)
    #     # mqttMessageInfo = self.mqttc.publish(topic, msg, qos=2)
    #     self.mqttc.publish(topic, msg, qos=2)
    #     print("send: " + topic + " " + str(data) + "\n")


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
            self.factorycache.clear()
        else:
            print('工厂数据错误!')


    def temp_mysql_save(self):
        # targetlist = []
        temp = list(models.topicGet.objects.filter(nid='2',ch='1').values_list('m'))
        self.append_list(temp,self.targetlist1)
        self.cache(self.targetlist1,'temp',len(self.targetlist1))
        self.targetlist1 = []

    def humi_mysql_save(self):
        # targetlist = []
        humi = list(models.topicGet.objects.filter(nid='2',ch='2').values_list('m'))
        self.append_list(humi,self.targetlist2)
        self.cache(self.targetlist2,'humi',len(self.targetlist2))
        self.targetlist2 = []

    def sun_mysql_save(self):
        # targetlist = []
        sun = list(models.topicGet.objects.filter(nid='2',ch='3').values_list('m'))
        self.append_list(sun,self.targetlist3)
        self.cache(self.targetlist3,'sun',len(self.targetlist3))
        self.targetlist3 = []

    def pm_mysql_save(self):
        # targetlist = []
        PM = list(models.topicGet.objects.filter(nid='3',ch='1').values_list('m'))
        self.append_list(PM,self.targetlist4)
        self.cache(self.targetlist4,'pm',len(self.targetlist4))
        self.targetlist4 = []

    def co2_mysql_save(self):
        # targetlist = []
        co2 = list(models.topicGet.objects.filter(nid='4',ch='1').values_list('m'))
        self.append_list(co2,self.targetlist5)
        self.cache(self.targetlist5,'co2',len(self.targetlist5))
        self.targetlist5 = []

    def pres_mysql_save(self, jsonObject):
        # targetlist = []
        pres = list(models.topicGet.objects.filter(nid='1',ch='1').values_list('m'))
        self.append_list(pres,self.targetlist6)
        self.cache(self.targetlist6,'waterpressure',len(self.targetlist6))
        self.targetlist6 = []


    def lightmysql_save(self):
        targetlist = []
        g = list(models.topicGet.objects.filter(nid='5',ch='3').values_list('m'))
        self.append_list(g,targetlist)
        for index, value in enumerate(targetlist):
            if value=='True':
                targetlist[index]=1
            elif value=='False':
                targetlist[index]=4
        for x in targetlist:
            models.lightStatus.objects.create(nid=x,status_change=3)

    def lightmysql_save2(self):
        targetlist = []
        h = list(models.topicGet.objects.filter(nid='5',ch='1').values_list('m'))
        self.append_list(h,targetlist)
        for index, value in enumerate(targetlist):
            if value == '0.0' or float(value)>0:
                targetlist[index]=2
        for x in targetlist:
            models.lightStatus.objects.create(nid=x,status_change=3)

    def lightmysql_save3(self):
        targetlist = []
        h = list(models.topicGet.objects.filter(nid='5',ch='2').values_list('m'))
        self.append_list(h,targetlist)
        for index, value in enumerate(targetlist):
            if value == '0.0' or float(value)>0:
                targetlist[index]=3
        for x in targetlist:
            models.lightStatus.objects.create(nid=x,status_change=3)





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
        self.mqttc.subscribe(topic)


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
        topicid = msg.topic[-5]
        topicch = msg.topic[-1]
        try:
            jsonObject = json.loads(msg.payload.decode('utf-8'))
        except Exception as e:
            errStr = "JSON loads Exception from msg.payload: " + str(e)
            print(errStr)
            return
        m = jsonObject['m']
        ts = jsonObject['ts']
        s = jsonObject['s']
        # models.topicGet.objects.create(nid=topicid,ch=topicch,m=m,ts=ts,s=s)
        # # print(jsonObject)
        # self.lightmysql_save2()
        # self.lightmysql_save3()
        # self.lightmysql_save()
        # 
        # 
        # 
        # self.pm_mysql_save()
        
        # self.co2_mysql_save()
        t = msg.topic
        if "id1/ch1" in t:
            self.pres_mysql_save(jsonObject)
        elif "id2/ch1" in t:
            self.temp_mysql_save(jsonObject)
        elif "id2/ch2" in t:
            self.humi_mysql_save(jsonObject)
        elif "id2/ch3" in t:
            self.sun_mysql_save(jsonObject)
        else:
            pass

    def random_save(self,data):
        # self.deviceswitch_create(data)
        self.watertower_create(data)
        self.air_create(data)
        self.boiler_create(data)
        self.firepro_create(data)
        self.pipe_create(data)


    def sender_simulation(self):
        payload = {}
        # payload['d'] = round(100.0 * random.random(), 2)
        # machine =  payload['m'] = random.randint(1,4)##红黄蓝绿灯
        tagName = 'test'
        topic = MQTT_TOPIC_PREFIX + "/" + tagName
        # status = payload['s'] = 4 #电机组装线3 转子组装线4
        # payload['q'] = 192
        utc = arrow.utcnow()
        time = payload['ts'] = utc.format('YYYY-MM-DDTHH:mm:ss.SSSSSS') + "Z"#时间戳
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
        # self.r_send(topic, payload)

    def random_interval(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.sender_simulation,trigger='interval', seconds=2)
        scheduler.start()


if __name__ == "__main__":
    da = DeviceAgent()
    da.setDaemon(True)
    da.start()
    try:
        while da.isAlive():
            pass
    except KeyboardInterrupt:
        print('stopped by keyboard')
    print('main end')