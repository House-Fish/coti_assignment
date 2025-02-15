import json
import requests
from requests.auth import HTTPBasicAuth
import re
from datetime import datetime, timezone
from OTXv2 import OTXv2

def read_file(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    return data

def write_file(input_file, data):
    with open(input_file, 'w') as f:
        json.dump(data, f, indent=4) 

def parse_groupib(data, spec_type):
    id_count = 1
    output_data = []
    for obj in data.get("objects", []):
        if obj.get("type") == "indicator":
            data = obj.get("pattern", "")

            pattern = r"\[(ipv4-addr:value|domain-name:value|file:hashes.'[^']*')\s=\s'([^']+)'\]"
            matches = re.findall(pattern, data)[0]

            if (spec_type not in matches[0]): 
                continue

            value = matches[1]
           
            # print(spec_type, value)

            parsed_obj = {
                "id": str(id_count),
                "name": obj.get("name", "unknown"),
                "type": spec_type,
                "value": value,
                "severity": "3",
                "created": obj.get("created", datetime.now(timezone.utc).isoformat()),
                "modified": obj.get("modified", datetime.now(timezone.utc).isoformat()),
                "description": "",
                "labels": obj.get("labels", ["label1"]),
                "spec_version": "spec1"
            }
            id_count+=1;
            output_data.append(parsed_obj)
    
    return output_data

def convert_datetime(dt):
    dt = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

def parse_alienvault(data, spec_type):
    id_count = 1
    output_data = []
    for obj in data:
        if obj["type"] != "domain":
            continue

        created_dt = convert_datetime(obj.get("created"))

        parsed_obj = {
            "id": str(id_count),
            "name": obj.get("name", "unknown"),
            "type": spec_type,
            "value": obj.get("indicator"),
            "severity": "3",
            "created": created_dt,
            "modified": obj.get("modified", datetime.now(timezone.utc).isoformat()),
            "description": "",
            "labels": obj.get("labels", ["label1"]),
            "spec_version": "spec1"
        }
        id_count+=1;
        output_data.append(parsed_obj)
    
    return output_data


def insert_parsed_stix(template, name, description, ioc_type, output_data):
    template["name"] = name
    template["description"] = description
    template["ioc_types"] = [ioc_type]
    template["source"]["ioc_upload"]["iocs"] = output_data
    return template 

def send_get_request(url, username, password):
    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    if response.status_code == 206: # cuz group IB weird... why not 200?
        try: 
            return response.json()
        except ValueError: 
            print("response not in JSON")
    else: 
        print(f"Request failed with status code {response.status_code}")

def send_put_request(payload, url, username, password):
    headers = {"Content-Type": "application/json"}

    response = requests.put(url, data=json.dumps(payload), headers=headers, auth=(username, password), verify=False)
    return response.status_code, response.json()

def send_post_request(payload, url, username, password):
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=(username, password), verify=False)
    return response.status_code, response.json()

def save_to_file(OTX):
    for item in PAYLOADS.values():
        if "https://tap.group-ib.com/api/taxii/v2.0/collections" not in item["source"]:
            response = OTX.get_pulse_indicators(item["source"])
        else:
            response = send_get_request(item["source"], GROUPIB_USERNAME, GROUPIB_PASSWORD)

        print(f"{item["name"]} - {item["description"]}\nReceived!")

        with open(f"{item['filename']}.json", "w") as file:
            json.dump(response, file, indent=4)
        print(f"Response written to {item['description']}.json")

def upload(item, key, t, parsed_stix):
    payload = insert_parsed_stix(TEMPLATE, item["name"], item["description"], t, parsed_stix)
    if (item["id"] == ""):
        status_code, post_response = send_post_request(payload, SIEM_URL, SIEM_USERNAME, SIEM_PASSWORD)
        PAYLOADS[key]["id"] = post_response.get("_id")
        write_file("payloads.json", PAYLOADS)
    else: 
        status_code, post_response = send_put_request(payload, SIEM_URL+item["id"], SIEM_USERNAME, SIEM_PASSWORD)
    print(status_code, post_response)

def update():
    for key, item in PAYLOADS.items():
        print(f"Uploading {item["name"]} - {item["description"]}")
        response = read_file(f"{item["filename"]}.json")

        for t in item["types"]:
            if "Alienvault" in item["name"]:
                # indicators = otx.get_pulse_indicators(item["source"])
                parsed_stix = parse_alienvault(response, t)
            else: 
                parsed_stix = parse_groupib(response, t)

            upload(item, key, t, parsed_stix)

PAYLOADS = read_file("payloads.json")
TEMPLATE = read_file("template.json")

GROUPIB_USERNAME = "<GROUP_IB_USERNAME>"
GROUPIB_PASSWORD = "<GROUPIB_API_KEY>"

SIEM_USERNAME = "admin"
SIEM_PASSWORD = "st1ong.Passw0r"
SIEM_URL = "https://192.168.8.129:9200/_plugins/_security_analytics/threat_intel/sources/"
OTX = OTXv2("<ALIENVAULT_OTX_API_KEY>")

def run():
    save_to_file(OTX)
    update()

run()
