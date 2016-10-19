#!/usr/bin/python
# coding: utf-8
# Bartosz Konrad <bartosz.konrad@gmail.com>
'''\
WebSocker Server
'''
import time
import gevent
import requests
import json
from gevent.pywsgi import WSGIServer
from gevent.lock import Semaphore
from geventwebsocket.handler import WebSocketHandler
from datetime import datetime


def process(ws, data, sem):
    print('{} got data "{}"'.format(datetime.now().strftime('%H:%M:%S'), data))
    with sem:
        ws.send(data)


def driveKitchenLeds(ws, data, sem):
    print('{} got data "{}"'.format(datetime.now().strftime('%H:%M:%S'), data))
    url = 'http://iot-atx.lan/leds?kth={}'.format(data['val'])
    r = requests.get(url)
    if r.status_code is not 200:
        with sem:
            # ws.send(r.text)
            ws.send('Error')


def driveBathroomLeds(ws, data, sem):
    print('{} got data "{}"'.format(datetime.now().strftime('%H:%M:%S'), data))
    url = 'http://iot-atx.lan/leds?bth={}'.format(data['val'])
    r = requests.get(url)
    if r.status_code is not 200:
        with sem:
            # ws.send(r.text)
            ws.send('Error')

def driveBedRoomLamps(ws, data, sem):
    print('{} got data "{}"'.format(datetime.now().strftime('%H:%M:%S'), data))
    url = 'http://iot-rms.lan/light?{}={}'.format(data['lamp'], data['val'])
    r = requests.get(url)
    if r.status_code is not 200:
        with sem:
            # ws.send(r.text)
            ws.send('Error')

def driveLivingRoomLamps(ws, data, sem):
    print('{} got data "{}"'.format(datetime.now().strftime('%H:%M:%S'), data))
    url = 'http://iot-rms.lan/light?{}={}'.format(data['lamp'], data['val'])
    r = requests.get(url)
    if r.status_code is not 200:
        with sem:
            # ws.send(r.text)
            ws.send('Error')


def rgbPower(ws, data, sem):
    print('{} got data "{}"'.format(datetime.now().strftime('%H:%M:%S'), data))
    r = requests.get('http://iot-atx.lan/leds?{}={}'.format(data['loc'], data['val']))
    if r.status_code is not 200:
        with sem:
            # ws.send(r.text)
            ws.send('Error')

def rgbStrip(ws, data, sem):
    print('{} got data "{}"'.format(datetime.now().strftime('%H:%M:%S'), data))
    payload = {'h': data['h'], 's': data['s'], 'l': data['v'], 'r': data['loc']}
    r = requests.get('http://rgb.lan/color', params=payload)
    if r.status_code is not 200:
        with sem:
            # ws.send(r.text)
            ws.send('Error')

def app(environ, start_response):
    ws = environ['wsgi.websocket']
    sem = Semaphore()
    while True:
        data = ws.receive()
        # print(data)
        parsed_json = json.loads(data)
        print(parsed_json)
        if parsed_json['type'] == 'kitchenLeds':
            gevent.spawn(driveKitchenLeds, ws, parsed_json, sem)
        if parsed_json['type'] == 'bathroomLeds':
            gevent.spawn(driveBathroomLeds, ws, parsed_json, sem)
        if parsed_json['type'] == 'bedRoomLamps':
            gevent.spawn(driveBedRoomLamps, ws, parsed_json, sem)
        if parsed_json['type'] == 'livingRoomLamps':
            gevent.spawn(driveLivingRoomLamps, ws, parsed_json, sem)
        if parsed_json['type'] == 'rgbPower':
            gevent.spawn(rgbPower, ws, parsed_json, sem)
        if parsed_json['type'] == 'rgbStrip':
            gevent.spawn(rgbStrip, ws, parsed_json, sem)

        # gevent.spawn(process, ws, data, sem)
        # gevent.spawn(rgbSetter, ws, data, sem)
        # if 'some' in data:
        #     gevent.spawn(process, ws, data, sem)
        # else:
        #     data = 'dd'
        #     gevent.spawn(process, ws, data, sem)
    # gevent.spawn(poller, ws)

server = WSGIServer(("", 10080), app, handler_class=WebSocketHandler)
server.serve_forever()
