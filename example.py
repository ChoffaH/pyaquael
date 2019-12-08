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
light.turn_on('200200112')
time.sleep(5)
light.turn_off()