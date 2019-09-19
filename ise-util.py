import argparse
import getpass
import sys

# ise library
import ise

datatypes = ('netdevgrp','netdev')

parser = argparse.ArgumentParser(description='Pull data from ISE')
parser.add_argument('datatypes', metavar='datatype', nargs='+', help="{} (or 'all' for all supported data)".format(' / '.join(datatypes)))
parser.add_argument('--hostname', required=True)
parser.add_argument('--port', type=int, default=9060)
parser.add_argument('--user', default="admin")

args = parser.parse_args()
password = getpass.getpass('Password:')

try:
  api = ise.API(hostname=args.hostname, user=args.user, password=password, debug=True)
except ValueError as err:
  print("Error: {}".format(err, file=sys.stderr))
  sys.exit(1)
#device = api.networkdevice('uuid')
#print(device['id'], device['authenticationSettings']['radiusSharedSecret'])

#sys.exit(0)

# all datatypes?
if 'all' in args.datatypes:
  api.networkgroups()
  api.networkdevicegroups()
else:
  for data in args.datatypes:
    if data == "netdevgrp":
      api.networkdevicegroups()
    elif data  == "netdev":
      api.networkdevices()
    else:
      print("Skipping invalid data type '{}'".format(data), file=sys.stderr)
