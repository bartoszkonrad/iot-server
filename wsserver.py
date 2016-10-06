#!/usr/bin/python
# coding: utf-8
# Bartosz Konrad <bartosz.konrad@gmail.com>
'''\
WebSocker Server
'''
import time
import gevent
import requests
from gevent.pywsgi import WSGIServer
from gevent.lock import Semaphore
from geventwebsocket.handler import WebSocketHandler
from datetime import datetime


def process(ws, data, sem):
    print('{} got data "{}"'.format(datetime.now().strftime('%H:%M:%S'), data))
    # gevent.sleep(5)
    with sem:
        ws.send(data)

def rgbSetter(ws, data, sem):
    values = data.split(';')
    payload = {'h': values[0], 's': values[1], 'l': values[2], 'r': values[3]}
    r = requests.get('http://rgb.lan/color', params=payload)
    # print('{} got data "{}"'.format(datetime.now().strftime('%H:%M:%S'), values))
    # print(r.url)
    # with sem:
    #     ws.send(r.text)


def poller(ws):
    print('{} poller'.format(datetime.now().strftime('%H:%M:%S')))
    while True:
        print('{} poller running'.format(datetime.now().strftime('%H:%M:%S')))
        ws.send(str(datetime.now()))
        time.sleep(2)


def app(environ, start_response):
    ws = environ['wsgi.websocket']
    sem = Semaphore()
    while True:
        data = ws.receive()
        # gevent.spawn(process, ws, data, sem)
        gevent.spawn(rgbSetter, ws, data, sem)
        # if 'some' in data:
        #     gevent.spawn(process, ws, data, sem)
        # else:
        #     data = 'dd'
        #     gevent.spawn(process, ws, data, sem)
    # gevent.spawn(poller, ws)

server = WSGIServer(("", 10080), app, handler_class=WebSocketHandler)
server.serve_forever()
