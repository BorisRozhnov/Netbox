"""
This script interract with netbox via pynetbox module for python 3

API Token: 0123456789abcdef0123456789abcdef01234567
/home/ansible/.ssh/id_rsa


nb = pynetbox.api(
    'http://localhost:8000',
    private_key_file='/path/to/private-key.pem',
    token='0123456789abcdef0123456789abcdef01234567',
    threading=True
)
"""


import copy as cp

enclosure_list = 'c:\enclosures.txt'  # IP addresses of blade enclosures
servers_list = 'c:\servers.txt'  # IP addresses of standalone servers
blades = []
servers = []






