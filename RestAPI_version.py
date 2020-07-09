"""
This script interract with netbox via REST API

API Token: 0123456789abcdef0123456789abcdef01234567
"""



########## EXAMPLES
# https://github.com/netbox-community/netbox/blob/master/docs/api/examples.md

#list of sites
$ curl -H "Accept: application/json; indent=4" http://localhost/api/dcim/sites/
{
    "count": 14,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 6,
            "name": "Corporate HQ",
            "slug": "corporate-hq",
            "region": null,
            "tenant": null,
            "facility": "",
            "asn": null,
            "physical_address": "742 Evergreen Terrace, Springfield, USA",
            "shipping_address": "",
            "contact_name": "",
            "contact_phone": "",
            "contact_email": "",
            "comments": "",
            "custom_fields": {},
            "count_prefixes": 108,
            "count_vlans": 46,
            "count_racks": 8,
            "count_devices": 254,
            "count_circuits": 6
        },
        ...
    ]
}

#BULK create multiple devices
curl -X POST -H "Authorization: Token <TOKEN>" -H "Content-Type: application/json" -H "Accept: application/json; indent=4" http://localhost:8000/api/dcim/devices/ --data '[
{"name": "device1", "device_type": 24, "device_role": 17, "site": 6},
{"name": "device2", "device_type": 24, "device_role": 17, "site": 6},
{"name": "device3", "device_type": 24, "device_role": 17, "site": 6},
]'
