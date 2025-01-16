#!/usr/bin/env python
"""Aquael module for controlling Aquael LED lights over UDP."""
import asyncio
import socket
import asyncudp

OFF_COLOR = [0, 0, 0]
UDP_PORT = 2390

class Hub():
  def __init__(self, hosts: list[str]):
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

  @property
  def brightness(self):
    return round(self._brightness_pct * 255)

  @brightness.setter
  def brightness(self, value: int):
    self._brightness_pct = value / 255

  @property
  def brightness_pct(self):
    return self._brightness_pct
  
  @brightness_pct.setter
  def brightness_pct(self, value: float):
    self._brightness_pct = min(max(value, 0), 1)

  def _adjust_color(self, c: int):
    color = min(max(round(c * self.brightness_pct), 1), 200)
    return "{:03d}".format(color)
  
  def _extract_mac_address(self, data) -> str:
    res = data.decode()
    mac_address = None
    if "MAC:" in res:
      mac_address = res.strip().split(":")[1:]
      mac_address = ":".join(mac_address)
    return mac_address
  
  def _extract_name(self, data) -> str:
    res = data.decode()
    return res
  
  def _extract_color(self, data):
    res = data.decode()
    color = OFF_COLOR
    if "ALL:" in res:
      color = res.strip().split(":")[1:]
      color = [int(c) for c in color]
    return color

  async def async_test_connection(self) -> bool:
    async with await asyncudp.create_socket(local_addr=("0.0.0.0", UDP_PORT), remote_addr=(self.host, UDP_PORT), reuse_port=True) as sock:
      sock.sendto(b"PWM_READ")
      await asyncio.wait_for(sock.recvfrom(), timeout=5)

    await asyncio.sleep(0) # Needed to avoid "Address already in use" error
    return True

  async def async_get_mac_address(self) -> str:
    async with await asyncudp.create_socket(local_addr=("0.0.0.0", UDP_PORT), remote_addr=(self.host, UDP_PORT), reuse_port=True) as sock:
      sock.sendto(b"MAC?")
      data, _ = await asyncio.wait_for(sock.recvfrom(), timeout=30)
      mac_address = self._extract_mac_address(data)

    await asyncio.sleep(0) # Needed to avoid "Address already in use" error
    return mac_address
  
  async def async_get_name(self) -> str:
    async with await asyncudp.create_socket(local_addr=("0.0.0.0", UDP_PORT), remote_addr=(self.host, UDP_PORT), reuse_port=True) as sock:
      sock.sendto(b"NAME?")
      data, _ = await asyncio.wait_for(sock.recvfrom(), timeout=30)
      name = self._extract_name(data)

    await asyncio.sleep(0) # Needed to avoid "Address already in use" error
    return name

  async def async_update(self):
    async with await asyncudp.create_socket(local_addr=("0.0.0.0", UDP_PORT), remote_addr=(self.host, UDP_PORT), reuse_port=True) as sock:
      sock.sendto(b"PWM_READ")
      data, _ = await asyncio.wait_for(sock.recvfrom(), timeout=30)
      self._color = self._extract_color(data)

    await asyncio.sleep(0) # Needed to avoid "Address already in use" error

  async def async_turn_on(self, r: int, b: int, w: int):
    rbw =  self._adjust_color(r) + self._adjust_color(b) + self._adjust_color(w)
    await self._async_dispatch_color(rbw)

  async def async_turn_off(self):
    rbw = "".join(["{:03d}".format(c) for c in OFF_COLOR])
    await self._async_dispatch_color(rbw)

  async def _async_dispatch_color(self, rbw: str):
    async with await asyncudp.create_socket(local_addr=("0.0.0.0", UDP_PORT), remote_addr=(self.host, UDP_PORT), reuse_port=True) as sock:
      message = f"PWM_SET:{rbw}"
      sock.sendto(message.encode())
      data, _ = await asyncio.wait_for(sock.recvfrom(), timeout=30)
      res = data.decode()
      if "PWMOK" not in res:
        raise ConnectionError(f"Error setting color on {self.host}")

    await asyncio.sleep(0) # Needed to avoid "Address already in use" error