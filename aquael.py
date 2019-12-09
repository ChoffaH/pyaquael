#!/usr/bin/env python
'''Usage:
  aquael poweron IPADDRESS RBW
  aquael poweroff IPADDRESS
  aquael (-h | --help)
  aquael --version
'''
from docopt import docopt
import socket

OFF_COLOR = '000000000'
class Hub():
  def __init__(self, hosts):
    sock = createSock()
    self._lights = [Light(sock, host['host'], host['name']) for host in hosts]

  @property
  def lights(self):
    return self._lights

class Light():
  def __init__(self, sock, ip, name = None):
    self._sock = sock
    self._ip = ip
    self._name = name
    self._is_on = False
    self._brightness = 255
  
  @property
  def name(self):
    return self._name

  @property
  def is_on(self):
    return self._is_on
  
  @property
  def brightness(self):
    return self._brightness

  @brightness.setter
  def brightness(self, value):
    self._brightness = value

  def turn_on(self, r, b, w):
    rbw =  self._adjust_color(r) + self._adjust_color(b) + self._adjust_color(w)
    self._set_color(rbw)
    self._is_on = True

  def turn_off(self):
    self._set_color(OFF_COLOR)
    self._is_on = False

  def _set_color(self, rbw):
    UDP_IP = self._ip
    UDP_PORT = 2390
    MESSAGE = 'PWM_SET:' + rbw
    self._sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))

  def _adjust_color(self, c):
    brightness_pct = self._brightness / 255
    color = int(round((c * brightness_pct)))
    color = color if color <= c else c
    color = color if color <= 200 else 200
    color = color if color >= 1 else 1
    return "{:03d}".format(color)

def createSock():
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.bind(('0.0.0.0', 2390))
  return sock

def __main():
  arguments = docopt(__doc__, version='0.0.6')
  ip = arguments['IPADDRESS']
  rbw = arguments['RBW']
  sock = createSock()
  light = Light(sock, ip)

  if arguments['poweron'] is True:
    light.turn_on(rbw)
  elif arguments['poweroff'] is True:
    light.turn_off()

if __name__ == '__main__':
  __main()