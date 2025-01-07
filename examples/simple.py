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

# Light 1
light1.update()

light1_mac_address = light1.get_mac_address()
light1_name = light1.get_name()

print(f'Light 1 MAC Address: {light1_mac_address}')
print(f'Light 1 Name: {light1_name}')
if light1.is_on:
  print(f'Light 1 is on. Color: {light1.color}')
else:
  print(f'Light 1 is off.')

print('')

# Light 2
light2.turn_off()
sleep(2)
light2.brightness_pct = 1
light2.turn_on(200, 200, 112)
light2.update()

light2_mac_address = light2.get_mac_address()
light2_name = light2.get_name()

print(f'Light 2 MAC Address: {light2_mac_address}')
print(f'Light 2 Name: {light2_name}')
if light2.is_on:
  print(f'Light 2 is on. Color: {light2.color}')
else:
  print(f'Light 2 is off.')