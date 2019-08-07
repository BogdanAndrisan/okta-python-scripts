import csv
import re
import sys
import requests
import json

import Data # data container, replace with your own

orgName = Data.orgName # replace with your own
apiKey = Data.apiKey # provide your own API token
api_token = "SSWS " + apiKey
headers = {'Accept': 'application/json',
           'Content-Type': 'application/json',
           'Authorization': api_token}

def CreateZone(data):
    createZoneUrl = "https://"+orgName+".com/api/v1/zones"
    response = requests.post(createZoneUrl, headers=headers, data=data)
    responseJSON = json.dumps(response.json())
    responseData = json.loads(responseJSON)

    if "errorCode" in responseJSON:
        print(responseData)
        return "Error"
    else:
        print(responseData)
        return responseData

def CreateZones():
    for x in range(1, 100):
        Dict = {               
                    "type": "IP",
                    "id": "null",
                    "name": "newNetworkZone" + str(x),
                    "status": "ACTIVE",
                    "created": "null",
                    "lastUpdated": "null",
                    "gateways": [
                        {
                            "type": "CIDR",
                            "value": "1.2.3.4/24"
                        },
                        {
                            "type": "CIDR",
                            "value": "2.3.4.5/24"
                        }
                    ],
                    "proxies": [
                        {
                            "type": "CIDR",
                            "value": "2.2.3.4/24"
                        },
                        {
                            "type": "CIDR",
                            "value": "3.3.4.5/24"
                        }
                    ]           
                }
        
        CreateZone(json.dumps(Dict))
    

if __name__ == "__main__":
    CreateZones()