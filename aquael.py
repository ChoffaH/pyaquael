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

class Light():
  def __init__(self, ip, name = None):
    self._ip = ip
    self._name = name
  
  @property
  def name(self):
    return self._name

  def turn_on(self, rbw):
    set_color(self._ip, rbw)

  def turn_off(self):
    set_color(self._ip, OFF_COLOR)

def set_color(ip, rbw):
  UDP_IP = ip
  UDP_PORT = 2390
  MESSAGE = 'PWM_SET:' + rbw

  print('UDP target IP:', UDP_IP)
  print('UDP target port:', UDP_PORT)
  print('message:', MESSAGE)

  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.bind(('0.0.0.0', 2390))
  sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))

def __main():
  arguments = docopt(__doc__, version='0.0.5')
  ip = arguments['IPADDRESS']
  rbw = arguments['RBW']
  light = Light(ip)

  if arguments['poweron'] is True:
    light.turn_on(rbw)
  elif arguments['poweroff'] is True:
    light.turn_off()

if __name__ == '__main__':
  __main()