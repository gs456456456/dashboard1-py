########################################
# Copyright (c) 2017 Shanghai Kimstars #
########################################

work with zigbee-data-forwarder


管理员用户名和密码在导入数据库同时需要重新创建 python3 manage.py createsuperuser
点击生产线上的任意方块即可进入明细页面

python3 manage.py migrate
python3 manage.py runserver
然后运行app1文件夹里的mqtt_sender.py即可

django admin:
admin
12345678


rotor:line3
elec:line10

yellow:待机
blue:检修
red:故障
green:运行
