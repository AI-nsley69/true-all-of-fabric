import requests
import json
import urllib
import os
import csv
from tqdm import tqdm
from bs4 import BeautifulSoup
from time import sleep

# Define some things about the environment
mcversion="1.18.1"
limit=100
loader="fabric"

def sendRequest(limit, offset):
    # Dictionary for get request
    request_data = {
    	"limit": limit,
    	"offset": offset,
    	"filters": f"categories={loader} AND versions={mcversion}"
    }
    # Deconstruct the dict into the url
    request_url = 'https://api.modrinth.com/v2/search?' + urllib.parse.urlencode(request_data)
    # Send the request, then return the response
    response = requests.get(url=request_url)
    return response.json()


def getAllModIds():
    total_hits = sendRequest(0, 0)["total_hits"]
    project_ids = []
    offset = 0
    while offset < total_hits:
        request = sendRequest(limit, offset)
        if len(request["hits"]) < 1:
            break
        for mod in request["hits"]:
            project_ids.append(mod["project_id"])
        offset += 100
    sleep(0.2)
    return project_ids


def getJarLinks(mod_id):
    url = "https://api.modrinth.com/v2/project/{mod_id}/version".format(mod_id=mod_id)
    response = requests.get(url)
    mod_info = response.json()
    for links in mod_info:
        files = links["files"]
        if len(files) > 0:
            files = files[0]
            if mcversion in links["game_versions"]:
                return files["url"]

def getLinksList(mods_id):
    mod_links = []
    for mod_id in tqdm(mods_id):
        mod_links.append(getJarLinks(mod_id))
        sleep(0.1)
    return mod_links


def writeToFile(mod_links):
    with open("jars.csv", "w", newline="") as f:
        writer = csv.writer(f, delimiter=" ", quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(mod_links)

    
print("Getting mod ids...")
mod_ids = getAllModIds()
print(f"Got {len(mod_ids)} mod ids!")
print("Getting jar links...")
mod_links = getLinksList(mod_ids)
print(f"Got {len(mod_links)} mod links!")
print("Writing links to links.csv")
writeToFile(mod_links)
print("Done! Please run download_jars.py to download the mods!")
