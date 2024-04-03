from pyaquael import aquael
from time import sleep

hosts = [
  {
    'name': 'Light 1',
    'host': '192.168.30.80'
  },
  {
    'name': 'Light 2',
    'host': '192.168.30.81'
  }
]
hub = aquael.Hub(hosts)
light1 = hub.lights[0]
light2 = hub.lights[1]

light1.update()
light2.turn_off()
sleep(2)
light2.brightness_pct = 1
light2.turn_on(200, 200, 112)
light2.update()

if light1.is_on:
  print(f'Light 1 is on? {light1.is_on} {light1.color}')

if light2.is_on:
  print(f'Light 2 is on? {light2.is_on} {light2.color}')