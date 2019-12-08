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
  
  @property
  def name(self):
    return self._name

  def turn_on(self, rbw):
    self._set_color(rbw)

  def turn_off(self):
    self._set_color(OFF_COLOR)

  def _set_color(self, rbw):
    UDP_IP = self._ip
    UDP_PORT = 2390
    MESSAGE = 'PWM_SET:' + rbw
    self._sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))

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