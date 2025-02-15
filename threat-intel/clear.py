import requests

# OpenSearch details
OPENSEARCH_URL = "https://192.168.8.129:9200"
HEADERS = {"Content-Type": "application/json"}
AUTH = ("admin", "st1ong.Passw0r")  # Basic Auth if needed

# Step 1: Get all threat sources
search_url = f"{OPENSEARCH_URL}/_plugins/_security_analytics/threat_intel/sources/_search"
search_payload = {
    "query": {"match_all": {}},  # Fetch all threat sources
    "size": 1000  # Adjust based on the number of sources
}

response = requests.post(search_url, json=search_payload, auth=AUTH, headers=HEADERS, verify=False)

if response.status_code == 200:
    sources = response.json().get("hits", {}).get("hits", [])
    
    if not sources:
        print("No threat sources found.")
    else:
        for source in sources:
            source_id = source["_id"]  # Extract the source ID
            
            delete_url = f"{OPENSEARCH_URL}/_plugins/_security_analytics/threat_intel/sources/{source_id}"
            del_response = requests.delete(delete_url, auth=AUTH, headers=HEADERS, verify=False)
            
            if del_response.status_code == 200:
                print(f"Deleted source: {source_id}")
            else:
                print(f"Failed to delete {source_id}: {del_response.text}")
else:
    print(f"Failed to fetch sources: {response.text}")
