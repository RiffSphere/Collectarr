import requests, json, configparser, sys, os, datetime
quiet=False
nolog=False

def log(text,time=True):
   pay=""
   if time:
      pay = datetime.datetime.now().strftime("[%y-%m-%d %H:%M:%S] ")
   pay=pay + text
      
   if not quiet==True: 
      try: print(pay)
      except: print(pay.encode(sys.getdefaultencoding(), errors = 'replace'))
   if not nolog==True: 
      f = open(os.path.join(config_path,'logs',"log_{}.txt".format(start_time)),'a+')
      if sys.version_info[0] == 2: f.write(pay.encode("utf-8", errors = "replace") + "\n")
      elif sys.version_info[0] == 3: f.write(pay + u"\n")
      f.close()

def lognoreturn(text):
    pay = datetime.datetime.now().strftime("[%y-%m-%d %H:%M:%S] ") + text
    if not quiet==True: 
        try: print(pay, end="")
        except: print(pay.encode(sys.getdefaultencoding(), errors = 'replace'))
    if not nolog==True: 
        f = open(os.path.join(config_path,'logs',"log_{}.txt".format(start_time)),'a+')
        if sys.version_info[0] == 2: f.write(pay.encode("utf-8", errors = "replace"))
        elif sys.version_info[0] == 3: f.write(pay)
        f.close()

def loginfo(text):
   if loginfoactive:
      pay="INFO - " + text
      log(pay)

def fatal(error):
    global printtime
    printtime = False
    if quiet: print(error)
    log("FATAL ERROR - " + error + u"\n")
    sys.exit("Fatal")

def nologfatal(error):
    global nolog, quiet
    quiet = False
    nolog = True
    fatal("ERROR - " + error)

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

def config():
   global host, apiKey, \
         quiet, nolog, nocollectionlog, loginfoactive, \
         rootfoldertype, \
         doaddcollections, doremovecollectarractorlists, doremovecollectarrcollectionlists, doremovealllists, doaddactors, \
         movieenabled, movieenableAuto, movieshouldMonitor, moviesearchOnAdd, moviemonitoredonly, \
         actorenabled, actorenableAuto, actorshouldMonitor, actorsearchOnAdd, actormonitoredonly, actormin, \
         movielistnameaddon, actorlistnameaddon, dryrun,  \
         tmdbapiKey

   print(config_path+"collectarr.conf")
   # Load configuration
   parser = configparser.ConfigParser()
   parser.read(config_path+"collectarr.conf")

   # Load mandatory settings
   try:
      # Program info
      dryrun=str2bool(parser.get("Collectarr","dryrun").strip())
      doaddcollections=str2bool(parser.get("Collectarr","addcollections").strip())
      doremovecollectarractorlists=str2bool(parser.get("Collectarr","removecollectarractorlists").strip())
      doremovecollectarrcollectionlists=str2bool(parser.get("Collectarr","removecollectarrcollectionlists").strip())
      doaddactors=str2bool(parser.get("Collectarr","addactors").strip())
      rootfoldertype=parser.get("Collectarr","rootfolder").lower().strip()
      movielistnameaddon=" " + parser.get("Collectarr","movielistnameaddon").strip()
      if movielistnameaddon=="": movielistnameaddon=" - Collection Added by Collectarr"
      actorlistnameaddon=" " + parser.get("Collectarr","actorlistnameaddon").strip()
      if actorlistnameaddon=="": actorlistnameaddon=" - Actor Added by Collectarr"

      # Radarr info
      hosturl=parser.get("Radarr","host").strip()
      port=parser.get("Radarr","port").strip()
      https=str2bool(parser.get("Radarr","https").strip())
      apiKey=parser.get("Radarr","apiKey").strip()

      # Movie info
      if doaddcollections:
         moviemonitoredonly=str2bool(parser.get("Movie","monitoredonly").strip())
         movieenabled=str2bool(parser.get("Movie","enabled").strip())
         movieenableAuto=str2bool(parser.get("Movie","enableAuto").strip())
         movieshouldMonitor=str2bool(parser.get("Movie","shouldMonitor").strip())
         moviesearchOnAdd=str2bool(parser.get("Movie","searchOnAdd").strip())
      
      # Actor info
      if doaddactors:
         actormonitoredonly=str2bool(parser.get("Actor","monitoredonly").strip())
         actorenabled=str2bool(parser.get("Actor","enabled").strip())
         actorenableAuto=str2bool(parser.get("Actor","enableAuto").strip())
         actorshouldMonitor=str2bool(parser.get("Actor","shouldMonitor").strip())
         actorsearchOnAdd=str2bool(parser.get("Actor","searchOnAdd").strip())
         actormin=int(parser.get("Actor","actormin").strip())
      
      # Log info
      quiet=str2bool(parser.get("Log","quiet").strip())
      nolog=str2bool(parser.get("Log","nolog").strip())
      nocollectionlog=str2bool(parser.get("Log","nocollectionlog").strip())
      loginfoactive=str2bool(parser.get("Log","loginfo").strip())

   except configparser.NoOptionError as error:
      fatal(error.message)

   # Try to load removealllists setting. This should not be used and can be removed from config file, so extra careful passing
   try:
      doremovealllists=str2bool(parser.get("Collectarr","removealllists"))
   except configparser.NoOptionError as error:
      doremovealllists=False
   
   # Try loading tmdbapi from config. Only needed for "smart" actor adding, so not always set
   try:
      tmdbapiKey=parser.get("tmdb","apiKey")
   except configparser.NoOptionError:
      tmdbapiKey=""

   # Combine config into host
   if https == True:
      host="https://"
   else:
      host="http://"
   host=host+hosturl+":"+port+"/api/v3/"

def setupRootfolder():
   global rootfolder
   # verify rootfoldertype is set and has a valid option
   if not(rootfoldertype == "first") and not(rootfoldertype == "movie"):
      fatal("rootfolder incorrectly set in config file")
   
   # get first configured rootfolder if configured to use
   if rootfoldertype == "first":
      response = requests.get(host+"rootfolder?apiKey="+apiKey)
      try:
         rootfolder = response.json()[0]["path"]
      except IndexError:
         fatal("Could not receive first rootpath from Radarr")

def testAPI():
   try:
      response = requests.get(host+"system/status?apiKey="+apiKey)
   except requests.ConnectionError:
      fatal("can not connect to Radarr, verify it is running, and the host, port and https are set correct in the config file")
   if response.status_code == 401:
      fatal("apiKey not correct")

def RemoveLists(CollectarrOnly=True, mode="none"):
   loginfo("Getting all current lists from Radarr")
   try:
      response = requests.get(host+"importlist?apiKey="+apiKey)
   except requests.ConnectionError:
      fatal("can not connect to Radarr, verify it is running, and the host, port and https are set correct in the config file")
   if response.status_code == 401:
      fatal("apiKey not correct")
   alllists = response.json()

   loginfo(str(len(alllists)) + " lists currently monitored.")
   # go over each import list
   for list in alllists:
      fromcollectarr=False
      if mode=="collection" and movielistnameaddon in list["name"]:
         fromcollectarr=True
      if mode=="actor" and actorlistnameaddon in list["name"]:
         fromcollectarr=True
      if fromcollectarr or not CollectarrOnly:
         lognoreturn("Removing " + list["name"])
         if not dryrun:
            try:
               r = requests.delete(url = host+"importlist/"+str(list["id"])+"?apiKey="+apiKey)
            except requests.ConnectionError:
               fatal("can not connect to Radarr, verify it is running, and the host, port and https are set correct in the config file")
            #output result
            if r.status_code==200:
               log(" - SUCCESS",False)
            elif r.status_code==401:
               fatal("apiKey not correct")
            else:
               log(" - FAILED: " + str(r.status_code),False)
         else:
            log(" - dryrun set to true, not pushing changes to Radarr",False)

def AddCollections():
   # setup collection, quality and rootfolder dictionaries
   # dirty way to do it but lazy
   colls={"0": "Nothing"}
   colls.pop("0")
   qualityprofile={"0": "Nothing"}
   qualityprofile.pop("0")
   rootfolders={"0":"Nothing"}
   rootfolders.pop("0")

   # get all movies in radarr
   try:
      response = requests.get(host+"movie?apiKey="+apiKey)
   except requests.ConnectionError:
      fatal("can not connect to Radarr, verify it is running, and the host, port and https are set correct in the config file")
   if response.status_code == 401:
      fatal("apiKey not correct")
   allmovies = response.json()

   loginfo("Checking " + str(len(allmovies)) + " movies in collection")

   # go over all movies in radarr, storing their collection information
   for movie in allmovies:
      if movie["monitored"] or moviemonitoredonly==False:
         isCollection=True
         try:
            temp = str(movie["collection"]["tmdbId"])
         except KeyError:
            if nocollectionlog==True:
               log("INFO - " + movie["title"] + " - No collection")
            isCollection=False

         if isCollection:
            colls.update({str(movie["collection"]["tmdbId"]): movie["collection"]["name"]})
            qualityprofile.update({str(movie["collection"]["tmdbId"]):str(movie["qualityProfileId"])})
            temp=movie["path"]
            temp="/".join(temp.split("/")[:-1])
            rootfolders.update({str(movie["collection"]["tmdbId"]):temp})
   if moviemonitoredonly:
      temp="monitored "
   else:
      temp=""
   loginfo(str(len(colls)) + " collections with " + temp + "movies found.")

   # check existing collections and remove
   try:
      response = requests.get(host+"importlist?apiKey="+apiKey)
   except requests.ConnectionError:
      fatal("can not connect to Radarr, verify it is running, and the host, port and https are set correct in the config file")
   if response.status_code == 401:
      fatal("apiKey not correct")
   alllists = response.json()

   loginfo(str(len(alllists)) + " lists currently monitored.")
   loginfo("Comparing existing lists with wanted collections from movies, and cleaning up.")
   # go over each import list
   for list in alllists:
      # check if tmdb list
      if list["listType"] == "tmdb":
         # remove value
         for fields in list["fields"]:
            try: 
               colls.pop(fields["value"])
            except KeyError:
               pass

   loginfo("Adding " + str(len(colls)) + " new collection lists")
   # go over all collections we found
   for x in colls:
      lognoreturn("Adding: " + x + " - " + colls[x])

      # setup data to add collection
      if rootfoldertype == "first":
         rtfolder = rootfolder
      if rootfoldertype == "movie":
         rtfolder=rootfolders[x]
      data={"enabled": movieenabled,
            "enableAuto": movieenableAuto,
            "shouldMonitor": movieshouldMonitor,
            "qualityProfileId": int(qualityprofile[x]),
            "searchOnAdd": moviesearchOnAdd,
            "minimumAvailability": "tba",
            "listType": "tmdb",
            "listOrder": 1,
            "name": colls[x] + movielistnameaddon,
            "fields": [{ "name": "collectionId", "value": x }],
            "implementationName": "TMDb Collection",
            "implementation": "TMDbCollectionImport",
            "configContract": "TMDbCollectionSettings",
            "infoLink": "https://wiki.servarr.com/Radarr_Supported_tmdbcollectionimport",
            "tags": [],
            "rootFolderPath": rtfolder}
      data=json.dumps(data, sort_keys=True, indent=4)
      if not dryrun:
         # add list to radarr
         try:
            r = requests.post(url = host+"importlist?apiKey="+apiKey, data=data)
         except requests.ConnectionError:
            fatal("can not connect to Radarr, verify it is running, and the host, port and https are set correct in the config file")
         #output result
         if r.status_code==201:
            log(" - SUCCESS",False)
         elif r.status_code==401:
            fatal("apiKey not correct")
         else:
            log(" - FAILED " + str(r.status_code),False)
      else:
         log(" - dryrun set to true, not pushing changes to Radarr",False)

def ActorLists():
   # setting up tmdb api call parameters
   tmdbprefix="https://api.themoviedb.org/3/movie/"
   tmdbsuffix="/credits?api_key=" + tmdbapiKey

   # ugly lazy dictionary setup
   castname={"0": "Nothing"}
   castname.pop("0")
   castcount={"0": "Nothing"}
   castcount.pop("0")
   qualityprofile={"0": "Nothing"}
   qualityprofile.pop("0")
   rootfolders={"0":"Nothing"}
   rootfolders.pop("0")

   loginfo("Getting all movies in Radarr")
   # getting all radarr movies
   try:
      response = requests.get(host+"movie?apiKey="+apiKey)
   except requests.ConnectionError:
      fatal("can not connect to Radarr, verify it is running, and the host, port and https are set correct in the config file")
   if response.status_code == 401:
      fatal("apiKey not correct")
   allmovies = response.json()

   # loop through radarr movies and request cast from tmbd
   for movie in allmovies:
      if movie["monitored"] or not actormonitoredonly:
         loginfo("Searching tmdb for "+movie["title"] + " actors")
         response = requests.get(tmdbprefix + str(movie["tmdbId"]) + tmdbsuffix)
         if response.status_code==200:
            allactors=response.json()
            # saving cast id, name and how often he appears
            for actor in allactors["cast"]:
               castname.update({str(actor["id"]):actor["name"]})
               try:
                  num=int(castcount[str(actor["id"])])+1
               except KeyError:
                  num=1
               castcount.update({str(actor["id"]):num})
               qualityprofile.update({str(actor["id"]):str(movie["qualityProfileId"])})
               temp=movie["path"]
               temp="/".join(temp.split("/")[:-1])
               rootfolders.update({str(actor["id"]):temp})
         else:
            log("Error getting tmdb info for" + movie["title"]+ ": " + str(response.status_code))

   # check existing collections and remove
   try:
      response = requests.get(host+"importlist?apiKey="+apiKey)
   except requests.ConnectionError:
      fatal("can not connect to Radarr, verify it is running, and the host, port and https are set correct in the config file")
   if response.status_code == 401:
      fatal("apiKey not correct")
   alllists = response.json()

   loginfo(str(len(alllists)) + " lists currently monitored.")
   loginfo("Comparing existing lists with potential actors, and cleaning up.")
   # go over each import list
   for list in alllists:
      # check if tmdb list
      if list["listType"] == "tmdb":
         # remove value
         for fields in list["fields"]:
            try: 
               castname.pop(fields["value"])
            except KeyError:
               pass

   counter=0
   for x in castname:
      if castcount[x] >= actormin:
         counter=counter+1
   loginfo(str(counter) + " new actors appear " + str(actormin) + " or more times as actor in movies in Radarr")
   for x in castname:
      if castcount[x] >= actormin:
         lognoreturn("Adding actor list for: " + castname[x] + " appearing in " + str(castcount[x]) + " movies in Radarr")
         if rootfoldertype == "first":
            rtfolder = rootfolder
         if rootfoldertype == "movie":
            rtfolder=rootfolders[x]
         data={"enabled":actorenabled,
               "enableAuto":actorenableAuto,
               "shouldMonitor":actorshouldMonitor,
               "qualityProfileId":int(qualityprofile[x]),
               "searchOnAdd":actorsearchOnAdd,
               "minimumAvailability":"tba",
               "listType":"tmdb",
               "listOrder":1,
               "name":castname[x]+actorlistnameaddon,
               "fields":[{"name":"personId","value":str(x)},
                        {"name":"personCast","value":True},
                        {"name":"personCastDirector","value":False},
                        {"name":"personCastProducer","value":False},
                        {"name":"personCastSound","value":False},
                        {"name":"personCastWriting","value":False}],
               "implementationName":"TMDb Person",
               "implementation":"TMDbPersonImport",
               "configContract":"TMDbPersonSettings",
               "infoLink":"https://wiki.servarr.com/Radarr_Supported_tmdbpersonimport",
               "tags":[],
               "rootFolderPath":rtfolder}

         data=json.dumps(data, sort_keys=True, indent=4)
         if not dryrun:
            # add list to radarr
            try:
               r = requests.post(url = host+"importlist?apiKey="+apiKey, data=data)
            except requests.ConnectionError:
               fatal("can not connect to Radarr, verify it is running, and the host, port and https are set correct in the config file")
            #output result
            if r.status_code==201:
               log(" - SUCCESS",False)
            elif r.status_code==401:
               fatal("apiKey not correct")
            else:
               log(" - FAILED " + str(r.status_code),False)
         else:
            log(" - dryrun set to true, not pushing changes to Radarr",False)


######################
# MAIN PROGRAM START #
######################

# Program Start time
start_time = datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S")   

# Config file and folder Check
#     Allow config file to be passed as parameter, useful for docker
if len(sys.argv) != 1 and sys.argv[1][0] != "-":
   config_path = sys.argv[1] + "/"
#     If not passed, use current dir
else:
   config_path = "./"
if not os.path.isfile(os.path.join(config_path, "collectarr.conf")):
    nologfatal(u"\n" + "Error - {}/collectarr.conf does not exist.".format(config_path))

# Create log folder
if not os.path.exists(os.path.join(config_path,"logs")): os.mkdir(os.path.join(config_path,"logs"))

# Load all settings from config
config()
loginfo("Config Loaded")
testAPI()
loginfo("API tested succesfully")
setupRootfolder()
loginfo("Rootfolder parsed")

if doremovealllists:
   loginfo("****************************************")
   loginfo("* Start removing ALL lists from Radarr *")
   loginfo("****************************************")
   RemoveLists(False)

if doremovecollectarractorlists:
   loginfo("*************************************************************")
   loginfo("* Start removing actor lists previously added by collectarr *")
   loginfo("*************************************************************")
   RemoveLists(True,"actor")
else:
   loginfo("*****************************************************")
   loginfo("* Removing collectarr lists disabled in config file *")
   loginfo("*****************************************************")

if doremovecollectarrcollectionlists:
   loginfo("******************************************************************")
   loginfo("* Start removing collection lists previously added by collectarr *")
   loginfo("******************************************************************")
   RemoveLists(True,"collection")
else:
   loginfo("****************************************************************")
   loginfo("* Removing collectarr collection lists disabled in config file *")
   loginfo("****************************************************************")

if doaddcollections: 
   loginfo("****************************")
   loginfo("* Start adding collections *")
   loginfo("****************************")
   AddCollections()
else:
   loginfo("**********************************************")
   loginfo("* Adding collections disabled in config file *")
   loginfo("**********************************************")

if doaddactors:
   loginfo("*******************************************************************")
   loginfo("* Start adding actor lists                                        *")
   loginfo("* Adding these lists can trigger more actors to be added next run *")
   loginfo("*******************************************************************")
   ActorLists()
else:
   loginfo("****************************************************")
   loginfo("* Adding actors disabled (set to 0) in config file *")
   loginfo("****************************************************")
