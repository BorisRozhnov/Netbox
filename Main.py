"""
This script interract with netbox via pynetbox module for python 3

API Token: 0123456789abcdef0123456789abcdef01234567
/home/ansible/.ssh/id_rsa


nb = pynetbox.api(
    'http://localhost:8000',
    private_key_file='/path/to/private-key.pem',
    token='0123456789abcdef0123456789abcdef01234567',
    threading=True
)
"""


def Get_enclosure_data(ip):
    """
    Connect to blade enclosure by IP address and return blade servers.
    Data returned in dictionary type
    """
    # print('hello from function Connect_Netbox')
    pass


def Get_server_data(ip):
    """
    Connect to standalone server by IP address and return parameters.
    Data returned in dictionary type
    """
    pass


import copy as cp

enclosure_list = 'c:\enclosures.txt'  # IP addresses of blade enclosures
servers_list = 'c:\servers.txt'  # IP addresses of standalone servers
blades = []
servers = []

# Enumerate enclosure list and get data from servers api
with open(enclosure_list, "r") as e:
    for line in e:
        blades = Get_enclosure_data(line)

        print(line)

# Enumerate server list and get data from servers api
with open(servers_list, "r") as e:
    for line in e:
        servers = Get_server_data(line)

        print(line)

# Getting data from netbox
import pynetbox

API_TOKEN = "0123456789abcdef0123456789abcdef01234567"
NB_URL = "http://192.168.56.101:8000"
nb = pynetbox.api(NB_URL, token=API_TOKEN)
nb_devices = nb.dcim.devices.all()

# working with nb devices
nb_blades = []
nb_enclosures = []
nd_servers = []
for nb_device in nb_devices:
    if str(nb_device.device_role) == 'Blade server':
        # blade server
        nb_blades.append({'name': nb_device.name,
                          'site': nb_device.site,
                          'rack': nb_device.rack,
                          'enclosure': nb_device.parent_device.display_name,
                          'bay': nb_device.parent_device.device_bay,
                          'status': nb_device.status,
                          'serial': nb_device.serial,
                          'ipaddress': nb_device.primary_ip4,
                          'type': nb_device.device_type,
                          'role': nb_device.device_role
                          })
    elif str(nb_device.device_role) == 'Blade enclosure':
        # enclosure
        nb_enclosures.append({'name': nb_device.name,
                              'site': nb_device.site,
                              'rack': nb_device.rack,
                              'status': nb_device.status,
                              'serial': nb_device.serial,
                              'ipaddress': nb_device.primary_ip4,
                              'type': nb_device.device_type,
                              'role': nb_device.device_role
                              })
    elif str(nb_device.device_role) == 'Standalone server':
        # standalone server
        nd_servers.append({'name': nb_device.name,
                           'site': nb_device.site,
                           'rack': nb_device.rack,
                           'status': nb_device.status,
                           'serial': nb_device.serial,
                           'ipaddress': nb_device.primary_ip4,
                           'type': nb_device.device_type,
                           'role': nb_device.device_role
                           })
    else:
        print('Unknown device role found.')
        break

# object server

f = open('input.txt', 'a')
f.close



enclosures2 = nb_devices.copy()
for server in enclosures2:
    if server.device_role != "Blade enclosure":
        server.remove(server)




# print(count if count > 1 else devices )

device_parameters = {
    "name": "just a simple PYNETBOX girl",
    "device_type": 1,
    "device_role": 1,
    "site": 3,
}
new_device = nb.dcim.devices.create(**device_parameters)
print(new_device)

nb.dcim.devices.count(name='s001nd-mb44')
nb.dcim.devices.filter(name='s001nd-mb44')
nb.dcim.devices.filter('s001nd-mb44')
nb.dcim.devices.filter(role='leaf-switch', status=True)

server = nb.dcim.devices.get(name='s001nd-mb44')
server.device_type
server.device_role
