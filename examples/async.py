from pyaquael import aquael
import asyncio

async def main():
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
  light1_test = await light1.async_test_connection()
  if not light1_test:
    print(f'Failed to connect to Light 1.')
  else:
    await light1.async_update()

    light1_mac_address = await light1.async_get_mac_address()
    light1_name = await light1.async_get_name()

    print(f'Light 1 MAC Address: {light1_mac_address}')
    print(f'Light 1 Name: {light1_name}')
    if light1.is_on:
      print(f'Light 1 is on. Color: {light1.color}')
    else:
      print(f'Light 1 is off.')

  print('')

  # Light 2
  light2_test = await light2.async_test_connection()
  if not light2_test:
    print(f'Failed to connect to Light 2.')
  else:
    await light2.async_turn_off()
    await asyncio.sleep(2)
    light2.brightness_pct = 1
    await light2.async_turn_on(200, 200, 112)
    await light2.async_update()

    light2_mac_address = await light2.async_get_mac_address()
    light2_name = await light2.async_get_name()

    print(f'Light 2 MAC Address: {light2_mac_address}')
    print(f'Light 2 Name: {light2_name}')
    if light2.is_on:
      print(f'Light 2 is on, color: {light2.color}')
    else:
      print(f'Light 2 is off.')

asyncio.run(main())