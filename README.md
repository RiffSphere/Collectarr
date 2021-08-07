# Collectarr

A Python script for checking your [Radarr](https://radarr.video/) database and setting up collection lists.
Also supports "smart" actor lists based on [TMDB](https://www.themoviedb.org/).

While Radarr has the tmdb collection id for each movie (that is part of a collection), and allows to quickly setup a collection list for monitoring from the movie page, there is no quick way to do so for all movies.
This script will poll Radarr for all movies, get the tmdb collection id, and set up a collection list for it.

- Example: If you have [The Fast and the Furious (2001)](https://www.themoviedb.org/movie/9799-the-fast-and-the-furious) in your collection, it will add a [The Fast and the Furious Collection](https://www.themoviedb.org/collection/9485?language=en-US) list to Radarr.

The script can also set up lists for actors. To do so, it will check all your movies, get the actors for each movie from TMDB, keep track how many movies your have with each actor, and add a list if that's more than a configured number.

- Example: If you have [The Fast and the Furious Collection](https://www.themoviedb.org/collection/9485?language=en-US) (time of writing there are 9 movies) in Radarr, and set actormin=8, a list for [Vin Diesel](https://www.themoviedb.org/person/12835-vin-diesel?language=en-US) will be created.

Last 3 options are to remove lists: ALL lists, Collectarr actor lists, Collectarr collection lists.

**Jump to:**

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
  
