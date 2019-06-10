import csv
import re
import sys
import requests
import json

orgName = "subdomain.okta" # replace with your own
apiKey = "" # provide your own API token
api_token = "SSWS " + apiKey
headers = {'Accept': 'application/json',
           'Content-Type': 'application/json',
           'Authorization': api_token}

userId = ""

def GetRequest(url):
    response = requests.get(url, headers=headers)
    responseData = json.dumps(response.json())
    data = json.loads(responseData)

    if "errorCode" in response:
        print("\nYou encountered the following Error: \n")
        print(response)
        print("\n")

        return "Error"
    else:
        return data

def GetUser():
    url = "https://"+orgName+".com/api/v1/users/"+userId
    responseJSON = GetRequest(url)
    if responseJSON != "Error":
        print(responseJSON['credentials']['recovery_question']['question'])

if __name__ == "__main__":
    GetUser()