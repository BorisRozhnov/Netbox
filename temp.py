import server_data
import netbox_data


blades = [
    {'bay': '01', 'name': 's001vs-esxi54.sibur.local', 'serial': 'CZJ3450BG3', 'status': 'OK', 'power': 'On', 'rack_name':'01', 'enclosure_name': '02', 'enclosure_ip': '10.2.12.161'},
    {'bay': '02', 'name': 's001vs-esxi55.sibur.local', 'serial': 'CZJ3450BG2', 'status': 'OK', 'power': 'On', 'rack_name':'02','enclosure_name': '01', 'enclosure_ip': '10.2.12.161'},
    {'bay': '03', 'name': 's001vs-esxi56.sibur.local', 'serial': '', 'status': 'OK', 'power': 'On', 'rack_name':'05','enclosure_name': '01', 'enclosure_ip': '10.2.12.161'}
          ]
print(blades[0]['name'])
print(blades)
