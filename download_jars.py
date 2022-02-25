import requests
import csv
import os
from tqdm import tqdm

download_dir = "mods/"

def getModLinks():
    mod_links = []
    with open("jars.csv", newline="") as f:
        reader = csv.reader(f, delimiter=' ', quotechar='|')
        for row in reader:
            mod_links = row
    return mod_links


def checkDir():
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)


def saveFile(url):
    file_name = url.split("/")[-1]
    request = requests.get(url, stream=True)
    with open(download_dir + file_name, "wb") as f:
        f.write(request.content)


print("Getting mod links from file...")
mod_links = getModLinks()
print("Checking for mods directory..")
checkDir()
print("Downloading each file..")
for mod_link in tqdm(mod_links):
    saveFile(mod_link)
    sleep(0.1)
print("Done! All jars should now be in mods/")
