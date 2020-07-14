# The module contains functions to get data from Datacenter HW
# HW planned to support:
# HP standalone servers
# HP Blade servers
# Lenovo Blade servers

import base64
import hpilo        # hp ilo module
import paramiko     # ssh common module
#import socket       # resolve hostnames
from typing import Dict, List, Any


def connect_lenovo_enclosure():
    """"""
    pass


def connect_hp_server(host,user,password):
    """
    This function wil make connection to
    HP standalone or blade server by hpilo
    """

    ilo = hpilo.Ilo(host,user,password)
    host_data = ilo.get_host_data()

    server = {'name': ilo.get_server_name(), 'product_name':host_data[1]['Product Name'], 'serial':host_data[1]['Serial Number'],'ip_address':ilo.get_network_settings()['ip_address']}
    return server

def connect_hp_enclosure(host,user,password,port=22):
    """
    The function connect to hp blade enclosure and return blade server's properties:
    bay, name, serial, status, enclosure name, enclosure ip
    Returns list of dictionaries
    """

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=password, port=port)
    #show server names
    stdin, stdout, stderr = client.exec_command("show server names")
    data_binary = stdout.read()
    errors = stderr.read()
    server_names = data_binary.decode()
    server_names = server_names.splitlines()
    #show rack name
    stdin, stdout, stderr = client.exec_command("show rack name")
    data_binary = stdout.read()
    errors += stderr.read()
    rack_name = data_binary.decode()
    rack_name = rack_name.splitlines()
    #show enclosure name
    stdin, stdout, stderr = client.exec_command("show enclosure info")
    data_binary = stdout.read()
    errors += stderr.read()
    enclosure_name = data_binary.decode()
    enclosure_name = enclosure_name.splitlines()
    #show oa network
    stdin, stdout, stderr = client.exec_command("show oa network")
    data_binary = stdout.read()
    errors += stderr.read()
    oa_network = data_binary.decode()
    oa_network = oa_network.splitlines()
    #show oa info
    stdin, stdout, stderr = client.exec_command("show oa info")
    data_binary = stdout.read()
    errors += stderr.read()
    oa_info = data_binary.decode()
    oa_info = oa_info.splitlines()
    #show server port map all
    stdin, stdout, stderr = client.exec_command("show server port map all")
    data_binary = stdout.read()
    errors += stderr.read()
    server_portmap = data_binary.decode()
    server_portmap = server_portmap.splitlines()
    client.close()

    if __name__ == "__main__":
        # print data in human format
        for i in range(len(server_names)):  # DEBUG
            print(server_names[i])          # DEBUG


    # parsing paramiko returned byte data - show rack name
    #ilo_enclosure_name = rack_name[7].split(':')[1].strip()
    for i in range(len(rack_name)):
        if 'Rack Name' in rack_name[i]:
            ilo_rack_name = rack_name[i].split(':')[1].strip()
            break
        else:
            ilo_rack_name = 'unknown'
    print(ilo_rack_name)
    # parsing paramiko returned byte data - show enclosure name
    for i in range(len(enclosure_name)):
        if 'Enclosure Name' in enclosure_name[i]:
            ilo_enclosure_name = enclosure_name[i].split(':')[1].strip()
            break
        else:
            ilo_enclosure_name = 'unknown'
    print(ilo_enclosure_name)
    # parsing paramiko returned byte data - show oa network
    for i in range(len(oa_network)):
        if 'IPv4 Address' in oa_network[i]:
            ilo_enclosure_ip = oa_network[i].split(':')[1].strip()
            break
        else:
            ilo_enclosure_ip = 'unknown'
    print(ilo_enclosure_ip)
    # parsing paramiko returned byte data - show server names
    ilo_blades: List[Dict[Any, Any]] = []
    for i in range(len(server_names)):
        #print(i)   # DEBUG
        ii = list(filter(lambda a:a != '', server_names[i].split(' ')))
        #print(len(ii)) # DEBUG
        #print(ii[0])   # DEBUG
        if len(ii) == 6 and len(ii[0]) <= 2: # all fields presented and first element size less 3
                server = {'bay': ("%02d" % int(ii[0])), 'name': ii[1], 'serial': ii[2], 'status': str(ii[3]), 'power': ii[4], 'rack_name_raw': ilo_rack_name, 'rack_name': ("%02d" % int(ilo_rack_name.split("_")[-1])), 'enclosure_name_raw': ilo_enclosure_name, 'enclosure_name': ("%02d" % int(ilo_enclosure_name.split("_")[-1])), 'enclosure_ip': ilo_enclosure_ip}
                ilo_blades.append(server)
        elif len(ii) == 5 and len(ii[0]) <= 2: # serial absent and first element size less 3
                server = {'bay': ("%02d" % int(ii[0])), 'name': ii[1], 'serial': '', 'status': ii[2], 'power': ii[3], 'rack_name_raw': ilo_rack_name, 'rack_name': ("%02d" % int(ilo_rack_name.split("_")[-1])), 'enclosure_name_raw': ilo_enclosure_name, 'enclosure_name': ("%02d" % int(ilo_enclosure_name.split("_")[-1])), 'enclosure_ip': ilo_enclosure_ip}
                ilo_blades.append(server)
    return ilo_blades
