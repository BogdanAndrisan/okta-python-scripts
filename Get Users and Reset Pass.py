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

def ResetPassword(userId, firstName, lastName, id):
    #change the end of the next line if you want to send Emails or not. By default it's set to false.
    resetPassUrl = "https://"+orgName+".com/api/v1/users/"+userId+"/lifecycle/reset_password?sendEmail=false"
    response = requests.post(resetPassUrl, headers=headers)
    responseJSON = json.dumps(response.json())
    responseData = json.loads(responseJSON)

    if "errorCode" in responseJSON:
        print("Password reset failed for " + firstName + " " + lastName + " - ID: " + id + ". Details:")
        print(responseData['errorCauses'])
        return "Error"
    else:
        print("Password was reset for " + firstName + " " + lastName + " - ID: " + id)
        print(responseData)
        return responseJSON

def GetUsersAndResetPassword():
    # for modifying query:
    # status eq \"ACTIVE\" or status eq \"STAGED\" or status eq \"DEPROVISIONED\" or status eq \"PROVISIONED\" or status eq \"RECOVERY\" or status eq \"PASSWORD_EXPIRED\"
    url = "https://"+orgName+".com/api/v1/users?search=status eq \"ACTIVE\""
    responseJSON = GetPaginatedResponse(url)

    if responseJSON != "Error":
        userFile = open("All-Users-In-Okta-Reset.csv", 'w',
                        newline='', encoding='utf-8')
        writer = csv.writer(userFile)
        writer.writerow(
            ["firstName", "lastName", "email", "login","id"])
        
        #set count to limit the number of Password Resets and filter a user if needed
        count = 2
        filterLogin = "john.doe@test.com"
        for user in responseJSON:
            firstName = user['profile']['firstName']
            lastName = user['profile']['lastName']
            email = user['profile']['email']
            login = user['profile']['login']
            id = user['id']
            if count > 0 and login != filterLogin:
                count -= 1
                response = ResetPassword(id, firstName, lastName, id)
            elif count == 0:
                print("Counter has reached number of users to Reset Password.")
            elif login == filterLogin:
                print("Skipping filtered user " + filterLogin)

            writer.writerow(
                [firstName, lastName, email, login,id])

if __name__ == "__main__":
    GetUsersAndResetPassword()