# The module contains functions to get and set data to netbox
# pynetbox mobule is used

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


