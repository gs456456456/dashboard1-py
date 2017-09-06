#!/usr/bin/env python
# -*- encoding=utf-8 -*-

########################################
# Copyright (c) 2017 Shanghai Kimstars #
########################################
import os
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

# from snippets.models import TestData

MQTT_SERVER = "192.168.1.2"
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60
MQTT_TOPIC_PREFIX = "/Kimstars"
MQTT_SEND_INTERVAL = 2


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
            if self.mqttConnected:
            #    self.sender_simulation()
            # time.sleep(MQTT_SEND_INTERVAL)
                self.mqttc.loop_forever()

    def stop(self):
        self._stop.set()
        if self.mqttc is not None:
            self.mqttc.disconnect()
            self.mqttc.loop_stop()

    def r_send(self, topic, data):
        if self.mqttc is None:
            return
        # 存数据
        models.lightStatus.objects.create(nid=data['m'],status_change=data['s'],now=data['ts'])
        msg = json.dumps(data)
        # mqttMessageInfo = self.mqttc.publish(topic, msg, qos=2)
        self.mqttc.publish(topic, msg, qos=2)
        print("send: " + topic + " " + str(data) + "\n")

    # The callback for when the client receives a CONNACK response from the
    # server.
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


    def append_list(self,origlist,targetlist):
        for x in origlist:
            for y in x:
                targetlist.append(y)

    ####接收mqtt数据并存入数据库

    def temp_mysql_save(self):
        targetlist = []
        temp = list(models.topicGet.objects.filter(nid='2',ch='1').values_list('m'))
        self.append_list(temp,targetlist)
        for x in targetlist:
            models.temperatureFac.objects.create(temperature=x)

    def humi_mysql_save(self):
        targetlist = []
        humi = list(models.topicGet.objects.filter(nid='2',ch='2').values_list('m'))
        self.append_list(humi,targetlist)
        for x in targetlist:
            models.temperatureFac.objects.create(humidity=x)

    def sun_mysql_save(self):
        targetlist = []
        sun = list(models.topicGet.objects.filter(nid='2',ch='3').values_list('m'))
        self.append_list(sun,targetlist)
        for x in targetlist:
            models.temperatureFac.objects.create(sun=x)

    def pm_mysql_save(self):
        targetlist = []
        PM = list(models.topicGet.objects.filter(nid='3',ch='1').values_list('m'))
        self.append_list(PM,targetlist)
        for x in targetlist:
            models.temperatureFac.objects.create(PM=x)

    def co2_mysql_save(self):
        targetlist = []
        co2 = list(models.topicGet.objects.filter(nid='4',ch='1').values_list('m'))
        self.append_list(co2,targetlist)
        for x in targetlist:
            models.temperatureFac.objects.create(co2=x)

    def pres_mysql_save(self):
        targetlist = []
        pres = list(models.topicGet.objects.filter(nid='1',ch='1').values_list('m'))
        self.append_list(pres,targetlist)
        for x in targetlist:
            models.temperatureFac.objects.create(waterpressure=x)

    def lightmysql_save(self):
        g = list(models.topicGet.objects.filter(nid='5',ch='3').values_list('m'))
        h = list(models.topicGet.objects.filter(nid='5',ch='4').values_list('m'))

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
        models.topicGet.objects.create(nid=topicid,ch=topicch,m=m,ts=ts,s=s)
        print(jsonObject)

    #
    def sender_simulation(self):
        payload = {}
        # payload['d'] = round(100.0 * random.random(), 2)
        machine =  payload['m'] = random.randint(1,4)##红黄蓝绿灯
        tagName = 'test'
        topic = MQTT_TOPIC_PREFIX + "/" + tagName
        status = payload['s'] = random.randint(3,4)#电机组装线3 转子组装线4
        # payload['q'] = 192
        utc = arrow.utcnow()
        time = payload['ts'] = utc.format('YYYY-MM-DDTHH:mm:ss.SSSSSS') + "Z"#时间戳
        self.r_send(topic, payload)

            # # co2 = payload['co2'] = random.randint(300,1000)
        # # temp = payload['temp'] =random.randint(20,33)
        # # humidity = payload['humi']=random.randint(0,100)
        # # sunshine = payload['sun']=random.randint(1000,2000)
        # # PM = payload['pm']=random.randint(0,50)
        # # # waterpressure = payload['waterpressure']=random.randint(0,10)
        # # waterpressure = payload['waterpressure']=random.choice([0.002,0.001,-0.003])
        # # switch1 = payload['sw1']=random.randint(1,2)
        # # switch2 = payload['sw2']=random.randint(1,2)
        # # switch3 = payload['sw3']=random.randint(1,2)
        # # switch4 = payload['sw4']=random.randint(1,2)
        # watertowerph = payload['wtph']=random.choice([3,6,9])
        # # watertowerheight = payload['wthe']=random.randint(0,10)
        # watertowerheight = payload['wthe']=random.choice([0.002,0.001,-0.003])
        # watertowerflow= payload['wtfl']=random.choice([4,6,9])
        # airpressure = payload['airp'] = random.randint(1000,2000)
        # windspeed = payload['winds']=random.randint(10,20)
        # windpressure = payload['windp']=random.randint(20,30)
        # boilerpressure = payload['boilp']=random.randint(20,30)
        # boilertemp = payload['boilt']=random.randint(20,30)
        # boilerwaterpressure = payload['boilwp']=random.randint(1000,2000)
        # boilerelec = payload['boile']=random.randint(30,40)
        # pipewaterpressure = payload['pipewp']=random.randint(300,500)



    def run(self):
        t1 = threading.Thread(target=self.run1)
        self.threading.append(t1)
        t2 = threading.Thread(target=self.run2)
        self.threading.append(t2)
        for t in self.threading:
            t.setDaemon(True)
            t.start()

    def run1(self):
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

    def run2(self):
        # remote mqtt parameters
        if not self.init_mqtt_client():
            self.stop()

        # self.loop_forever_local_mqtt_client()
        while not self._stop.is_set():
            # read from modbus tcp server
            if self.mqttConnected:
            #     self.sender_simulation()
            #     time.sleep(MQTT_SEND_INTERVAL)
                self.r_send(MQTT_TOPIC_PREFIX,s5)
                time.sleep(MQTT_SEND_INTERVAL)

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