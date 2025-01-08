from pyaquael import aquael
import asyncio

async def main():
  hosts = ['192.168.30.80', '192.168.30.81']
  hub = aquael.Hub(hosts)
  light1 = hub.lights[0]
  light2 = hub.lights[1]

  async def manage_light(light, name):
    light_test = await light.async_test_connection()
    if not light_test:
      print(f'Failed to connect to {name}.')
    else:
      await light.async_turn_off()
      await asyncio.sleep(2)
      light.brightness_pct = 1
      await light.async_turn_on(200, 200, 112)
      await light.async_update()

      light_mac_address = await light.async_get_mac_address()
      light_name = await light.async_get_name()

      print(f'{name} MAC Address: {light_mac_address}')
      print(f'{name} Name: {light_name}')
      if light.is_on:
        print(f'{name} is on. Color: {light.color}')
      else:
        print(f'{name} is off.')

  await manage_light(light1, 'Light 1')
  print('')
  await manage_light(light2, 'Light 2')

asyncio.run(main())