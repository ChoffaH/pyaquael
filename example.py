import aquael
import time

hosts = [
  {
    'name': 'Light 1',
    'host': '192.168.1.200'
  },
  {
    'name': 'Light 2',
    'host': '192.168.1.201'
  }
]
hub = aquael.Hub(hosts)
light = hub.lights[0]
light.brightness = 100
light.turn_on(200, 200, 112)
time.sleep(1)
light.brightness = 255
light.turn_on(200, 200, 112)
print(f'Light is on? {light.is_on}')