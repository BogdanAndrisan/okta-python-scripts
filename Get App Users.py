import csv
import json
import re
import sys
import requests

import Data # data container, replace with your own

orgName = Data.orgName # replace with your own
apiKey = Data.apiKey # provide your own API token
applicationId = ""

api_token = "SSWS "+ apiKey

headers = {'Accept':'application/json','Content-Type':'application/json','Authorization':api_token}

def GetPaginatedResponse(url):
    print("Getting GetPaginatedResponse")
    response = requests.request("GET", url, headers=headers)
    returnResponseList = []
    responseJSON = json.dumps(response.json())
    responseList = json.loads(responseJSON)
    returnResponseList += responseList

    if "errorCode" in responseJSON:
        print ("\nYou encountered following Error: \n")
        print (responseJSON)
        print ("\n")
        return "Error"
    else:
        headerLink= response.headers["Link"]
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
            headerLink= response.headers["Link"]

        returnJSON = json.dumps(returnResponseList)
        print("Done getting GetPaginatedResponse")
        return returnResponseList

def DownloadSFUsers():
    url = "https://"+orgName+".com/api/v1/apps/" + applicationId + "/users"
    responseJSON = GetPaginatedResponse(url)

    if responseJSON != "Error":
        userFile = open("All-Users-In-Okta-App-"+applicationId+".csv", 'w',newline='', encoding='utf-8')
        writer = csv.writer(userFile)
        writer.writerow(["id", "externalId", "userName"])

        for user in responseJSON:
            id = user[u"id"]
            externalId = user[u"externalId"]
            userName  = user[u"credentials"][u"userName"]
            writer.writerow([id,externalId,userName])

if __name__ == "__main__":
    DownloadSFUsers()