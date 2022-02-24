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
        for mod in request["hits"]:
            project_ids.append(mod["project_id"])
        offset += 100
    sleep(0.1)
    return project_ids


def getJarLinks(mod_id):
    url = "https://modrinth.com/mod/{mod_id}".format(mod_id=mod_id)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", href=lambda x: x and ".jar" in x)
    return [link.get("href") for link in links]


def getFilteredLinks(mod_id):
    mod_links = []
    for mod_id in tqdm(mod_id):
        links = getJarLinks(mod_id)
        for link in links:
            if (mcversion[0:4] in link) and not ("forge" in link.lower()):
                mod_links.append(link)
                break
    return mod_links


def writeToFile(mod_links):
    with open("jars.csv", "w", newline="") as f:
        writer = csv.writer(f, delimiter=" ", quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(mod_links)

    
print("Getting mod ids...")
mod_ids = getAllModIds()
print(f"Got {len(mod_ids)} mod ids!")
print("Getting jar links...")
mod_links = getFilteredLinks(mod_ids)
print(f"Got {len(mod_links)} mod links!")
print("Writing links to links.csv")
writeToFile(mod_links)
print("Done! Please run download_jars.py to download the mods!")
