#!/usr/bin/env python
'''Usage:
  aquael poweron IPADDRESS RBW
  aquael poweroff IPADDRESS
  aquael (-h | --help)
  aquael --version
'''
from docopt import docopt
import threading
import socket

OFF_COLOR = '000000000'
UDP_PORT = 2390

class Hub():
  def __init__(self, hosts):
    self._sock = self._create_sock()
    self._lights = [Light(self._sock, host['host'], host['name']) for host in hosts]
    thread = threading.Thread(target=self._recv_response, daemon=True)
    thread.start()

  @property
  def lights(self):
    return self._lights

  def _create_sock(self):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', UDP_PORT))
    return sock

  def _recv_response(self):
    while True:
      data, addr = self._sock.recvfrom(1024)
      ip, port = addr
      for light in self._lights:
        if light.ip == ip:
          res = data.decode()
          if 'ALL:' in res:
            colors = res.strip().split(':')
            colors.pop(0)
            light.color = ''.join(colors)


class Light():
  def __init__(self, sock, ip, name = None):
    self._sock = sock
    self._ip = ip
    self._name = name
    self._color = OFF_COLOR
    self._brightness = 255
  
  @property
  def ip(self):
    return self._ip

  @property
  def name(self):
    return self._name

  @property
  def is_on(self):
    return self._color != OFF_COLOR
  
  @property
  def color(self):
    return self._color

  @color.setter
  def color(self, value):
    self._color = value

  @property
  def brightness(self):
    return self._brightness

  @brightness.setter
  def brightness(self, value):
    self._brightness = value

  def turn_on(self, r, b, w):
    rbw =  self._adjust_color(r) + self._adjust_color(b) + self._adjust_color(w)
    self._dispatch_color(rbw)

  def turn_off(self):
    self._dispatch_color(OFF_COLOR)

  def update(self):
    self._dispatch_update()

  def _dispatch_color(self, rbw):
    message = 'PWM_SET:' + rbw
    self._sock.sendto(message.encode(), (self._ip, UDP_PORT))

  def _dispatch_update(self):
    message = 'PWM_READ'
    self._sock.sendto(message.encode(), (self._ip, UDP_PORT))

  def _adjust_color(self, c):
    brightness_pct = self._brightness / 255
    color = int(round((c * brightness_pct)))
    color = color if color <= c else c
    color = color if color <= 200 else 200
    color = color if color >= 1 else 1
    return "{:03d}".format(color)

def main_cli():
  arguments = docopt(__doc__, version='0.1.0')
  ip = arguments['IPADDRESS']
  rbw = arguments['RBW']
  sock = createSock()
  light = Light(sock, ip)

  if arguments['poweron'] is True:
    light.turn_on(rbw)
  elif arguments['poweroff'] is True:
    light.turn_off()

if __name__ == '__main__':
  main_cli()