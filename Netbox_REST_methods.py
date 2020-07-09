import requests
import json
from pprint import pprint

NETBOX = "http://192.168.56.101:8000/api"
TOKEN = "0123456789abcdef0123456789abcdef01234567"


def get_data(api_url):
    url = NETBOX + api_url
    result = []
    step = 1000
    offset = 0

    repeat = True

    headers = {
        'Authorization': TOKEN,
        'Accept': "application/json"
        }
    # while there is still data continue to request data
    while repeat:

        querystring = {"limit": step,
                       "offset": offset}
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = json.loads(response.text)

        repeat = data["next"]
        for prefix in data["results"]:
            if "ip-addresses" in api_url:
                result.append({'ip': prefix["address"],
                               'id': prefix["id"],
                               'status': prefix["status"]["value"],
                               'last_updated': prefix["last_updated"],
                               'tags': prefix["tags"]})
            if "prefixes" in api_url:
                result.append({'prefix': prefix["prefix"],
                               'id': prefix["id"],
                               'status': prefix["status"]["value"],
                               'tags': prefix["tags"]})
            if "vlans" in api_url:
                result.append({'vid': prefix["vid"],
                               'id': prefix["id"],
                               'status': prefix["status"]["value"],
                               'name': prefix["name"]})
        offset = offset + step
    return result


def post_data(payload, api_url):
    url = NETBOX + api_url
    headers = {
        'Authorization': TOKEN,
        'content-type': 'application/json',
        'Accept': "application/json"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    data = json.loads(response.text)
    pprint(data)


def patch_data(payload, api_url, unique_id):
    url = NETBOX + api_url + str(unique_id) + "/"
    headers = {
        'Authorization': TOKEN,
        'content-type': 'application/json',
        'Accept': "application/json"
        }

    response = requests.request("PATCH", url, json=payload, headers=headers)
    data = json.loads(response.text)
    print(data)


def delete_data(api_url, unique_id):
    url = NETBOX + api_url + str(unique_id) + "/"
    headers = {
        'Authorization': TOKEN,
        'Accept': "application/json"
        }

    response = requests.request("DELETE", url, headers=headers)
    # status_code = json.loads(response.status_code)
    print(response.status_code)
