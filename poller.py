#!/usr/bin/python
# coding: utf-8
# Bartosz Konrad <bartosz.konrad@gmail.com>
'''\
Sensor poller
'''

import schedule
import time
import os
from common import DB
#from systemd import journal 


db = DB()

def job():
    print("I'm working...")

def rpiTemp():
    res = os.popen('vcgencmd measure_temp').readline()
    rpi_temp = res.replace("temp=","").replace("'C\n","")
    sql = '''insert into sensors (value, type, location) values (%s, %s, %s)'''
    data = (rpi_temp, 'temp', 'rpi')
    db.insert(sql, data)
#    journal.write('dd')

schedule.every(10).seconds.do(rpiTemp)

while True:
    schedule.run_pending()
    time.sleep(1)
