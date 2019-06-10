import requests
import json
import re
import sys
import csv
import string

orgName = "subdomain.okta"
apiKey = ""
api_token = "SSWS " + apiKey

headers = {'Accept': 'application/json',
           'Content-Type': 'application/json', 'Authorization': api_token}

def GetPaginatedResponse(url):
    print("Getting Paginated Response")
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

def DeleteRequest(url):

    response = requests.delete(url, headers=headers)

    responseJSON = response
    responseJSON2 = json.dumps(response.json())
    responseList = json.loads(responseJSON2)
    print(responseList)

    if "errorCode" in responseJSON:
        print("\nYou encountered following Error: \n")
        print(responseJSON)
        print("\n")

        return "Error"
    else:
        return responseJSON


def DeleteUsers():

    ##### CSV Files #####
     # Deactive Users
    deactiveUsers = open("Deactive-Users.csv", 'w', newline='', encoding='utf-8')
    deactiveWriter = csv.writer(deactiveUsers)
    deactiveWriter.writerow(
        ["id", "firstName", "lastName", "email", "login", "status"])

    # Deleted Users
    deletedUsers = open("Deleted-Users.csv", 'w', newline='', encoding='utf-8')
    deletedWriter = csv.writer(deletedUsers)
    deletedWriter.writerow(
        ["firstName", "lastName", "email", "login", "status"])


    # Not Deleted Users
    notDeletedUsers = open('Not-Deleted-Users.csv', 'w', newline='', encoding='utf-8')
    notDeletedWriter = csv.writer(notDeletedUsers)
    notDeletedWriter.writerow(['firstName', 'lastName', 'login', 'error'])
    ##### CSV Files #####
    #status eq \"ACTIVE\" or status eq \"STAGED\" or status eq \"DEPROVISIONED\" or status eq \"PROVISIONED\" or status eq \"RECOVERY\" or status eq \"PASSWORD_EXPIRED\"
    url = "https://"+orgName+".com/api/v1/users?filter=status eq \"DEPROVISIONED\""
    deactivedUsers = GetPaginatedResponse(url)

    userInfoList = []

    deactivedUsersCount = 0
    deletedUsersCount = 0
    notDeletedUserCount = 0

    for user in deactivedUsers:

        userId = str(user["id"])

        # if "@company.com" not in user['profile']['login']:
        #     continue
        if deactivedUsersCount >= 2:
            break

        deleteUrl = "https://"+orgName+".com/api/v1/users/"+userId
        deactiveWriter.writerow([user["id"], user["profile"]["firstName"], user["profile"]["lastName"],
                                 user["profile"]["email"], user["profile"]["login"], user["status"]])
        deactivedUsersCount += 1
        response = DeleteRequest(deleteUrl)
        response = str(response)
        print(userId + " : " + response)

        if response == "<Response [204]>":
            print (str(user["profile"]["login"]) + " is Deleted")
            deletedUsersCount += 1
            deletedWriter.writerow([user["profile"]["firstName"], user["profile"]["lastName"],
                                    user["profile"]["email"], user["profile"]["login"], user["status"]])

        else:
            notDeletedUserCount += 1
            notDeletedWriter.writerow(
                [user["profile"]["firstName"], user["profile"]["lastName"], user["profile"]["login"], response])

    print ("Deactivated Users: " + str(deactivedUsersCount))
    print ("Deleted Users: " + str(deletedUsersCount))
    print ("Not Deleted Users: " + str(notDeletedUserCount))


if __name__ == "__main__":
    DeleteUsers()
