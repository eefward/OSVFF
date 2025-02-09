import requests
from bs4 import BeautifulSoup
import json
import re

#just for testing, makes strings into json files because terminal is too small
def jsonDump(soup, fileName = "testdata"):
    data = {"html": soup}

    with open(f"{fileName}.json", "w") as file:
        json.dump(data, file, indent=4)

#for html finding between lines, example
#div: <hello world>; start: "div: <", end: ">;" returns "hello world"
def findBetween(txt, start, end):
    start = txt.find(start) + len(start)
    end = txt.find(end, start)

    if start != -1 and end != -1:
        return txt[start:end]
    
    return None

def findEverything(username):
    return [
        username, 
        findRoblox(username),
        findFacebook(username),
        findTikToc(username),
        findGithub(username),
        findTwitter(username),
        findYoutube(username)
    ]
    

def findRoblox(username):
    payload = {"usernames": [username], "excludeBannedUsers": False }
    headers = {"Content-Type": "application/json"}
    response = requests.post("https://users.roblox.com/v1/usernames/users", json=payload, headers=headers)

    if response.status_code != 200: return None
    
    try:
        data = response.json()["data"][0]
    except:
        return {"Roblox": False}
    
    if not data: return {"Roblox": False}

    return {
        "Roblox": True, 
        "displayName": data["displayName"],
        "profile_url": f"https://www.roblox.com/users/{data['id']}/profile"
    }

def robloxFriendsCopyPaste(input):
    data = []

    matches = re.findall(r"@[a-zA-Z0-9]{3,20}\n", input)
    for match in matches:
        username = match[1:].strip() # Removes @ from the start and \n from the end
        print(username)
        data.append(findEverything(username))
    
    for specific_user in data:
        print(specific_user)

    
def findFacebook(username):
    url = f"https://www.facebook.com/{username}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser').prettify()
    actualUser = findBetween(soup, '{\"title\":\"', '\",\"accessory\":null,\"favicon\":null}')

    if actualUser:
        return {"Facebook": True, "displayName": actualUser, "profile_url": url}
    else:
        return {"Facebook": False}

def findTikToc(username):
    url = f"https://www.tiktok.com/@{username}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser').prettify()

    if soup.find(f'"uniqueId":"{username.lower()}"') != -1:
        displayName = findBetween(soup, '"nickname":"', '","avatarLarger"')
        return {"TikTok": True, "displayName": displayName, "profile_url": url}
    else:
        return {"TikTok": False}

'''
def findInstagram(username):
    url = f"https://www.instagram.com/{username}/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser").prettify()
    actualUser = findBetween(soup, '(@', '\u2022 Instagram photos and videos\" proper')

    if actualUser:
        return {"Instagram": True, "displayName": None, "profile_url": url} 
    else:
        return {"Instagram": False}
'''
        
def findGithub(username):
    url = f"https://api.github.com/users/{username}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        user_data = response.json()
        return {"Github": True, "displayName": user_data["name"], "profile_url": f'https://github.com/{username}'}
    else:
        return {"Github": False}

#through public github information dont sue me please
def findTwitter(username):
    url = f"https://api.github.com/users/{username}"
    
    response = requests.get(url)
    user_data = response.json()
    try:
        twitterUser = user_data["twitter_username"]
    except:
        return {"Twitter": False}
    
    if twitterUser:
        return {"Twitter": True, "displayName": None, "profile_url": f'https://x.com/{twitterUser}'}
    else:
        return {"Twitter": False}


def findYoutube(username):
    url = f"https://www.youtube.com/@{username}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser').prettify()

    if soup.find("404 Not Found") == -1:
        displayName = findBetween(soup, 'rel=\"alternate\"/>\n  <title>\n   ', ' - YouTube\n  </title>\n  <meta content=\"')
        return {"Youtube": True, "displayName": displayName, "profile_url": url}
    else:
        return {"Youtube": False}

"""
userinput = input("enter Name: ")
print(findRoblox(userinput))
print(findFacebook(userinput))
print(findTikToc(userinput))
print(findTwitter(userinput))
print(findGithub(userinput))
print(findYoutube(userinput))

with open("exampleRoblox.txt") as file:
    contents = file.read()
    
    robloxFriendsCopyPaste(contents)

"""