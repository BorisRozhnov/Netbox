import server_data
import netbox_data

#e161 = connect_hp_enclosure('10.2.12.161','netbox','netbox')
#e120 = connect_hp_enclosure('10.2.13.120','netbox','netbox')

#e20 = connect_hp_server('10.2.14.20','netbox','q123Q123')
#print(e161)

"""
# get blade enclosure ip addresses
f = open('enclosure_list.txt', 'r')
enclosure_list = f.readlines()
f.close()
print(enclosure_list)

#for line in enclosure_list:
    #print(line)
"""


#results = netbox_data.get_data_netbox(servertype='servers')
#print(results)

import netbox_data
#srv = netbox_data.get_data_netbox()[0]
#print(srv)

blades = [
    {'bay': '1', 'name': 's001vs-esxi54.sibur.local', 'serial': 'CZJ3450BG3', 'status': 'OK', 'power': 'On', 'enclosure_name': 'Rack_11', 'enclosure_ip': '10.2.12.161'},
    {'bay': '2', 'name': 's001vs-esxi55.sibur.local', 'serial': 'CZJ3450BG2', 'status': 'OK', 'power': 'On', 'enclosure_name': 'Rack_11', 'enclosure_ip': '10.2.12.161'},
    {'bay': '3', 'name': 's001vs-esxi56.sibur.local', 'serial': '', 'status': 'OK', 'power': 'On', 'enclosure_name': 'Rack_11', 'enclosure_ip': '10.2.12.161'}
          ]
#print(blades[0]['name'])

import pynetbox

API_TOKEN = "0123456789abcdef0123456789abcdef01234567"
NB_URL = "http://192.168.56.101:8000"

def create_blades_netbox(servers, url = NB_URL, token = API_TOKEN):
    """
    The function create blades in netbox
    blades are child devices located in specified rack, enclosure and bays
    """
    nb = pynetbox.api(url, token=token)
    for server in servers:
        device_parameters = {
            "name": server['name'],
            "device_type": 3,       #nb.dcim.device_types.get(3).serialize()
            "device_role": 3,       #nb.dcim.device_roles.get(3).serialize()
            "site": 1,              #need to mark somehow
            "serial": server['serial'],
            "rack": server['rack_name'],
            "enclosure": server['enclosure_name'],
            "bay":server['bay'],
            "primary_ip":server['enclosure_ip']
        }
        new_device = nb.dcim.devices.create(**device_parameters) # **kwarg
        print(new_device)
    #        "name": srv['name'],


#create_devices_netbox(blades)
#help(netbox_data.get_data_netbox)

"""
{'bay': ii[0], 'name': ii[1], 'serial': ii[2], 'status': str(ii[3]), 'power': ii[4], 'enclosure_name': ilo_enclosure_name, 'enclosure_ip': ilo_enclosure_ip}
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
"""





s=nb.dcim.devices.filter(device_type=1)

# put server into bay
z=nb.dcim.device_bays.all()
z[10].installed_device = {'name':'s001vs-esxi54.sibur.local'}
z[10].save()

