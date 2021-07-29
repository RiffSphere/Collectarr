import requests
import json
import configparser

parser = configparser.ConfigParser()
parser.read("collectarr.conf")

host=parser.get("config","host")
port=parser.get("config","port")
host="http://"+host+":"+port+"/api/v3/"
apiKey=parser.get("config","apiKey")
enabled=bool(parser.get("config","enabled"))
enableAuto=bool(parser.get("config","enableAuto"))
shouldMonitor=bool(parser.get("config","shouldMonitor"))
searchOnAdd=bool(parser.get("config","searchOnAdd"))

#host="http://10.0.0.11:7878/api/v3/"
apiKey="ec3e58837e6b4e69a7d638a3a416d450"
# get first configured rootfolder
response = requests.get(host+"rootfolder?apiKey="+apiKey)
rootfolder = response.json()[0]["path"]

# setup collection dictionary
colls={"0": "Nothing"}
colls.pop("0")

# get all movies in radarr
response = requests.get(host+"movie?apiKey="+apiKey)
allmovies = response.json()

# go over all movies in radarr, storing their collection information
for movie in allmovies:
   try:
      colls.update({str(movie["collection"]["tmdbId"]): movie["collection"]["name"]})
   except KeyError:
      print(movie["title"] + " - No collection")

# check existing collections and remove
response = requests.get(host+"importlist?apiKey="+apiKey)
alllists = response.json()
# go over each import list
for list in alllists:
   # check if tmdb list
   if list["listType"] == "tmdb":
      # remove value
      for fields in list["fields"]:
         try: 
            colls.pop(fields["value"])
         except KeyError:
            print("List with no downloaded movies found - Probably actor list")
#jprint(alllists)

# go over all collections we found
for x in colls:
   print("Adding: " + x + " - " + colls[x])

   # setup data to add collection
   data={"enabled": enabled,
         "enableAuto": enableAuto,
         "shouldMonitor": shouldMonitor,
         "qualityProfileId": 1,
         "searchOnAdd": searchOnAdd,
         "minimumAvailability": "tba",
         "listType": "tmdb",
         "listOrder": 1,
         "name": colls[x] + " - Added by Collectarr",
         "fields": [{ "name": "collectionId", "value": x }],
         "implementationName": "TMDb Collection",
         "implementation": "TMDbCollectionImport",
         "configContract": "TMDbCollectionSettings",
         "infoLink": "https://wiki.servarr.com/Radarr_Supported_tmdbcollectionimport",
         "tags": [],
         "rootFolderPath": rootfolder}
   data=json.dumps(data, sort_keys=True, indent=4)
   # add list to radarr
   r = requests.post(url = host+"importlist?apiKey="+apiKey, data=data)
   #output result
   if r.status_code==201:
      print("Added: " + x + " - " + colls[x])
   else:
      print("Error: " + x + " - " + colls[x] + " - Probably duplicate")
