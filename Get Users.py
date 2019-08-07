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


def GetUsers():
    url = "https://"+orgName+".com/api/v1/users?search=status eq \"ACTIVE\" or status eq \"STAGED\" or status eq \"DEPROVISIONED\" or status eq \"PROVISIONED\" or status eq \"RECOVERY\" or status eq \"PASSWORD_EXPIRED\""
    responseJSON = GetPaginatedResponse(url)

    if responseJSON != "Error":

        userFile = open("All-Users-In-Okta.csv", 'w',
                        newline='', encoding='utf-8')
        writer = csv.writer(userFile)
        writer.writerow(
            ["firstName", "lastName", "email", "login",
             "id", "status",
             "Credential Provider Type", "Credential provider Name",
             "middleName", "title", "displayName", "nickName", "secondEmail", "mobilePhone",
             "primaryPhone", "streetAddress", "city", "state", "zipCode", "countryCode", "postalAddress", "locale", "timezone",
             "userType", "employeeNumber", "costCenter", "organization", "division", "department", "managerId", "manager", "Location"])

        for user in responseJSON:

            firstName = user['profile']['firstName']
            lastName = user['profile']['lastName']
            email = user['profile']['email']
            login = user['profile']['login']
            id = user['id']

            status = user['status']
            type = user['credentials']['provider']['type']
            try:
                name = user['credentials']['recovery_question']['question']
            except KeyError:
                name = "no quest"
            try:
                middleName = user['profile']['middleName']
            except KeyError:
                middleName = ""
            try:
                title = user['profile']['title']
            except KeyError:
                title = ""
            try:
                displayName = user['profile']['displayName']
            except KeyError:
                displayName = ""
            try:
                nickName = user['profile']['nickName']
            except KeyError:
                nickName = ""
            try:
                secondEmail = user['profile']['secondEmail']
            except KeyError:
                secondEmail = ""
            try:
                mobilePhone = user['profile']['mobilePhone']
            except KeyError:
                mobilePhone = ""
            try:
                primaryPhone = user['profile']['primaryPhone']
            except KeyError:
                primaryPhone = ""
            try:
                streetAddress = user['profile']['streetAddress']
            except KeyError:
                streetAddress = ""
            try:
                city = user['profile']['city']
            except KeyError:
                city = ""
            try:
                state = user['profile']['state']
            except KeyError:
                state = ""
            try:
                zipCode = user['profile']['zipCode']
            except KeyError:
                zipCode = ""
            try:
                countryCode = user['profile']['countryCode']
            except KeyError:
                countryCode = ""
            try:
                postalAddress = user['profile']['postalAddress']
            except KeyError:
                postalAddress = ""
            try:
                locale = user['profile']['locale']
            except KeyError:
                locale = ""
            try:
                timezone = user['profile']['timezone']
            except KeyError:
                timezone = ""
            try:
                userType = user['profile']['userType']
            except KeyError:
                userType = ""
            try:
                employeeNumber = user['profile']['employeeNumber']
            except KeyError:
                employeeNumber = ""
            try:
                costCenter = user['profile']['costCenter']
            except KeyError:
                costCenter = ""
            try:
                organization = user['profile']['organization']
            except KeyError:
                organization = ""
            try:
                division = user['profile']['division']
            except KeyError:
                division = ""
            try:
                department = user['profile']['department']
            except KeyError:
                department = ""
            try:
                managerId = user['profile']['managerId']
            except KeyError:
                managerId = ""
            try:
                manager = user['profile']['manager']
            except KeyError:
                manager = ""
            try:
                Location = user['profile']['Location']
            except KeyError:
                Location = ""

            writer.writerow(
                [firstName, lastName, email, login,
                 id, status,
                 type, name,
                 middleName, title, displayName, nickName,
                 secondEmail, mobilePhone, primaryPhone, streetAddress,
                 city, state, zipCode, countryCode,
                 postalAddress, locale, timezone, userType,
                 employeeNumber, costCenter, organization, division,
                 department, managerId, manager, Location])


if __name__ == "__main__":
    GetUsers()
