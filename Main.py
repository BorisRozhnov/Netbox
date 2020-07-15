"""
Get daya from blade enclosure and put on netbox

API Token: 0123456789abcdef0123456789abcdef01234567
/home/ansible/.ssh/id_rsa
"""

import server_data
import netbox_data

NB_URL          = "http://192.168.56.101:8000"
API_TOKEN       = "0123456789abcdef0123456789abcdef01234567"
enclosure_list   = 'enclosures1.txt'                               # IP addresses of blade enclosures for site
servers_list    = 'servers.txt'                                   # IP addresses of standalone servers
blades = []                                                       # list for all blades from all enclosures


#create blades (there are no any checks if server exists)
#----------------------------------------------------------
# read the file
f = open(enclosure_list, 'r')
enclosures = f.readlines()
f.close()


#collect all the blades
for enclosure in enclosures:
    blades += server_data.connect_hp_enclosure(enclosure,'nexbox','netbox')

#collect all the netbox data (no need for this task)
nb_blades = netbox_data.get_data_netbox(url=NB_URL, token=API_TOKEN,servertype='blades')

#create blade servers in the netbox
# in case there are not site related data on servers it's necessary to point to the site(COD)
if blades and "nb_blades" in globals(): #run if all data exist
    netbox_data.create_blades_netbox(blades,site='01',url=NB_URL, token=API_TOKEN)

#----------------------------------------------------------
#future options
# try/except, exclusions
# patch if data changed (serial, ipaddress, location)
# get email if server state is no OK
# support lenovo enclosures
#----------------------------------------------------------
#----------------------------------------------------------
#----------------------------------------------------------





