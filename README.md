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
- 

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

## Rootfolder information
The rootfolder is where movies from a list will get added.
The same setting will be used for collections and actors.
There are 2 options to configure your rootfolder:
- first: use the first configured rootfolder in Radarr. Can be found under Settings -> Media Management
- movie:
    - Will take the path of the last movie added in Radarr that:
        - Is part of a collection
        - Has an actor in it
    - Removes the last part from it


