# true-all-of-fabric
A python script to try and download as many mods using a specificed modloader and mc version. Therefore creating a true all of fabric*
*According to modrinth and whatever this script manages to download lol

The script is not perfect, and currently will miss a lot of mods. This is definitely not playable, it may have some XML content in some of the jar files, download duplicates, download forge versions and miss a lot of mods. If you're actually trying to play this later on, I will be praying for you.
**I am not liable for any misuse with any APIs involved!**

## Usage
This script is split up into 2 different scripts, so we don't have to rescrape all of the mod links if the download fails etc.
First run the `get_links.py` script, this will get the links and store them in jars.csv, then run the `download_jars.py` to download the jars. Afterwards, you'll see a `mods` directory populated with different jar files.

