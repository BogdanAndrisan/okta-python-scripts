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


def GetPaginatedResponse(url):
    print("Getting GetPaginatedResponse")
    response = requests.request("GET", url, headers=headers)
    returnResponseList = []
    responseJSON = json.dumps(response.json())
    responseList = json.loads(responseJSON)
    returnResponseList += responseList

    if "errorCode" in responseJSON:
        print("\nYou encountered following Error: \n")
        print(responseJSON)
        print("\n")
        return "Error"
    else:
        headerLink = response.headers["Link"]

        while str(headerLink).find("rel=\"next\"") > -1:
            print(headerLink)
            linkItems = str(headerLink).split(",")

            nextCursorLink = ""
            for link in linkItems:
                if str(link).find("rel=\"next\"") > -1:
                    nextCursorLink = str(link)

            nextLink = str(nextCursorLink.split(";")[0]).strip()
            nextLink = nextLink[1:]
            nextLink = nextLink[:-1]

            url = nextLink

            response = requests.request("GET", url, headers=headers)
            responseJSON = json.dumps(response.json())
            responseList = json.loads(responseJSON)
            returnResponseList = returnResponseList + responseList
            headerLink = response.headers["Link"]

        returnJSON = json.dumps(returnResponseList)
        print("Done getting GetPaginatedResponse")
        return returnResponseList

def GetMFA(userId):
    listFactorsUrl = "https://"+orgName+".com/api/v1/users/"+userId+"/factors"
    response = requests.get(listFactorsUrl, headers=headers)
    responseJSON = json.dumps(response.json())
    responseData = json.loads(responseJSON)

    if "errorCode" in responseJSON:
        print(responseData['errorCauses'])
        return "Error"
    else:
        print(responseData)
        return responseData

def GetUsersMFA():
    # for modifying the query:
    # status eq \"ACTIVE\" or status eq \"STAGED\" or status eq \"DEPROVISIONED\" or status eq \"PROVISIONED\" or status eq \"RECOVERY\" or status eq \"PASSWORD_EXPIRED\"
    url = "https://"+orgName+".com/api/v1/users?search=status eq \"ACTIVE\""
    responseJSON = GetPaginatedResponse(url)

    if responseJSON != "Error":
        userFile = open("All-Users-In-Okta-MFA.csv", 'w',
                        newline='', encoding='utf-8')
        writer = csv.writer(userFile)
        writer.writerow(["First Name", "Last Name", "Email", "Login", "User ID", "Factors", "Factors full JSON Data"])

        for user in responseJSON:
            firstName = user['profile']['firstName']
            lastName = user['profile']['lastName']
            email = user['profile']['email']
            login = user['profile']['login']
            id = user['id']
            response = GetMFA(id)
            factors = [] 
            for mfa in response:
                factors.append(" Provider: " + mfa['provider'] + ", " + "FactorType: " + mfa['factorType'] + ", " + "Status: " + mfa['status'] + " ")
            writer.writerow([firstName, lastName, email, login, id, ";".join(factors), response])

if __name__ == "__main__":
    GetUsersMFA()