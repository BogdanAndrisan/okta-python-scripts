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

def CreateUser(data):
    createUserUrl = "https://"+orgName+".com/api/v1/users"
    response = requests.post(createUserUrl, headers=headers, data=data)
    responseJSON = json.dumps(response.json())
    responseData = json.loads(responseJSON)

    if "errorCode" in responseJSON:
        print(responseData['errorCauses'])
        return "Error"
    else:
        print(responseData['profile']['login'])
        return responseData

def CreateUsers():
    for x in range(1, 100):
        Dict = {
                    "profile": {
                        "firstName": "Python" + str(x),
                        "lastName": "Test" + str(x),
                        "email": "python" + str(x) + "@mydomain.com",
                        "login": "python" + str(x) + "@mydomain.com"
                    },
                    "credentials": {
                        "password" : { "value": "Password1!" },
                        "recovery_question": {
                        "question": "Who's a major player in the cowboy scene?",
                        "answer": "Annie Oakley"
                        }
                    }
                }
        
        CreateUser(json.dumps(Dict))
    

if __name__ == "__main__":
    CreateUsers()