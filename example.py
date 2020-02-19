import aquael

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
light.brightness = 255
light.turn_on(200, 200, 112)
light.update()

while True:
  if light.is_on:
    print(f'Light is on? {light.is_on} {light.color}')
    break