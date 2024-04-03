#!/usr/bin/env python
"""Aquael module for controlling Aquael LED lights over UDP."""
import asyncio
import socket
import asyncudp

OFF_COLOR = "000000000"
UDP_PORT = 2390

class Hub():
  def __init__(self, hosts):
    self._lights = [Light(host["host"], host["name"]) for host in hosts]

  @property
  def lights(self):
    return self._lights

class Light():
  def __init__(self, ip: str, name: str):
    self._ip = ip
    self._name = name
    self._color = OFF_COLOR
    self._brightness_pct = 1
  
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
    return round(self._brightness_pct * 255)

  @brightness.setter
  def brightness(self, value):
    self._brightness_pct = value / 255

  @property
  def brightness_pct(self):
    return self._brightness_pct
  
  @brightness_pct.setter
  def brightness_pct(self, value):
    self._brightness_pct = min(max(value, 0), 1)

  def _adjust_color(self, c):
    color = min(max(round(c * self.brightness_pct), 1), 200)
    return "{:03d}".format(color)

  # Sync methods
  def update(self):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
      sock.bind(("0.0.0.0", UDP_PORT))
      sock.sendto(b"PWM_READ", (self.ip, UDP_PORT))
      data = sock.recv(1024)
      res = data.decode()
      if "ALL:" in res:
        colors = res.strip().split(":")[1:]
        self._color = "".join(colors)

  def turn_on(self, r, b, w):
    rbw =  self._adjust_color(r) + self._adjust_color(b) + self._adjust_color(w)
    self._dispatch_color(rbw)

  def turn_off(self):
    self._dispatch_color(OFF_COLOR)

  def _dispatch_color(self, rbw):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
      sock.bind(("0.0.0.0", UDP_PORT))
      message = f"PWM_SET:{rbw}"
      sock.sendto(message.encode(), (self.ip, UDP_PORT))
      data = sock.recv(1024)
      res = data.decode()
      if "PWMOK" not in res:
        raise ConnectionError(f"Error setting color on {self.ip}")

  # Async methods
  async def async_update(self):
    async with await asyncudp.create_socket(local_addr=("0.0.0.0", UDP_PORT)) as sock:
      sock.sendto(b"PWM_READ", (self.ip, UDP_PORT))
      data, _ = await sock.recvfrom()
      res = data.decode()
      if "ALL:" in res:
        colors = res.strip().split(":")[1:]
        self._color = "".join(colors)

    await asyncio.sleep(0) # Needed to avoid "Address already in use" error

  async def async_turn_on(self, r, b, w):
    rbw =  self._adjust_color(r) + self._adjust_color(b) + self._adjust_color(w)
    await self._async_dispatch_color(rbw)

  async def async_turn_off(self):
    await self._async_dispatch_color(OFF_COLOR)

  async def _async_dispatch_color(self, rbw):
    async with await asyncudp.create_socket(local_addr=("0.0.0.0", UDP_PORT)) as sock:
      message = f"PWM_SET:{rbw}"
      sock.sendto(message.encode(), (self.ip, UDP_PORT))
      data, _ = await sock.recvfrom()
      res = data.decode()
      if "PWMOK" not in res:
        raise ConnectionError(f"Error setting color on {self.ip}")

    await asyncio.sleep(0) # Needed to avoid "Address already in use" error