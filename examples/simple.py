from pyaquael import aquael
from time import sleep

hosts = ['192.168.30.80', '192.168.30.81']
hub = aquael.Hub(hosts)
light1 = hub.lights[0]
light2 = hub.lights[1]

def manage_light(light, name):
  light_test = light.test_connection()
  if not light_test:
    print(f'Failed to connect to {name}.')
  else:
    light.turn_off()
    sleep(2)
    light.turn_on(200, 200, 112)
    light.update()

    light_mac_address = light.get_mac_address()
    light_name = light.get_name()

    print(f'{name} MAC Address: {light_mac_address}')
    print(f'{name} Name: {light_name}')
    if light.is_on:
      print(f'{name} is on. Color: {light.color}')
    else:
      print(f'{name} is off.')

manage_light(light1, 'Light 1')
print('')
manage_light(light2, 'Light 2')
