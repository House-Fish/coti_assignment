# Threat intelligence feeder
This utility is used to update threat intelligence sources in OpenSearch, it collects threat intelligence feeds from Group IB's TAXII 2.0 collection: 
- IOC::Common (ip & hash)
- Malware::C2
- Suspicious IP::Scanners
and Alienvault pulse 6737cf6c5e3e70a11e77b340.

No garentees that this project will support other threat feeds as many values are unique to each type. This project is a good base to build off if you would like to extend the functions to even more threat sources. 

## Requirements: 
- GroupIB API key
- Alienvault API key

## Runnning: 
- Update OpenSearch credentials
- Add GroupIB API credentials 
- Add Alienvault API key

``` bash
python -m venv .venv 
pip install -r requirements.txt
python parser.py

# an additional clear.py script has been created to delete all the threat feeds, mainly used for testing 
python clear.py
```