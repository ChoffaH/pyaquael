"""Aquael CLI

Usage:
  aquael-cli (-h | --help)
  aquael-cli --version
  aquael-cli poweron IPADDRESS [--brightness BRIGHTNESS] [-r RED] [-b BLUE] [-w WHITE]
  aquael-cli poweroff IPADDRESS

Options:
  -h --help                 Show this
  --version                 Show version
  --brightness BRIGHTNESS   Set brightness [default: 255]
  -r RED                    Set red color [default: 0]
  -b BLUE                   Set blue color [default: 0]
  -w WHITE                  Set white color [default: 0]
"""

from importlib.metadata import version
from docopt import docopt
from pyaquael import aquael
import asyncio

async def _async_main_cli():
  arguments = docopt(__doc__, version=version('pyaquael'))
  ip = arguments['IPADDRESS']
  brightness = int(arguments['--brightness'])
  r = int(arguments['-r'])
  b = int(arguments['-b'])
  w = int(arguments['-w'])
  hosts = [ip]

  hub = aquael.Hub(hosts)
  light = hub.lights[0]

  if arguments['poweron'] is True:
    light.brightness = brightness
    await light.async_turn_on(r, b, w)
  elif arguments['poweroff'] is True:
    await light.async_turn_off()

def main_cli():
  asyncio.run(_async_main_cli())