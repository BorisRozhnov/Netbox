import server_data
import netbox_data

API_TOKEN = "0123456789abcdef0123456789abcdef01234567"
NB_URL = "http://192.168.56.101:8000"
nb = pynetbox.api(NB_URL, token=API_TOKEN)



blades = [
    {'bay': '01', 'name': 's001vs-esxi54.sibur.local', 'serial': 'CZJ3450BG3', 'status': 'OK', 'power': 'On', 'rack_name':'01', 'enclosure_name': '02', 'enclosure_ip': '10.2.12.161'},
    {'bay': '02', 'name': 's001vs-esxi55.sibur.local', 'serial': 'CZJ3450BG2', 'status': 'OK', 'power': 'On', 'rack_name':'02','enclosure_name': '01', 'enclosure_ip': '10.2.12.161'},
    {'bay': '03', 'name': 's001vs-esxi56.sibur.local', 'serial': '', 'status': 'OK', 'power': 'On', 'rack_name':'05','enclosure_name': '01', 'enclosure_ip': '10.2.12.161'}
          ]
print(blades[0]['name'])
print(blades)


nb_devices = nb.dcim.devices.all()
nb_interfaces = nb.interfaces.all()
