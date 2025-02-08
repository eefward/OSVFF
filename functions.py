import requests
from bs4 import BeautifulSoup
import json

#just for testing, makes strings into json files because terminal is too small
def jsonDump(soup):
    data = {"html": soup}

    with open("testdata.json", "w") as file:
        json.dump(data, file, indent=4)

#for html finding between lines, example
#div: <hello world>; start: "div: <", end: ">;" returns "hello world"
def findBetween(txt, start, end):
    start = txt.find(start) + len(start)
    end = txt.find(end)

    if start != -1 and end != -1:
        return txt[start:end]
    
    return None

def findRoblox(username):
    payload = {"usernames": [username], "excludeBannedUsers": False }
    headers = {"Content-Type": "application/json"}
    response = requests.post("https://users.roblox.com/v1/usernames/users", json=payload, headers=headers)

    if response.status_code != 200: return None

    data = response.json()["data"][0]
    if not data: return {"Roblox": False}

    return {
        "Roblox": True, 
        "username": data["name"], 
        "displayName": data["displayName"],
        "profile": f"https://www.roblox.com/users/{data["id"]}/profile"
    }
    
def findFacebook(username):
    url = f"https://www.facebook.com/{username}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser').prettify()
    actualUser = findBetween(soup, '{\"title\":\"', '\",\"accessory\":null,\"favicon\":null}')

    if actualUser:
        return {"Facebook": True, "username": username, "displayName": actualUser, "profile_url": url}
    else:
        return {"Facebook": False}

def findTikToc(username):
    url = f"https://www.tiktok.com/@{username}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser').prettify()

    if soup.find(f'"uniqueId":"{username.lower()}"') != -1:
        return {"TikTok": True, "username": username.lower(), "displayName": username.lower(), "profile_url": url}
    else:
        return {"TikTok": False}

userinput = input("enter Name: ")
print(findRoblox(userinput))
print(findFacebook(userinput))
print(findTikToc(userinput))