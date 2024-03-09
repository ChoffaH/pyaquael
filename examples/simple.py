from pyaquael import aquael

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
light = hub.lights[0]
light.brightness = 150
light.turn_on(200, 200, 112)
light.update()

while True:
  if light.is_on:
    print(f'Light is on? {light.is_on} {light.color}')
    break