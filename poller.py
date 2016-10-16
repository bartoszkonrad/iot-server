#!/usr/bin/python
# coding: utf-8
# Bartosz Konrad <bartosz.konrad@gmail.com>
'''\
Sensor poller
'''

import schedule
import time
import os
import requests
from common import DB

db = DB()


def job():
    print("I'm working...")


def rpiTemp():
    res = os.popen('vcgencmd measure_temp').readline()
    rpitemp = res.replace("temp=", "").replace("'C\n", "")
    sql = '''insert into sensors (value, type, location) values (%s, %s, %s)'''
    data = (rpitemp, 'temp', 'rpi')
    db.insert(sql, data)


def bdrTemp():
    bdrtemp = requests.get('http://iot-rms.lan/temp?temp=bdr')
    sql = '''insert into sensors (value, type, location) values (%s, %s, %s)'''
    data = (bdrtemp.text, 'temp', 'bdr')
    db.insert(sql, data)


def lvrTemp():
    lvrtemp = requests.get('http://iot-rms.lan/temp?temp=lvr')
    sql = '''insert into sensors (value, type, location) values (%s, %s, %s)'''
    data = (lvrtemp.text, 'temp', 'lvr')
    db.insert(sql, data)

schedule.every(60).seconds.do(rpiTemp)
schedule.every(60).seconds.do(bdrTemp)
schedule.every(60).seconds.do(lvrTemp)

while True:
    schedule.run_pending()
    time.sleep(1)
