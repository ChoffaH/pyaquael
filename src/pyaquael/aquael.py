#!/usr/bin/env python
"""Aquael module for controlling Aquael LED lights over UDP."""
import asyncio
import socket
import asyncudp

OFF_COLOR = "000000000"
UDP_PORT = 2390

class Hub():
  def __init__(self, hosts):
    self._lights = [Light(host) for host in hosts]

  @property
  def lights(self):
    return self._lights

class Light():
  def __init__(self, host: str):
    self._host = host
    self._color = OFF_COLOR
    self._brightness_pct = 1
  
  @property
  def host(self):
    return self._host

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
  
  def _extract_mac_address(self, data):
    res = data.decode()
    mac_address = None
    if "MAC:" in res:
      mac_address = res.strip().split(":")[1:]
      mac_address = ":".join(mac_address)
    return mac_address
  
  def _extract_name(self, data):
    res = data.decode()
    return res
  
  def _extract_color(self, data):
    res = data.decode()
    color = None
    if "ALL:" in res:
      color = res.strip().split(":")[1:]
      color = "".join(color)
    return color

  # Sync methods
  def test_connection(self):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
      sock.settimeout(5)
      sock.bind(("0.0.0.0", UDP_PORT))
      try:
        sock.sendto(b"PWM_READ?", (self.host, UDP_PORT))
        sock.recv(1024)
        return True
      except socket.timeout:
        return False

  def get_mac_address(self):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
      sock.bind(("0.0.0.0", UDP_PORT))
      sock.sendto(b"MAC?", (self.host, UDP_PORT))
      data = sock.recv(1024)
      return self._extract_mac_address(data)
    
  def get_name(self):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
      sock.bind(("0.0.0.0", UDP_PORT))
      sock.sendto(b"NAME?", (self.host, UDP_PORT))
      data = sock.recv(1024)
      return self._extract_name(data)

  def update(self):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
      sock.bind(("0.0.0.0", UDP_PORT))
      sock.sendto(b"PWM_READ", (self.host, UDP_PORT))
      data = sock.recv(1024)
      self._color = self._extract_color(data)

  def turn_on(self, r, b, w):
    rbw =  self._adjust_color(r) + self._adjust_color(b) + self._adjust_color(w)
    self._dispatch_color(rbw)

  def turn_off(self):
    self._dispatch_color(OFF_COLOR)

  def _dispatch_color(self, rbw):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
      sock.bind(("0.0.0.0", UDP_PORT))
      message = f"PWM_SET:{rbw}"
      sock.sendto(message.encode(), (self.host, UDP_PORT))
      data = sock.recv(1024)
      res = data.decode()
      if "PWMOK" not in res:
        raise ConnectionError(f"Error setting color on {self.host}")

  # Async methods
  async def async_test_connection(self):
    async with await asyncudp.create_socket(local_addr=("0.0.0.0", UDP_PORT)) as sock:
      sock.sendto(b"PWM_READ", (self.host, UDP_PORT))
      try:
        await asyncio.wait_for(sock.recvfrom(), timeout=5)
        result = True
      except asyncio.TimeoutError:
        result = False

    await asyncio.sleep(0) # Needed to avoid "Address already in use" error
    return result

  async def async_get_mac_address(self):
    async with await asyncudp.create_socket(local_addr=("0.0.0.0", UDP_PORT)) as sock:
      sock.sendto(b"MAC?", (self.host, UDP_PORT))
      data, _ = await sock.recvfrom()
      mac_address = self._extract_mac_address(data)

    await asyncio.sleep(0) # Needed to avoid "Address already in use" error
    return mac_address
  
  async def async_get_name(self):
    async with await asyncudp.create_socket(local_addr=("0.0.0.0", UDP_PORT)) as sock:
      sock.sendto(b"NAME?", (self.host, UDP_PORT))
      data, _ = await sock.recvfrom()
      name = self._extract_name(data)

    await asyncio.sleep(0) # Needed to avoid "Address already in use" error
    return name

  async def async_update(self):
    async with await asyncudp.create_socket(local_addr=("0.0.0.0", UDP_PORT)) as sock:
      sock.sendto(b"PWM_READ", (self.host, UDP_PORT))
      data, _ = await sock.recvfrom()
      self._color = self._extract_color(data)

    await asyncio.sleep(0) # Needed to avoid "Address already in use" error

  async def async_turn_on(self, r, b, w):
    rbw =  self._adjust_color(r) + self._adjust_color(b) + self._adjust_color(w)
    await self._async_dispatch_color(rbw)

  async def async_turn_off(self):
    await self._async_dispatch_color(OFF_COLOR)

  async def _async_dispatch_color(self, rbw):
    async with await asyncudp.create_socket(local_addr=("0.0.0.0", UDP_PORT)) as sock:
      message = f"PWM_SET:{rbw}"
      sock.sendto(message.encode(), (self.host, UDP_PORT))
      data, _ = await sock.recvfrom()
      res = data.decode()
      if "PWMOK" not in res:
        raise ConnectionError(f"Error setting color on {self.host}")

    await asyncio.sleep(0) # Needed to avoid "Address already in use" error