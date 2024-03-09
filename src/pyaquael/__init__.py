from pyaquael import aquael
from docopt import docopt

def main_cli():
  arguments = docopt(__doc__, version='0.1.0')
  ip = arguments['IPADDRESS']
  rbw = arguments['RBW']
  hosts = [
    {
      'name': 'Light 1',
      'host': ip
    }
  ]

  hub = aquael.Hub(hosts)
  light = hub.lights[0]

  if arguments['poweron'] is True:
    light.turn_on(rbw)
  elif arguments['poweroff'] is True:
    light.turn_off()