"""
<<<<<<< HEAD
Get data from blade enclosure and put it onto netbox
=======
Get data from blade enclosure and put it on netbox
>>>>>>> cfcb7f4443b32ccfe5d18d1c96ddf0801497032e

API Token: 0123456789abcdef0123456789abcdef01234567
"""

import server_data
import netbox_data


NB_URL          = "https://s001tst-netbox.company.local/"
API_TOKEN       = "f6288560d1b21ed5a659a9786a9f9b5722bfb129"
enclosure_list   = 'enclosures.txt'                              # IP addresses of blade enclosures for site
servers_list     = 'servers.txt'                                  # IP addresses of standalone servers



#create blades (there are no any checks if server exists)

# read the files
f = open(enclosure_list, 'r')
enclosures = f.read().splitlines()
f.close()

f = open(servers_list, 'r')
servers = f.read().splitlines()
f.close()

## COLLECT DATA

#collect all the blades
blades = []                                                       # list for all blades from all enclosures
for enclosure in enclosures:
    blades += server_data.connect_hp_enclosure(enclosure,'netbox1','netbox1')

#collect all the servers
standalone = []
for server in servers:
    standalone += server_data.connect_hp_server(server,'Administrator','')

#collect all the netbox data (no need for this task)
nb_blades  = netbox_data.get_data_netbox(url=NB_URL, token=API_TOKEN,servertype='blades')
nb_servers = netbox_data.get_data_netbox(url=NB_URL, token=API_TOKEN,servertype='servers')

## PUT DATA ON NB

#create blade servers in the netbox
# in case there are not site related data on servers it's necessary to point to the site(COD)
if False:
    if blades and "nb_blades" in globals(): #run if all data exist
        netbox_data.create_blades_netbox(blades,site='01',url=NB_URL, token=API_TOKEN)

#create standalone servers in the netbox
# wo rack link
if True:
    if standalone:
        netbox_data.create_servers_netbox(standalone, url=NB_URL, token=API_TOKEN)

#print(standalone)
#print(nb_blades)

#----------------------------------------------------------
#future options
# try/except, exclusions
# patch if data changed (serial, ipaddress, location)
# get email if server state is no OK
# support lenovo enclosures
#----------------------------------------------------------






