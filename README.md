# Collectarr

A Python script for checking your [Radarr](https://radarr.video/) database and setting up collection lists.
Also supports "smart" actor lists based on [TMDB](https://www.themoviedb.org/).

While Radarr has the tmdb collection id for each movie (that is part of a collection), and allows to quickly setup a collection list for monitoring from the movie page, there is no quick way to do so for all movies.
This script will poll Radarr for all movies, get the tmdb collection id, and set up a collection list for it.

- Example: If you have [The Fast and the Furious (2001)](https://www.themoviedb.org/movie/9799-the-fast-and-the-furious) in your collection, it will add a [The Fast and the Furious Collection](https://www.themoviedb.org/collection/9485?language=en-US) list to Radarr.

The script can also set up lists for actors. To do so, it will check all your movies, get the actors for each movie from TMDB, keep track how many movies your have with each actor, and add a list if that's more than a configured number.

- Example: If you have [The Fast and the Furious Collection](https://www.themoviedb.org/collection/9485?language=en-US) (time of writing there are 9 movies) in Radarr, and set actormin=8, a list for [Vin Diesel](https://www.themoviedb.org/person/12835-vin-diesel?language=en-US) will be created.

**Jump to:**
- [Setting up config files](https://github.com/RiffSphere/Collectarr#setting-up-the-configuration-files)
- [Install and Run](https://github.com/RiffSphere/Collectarr#installation-and-running)
- [Special thanks](https://github.com/RiffSphere/Collectarr#special-thanks)

## Features:
- Automatically added into Radarr.
    - Using the list function: automatically updates when TMDB does.
    - Add Monitored _or_ Unmonitored.
    - Allow to automatically search when added or not (Radarr list setting).
- List for movies and actors.
    - List contains (configurable) description it's been added by Collectarr.
    - Different descriptions for collections and actors.
- Really fast when adding collections: All data is already in Radarr, just enabling it.
- Remove lists.
    - Remove all actor lists added by Collectarr.
    - Remove all collection lists added by Collectarr.
    - Remove all lists from Radarr.

## Requirements:
- Radarr
- Your own TMDB API key.
  
**Getting a TMDB API key:** TMDB offers free API keys to anyone with an account. Simply sign up and request a key via your account settings.
  
## Setting up the configuration files

The config folder can be named and placed anywhere on your computer.
The directory path can be specified when running the command.
If not specified, the script path will be used as config folder.

In the config folder, make a copy of `collectarr.conf.example`, rename it `collectarr.conf` and open it with any text editor.

#### tmdb settings
- **apiKey** - Set your tmdb api key. If you don't plan on using the "smart" actor feature, this can be empty

#### Radarr settings
- **host** - The hostname or IP of Radarr
- **port** - The port Radarr is using (7878 by default)
- **apiKey** - Can be found under Settings > General.
- **https** - [`True`|`False`] - Add `https://` instead of `http://` before the _server_ setting when putting the Radarr URL together. **only http tested**

#### Collectarr settings (actions taken in listed order)
- **dryrun** - [`True`|`False`] - Execute and log information as normally, but don't ask Radarr to make changes. Useful to test actor numbers or see how many collections you can complete
- **removealllists** - [`True`|`False`] - Delete all lists currently in Radarr. SHOULD BE USED WITH CARE. Created to clean up your lists if you started manually. Will delete all lists, including IMDB lists
- **removeCollectarractorlists** - [`True`|`False`] - Delete actor lists added by Collectarr (**actorlistnameaddon* will be used to determine)
- **removeCollectarrcollectionlists** - [`True`|`False`] - Delete collection lists added by Collectarr (**movielistnameaddon* will be used to determine)
- **addcollections** - [`True`|`False`] - Add lists for all collections Radarr has at least 1 movie from, ignoring existing ones
- **addactors** - [`True`|`False`] - Add lists for actors that appear in a lot (**actormin**) of movies you have, ignoring existings ones
- **rootfolder** - ['first'|'movie'] - [More info](https://github.com/RiffSphere/Collectarr#rootfolder-information)
- **movielistnameaddon** - List name will be collection name and what is set here. Used by **removeCollectarrcollectionlists**. Try to keep it specific
- **actorlistnameaddon** - List name will be actor name and what is set here. Used by **removeCollectarractorlists**. Try to keep it specific

#### Log settings
- **quiet** - [`False`|`True`] - Log to console, useful for debugging or docker
- **nolog** - [`True`|`False`] - Disable all logging if you just don't care
- **nocollectionlog** - [`True`|`False`] - Log all movies that are not part of a collection
- **loginfo** - [`True`|`False`] - Log more information

#### Movie/collection settings
- **monitoredonly** - [`True`|`False`] - Only scan movies monitored in Radarr
- **enabled** - [`True`|`False`] - Enable the list when added. **Should probably be True**
- **enableAuto* - [`True`|`False`] - Automatically add movies from the list. **Should probably be True**
- **shouldMonitor** - [`True`|`False`] - Monitor movies added by the list
- **searchOnAdd** - [`True`|`False`] - Search for movie when added

#### Actor settings
- **monitoredonly** - [`True`|`False`] - Only scan movies monitored in Radarr
- **enabled** - [`True`|`False`] - Enable the list when added. **Should probably be True**
- **enableAuto* - [`True`|`False`] - Automatically add movies from the list. **Should probably be True**
- **shouldMonitor** - [`True`|`False`] - Monitor movies added by the list
- **searchOnAdd** - [`True`|`False`] - Search for movie when added
- **actormin** - How many movies in your Radarr database should an actor be in before adding a list?
    -  Start high to prevent too many actors being added
    -  All movies are scanned on each run, so newly added movies can/will add more actor lists

## Installation and Running
**Local**
- Download and extract the zip or clone with git to a location of your choice.
- You may name and place the config folder anywhere on the computer, if not passed the config file is expected to be the same as the script folder.
- In the config folder, make a copy of `collectarr.conf.example` and rename it `collectarr.conf`, edit `collectarr.conf` for your values.
- In Command Prompt or Terminal, navigate into the downloaded folder and run `python collectarr.py ./config` (./config part can be dropped) to begin.

**Docker Container** 
Not completed.
```
docker create \
  --name=Collectarr \
  -v <path to data>:/config \
  riffsphere/collectarr
```

## Special thanks
Special thanks to [RhinoRhys](https://github.com/RhinoRhys). This script is inspired by his original [radarr-collections](https://github.com/RhinoRhys/radarr-collections).
Some of his code has been "reused" (aka stolen) for this project, as well as this layout being based on his.

Also thanks to the [Radarr](https://radarr.video/) project for their amazing tool, and [TMDB](https://www.themoviedb.org/) for the great api.

Feel free to clone and change all you want!

## Rootfolder information
The rootfolder is where movies from a list will get added.
The same setting will be used for collections and actors.
There are 2 options to configure your rootfolder:
- first: use the first configured rootfolder in Radarr. Can be found under Settings -> Media Management
- movie:
    - Will take the path of the **latest movie added** in Radarr that:
        - Is part of a collection
        - Has an actor in it
    - Removes the last part (movie name) from it
    - Example:
        - If you have [The Fast and the Furious (2001)](https://www.themoviedb.org/movie/9799-the-fast-and-the-furious) as only part of [The Fast and the Furious Collection](https://www.themoviedb.org/collection/9485?language=en-US) in Radarr, with path "/data/The Fast and the Furious (2001)", the [The Fast and the Furious Collection](https://www.themoviedb.org/collection/9485?language=en-US) list will have folder "/data"
        - If you also have [2 Fast 2 Furious (2003)](https://www.themoviedb.org/movie/584-2-fast-2-furious), added to Radarr after [The Fast and the Furious (2001)](https://www.themoviedb.org/movie/9799-the-fast-and-the-furious), with path "/movies/2 Fast 2 Furious (2003)", the [The Fast and the Furious Collection](https://www.themoviedb.org/collection/9485?language=en-US) list will have folder "/movies"


