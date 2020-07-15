# The module contains functions to get and set data to netbox
# pynetbox module is used

import pynetbox

API_TOKEN = "0123456789abcdef0123456789abcdef01234567"
NB_URL = "http://192.168.56.101:8000"

def get_data_netbox(url = NB_URL,token = API_TOKEN, servertype = 'blades'):
    """
    The function get data from netbox
    servertype parameter is used as a selector what to return:
    blades     = blade servers
    enclosures = blade enclosures
    servers    = standalone servers
    returns list of dictionaries
    """
    nb = pynetbox.api(url, token=token)
    nb_devices = nb.dcim.devices.all()

    # working with nb devices
    nb_blades = []
    nb_enclosures = []
    nb_servers = []
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
            nb_servers.append({'name': nb_device.name,
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


    # return data
    if servertype == 'blades':
        return nb_blades
    elif servertype == 'enclosures':
        return nb_enclosures
    elif servertype == 'servers':
        return nb_servers
    return nb_blades # default action when servertype is incorrect

def create_blades_netbox(servers, url = NB_URL, token = API_TOKEN, site = '01'):
    """
    The function create blades in netbox
    blades are child devices located in specified rack, enclosure and bays
    create blades only in 1 and 2 sites
    """
    nb = pynetbox.api(url, token=token)

    #site_id
    #if site   == '002':
    #    site_id=2
    #elif site == '320':
    #    site_id=3
    #else:
    #    site_id=1

    #creating blade servers
    for server in servers:
        device_parameters = {
            "name": server['name'],
            "device_type": 35,       #nb.dcim.device_types.get(3).serialize()        #3
            "device_role": 13,       #nb.dcim.device_roles.get(3).serialize()        #3
            "site": 1,        #1 if site=='001' else 2,                              #CorpCenter
            "serial": server['serial'],
            "rack": nb.dcim.racks.get(name=f'Cod{site}.Rack{server["rack_name"]}').id,
            "primary_ip":server['enclosure_ip']
        }
        new_device = nb.dcim.devices.create(**device_parameters) # **kwarg
        print(new_device)

        #putting blades to enclosure bays
        #print(f'Site{site}.Rack{server["rack_name"]}.Enclosure{server["enclosure_name"]}.Bay{server["bay"]}')      ##DEBUG
        thebay = nb.dcim.device_bays.get(name=f'Cod{site}.Rack{server["rack_name"]}.Enclosure{server["enclosure_name"]}.Bay{server["bay"]}')
        thebay.installed_device = {'name': server['name']}
        thebay.save()

        #creating interface and ip address
        if ['enclosure_ip']: #there is a ip address
            #create an interface
            new_int = nb.dcim.interfaces.create({'device':new_device.id, 'type':0, 'name':'management'})
            #create ip address
            new_ip = nb.ipam.ip_addresses.create({'device':new_device.id, 'interface': new_int.id, 'address':server["enclosure_ip"], 'status':1, 'description':'Blade enclosure management IP'})

