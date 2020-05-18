# coding=utf-8

import socket
import socks
import requests
from stem import Signal
from stem.control import Controller

with Controller.from_port(port = 9051) as controller:
    controller.authenticate()
    controller.signal(Signal.NEWNYM)

socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
socket.socket = socks.socksocket

print(requests.get('https://api.ipify.org/?format=json').text)