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

  await light1.async_update()
  await light2.async_turn_off()
  await asyncio.sleep(2)
  light2.brightness_pct = 1
  await light2.async_turn_on(200, 200, 112)
  await light2.async_update()

  if light1.is_on:
    print(f'Light 1 is on? {light1.is_on} {light1.color}')

  if light2.is_on:
    print(f'Light 2 is on? {light2.is_on} {light2.color}')

asyncio.run(main())