import requests
import json
import time
import pymongo
import datetime

dbName = "BottomOfTheBarrel"
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient[dbName]

def danMurphys():
    url = "https://api.danmurphys.com.au/apis/ui/Browse"

    danMurphysDb = mydb["DanMurphys"]
    now = datetime.datetime.now()
    todaysString = str(now.year) + '-' + str(now.month) + '-' + str(now.day)

    payloads = [
        "{\"department\":\"beer\",\"subDepartment\":\"craft beer\",\"filters\":[],\"pageNumber\":1,\"pageSize\":2000,\"sortType\":\"Relevance\",\"Location\":\"ListerFacet\"}",
        '{"department":"beer","subDepartment":"international beer","filters":[],"pageNumber":1,"pageSize":2000,"sortType":"Relevance","Location":"ListerFacet"}',
        '{"department":"beer","subDepartment":"full strength beer","filters":[],"pageNumber":1,"pageSize":2000,"sortType":"Relevance","Location":"ListerFacet"}',
        '{"department":"beer","subDepartment":"australian beer","filters":[],"pageNumber":1,"pageSize":2000,"sortType":"Relevance","Location":"ListerFacet"}',
        '{"department":"beer","subDepartment":"home brew","filters":[],"pageNumber":1,"pageSize":2000,"sortType":"Relevance","Location":"ListerFacet"}',
        '{"department":"beer","subDepartment":"mid strength beer","filters":[],"pageNumber":1,"pageSize":2000,"sortType":"Relevance","Location":"ListerFacet"}',
        '{"department":"beer","subDepartment":"low carb beer","filters":[],"pageNumber":1,"pageSize":2000,"sortType":"Relevance","Location":"ListerFacet"}',
        '{"department":"beer","subDepartment":"light beer","filters":[],"pageNumber":1,"pageSize":2000,"sortType":"Relevance","Location":"ListerFacet"}'
    ]

    headers = {
        'Accept': "application/json, text/plain, */*",
        'Content-Type': "application/json",
        'Origin': "https://www.danmurphys.com.au",
        'Referer': "https://www.danmurphys.com.au/beer/craft-beer",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
        'cache-control': "no-cache",
        'Postman-Token': "b92cec8f-94d6-402f-b94f-a2c1ace154f7"
    }

    for payload in payloads:
        response = requests.request("POST", url, data=payload, headers=headers)
        data = json.loads(response.text)
        
        for beer in data["Bundles"]:
            newBeer = {}
            for newProducts in beer["Products"]:
                newBeer["Prices"] = {}
                newBeer["Prices"][todaysString] = newProducts["Prices"]
                newBeer["IsOnSpecial"] = newProducts["IsOnSpecial"]
                newBeer["RichDescription"] = newProducts["RichDescription"]
                newBeer["Size"] = newProducts["PackageSize"]
                for newDetails in newProducts["AdditionalDetails"]:
                    if newDetails["Name"] == "producttitle":
                        newBeer["Name"] = newDetails["Value"]
                    if newDetails["Name"] == "countryoforigin":
                        newBeer["Origin"] = newDetails["Value"]
                    if newDetails["Name"] == "webbrandname":
                        newBeer["Brand"] = newDetails["Value"]
                    if newDetails["Name"] == "webalcoholpercentage":
                        newBeer["Alcohol"] = newDetails["Value"]
                    if newDetails["Name"] == "varietal":
                        newBeer["Type"] = newDetails["Value"]
                    if newDetails["Name"] == "standarddrinks":
                        newBeer["Standards"] = newDetails["Value"]
            danMurphysDb.insert_one(newBeer)


danMurphys()