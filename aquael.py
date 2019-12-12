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
        if light.ip == ip and 'PWMOK' in data.decode():
          light.evaluate_state()

class Light():
  def __init__(self, sock, ip, name = None):
    self._sock = sock
    self._ip = ip
    self._name = name
    self._is_on = False
    self._color = None
    self._brightness = 255
  
  @property
  def ip(self):
    return self._ip

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

  def turn_off(self):
    self._set_color(OFF_COLOR)
  
  def evaluate_state(self):
    self._is_on = self._color is not OFF_COLOR

  def _set_color(self, rbw):
    message = 'PWM_SET:' + rbw
    self._sock.sendto(message.encode(), (self._ip, UDP_PORT))
    self._color = rbw

  def _adjust_color(self, c):
    brightness_pct = self._brightness / 255
    color = int(round((c * brightness_pct)))
    color = color if color <= c else c
    color = color if color <= 200 else 200
    color = color if color >= 1 else 1
    return "{:03d}".format(color)

def __main():
  arguments = docopt(__doc__, version='0.0.9')
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