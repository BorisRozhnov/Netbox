"""
Get data from blade enclosure and put it onto netbox


API Token: 0123456789abcdef0123456789abcdef01234567
"""

import server_data
import netbox_data


NB_URL          = "https://s001tst-netbox.sibur.local/"
API_TOKEN       = "f6288560d1b21ed5a659a9786a9f9b5722bfb129"
enclosure_list   = 'enclosures1.txt'                              # IP addresses of blade enclosures for site
servers_list    = 'servers.txt'                                   # IP addresses of standalone servers



#create blades (there are no any checks if server exists)

# read the file
f = open(enclosure_list, 'r')
enclosures = f.read().splitlines()
f.close()


#collect all the blades
blades = []                                                       # list for all blades from all enclosures
for enclosure in enclosures:
    blades += server_data.connect_hp_enclosure(enclosure,'netbox','netbox')

#collect all the netbox data (no need for this task)
nb_blades = netbox_data.get_data_netbox(url=NB_URL, token=API_TOKEN,servertype='blades')

#create blade servers in the netbox
# in case there are not site related data on servers it's necessary to point to the site(COD)
#if blades and "nb_blades" in globals(): #run if all data exist
if blades:
    netbox_data.create_blades_netbox(blades,site='01',url=NB_URL, token=API_TOKEN)

#print(blades)
#print(nb_blades)
#----------------------------------------------------------
#future options
# try/except, exclusions
# patch if data changed (serial, ipaddress, location)
# get email if server state is no OK
# support lenovo enclosures
#----------------------------------------------------------
#----------------------------------------------------------
#----------------------------------------------------------





