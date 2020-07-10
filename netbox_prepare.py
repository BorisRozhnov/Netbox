"""
This is a file with one-time actions required for the initial setup
requirements:
1 sites must present
2 device roles must be created (al least 2)
3 device types must be created (height = 10U or less)

Create racks with 2 enclosure inside each with name patterns:
Rack        - SiteXXX.RackXX (Site001.Rack01)
Enclosure   - SiteXXX.RackXX.EnclosureXX (Site001.Rack01.Enclosure01)
Create 16 device bays in every enclosure with name pattern:
Bay         - SiteXXX.RackXX.EnclosureXX.BayXX (Site001.Rack01.Enclosure01.Bay01)

"""

import pynetbox

NB_URL = "http://192.168.56.101:8000"
API_TOKEN = "0123456789abcdef0123456789abcdef01234567"

def delete_all_racks_and_devices_netbox(url = NB_URL,token = API_TOKEN):
    """
    delete all devices and racks from netbox
    """
    nb = pynetbox.api(NB_URL, token=API_TOKEN)
    s = nb.dcim.devices.all()
    r = nb.dcim.racks.all()
    for x in range(len(s)):
        s[x].delete()
    nb.dcim.devices.count()
    for x in range(len(r)):
        r[x].delete()
    return "You made a right decision!"


def create_device_types_and_roles_netbox(url = NB_URL,token = API_TOKEN):
    """
    The function create:
    regions
    sites
    manufactures
    device types
    device roles
    required for create_racks_and_devices_netbox function run
    """
    nb = pynetbox.api(NB_URL, token=API_TOKEN)
    #regions
    nb.dcim.regions.create({'name': 'Default', 'slug': 'msk'})         # id1

    #sites
    nb.dcim.sites.create({'name': '001', 'slug': 'cod-1', 'description': 'COD-1 16/3'})         # id1
    nb.dcim.sites.create({'name': '002', 'slug': 'cod-1', 'description': 'COD-2 16/3'})         # id2
    nb.dcim.sites.create({'name': '320', 'slug': 'cod-1', 'description': 'COD-2 16/3'})         # id2

    #manufactures
    nb.dcim.manufacturers.create({'name': 'Hewlett-Packard', 'slug': 'hp'})     # id1
    nb.dcim.manufacturers.create({'name': 'IBM', 'slug': 'ibm'})                # id2
    nb.dcim.manufacturers.create({'name': 'Lenovo', 'slug': 'lenovo'})          # id3
    nb.dcim.manufacturers.create({'name': 'Noname', 'slug': 'noname'})          # id4
    nb.dcim.manufacturers.create({'name': 'Unknown', 'slug': 'na'})             # id5

    #device_roles
    nb.dcim.device_roles.create({'name': 'Standalone server', 'slug': 'standalone-server'})     # id1
    nb.dcim.device_roles.create({'name': 'Blade enclosure', 'slug': 'blade-enclosure'})         # id2
    nb.dcim.device_roles.create({'name': 'Blade server', 'slug': 'blade-server'})               # id3


    #device_types
    nb.dcim.device_types.create({'manufacturer': 1, 'model':'Blade enclosure C7000','slug':'C7000','u_height': 10, 'is_full_depth': True, 'subdevice_role': 'parent'})      # id1
    nb.dcim.device_types.create({'manufacturer': 1, 'model':'Blade enclosure C3000','slug':'C3000','u_height':  6, 'is_full_depth': True, 'subdevice_role': 'parent'})      # id2
    nb.dcim.device_types.create({'manufacturer': 1, 'model':'ProLiant BL460c','slug':'460','u_height':  0, 'is_full_depth': True, 'subdevice_role': 'child'})               # id3
    nb.dcim.device_types.create({'manufacturer': 1, 'model':'Blade Server', 'slug': 'blade', 'u_height': 0, 'is_full_depth': True, 'subdevice_role': 'child'})              # id4


def create_racks_and_devices_netbox(url = NB_URL,token = API_TOKEN, my_rack_count=2,my_sites= ['001','002']):
    """
    The function create racks and 2 enclosure in each rack in each site given
    Each enclosure has 16 bays
    """


    nb = pynetbox.api(NB_URL, token=API_TOKEN)

    # create list of 2-digit names
    count16 = ["%02d" % x for x in range(1,17)]                 # for 16 bay creation
    count   = ["%02d" % x for x in range(1,my_rack_count + 1)]  # for rack creation

    # create racks and enclosures
    for site in my_sites:

        for rack in count:
            rack = {
                'name':f'Site{site}.Rack{rack}',
                'site':site,
                'w':'19',
                'h':'42'
            }
            new_rack = nb.dcim.racks.create(**rack)  # **kwarg
            print(new_rack)

            # create enclosures

            enclosure1 = {
            'name': f'{new_rack.name}.Enclosure01',
            'site': site,
            'device_role': 2,
            'device_type': 1,
            'rack': new_rack.id,
            'face': 0,
            'position': 10
            }
            new_enclosure = nb.dcim.devices.create(**enclosure1)  # **kwarg
            print(new_enclosure)

            for bay in count16:
                enclosure_bay= {'name':f'{new_enclosure.name}.Bay{bay}', 'device':new_enclosure.id}
                new_bay = nb.dcim.device_bays.create(enclosure_bay)
                print(new_bay)

            enclosure2 = {
            'name': f'{new_rack.name}.Enclosure02',
            'site': site,
            'device_role': 2,
            'device_type': 1,
            'rack': new_rack.id,
            'face': 0,
            'position': 20
            }
            new_enclosure = nb.dcim.devices.create(**enclosure2)  # **kwarg
            print(new_enclosure)

            for bay in count16:
                enclosure_bay= {'name':f'{new_enclosure.name}.Bay{bay}', 'device':new_enclosure.id}
                new_bay = nb.dcim.device_bays.create(enclosure_bay)
                print(new_bay)

    return "have a nice day"

#create_device_types_and_roles_netbox
#delete_all_racks_and_devices_netbox()
#create_racks_and_devices_netbox(my_rack_count=8)