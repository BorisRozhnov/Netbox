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
    {'bay': '01', 'name': 's001vs-esxi54.sibur.local', 'serial': 'CZJ3450BG3', 'status': 'OK', 'power': 'On', 'rack_name':'01', 'enclosure_name': '02', 'enclosure_ip': '10.2.12.161'},
    {'bay': '02', 'name': 's001vs-esxi55.sibur.local', 'serial': 'CZJ3450BG2', 'status': 'OK', 'power': 'On', 'rack_name':'02','enclosure_name': '01', 'enclosure_ip': '10.2.12.161'},
    {'bay': '03', 'name': 's001vs-esxi56.sibur.local', 'serial': '', 'status': 'OK', 'power': 'On', 'rack_name':'05','enclosure_name': '01', 'enclosure_ip': '10.2.12.161'}
          ]
print(blades[0]['name'])
print(blades)


import pynetbox

API_TOKEN = "0123456789abcdef0123456789abcdef01234567"
NB_URL = "http://192.168.56.101:8000"

def create_blades_netbox(servers, url = NB_URL, token = API_TOKEN, site = '001'):
    """
    The function create blades in netbox
    blades are child devices located in specified rack, enclosure and bays
    create blades only in 1 and 2 sites
    """
    nb = pynetbox.api(url, token=token)

    #site_id
    if site   == '002':
        site_id=2
    elif site == '320':
        site_id=3
    else:
        site_id=1

    #creating blade servers
    for server in servers:
        device_parameters = {
            "name": server['name'],
            "device_type": 3,       #nb.dcim.device_types.get(3).serialize()
            "device_role": 3,       #nb.dcim.device_roles.get(3).serialize()
            "site": site_id,        #1 if site=='001' else 2,
            "serial": server['serial'],
            "rack": nb.dcim.racks.get(name=f'Site{site}.Rack{server["rack_name"]}').id,
            "primary_ip":server['enclosure_ip']
        }
        new_device = nb.dcim.devices.create(**device_parameters) # **kwarg
        print(new_device)
        #putting blades to enclosure bays
        #print(f'Site{site}.Rack{server["rack_name"]}.Enclosure{server["enclosure_name"]}.Bay{server["bay"]}')      ##DEBUG
        thebay = nb.dcim.device_bays.get(name=f'Site{site}.Rack{server["rack_name"]}.Enclosure{server["enclosure_name"]}.Bay{server["bay"]}')
        thebay.installed_device = {'name': server['name']}
        thebay.save()




create_blades_netbox(blades, site='002')


#help(netbox_data.get_data_netbox)


