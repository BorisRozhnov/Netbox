import server_data
import netbox_data


import pynetbox




NB_URL          = "https://s001tst-netbox.sibur.local/"
API_TOKEN       = "f6288560d1b21ed5a659a9786a9f9b5722bfb129"

#nb = pynetbox.api(NB_URL, token=API_TOKEN)
nb = netbox_data.connect_netbox(NB_URL,API_TOKEN)

#collect all the netbox data (no need for this task)
#nb_blades = netbox_data.get_data_netbox(url=NB_URL, token=API_TOKEN,servertype='blades')


blades = [
    {'bay': '01', 'name': 's001vs-esxi54.sibur.local', 'serial': 'CZJ3450BG3', 'status': 'OK', 'power': 'On', 'rack_name':'01', 'enclosure_name': '02', 'enclosure_ip': '10.2.12.161'},
    {'bay': '02', 'name': 's001vs-esxi55.sibur.local', 'serial': 'CZJ3450BG2', 'status': 'OK', 'power': 'On', 'rack_name':'02','enclosure_name': '01', 'enclosure_ip': '10.2.12.161'},
    {'bay': '03', 'name': 's001vs-esxi56.sibur.local', 'serial': '', 'status': 'OK', 'power': 'On', 'rack_name':'05','enclosure_name': '01', 'enclosure_ip': '10.2.12.161'}
          ]
#print(blades[0]['name'])
##print(nb_blades)


#nb_devices = nb.dcim.devices.filter('Cod01')
#print(nb_blades)
#nb_interfaces = nb.interfaces.all()
